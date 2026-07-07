import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_final_heatmap():
    perf_path = 'results/REPRODUCED_MATRIX_2021.csv'
    if not os.path.exists(perf_path):
        print("❌ Matriz de desempeño no encontrada.")
        return

    df = pd.read_csv(perf_path)
    df.set_index('dataset', inplace=True)
    
    # Limpiamos nombres de columnas para que se vean bien
    df.columns = [c.replace('f_test-', 'FT-').replace('l1-', 'L1-').replace('chi2-', 'CH-').replace('rfe-', 'RF-') for c in df.columns]

    plt.figure(figsize=(15, 20))
    sns.heatmap(df, annot=False, cmap='viridis', cbar_kws={'label': 'AUC-ROC'})
    plt.title('Matriz de Desempeño Histórica Reconstruida (2021)\n60 Datasets x 24 Parejas de Algoritmos', fontsize=16)
    plt.xlabel('Parejas Algorítmicas (FS-Clasificador)', fontsize=12)
    plt.ylabel('Datasets Microarray (60)', fontsize=12)
    
    plt.tight_layout()
    output_path = 'results/HEATMAP_REPRODUCED_2021.png'
    plt.savefig(output_path, dpi=300)
    print(f"✅ Heatmap guardado en {output_path}")

if __name__ == "__main__":
    generate_final_heatmap()
