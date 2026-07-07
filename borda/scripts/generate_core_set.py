import pandas as pd
import numpy as np
import os

def isolate_core_set():
    input_file = "results/master_training_table.parquet"
    output_file = "results/master_core_set.parquet"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading {input_file}...")
    df = pd.read_parquet(input_file)
    
    # Exclude metadata columns for density calculation
    metadata_cols = ['GSE_ID', 'Target', 'Technology_Label']
    gene_cols = [c for c in df.columns if c not in metadata_cols]
    
    print(f"Calculating gene density across {len(gene_cols)} features...")
    
    # Density is defined as non-zero and non-NaN
    # In our harmonized table, missing genes were filled with 0.0
    non_zero_counts = (df[gene_cols] > 0).sum(axis=1)
    density = non_zero_counts / len(gene_cols)
    
    mask = density >= 0.90
    core_df = df[mask]
    
    print(f"Total samples: {len(df)}")
    print(f"Core Set samples (>=90% density): {len(core_df)}")
    
    if len(core_df) > 0:
        print(f"Saving Core Set to {output_file}...")
        core_df.to_parquet(output_file)
        print("Done.")
    else:
        print("Warning: Core Set is empty! Check harmonization logic.")

if __name__ == "__main__":
    isolate_core_set()
