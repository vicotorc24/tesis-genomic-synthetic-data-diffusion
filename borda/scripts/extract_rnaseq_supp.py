import os
import glob
import pandas as pd
import numpy as np
import GEOparse
import requests
import tarfile
import gzip
import shutil
import io

def counts_to_tpm_proxy(df):
    """
    Crude TPM proxy by dividing raw counts by column totals in millions.
    """
    col_sums = df.sum(axis=0)
    col_sums[col_sums == 0] = 1 
    tpm_matrix = (df / col_sums) * 1e6
    return tpm_matrix

import urllib.request

def download_file(url, dest_path):
    print(f"      -> Downloading from FTP/HTTP...")
    if url.startswith('ftp://'):
        urllib.request.urlretrieve(url, dest_path)
    else:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                
def hunt_and_extract_supp_rna(max_success=5):
    report_path = 'results/class_balance_report.csv'
    valid_samples_path = 'results/verified_samples.csv'
    output_dir = 'results/normalized'
    supp_dir = 'results/supp_files'
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(supp_dir, exist_ok=True)
    
    report_df = pd.read_csv(report_path)
    samples_df = pd.read_csv(valid_samples_path)
    
    # Filter only RNA-seq
    rna_studies = report_df[report_df['Technology'] == 'RNA-seq']['GSE_ID'].tolist()
    print(f"Hunting for Supplementary counts within {len(rna_studies)} RNA-seq datasets...")
    
    success_count = 0
    for i, gse_id in enumerate(rna_studies):
        if success_count >= max_success:
            print(f"Reached success target ({max_success}). Halting hunt.")
            break
            
        parquet_out = os.path.join(output_dir, f"{gse_id}.parquet")
        if os.path.exists(parquet_out):
            print(f"[{i+1}/{len(rna_studies)}] {gse_id} already exists.")
            success_count += 1
            continue
            
        print(f"[{i+1}/{len(rna_studies)}] Auditing {gse_id}...")
        try:
            gse = GEOparse.get_GEO(gse_id, destdir=supp_dir, silent=True)
        except Exception as e:
            print(f"  -> GEOparse fetch failed: {e}")
            continue
            
        # Discover supplementary URLs
        supp_urls = []
        for k, v in gse.metadata.items():
            if k.startswith('supplementary_file'):
                for url in v:
                    supp_urls.append(url)
                    
        # Find candidates (usually end in .txt.gz, count.csv.gz, raw.tar)
        candidate_url = None
        for u in supp_urls:
            ulow = u.lower()
            if 'count' in ulow or 'matrix' in ulow or ulow.endswith('txt.gz') or ulow.endswith('csv.gz') or ulow.endswith('tsv.gz'):
                if ulow.endswith('.tar'): continue
                candidate_url = u
                break
                
        if not candidate_url:
            print(f"  -> No promising supplementary count file detected.")
            continue
            
        print(f"  -> Found candidate URL: {candidate_url}")
        filename = candidate_url.split('/')[-1]
        local_path = os.path.join(supp_dir, filename)
        
        try:
            download_file(candidate_url, local_path)
        except Exception as e:
            print(f"  -> Download failed: {e}")
            continue
            
        # Attempt to load the raw matrix into pandas
        try:
            if local_path.endswith('.csv.gz'):
                raw_df = pd.read_csv(local_path, index_col=0)
            elif local_path.endswith('.txt.gz') or local_path.endswith('.tsv.gz'):
                raw_df = pd.read_csv(local_path, sep='\t', index_col=0)
            elif local_path.endswith('.tar'):
                 print("  -> Skipped TAR format for safety.")
                 continue
            else:
                 raw_df = pd.read_csv(local_path, index_col=0, sep=None, engine='python')
        except Exception as e:
             print(f"  -> Parsing failed: {e}")
             continue
             
        # Verification: we need columns to somewhat match the standard sample GSM names
        valid_gsms_for_study = samples_df[(samples_df['GSE'] == gse_id) & (samples_df['Category'].isin(['Normal', 'Tumor']))]['GSM'].tolist()
        
        # Check column overlap
        matrix_cols = set(raw_df.columns.astype(str))
        intersect = set(valid_gsms_for_study).intersection(matrix_cols)
        
        if len(intersect) < 10:
            print(f"  -> Failed: The supplementary file doesn't map to standard strict GSM column headers. (matched {len(intersect)} columns)")
            continue
            
        print(f"  -> Great! Matched {len(intersect)} valid samples in the dataset.")
        
        # Crop dataset strictly to valid GSM columns
        final_valid_cols = list(intersect)
        raw_df = raw_df[final_valid_cols].copy()
        
        # Try numeric coercion
        try:
            raw_df = raw_df.apply(pd.to_numeric, errors='coerce')
        except:
            pass
            
        raw_df = raw_df.dropna()
        if raw_df.empty:
             print("  -> Failed: Matrix empty after dropping NaNs.")
             continue
             
        # Apply transformation: TPM + Log2
        print("  -> Synthesizing proxy TPM and Log2(x+1) Transform...")
        transformed_df = counts_to_tpm_proxy(raw_df)
        transformed_df = np.log2(transformed_df + 1)
        
        # Transpose to Samples x Genes
        study_matrix = transformed_df.transpose()
        
        # Add labels
        labels = []
        study_sub = samples_df[(samples_df['GSE'] == gse_id) & (samples_df['Category'].isin(['Normal', 'Tumor']))]
        for gsm_id in study_matrix.index:
            cat = study_sub[study_sub['GSM'] == str(gsm_id)].iloc[0]['Category']
            labels.append(1 if cat == 'Tumor' else 0)
            
        study_matrix.insert(0, 'Target', labels)
        
        # Save Parquet
        study_matrix.columns = study_matrix.columns.astype(str)
        study_matrix.to_parquet(parquet_out, compression='snappy')
        print(f"  -> SUCCESS! Assembled supplementary data into: {parquet_out}")
        success_count += 1
        
if __name__ == '__main__':
    # Try to rescue 5 RNA-seq studies to give CTGAN some biological RNA-seq textural variety
    hunt_and_extract_supp_rna(max_success=5)
