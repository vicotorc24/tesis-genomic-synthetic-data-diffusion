import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def main():
    print("🚀 Generating updated performance heatmap for Elite Borda (N=9309)...")
    
    # 1. Load results
    csv_path = 'borda/results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv'
    if not os.path.exists(csv_path):
        print(f"❌ No se encontró el archivo: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    # 2. Filter for the Real Elite Borda context
    df_real = df[df['Context'] == 'Real_Elite_Borda_2026'].copy()
    
    # Rename classifiers for cleaner labels if needed
    clf_mapping = {
        'XGBoost': 'XGBoost',
        'CatBoost': 'CatBoost',
        'TabPFN': 'TabPFN (SOTA 2026)',
        'SVM_RBF_SOTA': 'SVM (RBF)',
        'RandomForest_SOTA': 'Random Forest'
    }
    df_real['Classifier'] = df_real['Classifier'].map(clf_mapping)
    
    # Order selectors and classifiers for better presentation
    selectors_order = ['f_test', 'rfe', 'lasso', 'mrmr', 'shap']
    classifiers_order = ['SVM (RBF)', 'Random Forest', 'CatBoost', 'XGBoost', 'TabPFN (SOTA 2026)']
    
    # Pivot the data
    pivot_df = df_real.pivot(index='FS', columns='Classifier', values='AUC_Mean')
    
    # Reindex to force clean layout
    pivot_df = pivot_df.reindex(index=selectors_order, columns=classifiers_order)
    
    # Plot
    plt.figure(figsize=(11, 7))
    sns.set_theme(style="white")
    
    ax = sns.heatmap(
        pivot_df, 
        annot=True, 
        cmap='viridis', 
        fmt=".3f", 
        linewidths=.5, 
        cbar_kws={'label': 'AUC Score'},
        annot_kws={'size': 11, 'weight': 'bold'}
    )
    
    plt.title('Matriz de Desempeño Diagnóstico: Modelos de Clasificación\n(Datalake Real N=9,309 - Modelo Élite Borda)', fontsize=13, fontweight='bold', pad=20)
    plt.ylabel('Selector de Atributos', fontsize=12, fontweight='bold')
    plt.xlabel('Clasificador SOTA', fontsize=12, fontweight='bold')
    plt.xticks(rotation=15)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    # Save paths
    out_path1 = 'results/HEATMAP_PERFORMANCE_SOTA_2026.png'
    out_path2 = 'borda/results/HEATMAP_PERFORMANCE_SOTA_2026.png'
    
    os.makedirs(os.path.dirname(out_path1), exist_ok=True)
    plt.savefig(out_path1, dpi=300)
    
    os.makedirs(os.path.dirname(out_path2), exist_ok=True)
    plt.savefig(out_path2, dpi=300)
    
    plt.close()
    print("✅ Heatmap SOTA 2026 updated successfully in both locations!")

if __name__ == "__main__":
    main()
