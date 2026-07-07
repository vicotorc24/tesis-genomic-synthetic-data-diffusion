import os
import pandas as pd
import numpy as np
import GEOparse
import glob
from tqdm import tqdm
import gc
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Max workers: logical cores minus 1 to keep system responsive
MAX_WORKERS = max(1, multiprocessing.cpu_count() - 1)

def get_symbol_from_assignment(val):
    if not isinstance(val, str): return np.nan
    # Split by common GEO separators: //, ///, or :
    for sep in ['///', '//', ':']:
        if sep in val:
            parts = val.split(sep)
            # Gene symbol is usually in the middle or second part
            # NM_001256799 // STAT1 // ... -> STAT1
            if len(parts) > 1:
                cand = parts[1].strip()
                if cand and cand != '---':
                    return cand.upper()
            return parts[0].strip().upper()
    return val.strip().upper()

def harmonize_one(parquet_path):
    soft_dir = "results/soft"
    output_dir = "results/harmonized"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        gse_id = os.path.basename(parquet_path).replace('.parquet', '')
        df = pd.read_parquet(parquet_path)
        
        # Identify meta columns
        meta_cols = [c for c in ['Target', 'GSE_ID', 'Technology', 'Category'] if c in df.columns]
        sample_cols = [str(c) for c in df.columns if c not in meta_cols]
        
        if not sample_cols:
            return f"{gse_id}: Skip - No data columns"

        # Check if headers contain complex info (//)
        has_complex_headers = any(['//' in c for c in sample_cols[:100]])
        
        # Robust probe detection: 
        is_probe = any(['_at' in c for c in sample_cols[:100]]) or \
                   all([c.isdigit() or '.' in c for c in sample_cols[:20]])
        
        if (not is_probe or has_complex_headers) and len(sample_cols) > 0:
            # Try to clean headers first
            new_cols = {}
            for c in df.columns:
                if c in meta_cols:
                    new_cols[c] = c
                else:
                    new_cols[c] = get_symbol_from_assignment(str(c))
            
            df.rename(columns=new_cols, inplace=True)
            
            # After renaming, we might have '---' or other noise. Drop non-gene-like columns.
            valid_cols = [c for c in df.columns if str(c) not in ['---', 'nan', 'NAN', '']]
            df = df[valid_cols]
            
            # Collapse duplicates (Median is safest for normalized data)
            current_meta = [c for c in meta_cols if c in df.columns]
            expr_data = df.drop(columns=current_meta)
            
            if not expr_data.empty:
                expr_data = expr_data.groupby(axis=1, level=0).median()
                # Re-attach metadata
                for col in reversed(current_meta):
                    expr_data.insert(0, col, df[col])
                
                expr_data.to_parquet(os.path.join(output_dir, f"{gse_id}.parquet"))
                count = len(expr_data.columns) - len(current_meta)
                return f"{gse_id}: Harmonized from Headers ({count} genes)"

        # Fallback to GPL mapping if it looks like probes
        soft_path = os.path.join(soft_dir, f"{gse_id}_family.soft.gz")
        if not os.path.exists(soft_path):
            return f"{gse_id}: Skip - SOFT not found"
        
        gse = GEOparse.get_GEO(filepath=soft_path, silent=True)
        if not gse.gpls:
            return f"{gse_id}: Skip - No GPL"
        
        gpl = gse.gpls[list(gse.gpls.keys())[0]]
        table = gpl.table
        
        # Expanded priority search for symbol column
        candidate_cols = [
            'Gene Symbol', 'GENE_SYMBOL', 'Symbol', 'Official Symbol', 
            'gene_assignment', 'GENE', 'ID_REF', 'ASSOCIATED_GENE',
            'GB_ACC', 'ENTREZ_GENE_ID', 'ORF', 'NAME'
        ]
        found_col = None
        for c in candidate_cols:
            matches = [tc for tc in table.columns if c.lower() == tc.lower() or c.lower() in tc.lower()]
            if matches:
                found_col = matches[0]
                break
        
        if not found_col:
            return f"{gse_id}: Skip - No Symbol col in GPL"
        
        # Extract mapping
        mapping = table[['ID', found_col]].dropna()
        mapping[found_col] = mapping[found_col].apply(get_symbol_from_assignment)
            
        mapping_dict = dict(zip(mapping['ID'].astype(str), mapping[found_col].astype(str).str.upper()))
        
        # Apply mapping
        expr_df = df.drop(columns=meta_cols)
        expr_df.columns = [str(c) for c in expr_df.columns]
        valid_cols = [c for c in expr_df.columns if c in mapping_dict]
        expr_df = expr_df[valid_cols]
        expr_df.rename(columns=mapping_dict, inplace=True)
        
        # Collapse duplicates (Median)
        if not expr_df.empty:
            expr_df = expr_df.groupby(axis=1, level=0).median()
        
        # Re-add metadata
        for col in reversed(meta_cols):
            if col in df.columns:
                expr_df.insert(0, col, df[col])
            
        expr_df.to_parquet(os.path.join(output_dir, f"{gse_id}.parquet"))
        count = len(expr_df.columns) - len(meta_cols)
        
        return f"{gse_id}: Harmonized via GPL ({count} genes)"
        
    except Exception as e:
        return f"{gse_id}: Error - {str(e)}"

def run_harmonization():
    input_dir = "results/normalized"
    files = sorted(glob.glob(os.path.join(input_dir, "*.parquet")))
    print(f"Starting PARALLEL harmonization for {len(files)} files using {MAX_WORKERS} workers...")
    
    results = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(harmonize_one, f): f for f in files}
        for future in tqdm(as_completed(futures), total=len(files)):
            results.append(future.result())
        
    os.makedirs("REPORTS", exist_ok=True)
    with open("REPORTS/harmonization_log.txt", "w") as l:
        l.write("\n".join(results))
    
    print("\nHarmonization Finished. Check REPORTS/harmonization_log.txt")

if __name__ == "__main__":
    run_harmonization()

if __name__ == "__main__":
    run_harmonization()
