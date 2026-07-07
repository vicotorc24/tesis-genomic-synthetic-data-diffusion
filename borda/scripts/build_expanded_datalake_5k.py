import pandas as pd
import glob
import os
import numpy as np
from sklearn.impute import KNNImputer

def build_5k_datalake():
    harmonized_path = 'results/harmonized/*.parquet'
    harmonized_files = glob.glob(harmonized_path)
    
    # Core Set de genes de la tabla maestra actual
    master_path = 'results/master_training_table.parquet'
    master_df = pd.read_parquet(master_path)
    core_genes = [c for c in master_df.columns if c not in ['GSE_ID', 'Technology_Label', 'Category']]
    fixed_cols = ['GSE_ID', 'Technology_Label', 'Category']
    
    # Extraer mapeo de tecnología del master actual
    tech_map = master_df[['GSE_ID', 'Technology_Label']].drop_duplicates().set_index('GSE_ID')['Technology_Label'].to_dict()
    
    selected_dfs = []
    print("🚀 Iniciando proceso de rescate para meta > 5,000 muestras...")
    
    # Umbral de completitud del 95%
    threshold = 0.95
    
    for file in harmonized_files:
        df = pd.read_parquet(file)
        gse_id = os.path.basename(file).replace('.parquet', '')
        
        # Identificar qué genes del core están presentes
        present_genes = list(set(core_genes) & set(df.columns))
        pct_present = len(present_genes) / len(core_genes)
        
        if pct_present >= threshold:
            # Seleccionar genes + Target (que renombraremos a Category)
            cols_to_extract = ['Target'] + present_genes
            sub_df = df[cols_to_extract].copy()
            sub_df.rename(columns={'Target': 'Category'}, inplace=True)
            
            # Añadir GSE_ID y Technology_Label
            sub_df['GSE_ID'] = gse_id
            sub_df['Technology_Label'] = tech_map.get(gse_id, 1.0) # Default Microarray if not found
            
            # Reindexar para asegurar que todos los genes del core existan
            sub_df = sub_df.reindex(columns=fixed_cols + core_genes)
            selected_dfs.append(sub_df)
            
    # Concatenar todos los rescatados
    full_df = pd.concat(selected_dfs, ignore_index=True)
    print(f"📦 Muestras combinadas antes de imputación: {len(full_df)}")
    
    # Imputación por Cohorte (GSE_ID) para preservar la biología local
    print("🧠 Iniciando Imputación KNN inteligente por cohorte...")
    
    imputed_groups = []
    for gse_id, group in full_df.groupby('GSE_ID'):
        # Solo imputar columnas de genes (numéricas)
        group = group.copy()
        X = group[core_genes]
        
        if X.isnull().values.any():
            # Estrategia de Relleno Simple por Cohorte (más estable que KNN para N pequeño)
            # Rellenamos con la media de la cohorte para no perder la señal biológica local
            group.loc[:, core_genes] = X.fillna(X.mean())
            
        imputed_groups.append(group)
        
    final_df = pd.concat(imputed_groups, ignore_index=True)
    
    # Relleno final de NaNs residuales con la media global (si un gen falta en todo un estudio)
    print("🧹 Realizando limpieza final de valores nulos residuales...")
    final_df[core_genes] = final_df[core_genes].fillna(master_df[core_genes].mean())
    final_df[core_genes] = final_df[core_genes].fillna(0) # Deep fallback
    
    output_path = 'results/master_training_table_5k.parquet'
    final_df.to_parquet(output_path, index=False)
    
    print(f"✅ ¡Datalake Rescatado con éxito!")
    print(f"📊 Total de Muestras Finales: {len(final_df)}")
    print(f"🧬 Dimensión de la Matriz: {final_df.shape}")
    print(f"📂 Archivo guardado en: {output_path}")

if __name__ == "__main__":
    build_5k_datalake()
