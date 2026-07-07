import os
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

def main():
    print("🚀 Starting REAL Cohorts Analysis for Elite Borda...")
    real_path = 'borda/results/elite_borda_training_table.parquet'
    synth_path = 'borda/results/synthetic_samples_elite_borda_120000.parquet'
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        # Fallback to root paths if not found
        real_path = 'results/elite_borda_training_table.parquet'
        synth_path = 'results/synthetic_samples_elite_borda_120000.parquet'
        
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        print("❌ Error: Missing datasets.")
        return
        
    df_real = pd.read_parquet(real_path)
    df_synth = pd.read_parquet(synth_path)
    
    target_col = 'Category'
    tech_col = 'Technology_Label'
    features = [col for col in df_real.columns if col not in ['GSE_ID', target_col, tech_col]]
    
    ratios = [0, 1, 5, 11, 22]
    ratio_labels = ['1r', '1r+1s', '1r+5s', '1r+11s', '1r+22s']
    
    cohorts = [
        ('Microarrays', 1, 'Cohorte Aislada: Microarrays (Legado)', 'gray', '^', '--'),
        ('RNA_seq', 0, 'Cohorte Aislada: RNA-seq (Moderno)', 'royalblue', 's', '-.'),
        ('Harmonized', None, 'Datalake Armonizado (Sinergia Total)', 'darkorange', 'o', '-')
    ]
    
    results = {}
    
    clf = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        tree_method='hist'
    )
    
    for key, tech_val, label, color, marker, linestyle in cohorts:
        print(f"   Evaluating cohort: {key}...")
        if tech_val is not None:
            df_real_c = df_real[df_real[tech_col] == tech_val]
            df_synth_c = df_synth[df_synth[tech_col] == tech_val]
        else:
            df_real_c = df_real
            df_synth_c = df_synth
            
        X_real = df_real_c[features]
        y_real = df_real_c[target_col].astype(int)
        
        X_train_real, X_test_real, y_train_real, y_test_real = train_test_split(
            X_real, y_real, test_size=0.2, random_state=42, stratify=y_real
        )
        
        n_train = len(X_train_real)
        cohort_aucs = []
        
        for r in ratios:
            n_synth = int(n_train * r)
            if r == 0:
                X_train = X_train_real
                y_train = y_train_real
            else:
                synth_sample = df_synth_c.sample(n_synth, replace=True, random_state=42)
                X_synth_sample = synth_sample[features]
                y_synth_sample = synth_sample[target_col].astype(int)
                X_train = pd.concat([X_train_real, X_synth_sample])
                y_train = pd.concat([y_train_real, y_synth_sample])
                
            clf.fit(X_train, y_train)
            auc = roc_auc_score(y_test_real, clf.predict_proba(X_test_real)[:, 1])
            cohort_aucs.append(auc)
            print(f"      Ratio {r} (Real: {n_train}, Synth: {n_synth}) -> AUC = {auc:.4f}")
            
        results[key] = cohort_aucs
        
    # Plotting
    plt.figure(figsize=(10, 6))
    x_indices = np.arange(len(ratios))
    
    plt.plot(x_indices, results['Microarrays'], marker='^', color='gray', linewidth=2, linestyle='--', label='Cohorte Aislada: Microarrays (Legado)')
    plt.plot(x_indices, results['RNA_seq'], marker='s', color='royalblue', linewidth=2, linestyle='-.', label='Cohorte Aislada: RNA-seq (Moderno)')
    plt.plot(x_indices, results['Harmonized'], marker='o', color='darkorange', linewidth=3, label='Datalake Armonizado (Sinergia Total)')
    
    baseline_auc = results['Harmonized'][0]
    plt.axhline(y=baseline_auc, color='red', linestyle=':', alpha=0.6, label=f'Baseline Control (1r Armonizado) = {baseline_auc:.4f}')
    
    plt.xticks(x_indices, ratio_labels)
    plt.title('Evaluación Generativa por Cohortes Tecnológicas (Marco 1r+ns)', fontsize=14, fontweight='bold')
    plt.ylabel('Retención de Fidelidad Predictiva (ROC-AUC)')
    plt.xlabel('Nivel de Aumentación Sintética (Forest Diffusion)')
    plt.legend(loc='lower left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    os.makedirs('results/metrics/', exist_ok=True)
    os.makedirs('borda/results/metrics/', exist_ok=True)
    
    plt.savefig('results/metrics/comparativa_cohortes.png', dpi=300)
    plt.savefig('borda/results/metrics/comparativa_cohortes.png', dpi=300)
    plt.close()
    
    df_out = pd.DataFrame({
        'Escenario_Sintetico': ratio_labels,
        'Microarrays_Only': results['Microarrays'],
        'RNA_seq_Only': results['RNA_seq'],
        'Harmonized_Datalake': results['Harmonized']
    })
    df_out.to_csv('results/metrics/real_cohort_analysis.csv', index=False)
    df_out.to_csv('borda/results/metrics/real_cohort_analysis.csv', index=False)
    print("✅ REAL Cohorts Analysis completed successfully!")

if __name__ == "__main__":
    main()
