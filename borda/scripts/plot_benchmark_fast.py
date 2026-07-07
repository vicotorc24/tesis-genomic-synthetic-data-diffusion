import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_benchmark():
    os.makedirs('results/metrics', exist_ok=True)
    
    # 1. Plot TTR vs TSTS Bar Chart
    df = pd.read_csv('results/metrics/MODERN_BENCHMARK_RESULTS_FAST.csv')
    df_shap = df[df['FS'] == 'shap'].copy()
    
    # Clean Context labels
    df_shap['Context'] = df_shap['Context'].map({'Real_Baseline_2026': 'Real (Baseline)', 'Sintetico_TSTR_2026': 'Sintético (TSTS)'})
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_shap, x='Classifier', y='AUC_Mean', hue='Context', palette='viridis')
    plt.title('Comparativa de Discriminación Biológica (AUC) - Top 100 Genes (SHAP)', fontsize=14, fontweight='bold')
    plt.ylabel('ROC-AUC Score')
    plt.xlabel('Clasificador')
    plt.ylim(0.4, 1.0)
    plt.legend(title='Datos de Entrenamiento')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('results/metrics/comparativa_modelos.png', dpi=300)
    plt.close()

    # 2. Plot Augmentation Curve
    df_aug = pd.read_csv('results/metrics/augmentation_curve_results.csv')
    
    # Map absolute numbers to 1r+ns nomenclature
    labels = []
    base_size = 11219
    for s in df_aug['Synthetic_Samples']:
        if s == 0:
            labels.append('1r')
        else:
            ratio = int(s / base_size)
            labels.append(f'1r+{ratio}s')
            
    plt.figure(figsize=(10, 6))
    x_indices = range(len(df_aug['Synthetic_Samples']))
    plt.plot(x_indices, df_aug['AUC_Test_Real'], marker='o', linestyle='-', color='dodgerblue', linewidth=2, markersize=8)
    
    # Add baseline dashed line
    baseline_auc = df_aug.loc[df_aug['Synthetic_Samples'] == 0, 'AUC_Test_Real'].values[0]
    plt.axhline(y=baseline_auc, color='red', linestyle='--', label=f'Línea Base (1r) = {baseline_auc:.4f}')
    
    plt.xticks(x_indices, labels)
    plt.title('Curva de Aumentación TSTR bajo Marco 1r+ns', fontsize=14, fontweight='bold')
    plt.ylabel('ROC-AUC en Set de Prueba Real (Hold-out 20%)')
    plt.xlabel('Nivel de Aumentación (Cohortes Sintéticas inyectadas)')
    plt.legend()
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('results/metrics/curva_augmentacion.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_benchmark()
