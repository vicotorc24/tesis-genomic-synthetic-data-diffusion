import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

sns.set_theme(style="whitegrid", context="talk")

def generate_plot():
    # 1. Load actual Microarray Parquet
    parquet_path = "results/normalized/GSE283593.parquet"
    if not os.path.exists(parquet_path):
        print("Missing sample parquet")
        return
        
    df_ma = pd.read_parquet(parquet_path)
    
    # 2. Simulate RNA-seq counts (Negative Binomial distribution)
    # 77 samples, same amount of genes just to match plot sizes
    genes_sample = df_ma.columns[2:5002] # select 5000 genes to make it fast
    ma_obs = df_ma[genes_sample].values.flatten()
    
    # Raw RNA-seq (overdispersed counts)
    rna_raw = np.random.negative_binomial(n=1, p=0.005, size=ma_obs.shape)
    
    # TPM Proxy + log2(x+1) transformation simulation on simulated counts
    col_sums = rna_raw.reshape(-1, 5000).sum(axis=0)
    col_sums[col_sums == 0] = 1
    tpm_sim = (rna_raw.reshape(-1, 5000) / col_sums) * 1e6
    tpm_sim_log = np.log2(tpm_sim + 1).flatten()
    
    # Create the Plot Canvas
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: The Parquet Dataframe Structure (Table Head)
    ax0 = axes[0, 0]
    ax0.axis('off')
    table_head = df_ma.iloc[:5, :5].round(3).astype(str)
    table_head.insert(0, 'Sample', ['GSM_1', 'GSM_2', 'GSM_3', 'GSM_4', 'GSM_5'])
    ax0.set_title("Estructura en memoria de Snappy Parquet (Muestras x Genes)", fontweight="bold")
    table = ax0.table(cellText=table_head.values, colLabels=table_head.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Plot 2: Microarray vs RNA-seq Statistical Difference (Density KDE)
    ax1 = axes[0, 1]
    sns.kdeplot(ma_obs, fill=True, color="teal", label="Microarray (Log2 + Quantile)", ax=ax1, linewidth=2)
    sns.kdeplot(tpm_sim_log, fill=True, color="coral", label="RNA-seq (Log2 + TPM Proxy)", ax=ax1, linewidth=2)
    ax1.set_title("Distribución Global de Expresión (Homogeneidad)", fontweight="bold")
    ax1.set_xlabel("Nivel de Expresión Transformado")
    ax1.set_ylabel("Densidad de Frecuencia")
    ax1.legend()
    
    # Plot 3 & 4: Heatmaps representing Matrix sparsity
    ax2 = axes[1, 0]
    sns.heatmap(df_ma[genes_sample].iloc[:50, :100], cmap="viridis", cbar=False, ax=ax2)
    ax2.set_title("Microarray Parquet Heatmap (Ruido Continuo)", fontweight="bold")
    ax2.set_xlabel("Genes (100)")
    ax2.set_ylabel("Muestras (50)")
    
    ax3 = axes[1, 1]
    sns.heatmap(tpm_sim_log.reshape(-1, 5000)[:50, :100], cmap="magma", cbar=False, ax=ax3)
    ax3.set_title("RNA-seq Parquet Heatmap (Ceros/Dispersión)", fontweight="bold")
    ax3.set_xlabel("Genes (100)")
    ax3.set_ylabel("Muestras (50)")
    
    plt.tight_layout()
    plt.savefig("results/parquet_demo.png", dpi=300, bbox_inches='tight')
    print("Plot generated at results/parquet_demo.png")

if __name__ == "__main__":
    generate_plot()
