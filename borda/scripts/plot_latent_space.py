import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def main():
    print("🚀 Loading datasets for Latent Space PCA comparison...")
    real_path = 'borda/results/elite_borda_training_table.parquet'
    synth_path = 'borda/results/synthetic_samples_elite_borda_120000.parquet'
    ctgan_path = 'results/synthetic_samples_5000.parquet'
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path) or not os.path.exists(ctgan_path):
        print("❌ Error: Missing datasets.")
        return
        
    df_real = pd.read_parquet(real_path)
    df_forest = pd.read_parquet(synth_path)
    df_ctgan = pd.read_parquet(ctgan_path)
    
    # Identify gene features (excluding metadata columns)
    metadata_cols = ['GSE_ID', 'Category', 'Technology_Label']
    features = [col for col in df_real.columns if col not in metadata_cols]
    
    # Filter features that exist in CTGAN
    features_in_ctgan = [col for col in features if col in df_ctgan.columns]
    print(f"   Using {len(features_in_ctgan)} common gene features for PCA.")
    
    # Sample 1000 from each for visual clarity
    np.random.seed(42)
    sample_size = 1000
    
    X_real = df_real[features_in_ctgan].sample(n=min(sample_size, len(df_real)), random_state=42)
    X_forest = df_forest[features_in_ctgan].sample(n=min(sample_size, len(df_forest)), random_state=42)
    X_ctgan = df_ctgan[features_in_ctgan].sample(n=min(sample_size, len(df_ctgan)), random_state=42)
    
    # Labeling
    labels = (['Real'] * len(X_real)) + (['CTGAN (Mode Collapse)'] * len(X_ctgan)) + (['Forest Diffusion (SOTA)'] * len(X_forest))
    
    # Combine features
    combined_X = pd.concat([X_real, X_ctgan, X_forest], axis=0)
    
    # Standardize
    print("   Scaling features...")
    scaler = StandardScaler()
    combined_scaled = scaler.fit_transform(combined_X)
    
    # PCA
    print("   Running PCA...")
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(combined_scaled)
    
    # Plotting
    plt.figure(figsize=(10, 7))
    sns.set_style("whitegrid")
    
    # Premium color palette
    palette = {
        'Real': '#4A90E2',                  # Soft Blue
        'CTGAN (Mode Collapse)': '#FF6B6B',  # Coral Red
        'Forest Diffusion (SOTA)': '#1DD1A1' # Mint Green
    }
    
    plot_df = pd.DataFrame({
        'PC1': components[:, 0],
        'PC2': components[:, 1],
        'Origen': labels
    })
    
    sns.scatterplot(
        data=plot_df[plot_df['Origen'] == 'Real'],
        x='PC1', y='PC2',
        color=palette['Real'],
        marker='o',
        alpha=0.4,
        s=50,
        label='Real'
    )
    
    sns.scatterplot(
        data=plot_df[plot_df['Origen'] == 'CTGAN (Mode Collapse)'],
        x='PC1', y='PC2',
        color=palette['CTGAN (Mode Collapse)'],
        marker='x',
        alpha=0.6,
        s=40,
        label='CTGAN (Mode Collapse)'
    )
    
    sns.scatterplot(
        data=plot_df[plot_df['Origen'] == 'Forest Diffusion (SOTA)'],
        x='PC1', y='PC2',
        color=palette['Forest Diffusion (SOTA)'],
        marker='^',
        alpha=0.5,
        s=45,
        label='Forest Diffusion (SOTA)'
    )
    
    plt.title('Comparativa de Espacio Latente: Real vs. CTGAN vs. Forest Diffusion (2026)', fontsize=14, fontweight='bold')
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    plt.legend(title="Fuente de Datos", fontsize=10, loc='best')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    # Save output paths
    out_path1 = 'results/fidelity_pca_ctgan.png'
    out_path2 = 'borda/results/fidelity_pca_ctgan.png' # Advisor copy path
    
    plt.savefig(out_path1, dpi=300, bbox_inches='tight')
    
    # Create directory if missing
    os.makedirs(os.path.dirname(out_path2), exist_ok=True)
    plt.savefig(out_path2, dpi=300, bbox_inches='tight')
    
    plt.close()
    print("✅ PCA Comparison Plot generated successfully!")

if __name__ == "__main__":
    main()
