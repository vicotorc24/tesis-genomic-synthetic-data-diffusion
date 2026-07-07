import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, entropy
import os

def calculate_metafeatures(df, target_col='target', dataset_name='dataset_2026'):
    """Replicación exacta del motor de 40 meta-atributos de 2021."""
    # Asegurar que solo procesamos columnas numéricas (genes)
    X = df.drop(columns=[target_col], errors='ignore').select_dtypes(include=[np.number])
    y = df[target_col] if target_col in df.columns else pd.Series([0]*len(df))
    
    N, P = X.shape
    print(f"   - Procesando {N} muestras y {P} atributos...")
    
    # 1. Correlación (Muestreo para velocidad si es muy grande, pero aquí procesamos todo)
    corr_matrix = X.corr().values
    corr_tri = corr_matrix[np.triu_indices(P, k=1)]
    
    # 2. Covarianza
    cov_matrix = X.cov().values
    cov_tri = cov_matrix[np.triu_indices(P, k=1)]
    
    # 3. Distribución
    stds = X.std()
    skews = skew(X, axis=0, nan_policy='omit')
    kurts = kurtosis(X, axis=0, nan_policy='omit')
    var_coefs = stds / X.mean().replace(0, np.nan)
    
    # 4. Entropía
    class_counts = y.value_counts(normalize=True)
    class_entropy = entropy(class_counts) if len(class_counts) > 1 else 0
    
    meta = {
        'dataset': dataset_name,
        'X_correlation_max': np.nanmax(corr_tri),
        'X_correlation_mean': np.nanmean(corr_tri),
        'X_correlation_min': np.nanmin(corr_tri),
        'X_covariance_max': np.nanmax(cov_tri),
        'X_covariance_mean': np.nanmean(cov_tri),
        'X_covariance_min': np.nanmin(cov_tri),
        'X_kurtosis_max': np.nanmax(kurts),
        'X_kurtosis_mean': np.nanmean(kurts),
        'X_kurtosis_min': np.nanmin(kurts),
        'X_skewness_max': np.nanmax(skews),
        'X_skewness_mean': np.nanmean(skews),
        'X_skewness_min': np.nanmin(skews),
        'X_stand_dev_max': stds.max(),
        'X_stand_dev_mean': stds.mean(),
        'X_stand_dev_min': stds.min(),
        'X_var_coef_max': var_coefs.max(),
        'X_var_coef_mean': var_coefs.mean(),
        'X_var_coef_min': var_coefs.min(),
        'X_num_attrs_none': P,
        'X_num_obs_none': N,
        'X_ratio_obs_attrs_none': N/P,
        'y_norm_class_entropy_none': class_entropy,
        'y_num_classes_none': len(np.unique(y))
    }
    
    return pd.DataFrame([meta])

def load_2021_txt(path):
    """Cargador final corregido: Genes en filas, Muestras en columnas."""
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # Fila 1: Labels de las muestras (ej. 102 valores)
    labels = [int(x) for x in lines[1].strip().split()]
    
    # Filas 2+: Cada fila es un GEN (2000 filas)
    data_matrix = []
    gene_names = []
    for i, line in enumerate(lines[2:]):
        vals = [float(x) for x in line.strip().split()]
        data_matrix.append(vals)
        gene_names.append(f"Gene_{i+1}")
    
    # Convertimos a DataFrame: Inicialmente es (2000 genes x 102 muestras)
    # Lo transponemos para tener (102 muestras x 2000 genes)
    df = pd.DataFrame(data_matrix, index=gene_names).T
    df['target'] = labels
    return df

if __name__ == "__main__":
    os.makedirs('results', exist_ok=True)
    all_results = []
    
    # 1. Procesamiento masivo de los 60 datasets históricos (2021)
    base_path = 'REPORTS/documentos_tesis/microarray-data/'
    if os.path.exists(base_path):
        files = [f for f in os.listdir(base_path) if f.endswith('.txt')]
        print(f"📉 Iniciando extracción masiva de {len(files)} datasets históricos...")
        
        for i, filename in enumerate(sorted(files)):
            path = os.path.join(base_path, filename)
            print(f"   [{i+1}/{len(files)}] Procesando: {filename}")
            try:
                df_old = load_2021_txt(path)
                res = calculate_metafeatures(df_old, dataset_name=filename.replace('.txt', ''))
                all_results.append(res)
            except Exception as e:
                print(f"   ⚠️ Error en {filename}: {e}")
    
    # 2. Modernización: Aplicar al Datalake 2026
    path_2026 = 'results/elite_borda_training_table.parquet'
    if os.path.exists(path_2026):
        print(f"\n🚀 Extrayendo meta-atributos del Datalake 2026...")
        df_2026 = pd.read_parquet(path_2026)
        # Limpiar metadatos
        df_2026 = df_2026.drop(columns=['GSE_ID', 'Technology_Label'], errors='ignore')
        res_2026 = calculate_metafeatures(df_2026, target_col='Category', dataset_name='DATALAKE_2026')
        all_results.append(res_2026)
        
    # Guardar resultados consolidados
    if all_results:
        final_df = pd.concat(all_results)
        output_path = 'results/MASTER_METAFEATURES_2021_2026.csv'
        final_df.to_csv(output_path, index=False)
        print(f"\n✅ Extracción completa: {len(final_df)} registros guardados en {output_path}")
    else:
        print("❌ No se generaron resultados.")
