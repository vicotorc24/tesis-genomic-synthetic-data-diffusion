import pandas as pd
import numpy as np
import joblib
import os
import time
import argparse
import sys
import warnings
warnings.filterwarnings('ignore')

import xgboost as xgb
xgb.set_config(verbosity=0)
from tqdm import tqdm

# Compatibilidad para deserialización de Pickle
try:
    import train_fd_colab
    sys.modules['train_forest_diffusion_checkpoints'] = train_fd_colab
    from train_fd_colab import CheckpointForestDiffusionModel
except ImportError:
    try:
        from train_forest_diffusion_checkpoints import CheckpointForestDiffusionModel
    except ImportError:
        class CheckpointForestDiffusionModel:
            pass

def generate_samples():
    parser = argparse.ArgumentParser(description="Forest Diffusion — Generación Optimizada GPU (Plan B)")
    parser.add_argument('--dataset', type=str, default='elite_borda', help="Dataset a usar")
    parser.add_argument('--n_samples', type=int, default=120000, help="Número de pacientes a generar")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"🌲 Iniciando Generación Optimizada GPU (Plan B)")
    print(f"{'='*60}")
    print(f"  Dataset:  {args.dataset}")
    print(f"  Muestras: {args.n_samples}")
    print(f"{'='*60}\n")

    model_path = f'results/forest_diffusion_model_{args.dataset}.joblib'
    training_table_path = f'results/{args.dataset}_training_table.parquet'
    
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encontró el modelo en: {model_path}")
        return

    if not os.path.exists(training_table_path):
        print(f"❌ Error: No se encontró la tabla de entrenamiento en: {training_table_path}")
        return

    # 1. Extraer nombres de las características (genes) desde el parquet
    print(f"📖 Leyendo nombres de genes desde {training_table_path}...")
    df_train = pd.read_parquet(training_table_path)
    if 'GSE_ID' in df_train.columns:
        df_train = df_train.drop(columns=['GSE_ID'])
    features = df_train.columns.tolist()
    n_features = len(features)
    print(f"   ✅ Se identificaron {n_features} características biológicas.")

    # 2. Cargar el modelo ensamblado
    print(f"\n🧠 Cargando modelo ensamblado ({model_path})...")
    load_start = time.time()
    model = joblib.load(model_path)
    
    # Alinear herencia
    try:
        from ForestDiffusion import ForestDiffusionModel
        class RealCheckpointForestDiffusionModel(ForestDiffusionModel):
            pass
        model.__class__ = RealCheckpointForestDiffusionModel
        print("   🧬 Herencia de ForestDiffusionModel asignada dinámicamente.")
    except Exception as e:
        print(f"   ⚠️ No se pudo asignar herencia de ForestDiffusionModel: {e}")

    # FIX 1: regr vs regr_
    if hasattr(model, 'regr_') and getattr(model, 'regr', None) is None or (isinstance(getattr(model, 'regr', None), list) and model.regr[0][0] is None):
        model.regr = model.regr_
        
    # FIX 2: Convertir a Booster nativo y forzar CUDA una sola vez
    try:
        if hasattr(model.regr[0][0][0], 'get_booster'):
            print("   🔧 Convirtiendo XGBRegressors a Boosters nativos y configurando CUDA...")
            for j in range(len(model.regr)):
                for i in range(len(model.regr[j])):
                    for k in range(len(model.regr[j][i])):
                        if hasattr(model.regr[j][i][k], 'get_booster'):
                            model.regr[j][i][k] = model.regr[j][i][k].get_booster()
                        # Configurar GPU una sola vez sin el parámetro obsoleto 'predictor'
                        model.regr[j][i][k].set_param({'device': 'cuda'})
    except Exception as e:
        print(f"   ⚠️ Aviso en extracción de boosters: {e}")

    print(f"   ✅ Modelo cargado en {time.time() - load_start:.1f} segundos.")

    # 3. Inicializar ruido
    print(f"\n🎲 Inicializando {args.n_samples} pacientes con ruido puro en GPU (CuPy)...")
    try:
        import cupy as cp
        use_cupy = True
        X_curr = cp.random.normal(0, 1, (args.n_samples, n_features)).astype(cp.float32)
    except ImportError:
        print("   ⚠️ CuPy no está instalado. Usando NumPy (CPU) como fallback.")
        use_cupy = False
        X_curr = np.random.normal(0, 1, (args.n_samples, n_features)).astype(np.float32)

    # 4. Bucle de Integración de Euler 100% GPU
    dt = 1.0 / model.n_t
    print(f"\n🚀 Iniciando Des-Ruidificación (50 pasos en GPU A100)...")
    gen_start = time.time()

    import gc
    for t in tqdm(range(model.n_t - 1, -1, -1), desc="Pasos de Difusión"):
        # Predecir en GPU usando inplace_predict (sin DMatrix y sin caché de memoria)
        if use_cupy:
            Y_pred = cp.zeros_like(X_curr)
        else:
            Y_pred = np.zeros_like(X_curr)
            
        for k in range(n_features):
            booster = model.regr[0][t][k]
            Y_pred[:, k] = booster.inplace_predict(X_curr)
            
        # Actualizar X_curr
        X_curr = X_curr - (Y_pred * dt)

        # Liberar la memoria de los boosters del paso t que ya no se usarán
        model.regr[0][t] = None
        gc.collect()

    duration = (time.time() - gen_start) / 60
    print(f"✅ Generación completada con éxito en {duration:.2f} minutos.")

    # 5. Transformación inversa a escala biológica real
    print("\n🧬 Revirtiendo escalado matemático a perfiles genómicos...")
    if use_cupy:
        X_curr_cpu = X_curr.get()
    else:
        X_curr_cpu = X_curr
        
    X_final = model.scaler.inverse_transform(X_curr_cpu)

    # 6. Reconstruir DataFrame y post-procesar
    synthetic_df = pd.DataFrame(X_final, columns=features)
    discrete_columns = ['Technology_Label', 'Category']
    for col in discrete_columns:
        if col in synthetic_df.columns:
            synthetic_df[col] = synthetic_df[col].round().astype(int)
            if col in ['Category', 'Technology_Label']:
                synthetic_df[col] = synthetic_df[col].clip(0, 1)

    # 7. Guardar en Drive
    output_path = f'results/synthetic_samples_{args.dataset}_{args.n_samples}.parquet'
    synthetic_df.to_parquet(output_path)
    print(f"\n💾 Muestras biológicas guardadas en: {output_path}")

if __name__ == "__main__":
    generate_samples()
