"""
=============================================================================
VALIDACIÓN DEL CORE SET Y JUSTIFICACIÓN METODOLÓGICA TSTR
=============================================================================
Este script audita la integridad geométrica (filas, columnas, NaNs) de los 
datasets que conforman el "Core Set".

JUSTIFICACIÓN DEL SPLIT (¿Por qué no entrenamos con los 5,358 pacientes?):
1. TSTR (Train Synthetic, Test Real): Para validar la fidelidad de los datos 
   generados por CTGAN/Forest Diffusion, debemos evaluar los clasificadores SOTA
   (XGBoost, etc.) sobre pacientes reales que el generador JAMÁS haya visto.
2. Prevención de Fuga de Datos (Data Leakage): Si el modelo generativo "ve" 
   el Test Set durante el entrenamiento, memorizará la distribución y las 
   métricas de AUC saldrán artificialmente altas (sobreajuste metodológico).
   
Por lo tanto, la división estricta es:
- 4,286 (Train - 80%): Usado EXCLUSIVAMENTE para entrenar CTGAN/Forest Diffusion.
- 1,072 (Test - 20%): Intocable (bajo llave). Solo para validación ciega final.
=============================================================================
"""
import pandas as pd

def inspect_dataset(name, path):
    print(f"--- Inspeccionando {name} ---")
    try:
        df = pd.read_parquet(path)
        print(f"Path: {path}")
        print(f"Shape: {df.shape} (Muestras: {df.shape[0]}, Características: {df.shape[1]})")
        
        # Check for NaNs
        nan_count = df.isna().sum().sum()
        print(f"Valores NaN totales: {nan_count}")
        
        # Preview columns
        print("Primeras 5 columnas:", list(df.columns[:5]))
        print("Últimas 5 columnas:", list(df.columns[-5:]))
        print("\n")
    except Exception as e:
        print(f"Error al leer {path}: {e}\n")

if __name__ == "__main__":
    datasets = [
        ("Master Core Set (El Biobanco Puro - 5,358)", "results/master_core_set.parquet"),
        ("Core Train Set (80% para Entrenamiento Generativo - 4,286)", "results/core_train.parquet"),
        ("Core Test Set (20% Validación Ciega Intocable - 1,072)", "results/core_test.parquet"),
        ("Master Training Table (El masivo original - 28,048)", "results/master_training_table.parquet")
    ]
    
    for name, path in datasets:
        inspect_dataset(name, path)
