import pandas as pd
import GEOparse
import os

def find_matrices():
    vmeta = pd.read_csv("results/verified_samples.csv")
    verified_gses = vmeta['GSE'].unique()
    
    ingested_gses = []
    if os.path.exists("results/normalized"):
        ingested_gses = [f.split(".")[0] for f in os.listdir("results/normalized") if f.endswith(".parquet")]
        
    pending = [g for g in verified_gses if g not in ingested_gses]
    print(f"Checking {len(pending)} pending candidates...")
    
    results = []
    for gse in pending[:100]: # Check top 100 pending
        print(f"Auditing {gse}...")
        try:
            g = GEOparse.get_GEO(geo=gse, destdir="/tmp", silent=True, how="brief")
            supps = g.metadata.get('supplementary_file', [])
            if isinstance(supps, str): supps = [supps]
            
            for s in supps:
                if any(x in s.lower() for x in ['count', 'tpm', 'fpkm', 'matrix', 'normalization']):
                    if not s.endswith('RAW.tar'):
                        results.append({'GSE': gse, 'URL': s})
                        print(f"  FOUND: {s}")
        except Exception as e:
            print(f"  Error {gse}: {e}")
            
    df = pd.DataFrame(results)
    df.to_csv("results/manual_matrix_targets.csv", index=False)
    print("\nSaved high-quality targets to results/manual_matrix_targets.csv")

if __name__ == "__main__":
    find_matrices()
