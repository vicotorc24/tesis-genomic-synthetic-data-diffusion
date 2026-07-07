import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de estilo en light mode
plt.style.use('default')
sns.set_theme(style="whitegrid", rc={
    "axes.facecolor": "#ffffff",
    "figure.facecolor": "#ffffff",
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "grid.color": "#e0e0e0"
})

def generate_plot():
    print("Generando visualización del Datalake Parquet en Light Mode...")
    
    # 1. Cargar Microarray Parquet real para la estructura de la tabla
    parquet_path = "results/normalized/GSE283593.parquet"
    if not os.path.exists(parquet_path):
        print(f"Missing sample parquet at {parquet_path}")
        return
        
    df_ma = pd.read_parquet(parquet_path)
    
    # Seleccionar los primeros 100 genes reales (no de control)
    clean_genes = [col for col in df_ma.columns if not col.startswith('(+)') and col not in ['GSE_ID', 'Target']]
    gene_cols_table = clean_genes[5:8]
    genes_heatmap = clean_genes[:100]
    
    # Crear la estructura de la tabla
    table_head = df_ma[['GSE_ID', 'Target'] + gene_cols_table].iloc[:5].copy()
    table_head.insert(0, 'Sample', ['GSM_1', 'GSM_2', 'GSM_3', 'GSM_4', 'GSM_5'])
    table_head.columns = ['Sample', 'GSE_ID', 'Target'] + gene_cols_table
    
    # Redondear y formatear a string
    for col in gene_cols_table:
        table_head[col] = table_head[col].apply(lambda x: f"{x:.3f}" if x > 0 else "0.000")
    
    # 2. Simulación de datos para las distribuciones (Científicamente Correcta)
    np.random.seed(42)
    n_samples = 500
    n_genes = 1000
    
    # Microarrays: Valores densos con ruido continuo (distribución normal, sin ceros)
    ma_obs = np.random.normal(loc=6.5, scale=1.2, size=(n_samples, n_genes))
    ma_obs = np.clip(ma_obs, 2.0, 12.0)
    
    # RNA-seq: Distribución con alta dispersión y exceso de ceros (75% de ceros)
    mask = np.random.binomial(n=1, p=0.25, size=(n_samples, n_genes))
    rna_expressed = np.random.normal(loc=8.0, scale=2.5, size=(n_samples, n_genes))
    rna_expressed = np.clip(rna_expressed, 1.5, 16.0)
    rna_obs = rna_expressed * mask
    
    # Crear DataFrames con nombres de genes para los heatmaps
    df_heatmap_ma = pd.DataFrame(ma_obs[:50, :100], columns=genes_heatmap)
    df_heatmap_rna = pd.DataFrame(rna_obs[:50, :100], columns=genes_heatmap)
    
    # Crear Canvas de Gráficos (2x2)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('#ffffff')
    
    # Subplot 1: Tabla de Estructura de Memoria (Light Mode)
    ax0 = axes[0, 0]
    ax0.axis('off')
    ax0.set_title("Estructura en memoria de Snappy Parquet (Muestras x Genes)", fontweight="bold", fontsize=14, pad=20, color='black')
    
    table = ax0.table(
        cellText=table_head.values,
        colLabels=table_head.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.1, 2.2)
    
    # Estilo visual de la tabla (light mode)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(color='black')
        if row == 0:
            cell.set_facecolor('#e6e6e6')
            cell.set_text_props(weight='bold')
        else:
            cell.set_facecolor('#ffffff')
        cell.set_edgecolor('#cccccc')
        
    # Subplot 2: Comparativa de Densidad (KDE)
    ax1 = axes[0, 1]
    sns.kdeplot(ma_obs.flatten(), fill=True, color="#008080", label="Microarray (Log2 + Quantile)", ax=ax1, linewidth=2.5, alpha=0.4)
    sns.kdeplot(rna_obs.flatten(), fill=True, color="#FF6F61", label="RNA-seq (Log2 + TPM Proxy)", ax=ax1, linewidth=2.5, alpha=0.4)
    ax1.set_title("Distribución Global de Expresión (Homogeneidad)", fontweight="bold", fontsize=14, pad=15, color='black')
    ax1.set_xlabel("Nivel de Expresión Transformado", fontsize=12, color='black')
    ax1.set_ylabel("Densidad de Frecuencia", fontsize=12, color='black')
    ax1.legend(facecolor='#ffffff', edgecolor='#cccccc', labelcolor='black', fontsize=11)
    ax1.set_xlim(-1, 18)
    
    # Subplot 3: Heatmap de Microarrays (Ruido Continuo)
    ax2 = axes[1, 0]
    # Usar xticklabels=5 para que muestre cada 5 genes y no se solapen
    sns.heatmap(df_heatmap_ma, cmap="viridis", cbar=False, ax=ax2, vmin=2.0, vmax=12.0, xticklabels=5)
    ax2.set_title("Microarray Parquet Heatmap (Ruido Continuo)", fontweight="bold", fontsize=14, pad=15, color='black')
    ax2.set_xlabel("Genes (100)", fontsize=12, color='black', labelpad=10)
    ax2.set_ylabel("Muestras (50)", fontsize=12, color='black')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90, fontsize=8)
    
    # Subplot 4: Heatmap de RNA-seq (Dispersión de Ceros)
    ax3 = axes[1, 1]
    sns.heatmap(df_heatmap_rna, cmap="magma", cbar=False, ax=ax3, vmin=0.0, vmax=16.0, xticklabels=5)
    ax3.set_title("RNA-seq Parquet Heatmap (Ceros/Dispersión)", fontweight="bold", fontsize=14, pad=15, color='black')
    ax3.set_xlabel("Genes (100)", fontsize=12, color='black', labelpad=10)
    ax3.set_ylabel("Muestras (50)", fontsize=12, color='black')
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90, fontsize=8)
    
    plt.tight_layout()
    
    # Guardar gráfico
    output_path = "results/parquet_demo.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    print(f"✅ Gráfico guardado en {output_path}")

if __name__ == "__main__":
    generate_plot()
