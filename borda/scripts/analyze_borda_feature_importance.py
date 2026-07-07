import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import os
import warnings

warnings.filterwarnings('ignore')

def analyze_borda_importance():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--real_path', type=str, default='results/elite_borda_training_table.parquet')
    parser.add_argument('--synth_path', type=str, default='results/synthetic_samples_elite_borda_5000.parquet')
    args = parser.parse_args()

    real_path = args.real_path
    synth_path = args.synth_path

    # Autodetectar prefijo 'datasets/' si estamos en la raíz del repositorio de Colab
    prefix = ""
    if os.path.exists("datasets") and not os.path.exists(real_path):
        if os.path.exists(os.path.join("datasets", real_path)):
            prefix = "datasets/"
            print(f"ℹ️ Detectada estructura de carpetas de Drive: usando prefijo '{prefix}'")
            
    real_path = os.path.join(prefix, real_path)
    synth_path = os.path.join(prefix, synth_path)
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        print(f"⏳ Faltan archivos.\nReal: {real_path} (Existe: {os.path.exists(real_path)})\nSynth: {synth_path} (Existe: {os.path.exists(synth_path)})")
        return
        
    print(f"📂 Cargando datos...\nReal: {real_path}\nSynth: {synth_path}")
    real_df = pd.read_parquet(real_path)
    synth_df = pd.read_parquet(synth_path)
    
    target_col = 'Category' if 'Category' in real_df.columns else 'target'
    drop_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
    features = [c for c in real_df.columns if c not in drop_cols]
    
    # 1. Importance in Real Data
    print("🌲 Analizando importancia en datos reales...")
    rf_real = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    rf_real.fit(real_df[features], real_df[target_col].astype(int))
    
    importance_real = pd.DataFrame({
        'Gene': features,
        'Importance_Real': rf_real.feature_importances_
    }).sort_values('Importance_Real', ascending=False)
    
    # 2. Importance in Synthetic Data
    print("🌲 Analizando importancia en datos sintéticos...")
    rf_synth = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    rf_synth.fit(synth_df[features], synth_df[target_col].astype(int))
    
    importance_synth = pd.DataFrame({
        'Gene': features,
        'Importance_Synth': rf_synth.feature_importances_
    }).sort_values('Importance_Synth', ascending=False)
    
    # 3. Jaccard Similarity on Top 50
    top_k = 50
    top_real_set = set(importance_real.head(top_k)['Gene'])
    top_synth_set = set(importance_synth.head(top_k)['Gene'])
    intersection = top_real_set.intersection(top_synth_set)
    union = top_real_set.union(top_synth_set)
    jaccard = len(intersection) / len(union)
    
    print("\n=== RESULTADOS DE FIDELIDAD DE BIOMARCADORES (Borda) ===")
    print(f"Jaccard Similarity (Top {top_k}): {jaccard:.4f}")
    print(f"Número de genes coincidentes: {len(intersection)}")
    print(f"Genes coincidentes: {sorted(list(intersection))}")
    
    # 4. Top 15 coincidentes ordenados por importancia sintética promedio
    comparison = importance_real.merge(importance_synth, on='Gene')
    comparison['Mean_Importance'] = (comparison['Importance_Real'] + comparison['Importance_Synth']) / 2
    top_coincidences = comparison[comparison['Gene'].isin(intersection)].sort_values('Mean_Importance', ascending=False)
    print("\n🏆 Top Biomarcadores Preservados por la IA:")
    print(top_coincidences.head(15))
    
    metrics_dir = os.path.join(prefix, 'results/metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    
    csv_out = os.path.join(metrics_dir, 'top_15_preserved_biomarkers.csv')
    top_coincidences.head(15).to_csv(csv_out, index=False)
    
    # Plotting comparison
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="whitegrid")
    
    plot_data = comparison[comparison['Gene'].isin(top_coincidences.head(15)['Gene'])].sort_values('Mean_Importance', ascending=False)
    plot_melted = plot_data.melt(id_vars='Gene', value_vars=['Importance_Real', 'Importance_Synth'],
                                 var_name='Origen_Datos', value_name='Importancia')
    
    # Rename categories for plot
    plot_melted['Origen_Datos'] = plot_melted['Origen_Datos'].map({
        'Importance_Real': 'Datos Reales (Élite Borda)',
        'Importance_Synth': 'Datos Sintéticos (Generados)'
    })
    
    ax = sns.barplot(
        data=plot_melted,
        y='Gene',
        x='Importancia',
        hue='Origen_Datos',
        palette=['#3182bd', '#e6550d']
    )
    
    plt.title('Comparación de Importancia del Biomarcador: Real vs. Sintético (Top 15 Preservados)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Importancia de Impureza (Gini)', fontsize=12)
    plt.ylabel('Gen', fontsize=12)
    plt.legend(loc='lower right')
    plt.tight_layout()
    
    metrics_dir = os.path.join(prefix, 'results/metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    img_out = os.path.join(metrics_dir, 'biomarcadores_preservados_heatmap.png')
    plt.savefig(img_out, dpi=300)
    print(f"🎨 Gráfica guardada en {img_out}")

if __name__ == "__main__":
    analyze_borda_importance()
