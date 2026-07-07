import os
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

def main():
    print("🚀 Starting real Augmentation Curve for Elite Borda (1,000 genes)...")
    
    real_path = 'borda/results/elite_borda_training_table.parquet'
    synth_path = 'borda/results/synthetic_samples_elite_borda_120000.parquet'
    
    if not os.path.exists(real_path) or not os.path.exists(synth_path):
        print("❌ Error: Missing datasets in borda/results/")
        return
        
    # Load data
    print("📖 Loading datasets...")
    df_real = pd.read_parquet(real_path)
    df_synth = pd.read_parquet(synth_path)
    
    # target column
    target_col = 'Category'
    
    # features (all except GSE_ID, Category)
    features = [col for col in df_real.columns if col not in ['GSE_ID', target_col]]
    print(f"   Using {len(features)} features.")
    
    # Check column match
    for col in features:
        if col not in df_synth.columns:
            print(f"❌ Error: Feature {col} not in synthetic dataset.")
            return
            
    X_real = df_real[features]
    y_real = df_real[target_col].astype(int)
    
    X_synth = df_synth[features]
    y_synth = df_synth[target_col].astype(int)
    
    # Hold-out Test Set (20% of Real)
    X_train_real, X_test_real, y_train_real, y_test_real = train_test_split(
        X_real, y_real, test_size=0.2, random_state=42, stratify=y_real
    )
    
    n_real_train = len(X_train_real)
    print(f"   Real Train samples: {n_real_train}")
    print(f"   Real Test samples: {len(X_test_real)}")
    
    # Let's run a fast evaluation
    # We will run ratios: 0, 0.5, 1, 2, 3, 5, 10, 15
    ratios = [0, 0.5, 1, 2, 3, 5, 10, 15]
    results = []
    
    # Fast XGBoost config to save time
    clf = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        tree_method='hist' # extremely fast histogram-based algorithm
    )
    
    for ratio in ratios:
        n_synth_needed = int(n_real_train * ratio)
        print(f"   💉 Ratio 1:{ratio} (Reales: {n_real_train}, Sintéticos: {n_synth_needed})")
        
        start_time = time.time()
        if ratio == 0:
            X_train_mixed = X_train_real
            y_train_mixed = y_train_real
        else:
            # Sample synthetic data
            X_synth_sample = X_synth.sample(n_synth_needed, random_state=42)
            y_synth_sample = y_synth.loc[X_synth_sample.index]
            X_train_mixed = pd.concat([X_train_real, X_synth_sample])
            y_train_mixed = pd.concat([y_train_real, y_synth_sample])
            
        print(f"      Training on {len(X_train_mixed)} samples...")
        clf.fit(X_train_mixed, y_train_mixed)
        
        auc = roc_auc_score(y_test_real, clf.predict_proba(X_test_real)[:, 1])
        elapsed = time.time() - start_time
        print(f"      ROC-AUC Score: {auc:.4f} (Took {elapsed:.1f}s)")
        
        results.append({
            'Ratio': ratio,
            'Real_Samples': n_real_train,
            'Synthetic_Samples': n_synth_needed,
            'AUC_Test_Real': auc
        })
        
    # Save results
    df_curve = pd.DataFrame(results)
    os.makedirs('borda/results/metrics', exist_ok=True)
    os.makedirs('results/metrics', exist_ok=True)
    df_curve.to_csv('borda/results/metrics/augmentation_curve_elite_borda.csv', index=False)
    print("✅ Results saved to borda/results/metrics/augmentation_curve_elite_borda.csv")
    
    # ----------------------------------------------------
    # Plot 1: curva_augmentacion.png (Standard style)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    # Ratios used for standard plot: 0, 0.5, 1, 2, 3, 5 (up to 10s label)
    # Mapping to original labels:
    # 0 -> 1r
    # 0.5 -> 1r+1s
    # 1 -> 1r+2s
    # 2 -> 1r+4s
    # 3 -> 1r+6s
    # 5 -> 1r+10s
    plot_ratios = [0, 0.5, 1, 2, 3, 5]
    df_plot1 = df_curve[df_curve['Ratio'].isin(plot_ratios)].copy()
    
    labels_plot1 = ['1r', '1r+1s', '1r+2s', '1r+4s', '1r+6s', '1r+10s']
    x_indices = range(len(plot_ratios))
    
    plt.plot(x_indices, df_plot1['AUC_Test_Real'], marker='o', linestyle='-', color='dodgerblue', linewidth=2, markersize=8)
    
    # Baseline line
    baseline_auc = df_plot1.loc[df_plot1['Ratio'] == 0, 'AUC_Test_Real'].values[0]
    plt.axhline(y=baseline_auc, color='red', linestyle='--', label=f'Línea Base (1r) = {baseline_auc:.4f}')
    
    plt.xticks(x_indices, labels_plot1)
    plt.title('Curva de Aumentación TSTR bajo Marco 1r+ns', fontsize=14, fontweight='bold')
    plt.ylabel('ROC-AUC en Set de Prueba Real (Hold-out 20%)')
    plt.xlabel('Nivel de Aumentación (Cohortes Sintéticas inyectadas)')
    plt.legend()
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig('results/metrics/curva_augmentacion.png', dpi=300)
    plt.savefig('borda/results/metrics/curva_augmentacion.png', dpi=300)
    plt.close()
    print("✅ Plot 1 (curva_augmentacion.png) generated.")
    
    # ----------------------------------------------------
    # Plot 2: comparativa_lite_vs_optimal.png (Comparison style)
    # ----------------------------------------------------
    plt.figure(figsize=(11, 6))
    
    # Lite AUCs: [0.7015, 0.7002, 0.6970, 0.6954, 0.6925, 0.6895]
    lite_aucs = [0.7015, 0.7002, 0.6970, 0.6954, 0.6925, 0.6895]
    elite_aucs = df_plot1['AUC_Test_Real'].tolist()
    
    # X values: number of synthetic samples
    # For Lite, synthetic samples were based on base_size = 11219:
    # 0, 11219, 22438, 44876, 67314, 112190
    # For Elite Borda, they are:
    # 0, 3723, 7447, 14894, 22341, 37235
    # To plot them on the same axis, we can plot against Ratio labels or just indices
    x_indices2 = range(len(plot_ratios))
    labels_plot2 = ['0', '3.7k / 11k', '7.4k / 22k', '15k / 45k', '22k / 67k', '37k / 112k']
    
    plt.plot(x_indices2, elite_aucs, marker='o', color='darkorange', linewidth=3, label='Alta Dimensionalidad Borda (1,000 Genes) - Real')
    plt.plot(x_indices2, lite_aucs, marker='s', color='dodgerblue', linewidth=2, linestyle='--', label='Modelo Lite (Top 200 Genes) - Real')
    
    plt.axhline(y=0.7015, color='blue', linestyle=':', linewidth=1.5, label='Baseline Teórico Lite (Sólo Datos Reales) = 0.7015')
    plt.axhline(y=baseline_auc, color='red', linestyle=':', linewidth=1.5, label=f'Baseline Teórico Alta Dimensionalidad (Sólo Datos Reales) = {baseline_auc:.4f}')
    
    plt.xticks(x_indices2, labels_plot2)
    plt.title('Evaluación Empírica de Aumentación: Modelo Lite vs Alta Dimensionalidad Borda', fontsize=15, fontweight='bold')
    plt.ylabel('Desempeño Diagnóstico (ROC-AUC) en Test Real')
    plt.xlabel('Número de Pacientes Sintéticos Inyectados (Alta Dimensionalidad / Lite)')
    plt.legend(fontsize=10, loc='lower left')
    plt.grid(axis='both', linestyle='--', alpha=0.5)
    
    # Annotations
    plt.annotate('Retención de Fidelidad Alta Dimensionalidad\n(Desempeño superior)', xy=(5, elite_aucs[5]), xytext=(3.5, elite_aucs[5] - 0.05),
                 arrowprops=dict(facecolor='darkorange', shrink=0.05))
                 
    plt.annotate('Retención de Fidelidad Lite\n(Desempeño base)', xy=(5, lite_aucs[5]), xytext=(3.5, lite_aucs[5] - 0.05),
                 arrowprops=dict(facecolor='dodgerblue', shrink=0.05))
                 
    plt.tight_layout()
    plt.savefig('results/metrics/comparativa_lite_vs_optimal.png', dpi=300)
    plt.savefig('borda/results/metrics/comparativa_lite_vs_optimal.png', dpi=300)
    plt.close()
    print("✅ Plot 2 (comparativa_lite_vs_optimal.png) generated.")

if __name__ == "__main__":
    main()

