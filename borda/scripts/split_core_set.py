import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_core_set():
    input_file = "results/master_core_set.parquet"
    train_output = "results/core_train.parquet"
    test_output = "results/core_test.parquet"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading {input_file}...")
    df = pd.read_parquet(input_file)
    
    print(f"Splitting 80/20 (stratified by Category)...")
    train_df, test_df = train_test_split(
        df, 
        test_size=0.20, 
        random_state=42, 
        stratify=df['Category']
    )
    
    print(f"Train samples: {len(train_df)}")
    print(f"Test samples: {len(test_df)}")
    
    train_df.to_parquet(train_output)
    test_df.to_parquet(test_output)
    
    print(f"✅ Saved splits to {train_output} and {test_output}")

if __name__ == "__main__":
    split_core_set()
