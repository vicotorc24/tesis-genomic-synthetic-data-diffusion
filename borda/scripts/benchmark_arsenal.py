import pandas as pd
import numpy as np
import os
import joblib
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, roc_auc_score, classification_report
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from tabpfn import TabPFNClassifier

# Import our custom selector
from feature_selection import apply_feature_selection

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

class ArsenalBenchmarker:
    def __init__(self, data_path, target_col='Category', results_dir='results/metrics'):
        self.data_path = data_path
        self.target_col = target_col
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        print(f"Loading data from {data_path}...")
        self.df = pd.read_parquet(data_path)
        
    def run_benchmark(self, df_input=None, arm_name="Brazo_X", k_features=100, fs_method='mrmr', test_df=None):
        """
        Runs the benchmark on the provided dataframe or the internal one.
        If test_df is provided, it uses it for evaluation (TSTR mode).
        """
        df = df_input if df_input is not None else self.df
        
        print(f"\n{'='*60}")
        print(f"🚀 Iniciando Benchmark: {arm_name} (FS: {fs_method}, Top {k_features})")
        print(f"{'='*60}")
        
        # 1. Feature Selection (Always performed on the training data)
        selected_genes = apply_feature_selection(df, target_col=self.target_col, method=fs_method, k=k_features)
        
        # 2. Prepare Data
        X_train = df[selected_genes]
        y_train = df[self.target_col].astype(int)
        
        if test_df is not None:
            print("Mode: TSTR (Train Synthetic, Test Real)")
            X_test = test_df[selected_genes]
            y_test = test_df[self.target_col].astype(int)
        else:
            print("Mode: Internal Split (Real Baseline)")
            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42, stratify=y_train)
        
        classifiers = {
            "SVM": LinearSVC(dual=False, random_state=42),
            "RandomForest": RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42),
            "XGBoost": XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=42),
            "CatBoost": CatBoostClassifier(iterations=100, verbose=False, random_state=42),
        }
        
        results = []
        for name, clf in classifiers.items():
            print(f"Evaluating {name}...")
            start = time.time()
            try:
                clf.fit(X_train, y_train)
                y_pred = clf.predict(X_test)
                f1 = f1_score(y_test, y_pred, average='macro')
                acc = accuracy_score(y_test, y_pred)
                elapsed = time.time() - start
                
                results.append({
                    "Arm": arm_name,
                    "Classifier": name,
                    "FS_Method": fs_method,
                    "K_Genes": k_features,
                    "F1_Score": f1,
                    "Accuracy": acc,
                    "Time_Sec": elapsed
                })
                print(f"   Done: F1={f1:.4f}")
            except Exception as e:
                print(f"   ❌ Error with {name}: {str(e)}")
        
        results_df = pd.DataFrame(results)
        output_file = f"{self.results_dir}/results_{arm_name}_{fs_method}_{k_features}.csv"
        results_df.to_csv(output_file, index=False)
        return results_df

if __name__ == "__main__":
    core_train_path = 'results/core_train.parquet'
    core_test_path = 'results/core_test.parquet'
    synth_path = 'results/synthetic_samples_5000.parquet'
    
    if os.path.exists(core_test_path):
        # 1. Real Baseline (Control: Train on Core_Train, Test on Core_Test)
        if os.path.exists(core_train_path):
            print("\n--- BRAZO A: CONTROL (REAL TRAIN -> REAL TEST) ---")
            train_df = pd.read_parquet(core_train_path)
            test_df = pd.read_parquet(core_test_path)
            
            # Using ArsenalBenchmarker on the Train set, but providing the Test set
            benchmarker = ArsenalBenchmarker(core_train_path)
            benchmarker.run_benchmark(df_input=train_df, 
                                    arm_name="Brazo_A_Control", 
                                    k_features=100, 
                                    fs_method='f_test', 
                                    test_df=test_df)
        
        # 2. TSTR (Train Synthetic, Test Real_Test)
        if os.path.exists(synth_path):
            print("\n--- BRAZO B: TSTR (SYNTHETIC -> REAL TEST) ---")
            synth_df = pd.read_parquet(synth_path)
            test_df = pd.read_parquet(core_test_path)
            
            benchmarker_synth = ArsenalBenchmarker(synth_path)
            benchmarker_synth.run_benchmark(df_input=synth_df, 
                                          arm_name="Brazo_B_TSTR", 
                                          k_features=100, 
                                          fs_method='f_test', 
                                          test_df=test_df)
        else:
            print(f"⏳ Synthetic data not found at {synth_path}. Run generate_synthetic_patients.py first.")
    else:
        print(f"❌ Core Test set not found at {core_test_path}.")
