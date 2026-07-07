import pandas as pd
from ctgan import CTGAN
import torch
import os
import joblib
import time
import argparse

def train_ctgan():
    parser = argparse.ArgumentParser(description="CTGAN — Colab GPU Training")
    parser.add_argument('--epochs', type=int, default=100, help="Número de épocas de entrenamiento (default: 100)")
    parser.add_argument('--batch_size', type=int, default=500, help="Tamaño de lote (default: 500)")
    parser.add_argument('--data_subpath', type=str, default='datasets/results/elite_borda_training_table.parquet',
                        help="Sub-ruta dentro de Drive al archivo parquet")
    parser.add_argument('--output_dir', type=str, default='datasets/results',
                        help="Sub-ruta para guardar resultados")
    args = parser.parse_args()

    print("============================================================")
    print("  CTGAN — Colab GPU Training")
    print("============================================================")
    print(f"  Épocas:      {args.epochs}")
    print(f"  Batch Size:  {args.batch_size}")
    print(f"  Input:      {args.data_subpath}")
    print("============================================================")

    # Buscar ruta correcta en Google Colab o Local
    drive_base = '/content/drive/MyDrive'
    input_file = args.data_subpath
    output_dir = args.output_dir

    if os.path.exists(os.path.join(drive_base, input_file)):
        input_file = os.path.join(drive_base, input_file)
        output_dir = os.path.join(drive_base, output_dir)
        print("📁 Google Drive detectado como almacenamiento base.")
    else:
        print("⚠️  Google Drive no detectado. Usando rutas locales.")

    if not os.path.exists(input_file):
        print(f"❌ Error: No se encontró el dataset real en: {input_file}")
        return

    # 1. Cargar y preparar datos
    df = pd.read_parquet(input_file)
    print(f"✅ Dataset cargado: {df.shape[0]} muestras × {df.shape[1]} columnas")

    # Identificar columnas clínicas y discretas
    discrete_columns = []
    cols_to_drop = []
    
    # GSE_ID es un string identificador, lo removemos para el entrenamiento
    if 'GSE_ID' in df.columns:
        cols_to_drop.append('GSE_ID')
        
    for col in ['Category', 'target', 'Technology_Label']:
        if col in df.columns:
            df[col] = df[col].astype(int)
            discrete_columns.append(col)

    df_train = df.drop(columns=cols_to_drop)
    print(f"🧬 Columnas a entrenar: {df_train.shape[1]} (Discretas: {discrete_columns})")

    # 2. Inicializar CTGAN con soporte GPU (CUDA)
    use_cuda = torch.cuda.is_available()
    print(f"🖥️  ¿GPU disponible para PyTorch?: {'SÍ (CUDA)' if use_cuda else 'NO (Usando CPU)'}")
    
    ctgan = CTGAN(
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=True,
        cuda=use_cuda
    )

    # 3. Entrenamiento
    print("\n🚀 Iniciando entrenamiento del modelo CTGAN...")
    start_time = time.time()
    ctgan.fit(df_train, discrete_columns)
    duration = (time.time() - start_time) / 60
    print(f"\n✅ Entrenamiento completado en {duration:.2f} minutos.")

    # 4. Guardar Modelo y Muestras
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'ctgan_model_elite_borda.pkl')
    print(f"💾 Guardando modelo entrenado en {model_path}...")
    joblib.dump(ctgan, model_path)

    # Generación de 5,000 muestras para TSTR
    print("\n🎲 Generando 5,000 muestras sintéticas usando CTGAN...")
    df_synth = ctgan.sample(5000)
    
    # Re-introducir GSE_ID ficticio o nulo para mantener el esquema de datos idéntico
    if 'GSE_ID' in df.columns:
        df_synth['GSE_ID'] = 'SYNTHETIC_CTGAN'
        
    # Reordenar columnas para mantener consistencia exacta
    df_synth = df_synth[df.columns]

    synth_path = os.path.join(output_dir, 'synthetic_samples_ctgan_elite_borda_5000.parquet')
    print(f"💾 Guardando muestras sintéticas en {synth_path}...")
    df_synth.to_parquet(synth_path, index=False)
    
    print("\n🎉 ¡Flujo completo de CTGAN culminado exitosamente!")

if __name__ == "__main__":
    train_ctgan()
