import pandas as pd
import numpy as np
import os
import sys
import time
sys.path.append(os.getcwd()) # Asegurar que encuentre feature_selection.py
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from feature_selection import apply_feature_selection

# Configuración de 24 pares (FS x Classifier)
FS_METHODS = ['f_test', 'l1', 'chi2', 'rfe']
CLASSIFIERS = {
    'NaiveBayes': GaussianNB(),
    'KNeighbors': KNeighborsClassifier(n_neighbors=3),
    'LogicticRegresion': LogisticRegression(max_iter=1000, random_state=42),
    'SVN': SVC(kernel='linear', probability=True, random_state=42),
    'DecitionTree': DecisionTreeClassifier(random_state=42),
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42)
}

def load_2021_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    labels = [int(x) for x in lines[1].strip().split()]
    data_matrix = []
    for line in lines[2:]:
        vals = [float(x) for x in line.strip().split()]
        data_matrix.append(vals)
    df = pd.DataFrame(data_matrix).T
    df['target'] = labels
    return df

def run_reproduction():
    base_path = 'REPORTS/documentos_tesis/microarray-data/'
    results_path = 'results/REPRODUCED_MATRIX_2021.csv'
    checkpoint_path = 'results/checkpoints_reproduction/'
    os.makedirs(checkpoint_path, exist_ok=True)
    
    files = sorted([f for f in os.listdir(base_path) if f.endswith('.txt')])
    
    # Cargar progreso si existe
    if os.path.exists(results_path):
        final_df = pd.read_csv(results_path)
        processed_datasets = final_df['dataset'].tolist()
    else:
        final_df = pd.DataFrame()
        processed_datasets = []

    print(f"🚀 Iniciando Reproducción de Matriz 24x60 ({len(files)} datasets)...")
    
    for filename in files:
        dataset_name = filename.replace('.txt', '')
        if dataset_name in processed_datasets:
            print(f"   ⏩ Saltando {dataset_name} (ya procesado).")
            continue
            
        print(f"   📂 Procesando Dataset: {dataset_name}...")
        try:
            df = load_2021_txt(os.path.join(base_path, filename))
            dataset_results = {'dataset': dataset_name}
            
            for fs in FS_METHODS:
                # 1. Selección de Atributos (Top 100)
                selected_genes = apply_feature_selection(df, target_col='target', method=fs, k=100)
                X_subset = df[selected_genes]
                y = df['target']
                
                for clf_name, clf in CLASSIFIERS.items():
                    col_name = f"{fs.replace('l1', 'l1')}-{clf_name}" # Mapeo de nombres exacto
                    
                    # 2. Pipeline con Escalado + Clasificador
                    pipeline = Pipeline([
                        ('scaler', StandardScaler()),
                        ('clf', clf)
                    ])
                    
                    # 3. Validación Cruzada CV=5
                    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
                    
                    # Determinar si es binario o multiclase
                    n_classes = len(np.unique(y))
                    scoring = 'roc_auc' if n_classes == 2 else 'roc_auc_ovr'
                    
                    try:
                        scores = cross_val_score(pipeline, X_subset, y, cv=cv, scoring=scoring)
                        dataset_results[col_name] = np.mean(scores)
                    except Exception as e:
                        print(f"      ⚠️ Error en {col_name}: {e}")
                        dataset_results[col_name] = 0.5 # Valor por defecto (azar) en caso de excepción
                    
                    print(f"      ✅ {col_name}: {dataset_results[col_name]:.4f}")
            
            # Guardar resultado del dataset
            row_df = pd.DataFrame([dataset_results])
            final_df = pd.concat([final_df, row_df], ignore_index=True)
            final_df.to_csv(results_path, index=False)
            
            # Backup Checkpoint
            row_df.to_csv(f"{checkpoint_path}/{dataset_name}.csv", index=False)
            
        except Exception as e:
            print(f"   ⚠️ Error en {dataset_name}: {e}")

    print(f"\n✅ Reproducción finalizada. Matriz guardada en {results_path}")

if __name__ == "__main__":
    start_time = time.time()
    run_reproduction()
    print(f"--- Tiempo total: {(time.time() - start_time)/60:.2f} minutos ---")
