import pandas as pd
import numpy as np
import os

def audit_quality():
    master_path = 'results/master_training_table.parquet'
    if not os.path.exists(master_path):
        print("❌ Error: Master Table no encontrada.")
        return

    print(f"🔍 Iniciando auditoría profunda de {master_path}...")
    df = pd.read_parquet(master_path)
    
    # 1. Análisis Global de Ceros/Nulos
    total_cells = df.size
    total_zeros = (df == 0).sum().sum()
    total_nans = df.isnull().sum().sum()
    
    print("\n--- RESUMEN GLOBAL ---")
    print(f"Total de Filas: {len(df)}")
    print(f"Total de Columnas: {len(df.columns)}")
    print(f"Porcentaje de Ceros: {(total_zeros/total_cells)*100:.2f}%")
    print(f"Porcentaje de NaNs: {(total_nans/total_cells)*100:.2f}%")

    # 2. Análisis por Estudio (GSE)
    print("\n--- ANÁLISIS POR ESTUDIO (Top 10 más 'vacíos') ---")
    # Ignoramos columnas de metadatos para el conteo de genes
    gene_cols = df.drop(columns=['GSE_ID', 'Technology_Label', 'Category']).columns
    
    sparsity_per_study = []
    for gse_id, group in df.groupby('GSE_ID'):
        gene_data = group[gene_cols]
        zeros_in_study = (gene_data == 0).sum().sum()
        total_cells_study = gene_data.size
        sparsity = (zeros_in_study / total_cells_study) * 100
        sparsity_per_study.append({'GSE_ID': gse_id, 'Sparsity_Pct': sparsity, 'Samples': len(group)})
    
    sparsity_df = pd.DataFrame(sparsity_per_study).sort_values('Sparsity_Pct', ascending=False)
    print(sparsity_df.head(20))

    # 3. Análisis por Gen (Genes con más ceros)
    print("\n--- ANÁLISIS POR GEN (Genes con menor cobertura) ---")
    gene_sparsity = (df[gene_cols] == 0).sum() / len(df) * 100
    print(gene_sparsity.sort_values(ascending=False).head(20))

    # 4. Verificación de Rango de Valores
    print("\n--- RANGO DE EXPRESIÓN (Excluyendo ceros) ---")
    non_zero_values = df[gene_cols].values[df[gene_cols].values > 0]
    if len(non_zero_values) > 0:
        print(f"Mínimo: {non_zero_values.min():.4f}")
        print(f"Máximo: {non_zero_values.max():.4f}")
        print(f"Media: {non_zero_values.mean():.4f}")
    else:
        print("⚠️ ALERTA: No se encontraron valores mayores a cero en los genes.")

    # Guardar reporte detallado
    sparsity_df.to_csv('results/sparsity_audit_report.csv', index=False)
    print(f"\n✅ Reporte detallado guardado en results/sparsity_audit_report.csv")

if __name__ == "__main__":
    audit_quality()
