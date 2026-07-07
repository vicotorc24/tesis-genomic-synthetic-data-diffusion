import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_cdf_comparison(real_df, synth_df, genes, output_path='results/fidelity_cdf.png'):
    print(f"🎨 Generando Comparativa de Distribuciones (CDF) para genes: {genes}")
    
    n_genes = len(genes)
    fig, axes = plt.subplots(1, n_genes, figsize=(n_genes * 5, 5))
    if n_genes == 1: axes = [axes]
    
    sns.set_style("white")
    
    for i, gene in enumerate(genes):
        # Real
        sns.ecdfplot(real_df[gene], label='Real', color='#4A90E2', ax=axes[i], linewidth=2.5)
        # Sintético
        sns.ecdfplot(synth_df[gene], label='Sintético (CTGAN)', color='#FF6B6B', ax=axes[i], linestyle='--', linewidth=2.5)
        
        axes[i].set_title(f"Gen: {gene}", fontsize=12, fontweight='bold')
        axes[i].set_xlabel("Nivel de Expresión")
        axes[i].set_ylabel("Probabilidad Acumulativa")
        axes[i].legend()
    
    plt.suptitle("Fidelidad de Distribución: Real vs. Síntesis (2026)", fontsize=16, y=1.05)
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
        
        # Elegimos algunos de los genes que la IA identificó en el Top 500
        genes_to_plot = ['JAK2', 'TGFB1', 'NF1']
        plot_cdf_comparison(real_df, synth_df, genes_to_plot)
    else:
        print("⏳ Datos no listos.")
