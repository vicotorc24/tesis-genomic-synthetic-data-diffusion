import os
import pandas as pd
import numpy as np
import argparse

def counts_to_tpm_proxy(df):
    """ Crude TPM proxy by dividing raw counts by column totals in millions. """
    col_sums = df.sum(axis=0)
    col_sums[col_sums == 0] = 1 
    return (df / col_sums) * 1e6

def ingest_manual_rna(gse_id, counts_file_path):
    print(f"Iniciando Ingesta Manual RNA-Seq para {gse_id}...")
    samples_df = pd.read_csv('results/verified_samples.csv')
    
    # Check if GSE exists in verified metadata
    study_sub = samples_df[(samples_df['GSE'] == gse_id) & (samples_df['Category'].isin(['Normal', 'Tumor']))]
    if study_sub.empty:
        print(f"Error: El estudio {gse_id} no tiene muestras válidas en verified_samples.csv.")
        return
    
    # Load RAW matrix con detección de separador adaptativa
    print(f"Cargando matriz RAW desde {counts_file_path}...")
    try:
        # Primero intentamos detectar si es comma or tab leyendo una linea
        if counts_file_path.endswith('.gz'):
            import gzip
            with gzip.open(counts_file_path, 'rt', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()
        else:
            with open(counts_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()
        sep = '\t' if '\t' in first_line else ','
        
        raw_df = pd.read_csv(counts_file_path, sep=sep, index_col=0)
        # Limpieza crucial de nombres de columnas
        raw_df.columns = [str(c).strip() for c in raw_df.columns]
        
    except Exception as e:
        print(f"Error al cargar la matriz: {e}")
        return
        
    # 1. Identificar columnas que YA son GSMs válidos en TODA nuestra base de datos verificada
    valid_gsms_global = set(samples_df['GSM'].astype(str))
    matrix_cols = [str(c).strip() for c in raw_df.columns]
    found_gsms = set(matrix_cols).intersection(valid_gsms_global)
    
    # 2. Mapeo inteligente para el resto mediante metadatos específicos del estudio
    import GEOparse
    try:
        print(f"Traduciendo nombres para {gse_id} mediante NCBI GEO...")
        gse = GEOparse.get_GEO(gse_id, destdir='results/soft', silent=True)
        
        title_to_gsm = {}
        for col in matrix_cols:
            if col in found_gsms: continue
            
            for gsm_name, gsm in gse.gsms.items():
                # Search across all metadata fields for the column name
                found = False
                for val_list in gsm.metadata.values():
                    for val in val_list:
                        if col == str(val).strip() or col in str(val).strip():
                            title_to_gsm[col] = gsm_name
                            found = True
                            print(f"    Match found: {col} -> {gsm_name} (via {str(val).strip()})")
                            break
                    if found: break
                if found: break
            if not found:
                print(f"    No match for column: {col}")
                            
        print(f"Mapeo inteligente completado: {len(title_to_gsm)} nuevas columnas vinculadas.")
        raw_df.rename(columns=title_to_gsm, inplace=True)
    except Exception as e:
        print(f"La traducción de metadatos GEO dinámica falló: {e}")
        
    # Recalcular intersección tras el mapeo
    matrix_cols_final = set(raw_df.columns.astype(str))
    intersect = set(valid_gsms_global).intersection(matrix_cols_final)
    
    if len(intersect) < 2:
        # Fallback: a veces hay múltiples columnas de índice (e.g. GeneID, Symbol)
        # Si la primera columna no parece data, puede que el index_col=0 haya fallado o no sea suficiente
        print(f"Critico: Pocos matches ({len(intersect)}). Re-intentando con reset_index si el índice parece un GSM...")
        if str(raw_df.index.name) in valid_gsms_global or any(str(i).startswith('GSM') for i in raw_df.index[:3]):
             raw_df = raw_df.reset_index()
             matrix_cols_final = set(raw_df.columns.astype(str))
             intersect = set(valid_gsms_global).intersection(matrix_cols_final)
    
    if len(intersect) < 2:
        print(f"Critico: Los nombres de columnas de tu archivo {list(matrix_cols_final)[:5]} no coinciden con IDs verificados globales...")
        return
        
    print(f"Excelente. Se mapearon {len(intersect)} muestras (Normal/Tumor) válidas.")
    
    # Filtro estricto
    raw_df = raw_df[list(intersect)].copy()
    raw_df = raw_df.apply(pd.to_numeric, errors='coerce').dropna()
    
    # Pipeline Algoritmico: TPM + Log2(x+1)
    print("Aplicando Transformación Universal: TPM Proxy -> Espacio Log2...")
    tpm_df = counts_to_tpm_proxy(raw_df)
    log_df = np.log2(tpm_df + 1)
    
    # Transposición y Etiquetas con búsqueda GLOBAL
    study_matrix = log_df.transpose()
    print(f"Mapeo final: {len(study_matrix.index)} muestras detectadas.")
    labels = []
    dropped_indices = []
    for gsm_id in study_matrix.index:
        # Buscar en toda la DB de muestras verificadas
        matcher = samples_df[samples_df['GSM'] == str(gsm_id)]
        if not matcher.empty:
            cat = matcher.iloc[0]['Category']
            labels.append(1 if cat == 'Tumor' else 0)
        else:
            dropped_indices.append(gsm_id)
            
    if dropped_indices:
        print(f"Aviso: Se descartaron {len(dropped_indices)} muestras sin categoría verificada.")
        study_matrix = study_matrix.drop(index=dropped_indices)
        
    study_matrix.insert(0, 'Target', labels)
    
    # Exportar a Parquet
    os.makedirs('results/normalized', exist_ok=True)
    parquet_out = f'results/normalized/{gse_id}.parquet'
    study_matrix.columns = study_matrix.columns.astype(str)
    study_matrix.to_parquet(parquet_out, compression='snappy')
    print(f"¡ÉXITO! Se generó el Tensor Multi-Ómico en: {parquet_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingesta manual de conteos crudos RNA-seq")
    parser.add_argument("--gse", type=str, required=True, help="El ID oficial del estudio (e.g. GSE161369)")
    parser.add_argument("--file", type=str, required=True, help="Ruta al archivo TXT/CSV con los conteos RAW")
    args = parser.parse_args()
    
    ingest_manual_rna(args.gse, args.file)
