import os
import glob
import random
import shutil

def split_corpus(train_ratio=0.7, seed=42):
    random.seed(seed)
    normalized_dir = 'results/normalized/'
    train_dir = 'results/split/train/'
    test_dir = 'results/split/test/'
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    parquets = glob.glob(os.path.join(normalized_dir, '*.parquet'))
    if not parquets:
        print("No parquets found to split.")
        return
        
    random.shuffle(parquets)
    split_idx = int(len(parquets) * train_ratio)
    
    train_files = parquets[:split_idx]
    test_files = parquets[split_idx:]
    
    for f in train_files:
        shutil.copy(f, os.path.join(train_dir, os.path.basename(f)))
        
    for f in test_files:
        shutil.copy(f, os.path.join(test_dir, os.path.basename(f)))
        
    print(f"Corpus Splitting Complete:")
    print(f"Total Datasets: {len(parquets)}")
    print(f"Global_Train: {len(train_files)} Datasets")
    print(f"Global_Test: {len(test_files)} Datasets")
    print(f"Location: results/split/")

if __name__ == '__main__':
    split_corpus()
