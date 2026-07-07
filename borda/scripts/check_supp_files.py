import pandas as pd
import os
from Bio import Entrez
import time

Entrez.email = "antigravity.assistant@example.com"

def check_supps():
    # Load verified candidates
    vmeta = pd.read_csv("results/verified_samples.csv")
    verified_gses = vmeta['GSE'].unique()
    
    # Load already ingested
    ingested_gses = []
    if os.path.exists("results/normalized"):
        ingested_gses = [f.split(".")[0] for f in os.listdir("results/normalized") if f.endswith(".parquet")]
    
    remaining = [g for g in verified_gses if g not in ingested_gses]
    print(f"Checking {len(remaining)} pending candidates for supplementary files...")
    
    results = []
    for gse in remaining[:50]: # Check first 50
        try:
            handle = Entrez.esearch(db="gds", term=f"{gse}[Accession]", retmax=1)
            record = Entrez.read(handle)
            handle.close()
            
            if not record["IdList"]:
                continue
                
            gseid = record["IdList"][0]
            handle = Entrez.esummary(db="gds", id=gseid)
            summary = Entrez.read(handle)
            handle.close()
            
            supp_files = summary[0].get('SuppFile', '')
            results.append({
                'GSE': gse,
                'SuppFiles': supp_files
            })
            print(f"{gse}: {supp_files}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error {gse}: {e}")
            
    df = pd.DataFrame(results)
    df.to_csv("results/supp_file_audit.csv", index=False)
    print("\nSaved to results/supp_file_audit.csv")

if __name__ == "__main__":
    check_supps()
