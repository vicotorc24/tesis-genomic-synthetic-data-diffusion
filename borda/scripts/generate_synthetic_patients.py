import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import joblib
from sklearn.decomposition import PCA

# Set directories
RESULTS_DIR = 'results'
REPORTS_DIR = 'Reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_and_validate():
    model_path = os.path.join(RESULTS_DIR, 'ctgan_pilot_model.pkl')
    master_table_path = os.path.join(RESULTS_DIR, 'core_train.parquet')
    
    if not os.path.exists(model_path):
        print(f"❌ Error: El modelo {model_path} no existe. El entrenamiento parece seguir en curso.")
        return

    print("📂 Cargando modelo y CORE SET para comparación...")
    model = joblib.load(model_path)
    real_df = pd.read_parquet(master_table_path)
    # Drop GSE_ID for comparison as it's not in the training set
    real_df_for_comp = real_df.drop(columns=['GSE_ID'])

    num_samples = 5000
    print(f"🎲 Generando {num_samples} pacientes sintéticos...")
    # Generate samples. Technology_Label and Category will be generated based on the learned distribution.
    synthetic_df = model.sample(num_samples)
    
    # Save synthetic data
    synth_output_path = os.path.join(RESULTS_DIR, f'synthetic_samples_{num_samples}.parquet')
    synthetic_df.to_parquet(synth_output_path)
    print(f"✅ {num_samples} muestras sintéticas guardadas en {synth_output_path}")

    print("📊 Iniciando Validación Visual (PCA Alignment)...")
    
    # Combine for PCA
    # Use real core set for visualization
    sample_size = min(2000, len(real_df_for_comp))
    real_sample = real_df_for_comp.sample(sample_size)
    
    # Sample synthetic for visualization clarity
    synth_sample_size = 500
    synth_sample = synthetic_df.sample(synth_sample_size)
    
    combined = pd.concat([real_sample, synth_sample])
    labels = ['Real (Core Set)'] * sample_size + ['Synthetic'] * synth_sample_size
    
    pca = PCA(n_components=2)
    # Exclude metadata for PCA of gene expression
    features = combined.drop(columns=['Technology_Label', 'Category'])
    components = pca.fit_transform(features)
    
    pca_df = pd.DataFrame(data=components, columns=['PC1', 'PC2'])
    pca_df['Type'] = labels
    
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Type', alpha=0.6, palette={'Real (Core Set)': '#1f77b4', 'Synthetic': '#ff7f0e'})
    plt.title('Validación CORE SET: Alineación PCA Real vs Sintético')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    pca_plot_path = os.path.join(REPORTS_DIR, 'synthetic_vs_real_core_pca.png')
    plt.savefig(pca_plot_path)
    print(f"📈 Gráfico de alineación PCA guardado en {pca_plot_path}")

    # Feature distribution comparison (Top 5 highly variable genes)
    print("📈 Comparando distribuciones de los genes más variables...")
    variances = real_df_for_comp.drop(columns=['Technology_Label', 'Category']).var().sort_values(ascending=False)
    top_genes = variances.index[:5]
    
    fig, axes = plt.subplots(1, 5, figsize=(20, 5))
    for i, gene in enumerate(top_genes):
        sns.kdeplot(real_df_for_comp[gene], ax=axes[i], label='Real', fill=True)
        sns.kdeplot(synthetic_df[gene], ax=axes[i], label='Synthetic', fill=True)
        axes[i].set_title(gene)
        axes[i].legend()
    
    plt.tight_layout()
    dist_plot_path = os.path.join(REPORTS_DIR, 'synthetic_dist_comparison_core.png')
    plt.savefig(dist_plot_path)
    print(f"📈 Gráfico de distribución guardado en {dist_plot_path}")

    print("\n🚀 Validación completada.")

if __name__ == "__main__":
    if os.path.exists('results/ctgan_pilot_model.pkl'):
        generate_and_validate()
    else:
        print("⏳ El modelo aún no se ha guardado o no existe. Reintenta cuando finalice el entrenamiento.")
