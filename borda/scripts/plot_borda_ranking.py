import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import shap
import warnings

warnings.filterwarnings('ignore')

def plot_borda_ranking():
    print("📥 Cargando cohorte Élite completa para análisis Borda...")
    input_file = 'results/elite_full_training_table.parquet'
    
    if not os.path.exists(input_file):
        print(f"❌ Error: No se encontró {input_file}")
        return
        
    df = pd.read_parquet(input_file)
    target_col = 'Category' if 'Category' in df.columns else 'target'
    
    X = df.drop(columns=[col for col in ['GSE_ID', target_col, 'target', 'Technology_Label'] if col in df.columns])
    y = df[target_col].astype(int)
    
    print(f"📊 Dataset cargado: {X.shape[0]} muestras × {X.shape[1]} genes.")
    print("🗳️  Ejecutando algoritmos del Ensamble para votación Borda...")
    
    X_clean = np.array(X, dtype=np.float32)
    
    # 1. F-Test
    print("   [1/3] Calculando F-Test Ranks...")
    selector = SelectKBest(f_classif, k='all')
    selector.fit(X_clean, y)
    f_scores = np.nan_to_num(selector.scores_, nan=0.0)
    f_ranks = pd.Series(f_scores, index=X.columns).rank(ascending=False, method='min')
    
    # 2. Random Forest
    print("   [2/3] Entrenando Random Forest para Importancias...")
    rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
    rf.fit(X_clean, y)
    rf_ranks = pd.Series(rf.feature_importances_, index=X.columns).rank(ascending=False, method='min')
    
    # 3. SHAP (XGBoost)
    print("   [3/3] Entrenando XGBoost + SHAP para Explicabilidad...")
    model = xgb.XGBClassifier(n_estimators=50, max_depth=3, random_state=42, n_jobs=-1)
    model.fit(X_clean, y)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_clean)
    import_scores = np.abs(shap_values).mean(axis=0)
    shap_ranks = pd.Series(import_scores, index=X.columns).rank(ascending=False, method='min')
    
    # 4. Tabla Borda
    print("🗳️ Consolidando Votación Borda...")
    borda_df = pd.DataFrame({
        'F-Test Rank': f_ranks,
        'RF Rank': rf_ranks,
        'SHAP Rank': shap_ranks
    })
    borda_df['Borda Mean Rank'] = borda_df.mean(axis=1)
    borda_df = borda_df.sort_values(by='Borda Mean Rank', ascending=True)
    
    # Tomar los top 15 genes
    top_15 = borda_df.head(15)
    print("\n🏆 Top 15 Genes por Consenso Borda:")
    print(top_15)
    
    # Guardar CSV de soporte
    os.makedirs('results/metrics', exist_ok=True)
    top_15.to_csv('results/metrics/top_15_borda_ranks.csv')
    
    # Plotear Heatmap
    plt.figure(figsize=(10, 8))
    sns.set_theme(style="white")
    
    # Queremos que los rangos más bajos (1, 2, 3...) resalten en colores cálidos (oro/naranja)
    # y los rangos más altos en colores fríos. Usamos cmap reversa.
    ax = sns.heatmap(
        top_15,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd_r",
        linewidths=1.5,
        cbar_kws={'label': 'Rango (Menor es mejor)'}
    )
    
    plt.title('Consenso Ensemble Borda Count: Top 15 Genes Oncológicos', fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('Gen Selector', fontsize=12, fontweight='bold')
    plt.xlabel('Criterio de Evaluación de Importancia', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_png = 'results/metrics/consenso_borda_heatmap.png'
    plt.savefig(output_png, dpi=300)
    plt.close()
    
    print(f"\n✅ ¡Éxito! Gráfica premium de Borda guardada en {output_png}")

if __name__ == "__main__":
    plot_borda_ranking()
