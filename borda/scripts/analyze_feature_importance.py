import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import os

# Directories
RESULTS_DIR = 'results'
REPORTS_DIR = 'REPORTS'
os.makedirs(REPORTS_DIR, exist_ok=True)

def analyze_importance():
    real_path = os.path.join(RESULTS_DIR, 'core_train.parquet')
    synth_path = os.path.join(RESULTS_DIR, 'synthetic_samples_5000.parquet')
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        print("⏳ Faltan archivos. Asegúrate de que el entrenamiento y la generación hayan terminado.")
        return

    print("📂 Cargando datos para análisis de importancia...")
    real_df = pd.read_parquet(real_path).drop(columns=['GSE_ID'])
    synth_df = pd.read_parquet(synth_path)
    
    target = 'Category'
    # Features (genes) only
    features = [c for c in real_df.columns if c not in ['Technology_Label', 'Category']]
    
    # 1. Importance in Real Data
    print("🌲 Analizando importancia en datos REALES...")
    rf_real = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    rf_real.fit(real_df[features], real_df[target].astype(int))
    
    importance_real = pd.DataFrame({
        'Gene': features,
        'Importance_Real': rf_real.feature_importances_
    }).sort_values('Importance_Real', ascending=False)

    # 2. Importance in Synthetic Data
    print("🌲 Analizando importancia en datos SINTÉTICOS...")
    rf_synth = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    rf_synth.fit(synth_df[features], synth_df[target].astype(int))
    
    importance_synth = pd.DataFrame({
        'Gene': features,
        'Importance_Synth': rf_synth.feature_importances_
    }).sort_values('Importance_Synth', ascending=False)

    # 3. Comparison
    top_20_real = importance_real.head(20)
    # Merge for comparison
    comparison = top_20_real.merge(importance_synth, on='Gene')
    
    print("\n--- TOP 10 BIOMARCADORES DETECTADOS ---")
    print(comparison[['Gene', 'Importance_Real', 'Importance_Synth']].head(10))

    # 4. Visualization
    plt.figure(figsize=(12, 8))
    comp_melted = comparison.melt(id_vars='Gene', var_name='Data_Source', value_name='Importance')
    sns.barplot(data=comp_melted, y='Gene', x='Importance', hue='Data_Source', palette='viridis')
    plt.title('Comparación de Importancia Clínica: Real vs Sintético (Top 20 Genes Reales)')
    plt.xlabel('Gini Importance')
    plt.tight_layout()
    
    output_plot = os.path.join(REPORTS_DIR, 'feature_importance_comparison.png')
    plt.savefig(output_plot)
    print(f"\n✅ Gráfico guardado en {output_plot}")

    # Calculate Jaccard Similarity of Top 50 genes
    top_50_real_set = set(importance_real.head(50)['Gene'])
    top_50_synth_set = set(importance_synth.head(50)['Gene'])
    intersection = top_50_real_set.intersection(top_50_synth_set)
    jaccard = len(intersection) / len(top_50_real_set.union(top_50_synth_set))
    
    print(f"📊 Jaccard Similarity (Top 50 Biomarkers): {jaccard:.4f}")
    print(f"🧬 Genes comunes en Top 50: {len(intersection)}")

if __name__ == "__main__":
    analyze_importance()
