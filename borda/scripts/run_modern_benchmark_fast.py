import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from feature_selection import apply_feature_selection
import os
import time
import warnings

# Silenciamos warnings de versiones para una salida limpia
warnings.filterwarnings('ignore')

# Algoritmos SOTA 2026
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from tabpfn import TabPFNClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Configuración del Arsenal Moderno (Versión Táctica Rápida sin TabPFN)
MODERN_CLASSIFIERS = {
    'XGBoost': XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1),
    'CatBoost': CatBoostClassifier(iterations=100, depth=6, verbose=False, random_state=42),
    'SVM_RBF_SOTA': SVC(kernel='rbf', probability=True, random_state=42),
    'RandomForest_SOTA': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
}

# Selectores SOTA (mRMR y SHAP son los pilares 2026)
MODERN_SELECTORS = ['shap', 'mrmr', 'lasso', 'f_test', 'rfe']

def run_modern_experiment(df, context_name, k=100):
    results = []
    # Detección del target
    target_col = 'Category' if 'Category' in df.columns else 'target'
    
    print(f"\n🚀 Iniciando Arena SOTA 2026: {context_name}")
    print(f"   (Frontera Tecnológica: SHAP Selector + TabPFN Transformer)")
    
    df = df.dropna(subset=[target_col])
    
    # Dejamos que TabPFN y XGBoost usen muestras razonables.
    if len(df) > 1000:
        print(f"   ⚖️ Optimización: Muestreando 1,000 pacientes (Límite máximo recomendado para TabPFN en CPU)")
        df = df.sample(1000, random_state=42)
    
    for fs_name in MODERN_SELECTORS:
        try:
            print(f"🧬 Generando Selección con: {fs_name.upper()}")
            start_fs = time.time()
            selected_genes = apply_feature_selection(df, target_col=target_col, method=fs_name, k=k)
            fs_time = time.time() - start_fs
            
            X = df[selected_genes]
            y = df[target_col].astype(int)
            
            for clf_name, clf in MODERN_CLASSIFIERS.items():
                print(f"   ⏱️ Eval: {fs_name} + {clf_name}...")
                # 5-fold CV para máximo rigor académico
                scores = cross_val_score(clf, X, y, cv=5, scoring='roc_auc')
                
                results.append({
                    'Epoch': 2026,
                    'Context': context_name,
                    'FS': fs_name,
                    'Classifier': clf_name,
                    'AUC_Mean': np.mean(scores),
                    'AUC_Std': np.std(scores),
                    'FS_Time_Seconds': fs_time
                })
        except Exception as e:
            print(f"   ❌ Error en par SOTA {fs_name}: {e}")
            
    return pd.DataFrame(results)

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def run_mono_platform_baselines(df_real, k=100):
    results = []
    target_col = 'Category' if 'Category' in df_real.columns else 'target'
    tech_col = 'Technology_Label'
    
    if tech_col not in df_real.columns:
        print(f"⚠️ Columna {tech_col} no encontrada. Saltando baseline mono-plataforma.")
        return pd.DataFrame()
        
    print(f"\n🔬 Iniciando Líneas Base Mono-Plataforma...")
    for platform in df_real[tech_col].unique():
        df_plat = df_real[df_real[tech_col] == platform]
        print(f"   📊 Evaluando plataforma: {platform} (N={len(df_plat)})")
        
        # Limit size for speed in this test
        if len(df_plat) > 5000:
            df_plat = df_plat.sample(5000, random_state=42)
            
        selected_genes = apply_feature_selection(df_plat, target_col=target_col, method='mrmr', k=k)
        X = df_plat[selected_genes]
        y = df_plat[target_col].astype(int)
        
        clf = XGBClassifier(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1)
        scores = cross_val_score(clf, X, y, cv=5, scoring='roc_auc')
        
        results.append({
            'Experiment': 'Mono-Platform Baseline',
            'Platform': platform,
            'Classifier': 'XGBoost',
            'AUC_Mean': np.mean(scores),
            'AUC_Std': np.std(scores)
        })
    return pd.DataFrame(results)

def run_augmentation_curve(df_real, df_synth, k=100):
    results = []
    print(f"\n📈 Iniciando Curva de Amplificación Sintética (Dosis-Respuesta)...")
    target_col = 'Category' if 'Category' in df_real.columns else 'target'
    
    selected_genes = apply_feature_selection(df_real, target_col=target_col, method='mrmr', k=k)
    X_real = df_real[selected_genes]
    y_real = df_real[target_col].astype(int)
    
    missing = [g for g in selected_genes if g not in df_synth.columns]
    if missing:
         print(f"⚠️ Faltan genes en datos sintéticos. Saltando curva.")
         return pd.DataFrame()
         
    X_synth = df_synth[selected_genes]
    y_synth = df_synth[target_col].astype(int)
    
    # Hold-out Test Set (20% of Real)
    X_train_real, X_test_real, y_train_real, y_test_real = train_test_split(X_real, y_real, test_size=0.2, random_state=42, stratify=y_real)
    
    n_real_train = len(X_train_real)
    ratios = [0, 0.5, 1, 2, 3, 5] # 0 = TRTR Baseline
    
    clf = XGBClassifier(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1)
    
    for ratio in ratios:
        n_synth_needed = int(n_real_train * ratio)
        print(f"   💉 Ratio 1:{ratio} (Reales: {n_real_train}, Sintéticos: {n_synth_needed})")
        
        if n_synth_needed > len(X_synth) and ratio > 0:
            print(f"      ⚠️ No hay suficientes datos sintéticos. Usando todos los disponibles ({len(X_synth)}).")
            n_synth_needed = len(X_synth)
            
        if ratio == 0:
            X_train_mixed = X_train_real
            y_train_mixed = y_train_real
        else:
            X_synth_sample = X_synth.sample(n_synth_needed, random_state=42)
            y_synth_sample = y_synth.loc[X_synth_sample.index]
            X_train_mixed = pd.concat([X_train_real, X_synth_sample])
            y_train_mixed = pd.concat([y_train_real, y_synth_sample])
            
        clf.fit(X_train_mixed, y_train_mixed)
        auc = roc_auc_score(y_test_real, clf.predict_proba(X_test_real)[:, 1])
        
        results.append({
            'Ratio': ratio,
            'Real_Samples': n_real_train,
            'Synthetic_Samples': n_synth_needed,
            'AUC_Test_Real': auc
        })
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    os.makedirs('results/metrics', exist_ok=True)
    all_modern_results = []
    
    # Definir el camino óptimo (priorizar el Brazo Óptimo de 1000 genes si existe)
    path_real = 'results/optimal_training_table.parquet'
    path_synth = 'results/synthetic_samples_optimal_120000.parquet'
    
    if not os.path.exists(path_real): # Fallback al Brazo Lite si no hay Óptimo aún
        path_real = 'results/lite_training_table.parquet'
        path_synth = 'results/synthetic_samples_lite_5000.parquet'
        
    df_real = None
    df_synth = None

    # 1. Escenario Datalake Real
    if os.path.exists(path_real):
        df_real = pd.read_parquet(path_real)
        all_modern_results.append(run_modern_experiment(df_real, 'Real_Baseline_2026'))
        
        # 1.1 Ejecutar Línea Base Mono-Plataforma
        df_mono = run_mono_platform_baselines(df_real)
        if not df_mono.empty:
            df_mono.to_csv('results/metrics/MONO_PLATFORM_BASELINES.csv', index=False)
            print("✅ Líneas Base Mono-Plataforma guardadas.")

    # 2. Escenario Sintético TSTR
    if os.path.exists(path_synth):
        df_synth = pd.read_parquet(path_synth)
        all_modern_results.append(run_modern_experiment(df_synth, 'Sintetico_TSTR_2026'))

    # 3. Guardar Benchmark SOTA
    if all_modern_results:
        final_df = pd.concat(all_modern_results)
        output_path = 'results/metrics/MODERN_BENCHMARK_RESULTS_FAST.csv'
        final_df.to_csv(output_path, index=False)
        print(f"\n✅ Matriz de Desempeño SOTA 2026 generada en {output_path}")
    else:
        print("❌ No se pudieron ejecutar los experimentos modernos principales.")
        
    # 4. Curva de Dosis-Respuesta (Amplificación)
    if df_real is not None and df_synth is not None:
        df_curve = run_augmentation_curve(df_real, df_synth)
        if not df_curve.empty:
            df_curve.to_csv('results/metrics/augmentation_curve_results.csv', index=False)
            print("✅ Curva de Saturación Sintética guardada.")
