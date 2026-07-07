import pandas as pd
import glob
import os
import numpy as np

def audit_rescue():
    harmonized_path = 'results/harmonized/*.parquet'
    harmonized_files = glob.glob(harmonized_path)
    
    # El Core Set de genes lo sacamos de la tabla maestra actual
    master_path = 'results/master_training_table.parquet'
    master_df = pd.read_parquet(master_path)
    core_genes = [c for c in master_df.columns if c not in ['GSE_ID', 'Technology_Label', 'Category']]
    
    results = []
    
    print(f"🧐 Audidando {len(harmonized_files)} archivos armonizados...")
    
    for file in harmonized_files:
        df = pd.read_parquet(file)
        # Identificar qué genes del core están presentes en este estudio
        present_genes = list(set(core_genes) & set(df.columns))
        n_present = len(present_genes)
        pct_present = (n_present / len(core_genes)) * 100
        
        n_samples = len(df)
        
        results.append({
            'file': os.path.basename(file),
            'samples': n_samples,
            'genes_present': n_present,
            'pct_core': pct_present
        })
        
    audit_df = pd.DataFrame(results)
    
    # Calcular potencial de rescate por umbrales
    thresholds = [100, 95, 90, 80, 70, 50]
    print("\n📈 POTENCIAL DE RESCATE SEGÚN UMBRAL DE CORE SET:")
    
    for t in thresholds:
        eligible = audit_df[audit_df['pct_core'] >= t]
        total_samples = eligible['samples'].sum()
        print(f"- Umbral {t}% del Core Set: {total_samples} muestras disponibles ({len(eligible)} estudios)")

if __name__ == "__main__":
    audit_rescue()
