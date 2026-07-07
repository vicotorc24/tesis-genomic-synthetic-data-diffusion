import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_correlation_fidelity(real_df, synth_df, top_n=30, output_path='results/fidelity_correlations.png'):
    print(f"🎨 Generando Comparativa de Correlaciones (Heatmap) para Top {top_n} genes...")
    
    # Seleccionar genes más variables del Real para comparar
    top_genes = real_df.var().sort_values(ascending=False).head(top_n).index
    
    corr_real = real_df[top_genes].corr()
    corr_synth = synth_df[top_genes].corr()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Real
    sns.heatmap(corr_real, cmap='coolwarm', vmin=-1, vmax=1, ax=ax1, cbar=False)
    ax1.set_title("Estructura de Red REAL", fontsize=14, fontweight='bold')
    
    # Sintético
    sns.heatmap(corr_synth, cmap='coolwarm', vmin=-1, vmax=1, ax=ax2)
    ax2.set_title("Estructura de Red SINTÉTICA (CTGAN)", fontsize=14, fontweight='bold')
    
    plt.suptitle("Fidelidad de Red: Preservación de la Interactómica Génica (2026)", fontsize=18, y=1.05)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en {output_path}")
    plt.close()

if __name__ == "__main__":
    real_path = 'results/core_train.parquet'
    synth_path = 'results/synthetic_samples_5000.parquet'
    
    if os.path.exists(real_path) and os.path.exists(synth_path):
        real_df = pd.read_parquet(real_path)
        synth_df = pd.read_parquet(synth_path)
        
        # Filtrar columnas numéricas (genes)
        actual_cols_to_drop = [col for col in ['GSE_ID', 'Category', 'Technology_Label'] if col in real_df.columns]
        real_genes = real_df.drop(columns=actual_cols_to_drop)
        
        actual_cols_to_drop_s = [col for col in ['GSE_ID', 'Category', 'Technology_Label'] if col in synth_df.columns]
        synth_genes = synth_df.drop(columns=actual_cols_to_drop_s)
        
        plot_correlation_fidelity(real_genes, synth_genes)
    else:
        print("⏳ Datos no listos.")
