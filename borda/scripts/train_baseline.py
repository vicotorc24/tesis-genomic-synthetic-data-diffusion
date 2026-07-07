import os
import glob
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler

def load_and_intersect_parquets(parquet_paths):
    """
    Loads all parquet dataframes and strictly INNERS JOINS them on common gene symbols.
    This prevents memory explosions with NaNs across different microarray platforms.
    """
    print(f"Loading {len(parquet_paths)} parquet datalakes...")
    dfs = []
    
    # Pre-scan for common columns
    common_cols = set()
    for i, p in enumerate(parquet_paths):
        df = pd.read_parquet(p)
        if len(dfs) == 0:
            common_cols = set(df.columns)
            dfs.append(df)
        else:
            common_cols = common_cols.intersection(set(df.columns))
            # Just append memory-efficiently, we'll subset at the end
            dfs.append(df)
            
    print(f"Identified {len(common_cols)} strictly overlapping canonical genes across all platforms.")
    
    # Subset all frames to the strict consensus genes
    common_cols_list = sorted(list(common_cols))
    
    # Ensure Target is at the front
    if 'Target' in common_cols_list:
        common_cols_list.remove('Target')
        common_cols_list.insert(0, 'Target')
        
    for i in range(len(dfs)):
        dfs[i] = dfs[i][common_cols_list]
        
    global_matrix = pd.concat(dfs, ignore_index=True)
    return global_matrix

def augment_with_gaussian_noise(df, noise_scale=0.1):
    """
    Control Algorithm: Doubles the training dataset by adding Gaussian
    white noise proportional to the variance of each gene (baseline synthesis).
    """
    print(f"Executing Gaussian Noise Augmentation (scale={noise_scale})...")
    numeric_features = df.drop(columns=['Target'])
    std_dev = numeric_features.std(axis=0)
    
    # Generate Gaussian Matrix
    noise = np.random.normal(loc=0.0, scale=std_dev * noise_scale, size=numeric_features.shape)
    synthetic_features = numeric_features + noise
    
    # Clamp negative values to 0 (biology constraint)
    synthetic_features[synthetic_features < 0] = 0
    
    # Assemble synthetic mock patients
    synthetic_df = pd.DataFrame(synthetic_features, columns=numeric_features.columns)
    synthetic_df.insert(0, 'Target', df['Target'].values)  # Inherit labels
    
    # Combine Origin + Synthetic
    augmented_df = pd.concat([df, synthetic_df], ignore_index=True)
    print(f"Augmented Matrix Size: {df.shape[0]} -> {augmented_df.shape[0]} Mock Patients")
    return augmented_df

def run_baseline_evaluation():
    train_dir = 'results/split/train/'
    test_dir = 'results/split/test/'
    
    train_paths = glob.glob(os.path.join(train_dir, '*.parquet'))
    test_paths = glob.glob(os.path.join(test_dir, '*.parquet'))
    
    if not train_paths or not test_paths:
        print("Error: Train/Test split not found. Run split_corpus.py first.")
        return
        
    train_df = load_and_intersect_parquets(train_paths)
    print(f"Materialized Global Training Matrix: {train_df.shape}")
    
    # Apply Statistical Baseline Augmentation
    augmented_train = augment_with_gaussian_noise(train_df, noise_scale=0.15)
    
    # Prepare Arrays
    X_train = augmented_train.drop(columns=['Target']).values
    y_train = augmented_train['Target'].values
    
    # Standardize (Crucial for SVM convergence in high-D genomics)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train SVM Classifier
    print("Training the SVM Classifior (Control Model)...")
    clf = LinearSVC(dual=False, max_iter=2000, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    # Test Evaluation
    print("Testing against Unseen Real Patients (Global Test Set)...")
    test_df = load_and_intersect_parquets(test_paths)
    
    # Must enforce identical feature space structure as training!
    X_test = test_df[augmented_train.drop(columns=['Target']).columns].values
    y_test = test_df['Target'].values
    
    X_test_scaled = scaler.transform(X_test)
    
    # Predictions
    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("-" * 50)
    print("====== BASELINE RESULTS (Gaussiano + SVM) ======")
    print(f"F1-Score: {f1:.4f}")
    print(f"Accuracy: {acc:.4f}")
    print("Detailed Matrix:")
    print(classification_report(y_test, y_pred))
    print("-" * 50)
    print("Este puntaje es el muro que CTGAN debe superar matemáticamente en la Tesis.")

if __name__ == '__main__':
    run_baseline_evaluation()
