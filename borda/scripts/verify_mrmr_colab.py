import pandas as pd
import numpy as np
import os
import torch
import warnings
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from tabpfn import TabPFNClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Silenciar advertencias
warnings.filterwarnings('ignore')

def run_mrmr_colab_verification():
    # Detectar dispositivo
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️ Dispositivo detectado para TabPFN: {device.upper()}")
    
    # 1. Definir rutas autodetectando prefijo 'datasets/' en Colab
    real_path = 'results/elite_borda_training_table.parquet'
    synth_path = 'results/synthetic_samples_elite_borda_5000.parquet'
    
    if os.path.exists("datasets"):
        real_path = os.path.join("datasets", real_path)
        synth_path = os.path.join("datasets", synth_path)
        
    print(f"📁 Cargando Real desde: {real_path}")
    print(f"📁 Cargando Sintético desde: {synth_path}")
    
    # Clasificadores idénticos al benchmark de la CPU
    classifiers = {
        'XGBoost': XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1),
        'CatBoost': CatBoostClassifier(iterations=100, depth=6, verbose=False, random_state=42),
        'TabPFN': TabPFNClassifier(n_estimators=8, device=device, ignore_pretraining_limits=True),
        'SVM_RBF_SOTA': SVC(kernel='rbf', probability=True, random_state=42),
        'RandomForest_SOTA': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    }
    
    # 2. Cargar la librería de mRMR
    try:
        from mrmr import mrmr_classif
    except ImportError:
        print("❌ ERROR: La librería 'mrmr-selection' no está instalada. Ejecuta '!pip install mrmr-selection' primero.")
        return

    # 3. Función interna para evaluar un dataset
    def evaluate_dataset(path, name):
        if not os.path.exists(path):
            print(f"❌ Archivo no encontrado: {path}")
            return
            
        df = pd.read_parquet(path)
        target_col = 'Category' if 'Category' in df.columns else 'target'
        df = df.dropna(subset=[target_col])
        
        # Parseo de strings anidados si los hay
        metadata_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
        for col in df.columns:
            if df[col].dtype == object and col not in metadata_cols:
                df[col] = df[col].astype(str).str.replace(r'[\[\]]', '', regex=True).astype(float)
                
        # Limitar a 5000 muestras para CPU
        if len(df) > 5000:
            df = df.sample(5000, random_state=42)
            
        X = df.drop(columns=[col for col in ['GSE_ID', target_col, 'target'] if col in df.columns])
        y = df[target_col].astype(int)
        
        print(f"\n🚀 Iniciando mRMR en {name} (Seleccionando Top 100 Genes)...")
        selected_features = mrmr_classif(X=X, y=y, K=100)
        X_sel = df[selected_features]
        
        print(f"✅ Genes seleccionados por mRMR. Iniciando evaluación predictiva (3-Fold CV)...")
        for clf_name, clf in classifiers.items():
            scores = cross_val_score(clf, X_sel, y, cv=3, scoring='roc_auc')
            print(f"   📊 [mRMR + {clf_name}] ROC-AUC: {np.mean(scores):.6f} ± {np.std(scores):.6f}")

    evaluate_dataset(real_path, "Real (Control)")
    evaluate_dataset(synth_path, "Sintético (TSTS)")

if __name__ == '__main__':
    run_mrmr_colab_verification()
