import pandas as pd
import numpy as np
import os

def clean_datasets():
    print("🧹 Iniciando proceso de limpieza y alineación de datasets...")
    
    # 1. Limpiar el dataset real
    real_path = 'results/elite_borda_training_table.parquet'
    if not os.path.exists(real_path):
        print(f"❌ Error: No se encontró {real_path}")
        return
        
    df_real = pd.read_parquet(real_path)
    print(f"   Real original: {df_real.shape[0]} muestras, {df_real.shape[1]} columnas")
    
    meta_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
    gene_cols = [c for c in df_real.columns if c not in meta_cols]
    
    # Filtrar cohorte elite (varianza > 0)
    row_vars = df_real[gene_cols].var(axis=1)
    df_real_clean = df_real[row_vars > 0].copy()
    print(f"   Real limpio (cohorte Élite): {df_real_clean.shape[0]} muestras")
    
    # Guardar en su ruta original (limpieza definitiva)
    df_real_clean.to_parquet(real_path, index=False)
    print(f"   💾 Dataset real limpio guardado en {real_path}")
    
    # 2. Generar dataset sintético limpio (5000 muestras)
    # Hacemos aumento de datos biológico sobre la cohorte elite para mantener la correlación y distribución perfectas
    print("\n🌲 Generando dataset sintético limpio (5000 muestras)...")
    np.random.seed(42)
    df_synth_base = df_real_clean.sample(5000, replace=True, random_state=42)
    df_synth_genes = df_synth_base[gene_cols]
    
    # Añadir un 5% de ruido biológico basado en la desviación de cada gen
    gene_stds = df_real_clean[gene_cols].std()
    noise = np.random.normal(0, 0.05, df_synth_genes.shape) * gene_stds.values
    df_synth_genes_noisy = df_synth_genes + noise
    
    df_synth = df_synth_base.copy()
    df_synth[gene_cols] = df_synth_genes_noisy
    
    # Asegurar que Category y target existan y estén alineados
    if 'Category' in df_synth.columns:
        df_synth['Category'] = df_synth['Category'].astype(int)
    if 'target' in df_synth.columns:
        df_synth['target'] = df_synth['target'].astype(int)
        
    synth_path = 'results/synthetic_samples_elite_borda_5000.parquet'
    df_synth.to_parquet(synth_path, index=False)
    print(f"   💾 Dataset sintético limpio guardado en {synth_path}")
    print("✅ Alineación completa.")

if __name__ == "__main__":
    clean_datasets()
