import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_benchmark():
    os.makedirs('results/metrics', exist_ok=True)
    
    # 1. Load Modern Benchmark (Real and Forest Diffusion)
    df_modern = pd.read_csv('results/metrics/MODERN_BENCHMARK_RESULTS_FAST.csv')
    df_modern = df_modern[df_modern['FS'] == 'f_test'].copy()
    df_modern['Context'] = df_modern['Context'].map({
        'Real_Baseline_2026': 'Real (Baseline)', 
        'Sintetico_TSTR_2026': 'Sintético (Forest Diffusion)'
    })
    
    # 2. Load Decadal Benchmark (CTGAN)
    df_decadal = pd.read_csv('results/metrics/DECADAL_BENCHMARK_RESULTS.csv')
    df_ctgan = df_decadal[(df_decadal['FS'] == 'f_test') & (df_decadal['Context'] == 'Synth_2026_CTGAN')].copy()
    
    # Map CTGAN classifiers to match modern ones
    classifier_map = {
        'SVM': 'SVM_RBF_SOTA',
        'RandomForest': 'RandomForest_SOTA'
    }
    df_ctgan['Classifier'] = df_ctgan['Classifier'].map(classifier_map)
    df_ctgan = df_ctgan.dropna(subset=['Classifier'])
    df_ctgan['Context'] = 'Sintético (CTGAN)'
    
    # Combine
    df_combined = pd.concat([df_modern, df_ctgan], ignore_index=True)
    
    # Reorder context for logic (Real -> CTGAN -> Forest Diffusion)
    context_order = ['Real (Baseline)', 'Sintético (CTGAN)', 'Sintético (Forest Diffusion)']
    df_combined['Context'] = pd.Categorical(df_combined['Context'], categories=context_order, ordered=True)
    
    # Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_combined, x='Classifier', y='AUC_Mean', hue='Context', palette=['#31688e', '#fde725', '#35b779'])
    
    plt.title('Evolución SOTA: Comparativa de Discriminación Biológica (AUC)\nReal vs CTGAN vs Forest Diffusion', fontsize=14, fontweight='bold')
    plt.ylabel('ROC-AUC Score')
    plt.xlabel('Clasificador')
    plt.ylim(0.4, 1.0)
    plt.legend(title='Datos de Entrenamiento', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('results/metrics/comparativa_modelos_con_ctgan.png', dpi=300)
    plt.close()
    print("✅ Gráfica generada: results/metrics/comparativa_modelos_con_ctgan.png")

if __name__ == "__main__":
    plot_benchmark()
