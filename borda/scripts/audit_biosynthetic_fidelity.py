import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import spearmanr

def calculate_shap_importance(df, target_col='Category', k=100):
    """Calcula la importancia SHAP global para un dataset."""
    X = df.drop(columns=[col for col in ['GSE_ID', target_col, 'target', 'Technology_Label'] if col in df.columns])
    y = df[target_col if target_col in df.columns else 'target'].astype(int)
    
    model = xgb.XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Importancia global: promedio del valor absoluto de SHAP
    import_scores = np.abs(shap_values).mean(axis=0)
    shap_series = pd.Series(import_scores, index=X.columns)
    return shap_series.sort_values(ascending=False).head(k)

def audit_fidelity():
    print("🚀 Iniciando Auditoría de Fidelidad SOTA 2026 (SHAP)...")
    
    real_path = 'results/core_test.parquet'
    syn_path = 'results/synthetic_core_samples.parquet' # Generado tras entrenamiento
    
    if not os.path.exists(real_path) or not os.path.exists(syn_path):
        print(f"⚠️ Error: No se encuentran los archivos. Real: {os.path.exists(real_path)}, Syn: {os.path.exists(syn_path)}")
        print("Asegúrate de haber generado las muestras sintéticas primero.")
        return

    # Load data
    df_real = pd.read_parquet(real_path)
    df_syn = pd.read_parquet(syn_path)
    
    print(f"📊 Comparando Real (N={len(df_real)}) vs Sintético (N={len(df_syn)})...")
    
    # Calculate SHAP rankings
    top_real = calculate_shap_importance(df_real, k=100)
    top_syn = calculate_shap_importance(df_syn, k=100)
    
    # Jaccard Similarity
    set_real = set(top_real.index)
    set_syn = set(top_syn.index)
    intersection = len(set_real.intersection(set_syn))
    jaccard = intersection / len(set_real.union(set_syn))
    
    print("\n" + "="*40)
    print(f"🧬 RESULTADOS DE FIDELIDAD BIOLÓGICA")
    print("="*40)
    print(f"✅ Genes coincidentes en Top 100: {intersection}")
    print(f"✅ Índice de Jaccard: {jaccard:.4f}")
    
    # Guardar reporte
    with open('results/SHAP_FIDELITY_AUDIT.md', 'w') as f:
        f.write("# Reporte de Fidelidad Biosintética (SHAP 2026)\n\n")
        f.write(f"- **Muestras Reales**: {len(df_real)}\n")
        f.write(f"- **Muestras Sintéticas**: {len(df_syn)}\n")
        f.write(f"- **Solapamiento Genético (Top 100)**: {intersection} genes\n")
        f.write(f"- **Índice de Jaccard**: {jaccard:.4f}\n\n")
        f.write("## Top 10 Genes Coincidentes\n")
        common = list(set_real.intersection(set_syn))[:10]
        for g in common:
            f.write(f"- {g}\n")
            
    print(f"\n💾 Reporte guardado en results/SHAP_FIDELITY_AUDIT.md")

if __name__ == "__main__":
    audit_fidelity()
