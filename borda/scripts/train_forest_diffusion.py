import pandas as pd
import numpy as np
from ForestDiffusion import ForestDiffusionModel
import joblib
import os
import time
import argparse
import shutil

def train_forest():
    # 1. Configuración de Argumentos (Optimizado para Notebook y CLI)
    parser = argparse.ArgumentParser(description="Entrenamiento SOTA Blindado de Forest Diffusion")
    parser.add_argument('--dataset', type=str, default='master', choices=['core', 'master'],
                        help="Selecciona 'core' (4.2k) o 'master' (28k)")
    parser.add_argument('--gpu', action='store_true', default=True,
                        help="Activa la aceleración de hardware NVIDIA")
    
    args, unknown = parser.parse_known_args()

    # 2. Ruteo Dinámico de Rutas
    if args.dataset == 'master':
        print("🚀 [MODO: ACTO 3] Iniciando entrenamiento masivo de 28k muestras...")
        input_path = 'results/master_training_table.parquet'
        local_model = '/content/forest_diffusion_model_master.joblib'
        drive_model = '/content/drive/MyDrive/tesis_genetica/results/forest_diffusion_model_master.joblib'
    else:
        print("🎯 [MODO: ACTO 2] Entrenando Core Set (Duelo Justo)...")
        input_path = 'results/core_train.parquet'
        local_model = '/content/forest_diffusion_model_core.joblib'
        drive_model = '/content/drive/MyDrive/tesis_genetica/results/forest_diffusion_model_core.joblib'
    
    if not os.path.exists(input_path):
        print(f"❌ Error: No se encuentra {input_path}. Verifica el montaje de Drive.")
        return

    # 3. Carga y Preprocesamiento (Optimización de RAM)
    print("Leyendo archivo parquet...")
    df = pd.read_parquet(input_path)
    df_train = df.drop(columns=['GSE_ID']) if 'GSE_ID' in df.columns else df
    X_train = df_train.to_numpy().astype(np.float32)
    
    print(f"Dataset cargado: {df_train.shape}")

    # 4. Entrenamiento del Modelo SOTA
    xgboost_kwargs = {'tree_method': 'hist', 'device': 'cuda'} if args.gpu else {}
    
    print(f"🧬 Ajustando Bosques de Difusión (n_t=50, model_type='flow')...")
    start_time = time.time()
    
    model = ForestDiffusionModel(
        X_train, 
        model_type='flow', 
        n_t=50, 
        duplicate_K=1, 
        n_jobs=-1,
        **xgboost_kwargs
    )
    
    model.fit(X_train)
    
    duration = (time.time() - start_time) / 3600
    print(f"\n✅ Entrenamiento completado en {duration:.2f} horas.")
    
    # 5. GUARDADO BLINDADO (Local -> Drive)
    print(f"💾 Guardando modelo LOCALMENTE con compresión máxima (Joblib)...")
    try:
        # Usamos compresión=9 para minimizar el impacto en el almacenamiento de Drive
        joblib.dump(model, local_model, compress=9)
        
        print(f"🛰️ Transfiriendo archivo al repositorio en Drive...")
        shutil.copy(local_model, drive_model)
        
        if os.path.exists(drive_model):
            final_size = os.path.getsize(drive_model) / (1024**3)
            print(f"✅ ¡ÉXITO TOTAL! Modelo asegurado en Drive.")
            print(f"📦 Tamaño final: {final_size:.2f} GB")
        else:
            print("⚠️ Error de sincronización. Intentando guardado directo...")
            joblib.dump(model, drive_model, compress=9)
            
    except Exception as e:
        print(f"❌ Error crítico durante el guardado: {e}")
        # Intento de último recurso (ahora con compresión)
        joblib.dump(model, drive_model, compress=9)

if __name__ == "__main__":
    train_forest()
