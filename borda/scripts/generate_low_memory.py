import pandas as pd
import numpy as np
import joblib
import os
import time
import argparse
import xgboost as xgb
from tqdm import tqdm

def generate_low_memory():
    parser = argparse.ArgumentParser(description="Forest Diffusion — Generación SOTA Low-Memory (Mac)")
    parser.add_argument('--dataset', type=str, default='optimal', help="Dataset a usar (ej. 'optimal')")
    parser.add_argument('--n_samples', type=int, default=5000, help="Número de pacientes a generar")
    parser.add_argument('--n_t', type=int, default=50, help="Número de pasos de difusión")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"🌲 Iniciando Generación Low-Memory SOTA (Flow Matching)")
    print(f"{'='*60}")
    
    # Autodetectar prefijo 'datasets/' si estamos en la raíz del repositorio de Colab
    prefix = ""
    if os.path.exists("datasets") and not os.path.exists(f"results/{args.dataset}_training_table.parquet"):
        if os.path.exists(f"datasets/results/{args.dataset}_training_table.parquet"):
            prefix = "datasets/"
            print(f"ℹ️ Detectada estructura de carpetas de Drive: usando prefijo '{prefix}'")

    steps_dir = f'{prefix}results/checkpoints/steps_{args.dataset}'
    shell_path = f'{prefix}results/forest_diffusion_shell_{args.dataset}.joblib'
    training_table_path = f'{prefix}results/{args.dataset}_training_table.parquet'
    output_path = f'{prefix}results/synthetic_samples_{args.dataset}_{args.n_samples}.parquet'
    
    # Validaciones
    if not os.path.exists(steps_dir):
        print(f"❌ Error: Falta el directorio de pasos {steps_dir}")
        return
        
    print(f"📖 Leyendo nombres de genes desde {training_table_path}...")
    df_train = pd.read_parquet(training_table_path)
    df_train = df_train.drop(columns=['GSE_ID', 'Category', 'target'], errors='ignore')
    features = df_train.columns.tolist()
    n_features = len(features)
    print(f"   ✅ Se identificaron {n_features} características biológicas.")

    # Recuperar MinMaxScaler localmente usando la tabla original
    print(f"\n🐚 Recalculando el modelo matemático de escalas (MinMaxScaler)...")
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    
    # Entrenar el scaler con los datos originales
    X_train_original = df_train.to_numpy().astype(np.float32)
    scaler.fit(X_train_original)
    
    # Liberar memoria de los datos reales
    del df_train
    del X_train_original
    import gc
    gc.collect()
    print("   ✅ Escalas matemáticas calculadas y listas.")

    # 1. Crear Ruido Inicial (Paso T)
    print(f"\n🎲 Inicializando {args.n_samples} pacientes con ruido puro...")
    X_curr = np.random.normal(0, 1, (args.n_samples, n_features)).astype(np.float32)

    # 2. Integración de Euler (Flow Matching Reversa)
    dt = 1.0 / args.n_t
    print("\n⏳ Iniciando proceso de Des-Ruidificación (Generación)...")
    
    gen_start = time.time()
    
    # Bucle desde paso n_t-1 (49) hacia atrás hasta 0
    for t in tqdm(range(args.n_t - 1, -1, -1), desc="Pasos de Difusión"):
        step_file = os.path.join(steps_dir, f"step_{t}.joblib")
        if not os.path.exists(step_file):
            print(f"\n❌ Error crítico: Falta el paso {step_file}")
            return
            
        # a) Cargar archivo del paso aislado
        feature_models = joblib.load(step_file)
        
        # b) Extraer XGBoost Boosters para inferencia rápida
        boosters = []
        for mdl in feature_models:
            if hasattr(mdl, 'get_booster'):
                booster = mdl.get_booster()
            else:
                booster = mdl
            # FORZAR CPU: Si el modelo se entrenó en Colab con GPU, intentará 
            # buscar una tarjeta CUDA en la Mac y crasheará. Lo forzamos a CPU.
            booster.set_param({'device': 'cpu', 'predictor': 'cpu_predictor'})
            boosters.append(booster)
                
        # Preparar matriz DMatrix (XGBoost nativo es más rápido y gasta menos RAM)
        dmatrix = xgb.DMatrix(X_curr)
        
        # c) Predecir la corrección (Vector de Velocidad Y_pred)
        Y_pred = np.zeros_like(X_curr)
        for k in range(n_features):
            Y_pred[:, k] = boosters[k].predict(dmatrix)
            
        # d) Integración matemática de Euler: X_{t-1} = X_t - Y_t * dt
        X_curr = X_curr - (Y_pred * dt)
        
        # e) Liberar RAM explícitamente para no crashear la Mac
        del feature_models
        del boosters
        del Y_pred
        del dmatrix

    duration = (time.time() - gen_start) / 60
    print(f"\n✅ Integración matemática completada en {duration:.2f} minutos.")

    # 3. Transformación Inversa a escala biológica real
    print("🧬 Revirtiendo escalado matemático a perfiles genómicos reales...")
    X_final = scaler.inverse_transform(X_curr)

    # 4. Reconstrucción y Post-Procesamiento del DataFrame
    synthetic_df = pd.DataFrame(X_final, columns=features)
    
    # Las categorías biológicas no pueden tener decimales
    discrete_columns = ['Technology_Label', 'Category']
    for col in discrete_columns:
        if col in synthetic_df.columns:
            synthetic_df[col] = synthetic_df[col].round().astype(int)
            if col == 'Category':
                synthetic_df[col] = synthetic_df[col].clip(0, 1)
            elif col == 'Technology_Label':
                synthetic_df[col] = synthetic_df[col].clip(0, 1)

    # 5. Guardar el archivo Parquet
    synthetic_df.to_parquet(output_path)
    print(f"\n🎉 ¡ÉXITO! Muestras sintéticas guardadas en: {output_path}")
    print(f"📦 Tamaño final en disco: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_low_memory()
