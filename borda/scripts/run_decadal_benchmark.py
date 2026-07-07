import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from feature_selection import apply_feature_selection
import os
import time

# Algoritmos de Clasificación del Arsenal 2021
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

CLASSIFIERS = {
    'DecisionTree': DecisionTreeClassifier(random_state=42),
    'KNeighbors': KNeighborsClassifier(),
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'NaiveBayes': GaussianNB(),
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
}

# Selectores Oficiales de la Tabla 3 de la Tesis 2021
SELECTORS = ['f_test', 'chi2', 'l1', 'rfe']

def run_experiment(df, context_name, k=100):
    results = []
    
    # Detección dinámica del target (Category en 2026, target en 2021)
    target_col = 'Category' if 'Category' in df.columns else 'target'
    if target_col not in df.columns:
        print(f"   ❌ No se encontró columna objetivo en {context_name}")
        return pd.DataFrame()

    print(f"\n🏟️  Iniciando Arena en contexto: {context_name} (Target: {target_col})")
    
    # Asegurar que el target sea binario y no tenga NaNs
    df = df.dropna(subset=[target_col])
    
    for fs_name in SELECTORS:
        try:
            print(f"🚀 Ejecutando Selector: {fs_name}")
            start_fs = time.time()
            # Pasamos el target detectado al motor de selección
            selected_genes = apply_feature_selection(df, target_col=target_col, method=fs_name, k=k)
            fs_time = time.time() - start_fs
            
            X = df[selected_genes]
            y = df[target_col].astype(int)
            
            for clf_name, clf in CLASSIFIERS.items():
                print(f"   ⏱️ {fs_name} + {clf_name}...")
                # Usamos 5-fold CV para estabilidad académica
                scores = cross_val_score(clf, X, y, cv=5, scoring='roc_auc', n_jobs=-1)
                
                results.append({
                    'Context': context_name,
                    'FS': fs_name,
                    'Classifier': clf_name,
                    'AUC_Mean': np.mean(scores),
                    'AUC_Std': np.std(scores),
                    'FS_Time': fs_time
                })
        except Exception as e:
            print(f"   ❌ Error en par {fs_name}: {e}")
            
    return pd.DataFrame(results)

if __name__ == "__main__":
    # Importamos el cargador de la Tesis 2021
    from scripts.extract_decadal_metafeatures import load_2021_txt
    
    os.makedirs('results/metrics', exist_ok=True)
    all_benchmarks = []
    
    # 1. Escenario A: Real 2021 (Baseline de la Tesis)
    path_2021 = 'REPORTS/documentos_tesis/microarray-data/dataset_prostate_singh.txt'
    if os.path.exists(path_2021):
        print("📉 Evaluando Punto de Partida: Prostate Singh 2021")
        df_2021 = load_2021_txt(path_2021)
        all_benchmarks.append(run_experiment(df_2021, 'Real_2021_Prostate'))

    # 2. Escenario B: Real 2026 (Datalake Armonizado)
    path_2026 = 'results/core_train.parquet'
    if os.path.exists(path_2026):
        print("\n🚀 Evaluando Datalake Armonizado 2026 (Real)")
        df_real = pd.read_parquet(path_2026)
        # Reducimos a una muestra para velocidad si es necesario, pero intentamos total
        # df_real = df_real.sample(min(2000, len(df_real))) 
        all_benchmarks.append(run_experiment(df_real, 'Real_2026'))
        
    # 3. Escenario C: Sintético 2026 (CTGAN)
    path_synth = 'results/synthetic_samples_5000.parquet'
    if os.path.exists(path_synth):
        print("\n✨ Evaluando IA Generativa 2026 (Sintético)")
        df_synth = pd.read_parquet(path_synth)
        all_benchmarks.append(run_experiment(df_synth, 'Synth_2026_CTGAN'))

    if all_benchmarks:
        master_df = pd.concat(all_benchmarks)
        master_df.to_csv('results/metrics/DECADAL_BENCHMARK_RESULTS.csv', index=False)
        print(f"\n✅ Matriz de Desempeño Decadal generada en results/metrics/DECADAL_BENCHMARK_RESULTS.csv")
    else:
        print("❌ No se pudieron ejecutar los experimentos.")
