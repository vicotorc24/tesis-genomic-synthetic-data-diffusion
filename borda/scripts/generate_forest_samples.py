import pandas as pd
import numpy as np
import joblib
import os
import time
import argparse
import sys

# Compatibilidad para deserialización de Pickle
try:
    import train_fd_colab
    sys.modules['train_forest_diffusion_checkpoints'] = train_fd_colab
    from train_fd_colab import CheckpointForestDiffusionModel
except ImportError:
    try:
        from train_forest_diffusion_checkpoints import CheckpointForestDiffusionModel
    except ImportError:
        # Fallback local
        class CheckpointForestDiffusionModel:
            pass


def generate_samples():
    parser = argparse.ArgumentParser(description="Forest Diffusion — Generación SOTA de Pacientes Sintéticos")
    parser.add_argument('--dataset', type=str, default='lite', 
                        help="Dataset a usar (ej. 'lite' o 'master')")
    parser.add_argument('--n_samples', type=int, default=5000, 
                        help="Número de pacientes sintéticos a generar (default: 5000)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"🌲 Iniciando Generación SOTA 2026: Forest Diffusion")
    print(f"{'='*60}")
    print(f"  Dataset:  {args.dataset}")
    print(f"  Muestras: {args.n_samples}")
    print(f"{'='*60}\n")

    model_path = f'results/forest_diffusion_model_{args.dataset}.joblib'
    training_table_path = f'results/{args.dataset}_training_table.parquet'
    
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encontró el modelo ensamblado en: {model_path}")
        print("   Asegúrate de haberlo descargado de Google Drive.")
        return

    if not os.path.exists(training_table_path):
        print(f"❌ Error: No se encontró la tabla de entrenamiento en: {training_table_path}")
        print("   Se necesita para extraer los nombres de los genes.")
        return

    # 1. Extraer nombres de las características (genes) desde el parquet
    print(f"📖 Leyendo nombres de genes desde {training_table_path}...")
    df_train = pd.read_parquet(training_table_path)
    # Remover GSE_ID si existe (el modelo no se entrena con los IDs)
    if 'GSE_ID' in df_train.columns:
        df_train = df_train.drop(columns=['GSE_ID'])
    features = df_train.columns.tolist()
    print(f"   ✅ Se identificaron {len(features)} características biológicas.")

    # 2. Cargar el modelo ensamblado
    print(f"\n🧠 Cargando modelo ensamblado ({model_path})...")
    load_start = time.time()
    model = joblib.load(model_path)
    
    # 🩹 DYNAMIC CLASS ASSIGNMENT: Si el modelo fue entrenado con train_fd_colab.py,
    # no heredará de ForestDiffusionModel y no tendrá el método generate().
    # Cambiamos su clase dinámicamente para restaurar la herencia.
    try:
        from ForestDiffusion import ForestDiffusionModel
        class RealCheckpointForestDiffusionModel(ForestDiffusionModel):
            pass
        model.__class__ = RealCheckpointForestDiffusionModel
        print("   🧬 Herencia de ForestDiffusionModel asignada dinámicamente.")
    except Exception as e:
        print(f"   ⚠️ No se pudo asignar herencia de ForestDiffusionModel: {e}")

    
    # 🩹 FIX 1: El ensamblador guardó los árboles en 'model.regr_', pero 
    # la librería original los busca en 'model.regr'.
    if hasattr(model, 'regr_') and getattr(model, 'regr', None) is None or (isinstance(getattr(model, 'regr', None), list) and model.regr[0][0] is None):
        model.regr = model.regr_
        
    # 🩹 FIX 2: ForestDiffusion internamente envía objetos DMatrix a predict(),
    # pero nuestros modelos son XGBRegressor (esperan arrays). Extraemos los Boosters nativos.
    try:
        if hasattr(model.regr[0][0][0], 'get_booster'):
            print("   🔧 Convirtiendo XGBRegressors a Boosters nativos para generación rápida...")
            for j in range(len(model.regr)):
                for i in range(len(model.regr[j])):
                    for k in range(len(model.regr[j][i])):
                        if hasattr(model.regr[j][i][k], 'get_booster'):
                            model.regr[j][i][k] = model.regr[j][i][k].get_booster()
    except Exception as e:
        print(f"   ⚠️ Aviso en extracción de boosters: {e}")

    print(f"   ✅ Modelo cargado en {time.time() - load_start:.1f} segundos.")
    
    # 3. Generar las muestras sintéticas
    print(f"\n🚀 Generando {args.n_samples} pacientes sintéticos...")
    gen_start = time.time()
    synthetic_numpy = model.generate(batch_size=args.n_samples)
    duration = (time.time() - gen_start) / 60
    
    # 4. Reconstruir el DataFrame
    synthetic_df = pd.DataFrame(synthetic_numpy, columns=features)
    
    # Post-procesamiento: Asegurar que las variables discretas/categóricas sean enteros
    discrete_columns = ['Technology_Label', 'Category']
    for col in discrete_columns:
        if col in synthetic_df.columns:
            synthetic_df[col] = synthetic_df[col].round().astype(int)
            # Acotar el rango biológico (ej. Category 0 o 1)
            if col in ['Category', 'Technology_Label']:
                synthetic_df[col] = synthetic_df[col].clip(0, 1)


    print(f"✅ Generación completada con éxito en {duration:.2f} minutos.")
    
    # 5. Guardar en disco
    output_path = f'results/synthetic_samples_{args.dataset}_{args.n_samples}.parquet'
    synthetic_df.to_parquet(output_path)
    print(f"\n💾 Muestras biológicas guardadas en: {output_path}")

if __name__ == "__main__":
    generate_samples()
