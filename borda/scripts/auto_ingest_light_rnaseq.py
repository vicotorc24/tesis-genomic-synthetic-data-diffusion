import os
import pandas as pd
import urllib.request
import GEOparse
from ingest_manual_rnaseq import ingest_manual_rna

def auto_sweep_light_rnaseq():
    print("Iniciando escaneo masivo de RNA-seq livianos...")
    df = pd.read_csv('results/class_balance_report.csv')
    rna_studies = df[df['Technology'] == 'RNA-seq']['GSE_ID'].tolist()
    
    os.makedirs('/tmp/rna_downloads', exist_ok=True)
    os.makedirs('results/normalized', exist_ok=True)
    
    success_count = 0
    
    for gse_id in rna_studies:
        parquet_out = f'results/normalized/{gse_id}.parquet'
        if os.path.exists(parquet_out):
            print(f"{gse_id} ya existe. Saltando...")
            continue
            
        print(f"\nAuditando {gse_id}...")
        try:
            gse = GEOparse.get_GEO(gse_id, destdir='results/soft', silent=True)
            files = [k for k in gse.metadata.keys() if 'supplementary_file' in k]
            
            candidates = []
            for f_key in files:
                url = gse.metadata[f_key][0]
                if url.endswith('.txt.gz') or url.endswith('.csv.gz'):
                    if '_GEO_sample_info' not in url and 'metadata' not in url.lower():
                        candidates.append(url)
            
            if not candidates:
                print(f"-> {gse_id} no tiene matrices puras (posible RAW.tar). Saltando.")
                continue
                
            # Tomamos la primera matriz pura
            target_url = candidates[0]
            extension = '.csv.gz' if '.csv' in target_url else '.txt.gz'
            temp_path = f'/tmp/rna_downloads/{gse_id}_matrix{extension}'
            
            print(f"-> ¡Matriz pura encontrada! Descargando {target_url}...")
            urllib.request.urlretrieve(target_url, temp_path)
            
            # Ejecutamos nuestra poderosa función heurística
            print(f"-> Procesando {gse_id} con la heurstica Multi-Ómica...")
            ingest_manual_rna(gse_id, temp_path)
            
            if os.path.exists(parquet_out):
                success_count += 1
                
        except Exception as e:
            print(f"-> Error procesando {gse_id}: {e}")
            
    print(f"\n=== BARRIDO COMPLETADO ===")
    print(f"Se extrajeron {success_count} nuevos datasets RNA-seq nativos.")

if __name__ == "__main__":
    auto_sweep_light_rnaseq()
