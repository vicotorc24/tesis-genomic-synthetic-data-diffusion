import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from feature_selection import apply_feature_selection
import os

def calculate_jaccard(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

def run_stability_experiment(real_path, synth_path, sizes=[100, 500, 1000, 3000, 5000], top_k=100):
    print(f"🧪 Iniciando Experimento de Estabilidad Genómica (Top {top_k})")
    
    real_df = pd.read_parquet(real_path)
    synth_df_full = pd.read_parquet(synth_path)
    
    # 1. FS sobre Real (Gold Standard) utilizando f_test para velocidad
    real_genes = apply_feature_selection(real_df, method='f_test', k=top_k)
    
    jaccard_scores = []
    
    for size in sizes:
        print(f"Probando cohorte sintética de tamaño: {size}...")
        temp_synth = synth_df_full.sample(n=size, random_state=42)
        synth_genes = apply_feature_selection(temp_synth, method='f_test', k=top_k)
        
        score = calculate_jaccard(real_genes, synth_genes)
        jaccard_scores.append(score)
    
    # 2. Generar Gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, jaccard_scores, marker='o', linestyle='-', color='#FF6B6B', linewidth=2.5, markersize=8)
    plt.fill_between(sizes, jaccard_scores, alpha=0.1, color='#FF6B6B')
    
    plt.title("Curva de Estabilidad Genómica: Rescate de Biomarcadores vs. Tamaño de Cohorte", fontsize=14, fontweight='bold')
    plt.xlabel("Número de Pacientes Sintéticos Generados", fontsize=12)
    plt.ylabel(f"Índice de Jaccard (Top {top_k} Genes)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    output_path = 'results/genomic_stability_curve.png'
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Curva de estabilidad guardada en {output_path}")
    plt.close()

if __name__ == "__main__":
    real_path = 'results/core_train.parquet'
    synth_path = 'results/synthetic_samples_5000.parquet'
    
    if os.path.exists(real_path) and os.path.exists(synth_path):
        run_stability_experiment(real_path, synth_path)
    else:
        print("⏳ Esperando datos...")
