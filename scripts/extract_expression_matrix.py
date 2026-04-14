import os
import gc
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import GEOparse

GEOparse.logger.set_verbosity("ERROR")

def quantile_normalize(df):
    """
    Performs quantile normalization on a pandas DataFrame.
    Rows are genes and Columns are samples.
    """
    # 1. Sort each column
    dic = {}
    for col in df:
        dic[col] = df[col].sort_values(ascending=False).values
    sorted_df = pd.DataFrame(dic)
    
    # 2. Find row means
    rank_mean = sorted_df.mean(axis=1)
    
    # 3. Replace original values with the mean of the corresponding rank
    qnorm_df = df.copy()
    for col in qnorm_df:
        # Get ranks; method='first' breaks ties
        ranks = qnorm_df[col].rank(method="first", ascending=False).astype(int) - 1
        qnorm_df[col] = ranks.map(rank_mean)
        
    return qnorm_df

def counts_to_tpm_proxy(df):
    """
    Proxies a TPM transform (CPM) if exact gene lengths are unavailable.
    (reads per gene / total reads in sample) * 1,000,000
    """
    # Normalize each column by its sum, then multiply by 1e6
    col_sums = df.sum(axis=0)
    col_sums[col_sums == 0] = 1  # Avoid division by zero
    tpm_df = (df / col_sums) * 1e6
    return tpm_df

def get_symbol_column(gpl_df):
    candidates = ['Gene Symbol', 'Gene_Symbol', 'Symbol', 'GENE_SYMBOL', 'Gene', 'Official Symbol', 'Gene symbol', 'GENE', 'gene_assignment']
    for cand in candidates:
        if cand in gpl_df.columns:
            return cand
    for col in gpl_df.columns:
        if 'symbol' in str(col).lower():
            return col
    return None

def process_study(gse_id, technology, valid_samples_df):
    """
    Parse the study, map genes, apply V11 normalizations, and return the Parquet dataframe.
    """
    try:
        gse = GEOparse.get_GEO(geo=gse_id, destdir="results/soft", silent=True)
    except Exception as e:
        print(f"Skipping {gse_id}: Soft file parse error: {e}")
        return None
        
    study_metadata = valid_samples_df[(valid_samples_df['GSE'] == gse_id) & (valid_samples_df['Category'].isin(['Normal', 'Tumor']))]
    valid_gsms = study_metadata['GSM'].tolist()
    
    # Build mapping if Microarray
    mapping = None
    if gse.gpls:
        gpl_name = list(gse.gpls.keys())[0]
        gpl = gse.gpls[gpl_name]
        symbol_col = get_symbol_column(gpl.table)
        if symbol_col:
            mapping = gpl.table.set_index('ID')[symbol_col].to_dict()
    
    expression_dfs = []
    skipped_count = 0
    
    for gsm_name in valid_gsms:
        if gsm_name not in gse.gsms:
            continue
            
        gsm = gse.gsms[gsm_name]
        if gsm.table.empty or 'ID_REF' not in gsm.table.columns or 'VALUE' not in gsm.table.columns:
            skipped_count += 1
            continue
            
        df_gsm = gsm.table[['ID_REF', 'VALUE']].copy()
        
        # 1. Map ID_REF to Gene Symbol
        if mapping:
            df_gsm['Gene'] = df_gsm['ID_REF'].map(mapping)
            # Fallback for unmapped or RNA-seq masquerading
            df_gsm['Gene'] = df_gsm['Gene'].fillna(df_gsm['ID_REF'])
        else:
            df_gsm['Gene'] = df_gsm['ID_REF']
            
        df_gsm = df_gsm.dropna(subset=['Gene', 'VALUE'])
        df_gsm['Gene'] = df_gsm['Gene'].astype(str).str.split('///').str[0].str.strip()
        df_gsm = df_gsm[(df_gsm['Gene'] != '') & (df_gsm['Gene'] != 'nan') & (df_gsm['Gene'].str.len() > 1)]
        
        # Deduplication
        df_gsm['VALUE'] = pd.to_numeric(df_gsm['VALUE'], errors='coerce')
        df_gsm = df_gsm.dropna(subset=['VALUE'])
        
        # If Microarray, we can take median. If RNA-seq counts, we sum duplicates.
        if technology == 'Microarray':
            collapsed = df_gsm.groupby('Gene')['VALUE'].median().reset_index()
        else:
            collapsed = df_gsm.groupby('Gene')['VALUE'].sum().reset_index()
            
        collapsed = collapsed.rename(columns={'VALUE': gsm_name})
        collapsed = collapsed.set_index('Gene')
        expression_dfs.append(collapsed)
        
    if not expression_dfs:
        print(f"[{gse_id}] No valid GSM tables found or parsed. (Skipped {skipped_count} samples)")
        return None
        
    # Merge into Global Matrix (Genes as Rows, Samples as Columns)
    study_matrix = pd.concat(expression_dfs, axis=1)
    
    # Drop rows (genes) that have NaN in ANY sample.
    study_matrix = study_matrix.dropna()
    
    if study_matrix.empty:
        print(f"[{gse_id}] Resulting matrix is empty after resolving missing gene values.")
        return None
        
    # 2. V11 Normalization based on Technology
    if technology == 'Microarray':
        study_matrix = quantile_normalize(study_matrix)
    elif technology == 'RNA-seq':
        study_matrix = counts_to_tpm_proxy(study_matrix)
        
    # 3. Log2(x + 1) transform
    # clip at 0 to avoid log2 of negative numbers (some microarrays output negative intensities)
    study_matrix = study_matrix.clip(lower=0) 
    study_matrix = np.log2(study_matrix + 1)
    
    # 4. Transpose so rows = Samples, Columns = Genes
    study_matrix = study_matrix.transpose()
    
    # 5. Attach Label (0: Normal, 1: Tumor)
    # create a dict of GSM -> label (0 for Normal, 1 for Tumor)
    labels = []
    for gsm in study_matrix.index:
        sample_info = study_metadata[study_metadata['GSM'] == gsm].iloc[0]
        if sample_info['Category'] == 'Tumor':
            labels.append(1)
        elif sample_info['Category'] == 'Normal':
            labels.append(0)
            
    study_matrix.insert(0, 'Target', labels)
    study_matrix.insert(0, 'GSE_ID', gse_id)
    
    return study_matrix

def build_corpus():
    print("Initializing Multi-omics Expression Extraction Pipeline (V11)")
    
    if not os.path.exists("results/verified_samples.csv"):
        print("Error: verified_samples.csv not found.")
        return
        
    os.makedirs("results/normalized", exist_ok=True)
    
    df = pd.read_csv("results/verified_samples.csv")
    report = pd.read_csv("results/class_balance_report.csv")
    
    # Create a quick dict of GSE -> Technology
    tech_map = dict(zip(report['GSE_ID'], report['Technology']))
    
    gse_list = df['GSE'].unique()
    print(f"Began unified extraction for {len(gse_list)} datasets...")
    
    success_count = 0
    fail_count = 0
    
    # For speed and progress updates, we process sequentially and save immediately
    for i, gse_id in enumerate(gse_list):
        output_file = f"results/normalized/{gse_id}.parquet"
        
        if os.path.exists(output_file):
            print(f"[{i}/{len(gse_list)}] {gse_id} already extracted. Skipping...")
            success_count += 1
            continue
            
        tech = tech_map.get(gse_id, 'Microarray')
        print(f"[{i}/{len(gse_list)}] Processing {gse_id} ({tech})...")
        
        res = process_study(gse_id, tech, df)
        if res is not None:
            # Save using pyarrow snappy compression
            table = pa.Table.from_pandas(res)
            pq.write_table(table, output_file, compression='snappy')
            print(f"  -> Successfully generated Parquet: {res.shape[0]} samples, {res.shape[1]-2} genes")
            success_count += 1
        else:
            fail_count += 1
            
        gc.collect() # prevent memory leaks over 282 loops
        
    print(f"\nPipeline Finished! Successfully extracted: {success_count} | Failed: {fail_count}")

if __name__ == "__main__":
    build_corpus()
