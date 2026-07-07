import pandas as pd
import glob
import os
import json
from collections import Counter
from tqdm import tqdm

def find_intersection():
    input_dir = "results/harmonized"
    files = glob.glob(os.path.join(input_dir, "*.parquet"))
    print(f"Analyzing {len(files)} harmonized files for gene frequency...")
    
    gene_counter = Counter()
    metadata_cols = {'Target', 'GSE_ID', 'Technology', 'Category'}
    
    for f in tqdm(files):
        try:
            # We only need the columns, not the data (much faster)
            df = pd.read_parquet(f, columns=[]) # read_parquet with columns=[] only reads metadata/headers in some engines
            # Wait, read_parquet with columns=[] might not work for getting all headers easily depending on engine
            # Better to read just one row
            df_sample = pd.read_parquet(f).iloc[:1]
            genes = [c for c in df_sample.columns if c not in metadata_cols]
            gene_counter.update(genes)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    # Convert to DataFrame for easier analysis
    freq_df = pd.DataFrame.from_dict(gene_counter, orient='index', columns=['Frequency'])
    freq_df.index.name = 'Gene'
    freq_df = freq_df.sort_values(by='Frequency', ascending=False)
    
    # Save full frequency report
    os.makedirs("REPORTS", exist_ok=True)
    freq_df.to_csv("REPORTS/gene_frequency_report.csv")
    
    # Selection Strategy:
    # We take the TOP 2500 most frequent genes across all successfully harmonized studies.
    # We ignore genes that only appear in 1 study to ensure some overlap.
    
    final_genes = freq_df[freq_df['Frequency'] > 1].head(2500).index.tolist()
    
    print(f"\nReporte de Intersección (NUEVO COMPROMISO TOP 2,500):")
    print(f"- Total de genes únicos encontrados: {len(freq_df)}")
    print(f"- Genes en > 1 estudio: {len(freq_df[freq_df['Frequency'] > 1])}")
    print(f"- Genes seleccionados para Master Table: {len(final_genes)}")
    
    # Save the feature list
    feature_config = {
        "n_source_files": len(files),
        "n_features": len(final_genes),
        "features": final_genes
    }
    
    with open("results/feature_selection.json", "w") as j:
        json.dump(feature_config, j, indent=4)
        
    print("\nFeature Selection JSON saved at: results/feature_selection.json")

if __name__ == "__main__":
    find_intersection()
