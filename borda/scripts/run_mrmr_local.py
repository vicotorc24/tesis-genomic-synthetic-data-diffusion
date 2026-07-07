import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from tabpfn import TabPFNClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from mrmr import mrmr_classif
import warnings
import time
warnings.filterwarnings('ignore')

classifiers = {
    'XGBoost': XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1),
    'CatBoost': CatBoostClassifier(iterations=100, depth=6, verbose=False, random_state=42),
    'TabPFN': TabPFNClassifier(n_estimators=8, device='cpu', ignore_pretraining_limits=True),
    'SVM_RBF_SOTA': SVC(kernel='rbf', probability=True, random_state=42),
    'RandomForest_SOTA': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
}

def run_mrmr_eval(df_path, context_name):
    print(f"\n🚀 Running mRMR for: {context_name}")
    df = pd.read_parquet(df_path)
    target_col = 'Category' if 'Category' in df.columns else 'target'
    df = df.dropna(subset=[target_col])
    
    # Parse object columns
    metadata_cols = ['GSE_ID', 'Category', 'target', 'Technology_Label']
    for col in df.columns:
        if df[col].dtype == object and col not in metadata_cols:
            df[col] = df[col].astype(str).str.replace(r'[\[\]]', '', regex=True).astype(float)
            
    # Sample 5000
    if len(df) > 5000:
        df = df.sample(5000, random_state=42)
        
    X = df.drop(columns=[col for col in ['GSE_ID', target_col, 'target'] if col in df.columns])
    y = df[target_col].astype(int)
    
    print("🧬 Selecting Top 100 features using mRMR...")
    start_time = time.time()
    selected_features = mrmr_classif(X=X, y=y, K=100)
    fs_time = time.time() - start_time
    print(f"✅ Selected {len(selected_features)} features in {fs_time:.2f}s")
    
    X_sel = df[selected_features]
    
    for clf_name, clf in classifiers.items():
        print(f"   ⏱️ Eval: mRMR + {clf_name}...")
        scores = cross_val_score(clf, X_sel, y, cv=3, scoring='roc_auc')
        print(f"RESULT_{context_name}_{clf_name}_AUC: {np.mean(scores):.10f} ± {np.std(scores):.10f}")

# run_mrmr_eval('results/elite_borda_training_table.parquet', 'Real')
run_mrmr_eval('results/synthetic_samples_elite_borda_5000.parquet', 'Synth')
