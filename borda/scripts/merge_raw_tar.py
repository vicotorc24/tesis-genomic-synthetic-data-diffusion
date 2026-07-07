import pandas as pd
import os
import sys
import glob

def merge_tar_dir(directory, output_file):
    files = glob.glob(os.path.join(directory, "*.txt*")) + \
            glob.glob(os.path.join(directory, "*.csv*")) + \
            glob.glob(os.path.join(directory, "*.tsv*"))
    
    if not files:
        print("No counts files found.")
        return False
        
    all_dfs = []
    for f in files:
        gsm = os.path.basename(f).split('_')[0]
        if not gsm.startswith('GSM'):
            continue
            
        print(f"Reading {gsm}...")
        df = pd.read_csv(f, sep=None, engine='python', index_col=0)
        # Assume 1st numeric column is counts
        counts_col = df.select_dtypes(include=['number']).columns[0]
        series = df[counts_col].copy()
        series.name = gsm
        all_dfs.append(series)
        
    if not all_dfs:
        print("No valid GSM files mapped.")
        return False
        
    combined = pd.concat(all_dfs, axis=1)
    combined.to_csv(output_file)
    print(f"Combined matrix saved to {output_file} with shape {combined.shape}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_raw_tar.py <dir> <output_csv>")
    else:
        merge_tar_dir(sys.argv[1], sys.argv[2])
