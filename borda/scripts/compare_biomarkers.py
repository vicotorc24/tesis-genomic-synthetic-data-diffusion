import pandas as pd
import numpy as np
from feature_selection import apply_feature_selection
import os

def calculate_jaccard(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

def run_biomarker_audit(real_path, synth_path, top_k=50, method='f_test'):
    print(f"\n🧪 Iniciando Auditoría de Inteligencia (Top {top_k} via {method})")
    
    real_df = pd.read_parquet(real_path)
    synth_df = pd.read_parquet(synth_path)
    
    # 1. FS sobre Real
    print("Analizando Verdad Biológica (Real)...")
    real_genes = apply_feature_selection(real_df, method=method, k=top_k)
    
    # 2. FS sobre Sintético
    print("Analizando Reconstrucción IA (Sintético)...")
    synth_genes = apply_feature_selection(synth_df, method=method, k=top_k)
    
    # 3. Comparación
    score = calculate_jaccard(real_genes, synth_genes)
    overlap = len(set(real_genes).intersection(set(synth_genes)))
    
    print("-" * 30)
    print(f"RESUMEN DE AUDITORÍA:")
    print(f"Genes coincidentes: {overlap} de {top_k}")
    print(f"Índice de Jaccard: {score:.4f}")
    print("-" * 30)
    
    return {
        'method': method,
        'jaccard': score,
        'overlap': overlap,
        'real_top': real_genes[:10],
        'synth_top': synth_genes[:10]
    }

if __name__ == "__main__":
    real_path = 'results/core_train.parquet'
    synth_path = 'results/synthetic_samples_5000.parquet'
    
    if os.path.exists(synth_path):
        results = run_biomarker_audit(real_path, synth_path)
        print(f"Top 10 Reales: {results['real_top']}")
        print(f"Top 10 Sintéticos: {results['synth_top']}")
    else:
        print("⏳ Data sintética no encontrada. Generando...")
