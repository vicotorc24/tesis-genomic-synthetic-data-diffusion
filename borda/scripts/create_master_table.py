import pandas as pd
import glob
import os
import json
import numpy as np
from tqdm import tqdm
import gc

def create_master_table():
    # 1. Load Feature Selection
    config_path = "results/feature_selection.json"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return
        
    with open(config_path, "r") as j:
        config = json.load(j)
    
    selected_features = config['features']
    print(f"Building Master Table with {len(selected_features)} gene features...")
    
    # 2. Get Harmonized Files and Technology mapping
    input_dir = "results/harmonized"
    files = sorted(glob.glob(os.path.join(input_dir, "*.parquet")))
    
    # We need the Technology info to add the conditional label
    balance = pd.read_csv('results/class_balance_report.csv')
    tech_map = dict(zip(balance['GSE_ID'], balance['Technology']))
    
    all_chunks = []
    
    print(f"Processing {len(files)} files...")
    for f in tqdm(files):
        try:
            gse_id = os.path.basename(f).replace('.parquet', '')
            df = pd.read_parquet(f)
            
            # Map Technology to numeric label (Conditional GAN needs numeric/categorical info)
            # RNA-seq -> 0, Microarray -> 1
            tech_str = tech_map.get(gse_id, 'Microarray') # Default to Microarray if unknown
            tech_label = 0 if tech_str == 'RNA-seq' else 1
            
            # Prepare metadata columns
            meta_cols = {
                'GSE_ID': gse_id,
                'Technology': tech_label,
                'Target': df['Target'].values # 0 for Normal, 1 for Tumor
            }
            
            # Select/Filter Genes
            # If gene is missing, fill with 0.0 (Log space)
            # Reindex is efficient for this
            expr_df = df.reindex(columns=selected_features, fill_value=0.0)
            
            # Insert metadata at the beginning
            expr_df.insert(0, 'Category', df['Target']) # Column for easier TSTR validation later
            expr_df.insert(0, 'Technology_Label', tech_label)
            expr_df.insert(0, 'GSE_ID', gse_id)
            
            # Optimize memory: float32
            # Only columns that are not GSE_ID
            float_cols = [c for c in expr_df.columns if c != 'GSE_ID']
            expr_df[float_cols] = expr_df[float_cols].astype(np.float32)
            
            all_chunks.append(expr_df)
            
            # Clean up
            del df
            del expr_df
            
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    # 3. Final Concatenation
    print("\nConcatenating all studies...")
    master_df = pd.concat(all_chunks, ignore_index=True)
    
    # 4. Export
    os.makedirs("results", exist_ok=True)
    output_path = "results/master_training_table.parquet"
    print(f"Saving Master Table to {output_path}...")
    master_df.to_parquet(output_path, compression='snappy')
    
    print(f"\nSUCCESS! Master Table Created.")
    print(f"- Total Samples: {len(master_df)}")
    print(f"- Total Features: {len(master_df.columns)}")
    print(f"- File: {output_path}")

if __name__ == "__main__":
    create_master_table()
