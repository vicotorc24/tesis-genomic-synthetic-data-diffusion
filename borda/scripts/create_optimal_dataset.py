import pandas as pd
import numpy as np
import time
import os
import sys

def extract_optimal_dataset(input_parquet, output_parquet, k=1000):
    print(f"🚀 Iniciando extracción del Brazo Óptimo ({k} genes) mediante Ensemble...")
    start = time.time()
    
    # 1. Cargar el Datalake Maestro
    print(f"📥 Cargando {input_parquet}...")
    df = pd.read_parquet(input_parquet)
    print(f"📊 Dataset original: {df.shape[0]} pacientes, {df.shape[1]} columnas")
    
    # 2. Separar metadatos de los genes
    metadata_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
    existing_meta = [col for col in metadata_cols if col in df.columns]
    df_genes = df.drop(columns=existing_meta)
    
    # 3. Filtrar cohorte elite (varianza > 0 por paciente)
    print("🧬 Filtrando cohorte Élite (descartando pacientes con varianza cero)...")
    row_vars = df_genes.var(axis=1)
    df_clean = df[row_vars > 0].copy()
    print(f"   Muestras en cohorte Élite: {df_clean.shape[0]}")
    
    # Guardar también el set completo sin selección de genes (9,309 pacientes, 2,503 columnas)
    full_output_parquet = output_parquet.replace('elite_borda', 'elite_full')
    print(f"💾 Guardando cohorte Élite Completa (2.5k genes) en {full_output_parquet}...")
    df_clean.to_parquet(full_output_parquet, index=False)
    
    # 4. Seleccionar el Top K usando Borda Count Ensemble
    print("🗳️ Seleccionando genes usando el ranking Ensemble Borda Count...")
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from feature_selection import apply_feature_selection
    top_genes = apply_feature_selection(df_clean, target_col='Category', method='ensemble', k=k)
    
    # 5. Ensamblar y Guardar
    df_meta_clean = df_clean[existing_meta]
    df_optimal = pd.concat([df_meta_clean, df_clean[top_genes]], axis=1)
    print(f"💾 Guardando Brazo Óptimo en {output_parquet}...")
    df_optimal.to_parquet(output_parquet, index=False)
    
    print(f"🎉 ¡Éxito! Brazo Óptimo creado en {time.time() - start:.2f} segundos.")
    print(f"Nuevo tamaño: {df_optimal.shape[0]} pacientes, {df_optimal.shape[1]} columnas.")

if __name__ == "__main__":
    extract_optimal_dataset(
        input_parquet='results/master_training_table.parquet',
        output_parquet='results/elite_borda_training_table.parquet',
        k=1000
    )
