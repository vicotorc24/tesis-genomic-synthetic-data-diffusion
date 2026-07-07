import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_low_data_augmentation():
    print("Cargando datos...")
    # Load Real Test Data (Jurado Imparcial)
    test_df = pd.read_parquet('results/core_test.parquet')
    X_test = test_df.drop(columns=['Target'])
    y_test = test_df['Target']
    
    # Load Real Train Data
    train_df = pd.read_parquet('results/core_train.parquet')
    
    # Load Synthetic Data
    synth_df = pd.read_parquet('results/synthetic_samples_lite_5000.parquet')
    
    # Ensure same columns
    common_cols = list(set(train_df.columns).intersection(set(synth_df.columns)))
    target_col = 'Target'
    features = [c for c in common_cols if c != target_col]
    
    X_test = X_test[features]
    
    # Low Data Regime: We only have 200 real patients
    low_data_train = train_df.sample(n=200, random_state=42)
    X_real_base = low_data_train[features]
    y_real_base = low_data_train[target_col]
    
    results = []
    
    # 1. Baseline: Train strictly on 200 real patients
    clf = xgb.XGBClassifier(eval_metric='logloss', random_state=42, use_label_encoder=False)
    clf.fit(X_real_base, y_real_base)
    preds = clf.predict_proba(X_test)[:, 1]
    baseline_auc = roc_auc_score(y_test, preds)
    results.append({'Synthetic_Added': 0, 'AUC': baseline_auc})
    print(f"Baseline (200 Real): {baseline_auc:.4f}")
    
    # 2. Add Synthetic Data in steps
    synth_steps = [100, 500, 1000, 2000, 5000]
    
    for step in synth_steps:
        synth_subset = synth_df.sample(n=step, random_state=42)
        X_synth = synth_subset[features]
        y_synth = synth_subset[target_col]
        
        # Combine
        X_combined = pd.concat([X_real_base, X_synth])
        y_combined = pd.concat([y_real_base, y_synth])
        
        clf.fit(X_combined, y_combined)
        preds = clf.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, preds)
        results.append({'Synthetic_Added': step, 'AUC': auc})
        print(f"Added {step} Synthetic -> AUC: {auc:.4f}")
        
    df_res = pd.DataFrame(results)
    
    # PLOT
    plt.figure(figsize=(10, 6))
    plt.plot(df_res['Synthetic_Added'], df_res['AUC'], marker='o', linestyle='-', color='forestgreen', linewidth=3, markersize=10)
    
    plt.axhline(y=baseline_auc, color='red', linestyle='--', linewidth=2, label=f'Baseline (Sólo 200 Reales) = {baseline_auc:.3f}')
    
    plt.title('Curva de Aumentación TSTR en Régimen de Datos Bajos', fontsize=15, fontweight='bold')
    plt.ylabel('Desempeño Diagnóstico (ROC-AUC) en Test Real')
    plt.xlabel('Número de Pacientes Sintéticos Añadidos (Generados por Forest Diffusion)')
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    
    plt.annotate('Convergencia Asintótica\n(Rendimientos Decrecientes)', 
                 xy=(5000, df_res['AUC'].iloc[-1]), 
                 xytext=(3000, df_res['AUC'].iloc[-1] - 0.02),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=11)
                 
    plt.tight_layout()
    plt.savefig('results/metrics/curva_augmentacion_low_data.png', dpi=300)
    print("Gráfico generado en results/metrics/curva_augmentacion_low_data.png")

if __name__ == "__main__":
    run_low_data_augmentation()
