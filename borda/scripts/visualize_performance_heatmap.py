import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_heatmaps():
    # 1. Cargar resultados
    modern_df = pd.read_csv('results/metrics/MODERN_BENCHMARK_RESULTS_2026.csv')
    decadal_df = pd.read_csv('results/metrics/DECADAL_BENCHMARK_RESULTS.csv')
    
    # 2. Filtrar para el Datalake Real 2026 en ambos escenarios
    # Moderno
    modern_real = modern_df[modern_df['Context'] == 'Datalake_Real_2026']
    modern_pivot = modern_real.pivot(index='FS', columns='Classifier', values='AUC_Mean')
    
    # Decadal (Legacy algorithms on Real 2026)
    decadal_real = decadal_df[decadal_df['Context'] == 'Real_2026']
    decadal_pivot = decadal_real.pivot(index='FS', columns='Classifier', values='AUC_Mean')
    
    # 3. Graficar Comparativa SOTA 2026
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="white")
    
    ax = sns.heatmap(modern_pivot, annot=True, cmap='viridis', fmt=".3f", 
                    linewidths=.5, cbar_kws={'label': 'AUC Score'})
    
    plt.title('Matriz de Desempeño Diagnóstico: Modelos de Clasificación\n(Datalake Real N=1024)', fontsize=14, pad=20)
    plt.ylabel('Selector de Atributos', fontsize=12)
    plt.xlabel('Clasificador SOTA', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('results/HEATMAP_PERFORMANCE_SOTA_2026.png', dpi=300)
    print("✅ Heatmap SOTA 2026 guardado en results/HEATMAP_PERFORMANCE_SOTA_2026.png")
    
    # 4. Graficar Comparativa Decadal (Legacy vs SOTA)
    plt.figure(figsize=(12, 8))
    sns.heatmap(decadal_pivot, annot=True, cmap='magma', fmt=".3f", 
                linewidths=.5, cbar_kws={'label': 'AUC Score'})
    
    plt.title('Matriz Decadal: Algoritmos Históricos 2021 sobre Datalake 2026\n(Validación de Robustez de Datos)', fontsize=15, pad=20)
    plt.ylabel('Selector Clásico', fontsize=12)
    plt.xlabel('Clasificador Clásico', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('results/HEATMAP_LEGACY_CONTRAST_2026.png', dpi=300)
    print("✅ Heatmap Contraste Legacy guardado en results/HEATMAP_LEGACY_CONTRAST_2026.png")

if __name__ == "__main__":
    os.makedirs('results', exist_ok=True)
    generate_heatmaps()
