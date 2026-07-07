import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_benchmark_elite():
    csv_path = 'results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv'
    prefix = ""
    if not os.path.exists(csv_path) and os.path.exists('datasets/' + csv_path):
        prefix = 'datasets/'

    full_path = os.path.join(prefix, csv_path)

    if not os.path.exists(full_path):
        print(f"❌ No se encontró el archivo {full_path}")
        return

    df = pd.read_csv(full_path)
    
    # Filter for SHAP (since it represents SOTA feature selection)
    df_shap = df[df['FS'] == 'shap'].copy()
    
    # Map Context names
    df_shap['Context'] = df_shap['Context'].map({
        'Real_Elite_Borda_2026': 'Real (Baseline)',
        'Sintetico_Elite_Borda_2026': 'Sintético (TSTR)'
    })
    
    plt.figure(figsize=(10, 6))
    
    # Define colors
    colors = ['#1f77b4', '#ff7f0e'] # Real vs Synth
    
    sns.barplot(data=df_shap, x='Classifier', y='AUC_Mean', hue='Context', palette=colors)
    
    plt.title('Comparativa de Desempeño ROC-AUC - Alta Dimensionalidad Borda (Top 100 Genes SHAP)\nReal vs Sintético (TSTR)', fontsize=13, fontweight='bold')
    plt.ylabel('ROC-AUC Score')
    plt.xlabel('Clasificador')
    plt.ylim(0.4, 1.0)
    plt.legend(title='Datos de Entrenamiento', loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_plot = os.path.join(prefix, 'results/metrics/comparativa_modelos_elite.png')
    plt.savefig(output_plot, dpi=300)
    plt.close()
    print(f"✅ Gráfica guardada en: {output_plot}")

if __name__ == "__main__":
    plot_benchmark_elite()
