import os
import pandas as pd
from Bio import Entrez
import time

Entrez.email = "antigravity.assistant@example.com"

def fetch_by_term(term, tech_label, max_results=500, max_keep=300):
    print(f"\nSearching GEO for {tech_label}: {term}")
    handle = Entrez.esearch(db="gds", term=term, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    print(f"Found {record['Count']} total records, fetching summaries for top {len(id_list)}...")
    
    candidates = []
    for i in range(0, len(id_list), 50):
        chunk = id_list[i:i+50]
        handle = Entrez.esummary(db="gds", id=",".join(chunk))
        summaries = Entrez.read(handle)
        handle.close()
        
        for summary in summaries:
            accession = summary.get('Accession', '')
            gse = accession if accession.startswith("GSE") else f"GSE{summary.get('GSE', '')}"
            if not gse or gse == "GSE":
                continue
                
            title = summary.get('title', '')
            n_samples = summary.get('n_samples', 0)
            
            if n_samples is not None and int(n_samples) >= 50:
                candidates.append({
                    'GSE': gse,
                    'Title': title,
                    'Samples': int(n_samples),
                    'PDAT': summary.get('PDAT', ''),
                    'Technology': tech_label
                })
        time.sleep(1) # respect API limits
        
    df = pd.DataFrame(candidates)
    if not df.empty:
        df = df.head(max_keep)
        return df
    return pd.DataFrame()

def get_geo_candidates():
    term_rnaseq = '"Homo sapiens"[porgn] AND "Expression profiling by high throughput sequencing"[DataSet Type] AND (cancer OR tumor) AND "gse"[Entry Type]'
    df_rnaseq = fetch_by_term(term_rnaseq, 'RNA-seq', max_results=2000, max_keep=300)
    
    term_array = '"Homo sapiens"[porgn] AND "Expression profiling by array"[DataSet Type] AND (cancer OR tumor) AND "gse"[Entry Type]'
    df_array = fetch_by_term(term_array, 'Microarray', max_results=5000, max_keep=800)
    
    frames = [df_rnaseq, df_array]
    frames = [f for f in frames if not f.empty]
    
    if frames:
        df = pd.concat(frames, ignore_index=True)
        # Drop mixed platform duplicates if any
        df = df.drop_duplicates(subset=['GSE'])
        
        rna_c = len(df[df['Technology'] == 'RNA-seq'])
        arr_c = len(df[df['Technology'] == 'Microarray'])
        
        print(f"\nFiltered down to {len(df)} candidates (RNA-seq: {rna_c}, Microarray: {arr_c}) with >= 50 samples.")
        os.makedirs("results", exist_ok=True)
        df.to_csv("results/geo_candidates.csv", index=False)
        print("Saved to results/geo_candidates.csv")
    else:
        print("No candidates found matching criteria.")

if __name__ == "__main__":
    get_geo_candidates()
