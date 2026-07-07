import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
import sys
import time
import warnings
import torch
import argparse

from sklearn.feature_selection import SelectKBest, f_classif, chi2, RFE, SelectFromModel
from sklearn.linear_model import Lasso

def apply_feature_selection(df, target_col='Category', method='f_test', k=100):
    """
    Módulo de Selección de Características Híbrido (2021 vs 2026)
    - Legacy: f_test, chi2, rfe, l1
    - SOTA: mrmr, importance
    """
    print(f"🔍 Aplicando Selección de Atributos: {method} (Top {k} genes)...")
    
    # Pre-processing: Split X, y
    X = df.drop(columns=[col for col in ['GSE_ID', target_col, 'target'] if col in df.columns])
    y = df[target_col if target_col in df.columns else 'target'].astype(int)
    
    selected_features = []
    
    if method == 'f_test':
        selector = SelectKBest(f_classif, k=k)
        selector.fit(X, y)
        selected_features = X.columns[selector.get_support()].tolist()
        
    elif method == 'chi2':
        X_pos = X.clip(lower=0) 
        selector = SelectKBest(chi2, k=k)
        selector.fit(X_pos, y)
        selected_features = X.columns[selector.get_support()].tolist()
        
    elif method == 'rfe':
        print("   (RFE optimizado con ensambles de árboles rápidos...)")
        estimator = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42, n_jobs=-1)
        selector = RFE(estimator=estimator, n_features_to_select=k, step=0.1)
        selector.fit(X, y)
        selected_features = X.columns[selector.get_support()].tolist()
        
    elif method == 'l1' or method == 'lasso':
        lasso = SelectFromModel(Lasso(alpha=0.01), max_features=k)
        lasso.fit(X, y)
        selected_features = X.columns[lasso.get_support()].tolist()
        
    elif method == 'mrmr':
        try:
            from mrmr import mrmr_classif
            selected_features = mrmr_classif(X=X, y=y, K=k)
        except ImportError:
            print("⚠️ Carga de mrmr falló. Fallback a F-Test.")
            selector = SelectKBest(f_classif, k=k)
            selector.fit(X, y)
            selected_features = X.columns[selector.get_support()].tolist()

    elif method == 'shap':
        import xgboost as xgb
        import shap
        print("   (SHAP: Entrenando modelo de referencia para explicar importancia...)")
        X_clean = np.array(X, dtype=np.float32)
        
        model = xgb.XGBClassifier(n_estimators=100, max_depth=3, random_state=42, n_jobs=-1)
        model.fit(X_clean, y)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_clean)
        
        import_scores = np.abs(shap_values).mean(axis=0)
        shap_series = pd.Series(import_scores, index=X.columns)
        selected_features = shap_series.sort_values(ascending=False).head(k).index.tolist()
            
    elif method in ['importance', 'random_forest']:
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(X, y)
        importances = pd.Series(rf.feature_importances_, index=X.columns)
        selected_features = importances.sort_values(ascending=False).head(k).index.tolist()

    elif method == 'ensemble':
        print("   (Ensemble: Aplicando Votación Borda entre SHAP, Random Forest y F-Test...)")
        X_clean = np.array(X, dtype=np.float32)
        
        selector = SelectKBest(f_classif, k='all')
        selector.fit(X_clean, y)
        f_scores = np.nan_to_num(selector.scores_, nan=0.0)
        f_ranks = pd.Series(f_scores, index=X.columns).rank(ascending=False, method='min')
        
        rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
        rf.fit(X_clean, y)
        rf_ranks = pd.Series(rf.feature_importances_, index=X.columns).rank(ascending=False, method='min')
        
        import xgboost as xgb
        import shap
        model = xgb.XGBClassifier(n_estimators=50, max_depth=3, random_state=42, n_jobs=-1)
        model.fit(X_clean, y)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_clean)
        import_scores = np.abs(shap_values).mean(axis=0)
        shap_ranks = pd.Series(import_scores, index=X.columns).rank(ascending=False, method='min')
        
        borda_df = pd.DataFrame({
            'F_Test': f_ranks,
            'RF': rf_ranks,
            'SHAP': shap_ranks
        })
        borda_df['Mean_Rank'] = borda_df.mean(axis=1)
        
        selected_features = borda_df.sort_values(by='Mean_Rank', ascending=True).head(k).index.tolist()
        print(f"   (Ensemble Borda Count: Mejores genes extraídos con éxito)")

    print(f"✅ Selección completada: {len(selected_features)} genes identificados.")
    return selected_features

# Silenciamos warnings de versiones para una salida limpia
warnings.filterwarnings('ignore')

# Algoritmos SOTA 2026
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from tabpfn import TabPFNClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def main():
    parser = argparse.ArgumentParser(description="Arena SOTA Élite CPU Benchmark (Optimized)")
    parser.add_argument('--dry-run', action='store_true', help="Ejecutar prueba rápida de 1 combinación en segundos")
    parser.add_argument('--real_path', type=str, default='results/elite_borda_training_table.parquet')
    parser.add_argument('--synth_path', type=str, default='results/synthetic_samples_elite_borda_5000.parquet')
    args = parser.parse_args()

    # Detección de dispositivo para TabPFN
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️  Dispositivo detectado para TabPFN: {device.upper()}")

    classifiers = {
        'XGBoost': XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1),
        'CatBoost': CatBoostClassifier(iterations=100, depth=6, verbose=False, random_state=42),
        'TabPFN': TabPFNClassifier(n_estimators=8, device=device, ignore_pretraining_limits=True),
        'SVM_RBF_SOTA': SVC(kernel='rbf', probability=True, random_state=42),
        'RandomForest_SOTA': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    }

    selectors = ['shap', 'mrmr', 'lasso', 'f_test', 'rfe']
    cv_folds = 3
    sample_size = 5000

    if args.dry_run:
        print("🧪 MODO DRY-RUN ACTIVO: Usando parámetros ultra-ligeros para verificación de código.")
        classifiers = {'XGBoost': XGBClassifier(n_estimators=10, max_depth=3, random_state=42, n_jobs=-1)}
        selectors = ['f_test']
        cv_folds = 2
        sample_size = 500

    def run_modern_experiment(df, context_name, k=100):
        results = []
        target_col = 'Category' if 'Category' in df.columns else 'target'
        
        print(f"\n🚀 Iniciando Arena SOTA ÉLITE (Borda): {context_name}")
        print(f"   (Frontera Tecnológica: SHAP Selector + TabPFN Transformer)")
        
        df = df.dropna(subset=[target_col])
        
        # FIX: Parseo de strings anidados (como '[8.084E-1]') que hacían crashear a SHAP
        metadata_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
        for col in df.columns:
            if df[col].dtype == object and col not in metadata_cols:
                df[col] = df[col].astype(str).str.replace(r'[\[\]]', '', regex=True).astype(float)
        
        if len(df) > sample_size:
            print(f"   ⚖️ Optimización CPU: Muestreando {sample_size} pacientes")
            df = df.sample(sample_size, random_state=42)
        
        for fs_name in selectors:
            try:
                print(f"🧬 Generando Selección con: {fs_name.upper()}")
                start_fs = time.time()
                selected_genes = apply_feature_selection(df, target_col=target_col, method=fs_name, k=k)
                fs_time = time.time() - start_fs
                
                X = df[selected_genes]
                y = df[target_col].astype(int)
            except Exception as e:
                print(f"   ❌ Error en selector {fs_name}: {e}")
                continue
                
            for clf_name, clf in classifiers.items():
                try:
                    print(f"   ⏱️ Eval: {fs_name} + {clf_name}...")
                    scores = cross_val_score(clf, X, y, cv=cv_folds, scoring='roc_auc')
                    
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
                    print(f"   ❌ Error en par SOTA {fs_name} + {clf_name}: {e}")
                
        return pd.DataFrame(results)

    # Autodetectar prefijo 'datasets/' si estamos en la raíz del repositorio de Colab
    prefix = ""
    if os.path.exists("datasets") and not os.path.exists(args.real_path):
        if os.path.exists(os.path.join("datasets", args.real_path)):
            prefix = "datasets/"
            print(f"ℹ️ Detectada estructura de carpetas de Drive: usando prefijo '{prefix}'")

    real_path = os.path.join(prefix, args.real_path)
    synth_path = os.path.join(prefix, args.synth_path)

    metrics_dir = os.path.join(prefix, 'results/metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    all_modern_results = []
    
    # 1. Escenario Real ÉLITE Borda (1000 genes)
    if os.path.exists(real_path):
        df_real = pd.read_parquet(real_path)
        all_modern_results.append(run_modern_experiment(df_real, 'Real_Elite_Borda_2026'))
    else:
        print(f"❌ No se encontró {real_path}")

    # 2. Escenario Sintético ÉLITE Borda (Generado por Generador)
    if os.path.exists(synth_path):
        df_synth = pd.read_parquet(synth_path)
        all_modern_results.append(run_modern_experiment(df_synth, 'Sintetico_Elite_Borda_2026'))
    else:
        print(f"❌ No se encontró {synth_path}")

    if all_modern_results:
        final_df = pd.concat(all_modern_results)
        suffix = "_DRYRUN" if args.dry_run else ""
        output_path = os.path.join(metrics_dir, f'MODERN_BENCHMARK_RESULTS_ELITE_2026{suffix}.csv')
        final_df.to_csv(output_path, index=False)
        print(f"\n✅ Matriz de Desempeño SOTA ÉLITE generada en {output_path}")
        if args.dry_run:
            print("🔬 Contenido generado (Prueba rápida):")
            print(final_df[['Context', 'FS', 'Classifier', 'AUC_Mean']])
    else:
        print("❌ No se pudieron ejecutar los experimentos óptimos.")

if __name__ == "__main__":
    main()
