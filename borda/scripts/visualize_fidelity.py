import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os

def plot_fidelity_pca(real_df, synth_dfs, output_path='results/fidelity_pca.png'):
    """
    Genera un gráfico de PCA para comparar la distribución de datos Reales vs Sintéticos.
    synth_dfs: Diccionario con {Nombre: DataFrame}
    """
    print("🎨 Generando Gráfico de Fidelidad PCA (Real vs Sintético)...")
    
    # 1. Preparar datos
    # Solo genes (numéricos)
    actual_cols_to_drop = [col for col in ['GSE_ID', 'Category', 'Technology_Label'] if col in real_df.columns]
    X_real = real_df.drop(columns=actual_cols_to_drop)
    
    # Combinar para un PCA unificado
    combined_X = X_real.copy()
    labels = ['Real'] * len(X_real)
    
    for name, s_df in synth_dfs.items():
        actual_s_drop = [col for col in ['GSE_ID', 'Category', 'Technology_Label'] if col in s_df.columns]
        X_s = s_df.drop(columns=actual_s_drop)
        combined_X = pd.concat([combined_X, X_s])
        labels.extend([name] * len(X_s))
    
    # 2. Escalamiento y PCA
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(combined_X)
    
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    
    # 3. Plot
    plt.figure(figsize=(10, 7))
    sns.set_style("whitegrid")
    
    # Paleta de colores Premium
    palette = {"Real": "#4A90E2", "CTGAN": "#FF6B6B", "ForestDiffusion": "#1DD1A1"}
    
    scatter_df = pd.DataFrame({
        'PC1': components[:, 0],
        'PC2': components[:, 1],
        'Origen': labels
    })
    
    sns.scatterplot(
        data=scatter_df, 
        x='PC1', y='PC2', 
        hue='Origen', 
        style='Origen',
        palette=palette,
        alpha=0.4,
        s=40
    )
    
    plt.title("Comparativa de Espacio Latente: Realidad vs. Síntesis (2026)", fontsize=14, fontweight='bold')
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    plt.legend(title="Fuente de Datos")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en {output_path}")
    plt.close()

if __name__ == "__main__":
    real_path = 'results/core_train.parquet'
    ctgan_path = 'results/synthetic_samples_5000.parquet'
    
    if os.path.exists(real_path) and os.path.exists(ctgan_path):
        real_df = pd.read_parquet(real_path).sample(1000) # Muestreo para velocidad
        ctgan_df = pd.read_parquet(ctgan_path).sample(1000)
        
        plot_fidelity_pca(real_df, {"CTGAN": ctgan_df}, output_path='results/fidelity_pca_ctgan.png')
    else:
        print("⏳ Datos no listos. Asegúrate de que 'core_train' y 'synthetic_samples' existan.")
