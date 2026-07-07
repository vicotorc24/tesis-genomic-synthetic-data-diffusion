import pandas as pd
from ctgan import CTGAN
import torch
import os
import joblib
import time

def train_pilot():
    print("🚀 Cargando CORE_TRAIN (80%) para entrenamiento estricto...")
    input_file = 'results/core_train.parquet'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} no encontrado. Ejecuta scripts/generate_core_set.py primero.")
        return

    df = pd.read_parquet(input_file)
    
    # CTGAN training focuses on gene expression
    # GSE_ID is a string/identifier, we drop it for training but keep Technology and Category
    discrete_columns = ['Technology_Label', 'Category']
    df_train = df.drop(columns=['GSE_ID'])
    
    # Ensure discrete columns are treated as such (some might be float64 after reindexing)
    df_train['Technology_Label'] = df_train['Technology_Label'].astype(int)
    df_train['Category'] = df_train['Category'].astype(int)
    
    print(f"Dataset shape: {df_train.shape}")
    print(f"Discrete columns: {discrete_columns}")
    
    # Initialize CTGAN
    # High epochs for the curated Core Set (50 epochs for validation)
    ctgan = CTGAN(epochs=50, batch_size=500, verbose=True)
    
    print("\nStarting Training (Fast Validation: 50 epochs)...")
    start_time = time.time()
    
    ctgan.fit(df_train, discrete_columns)
    
    duration = (time.time() - start_time) / 60
    print(f"\n✅ Entrenamiento completado en {duration:.2f} minutos.")
    
    # Save the model
    os.makedirs('results', exist_ok=True)
    model_path = 'results/ctgan_pilot_model.pkl'
    print(f"Guardando modelo en {model_path}...")
    joblib.dump(ctgan, model_path)
    
    print("\n¡ÉXITO! El modelo generativo CORE está listo para validación.")

if __name__ == "__main__":
    train_pilot()
