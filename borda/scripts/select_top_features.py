import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
import os
import time

def main():
    print("============================================================")
    print("  Feature Selection: Top 200 Genes SOTA")
    print("============================================================")

    # 1. Cargar el dataset maestro
    input_path = 'results/master_training_table.parquet'
    output_path = 'results/lite_training_table.parquet'
    
    print(f"\n🚀 Leyendo dataset maestro desde: {input_path}")
    df = pd.read_parquet(input_path)
    
    print(f"   📐 Dataset cargado: {df.shape[0]:,} muestras × {df.shape[1]:,} columnas")
    
    # Identificar metadata (excluirla del ranking de genes)
    metadata_cols = ['GSE_ID', 'Technology_Label', 'Category']
    gene_cols = [c for c in df.columns if c not in metadata_cols]
    
    print(f"\n🧬 Separando {len(gene_cols)} genes para evaluación...")

    X = df[gene_cols].to_numpy()
    y = df['Category'].to_numpy()
    
    # 2. Entrenar modelo rápido para obtener la importancia de los features
    print(f"⏳ Entrenando XGBClassifier para evaluar el poder predictivo de los genes...")
    start_time = time.time()
    
    # Usamos tree_method='hist' para máxima velocidad en CPU/Mac
    model = XGBClassifier(
        n_estimators=100, 
        max_depth=6, 
        learning_rate=0.1, 
        tree_method='hist',
        n_jobs=-1,
        random_state=42
    )
    
    model.fit(X, y)
    
    print(f"   ✅ Evaluación completada en {time.time() - start_time:.1f} segundos.")
    
    # 3. Extraer los mejores genes
    importances = model.feature_importances_
    
    # Crear un DataFrame con los genes y sus importancias
    feature_imp_df = pd.DataFrame({
        'Gene': gene_cols,
        'Importance': importances
    })
    
    # Ordenar y tomar los Top 200
    top_200_genes = feature_imp_df.sort_values(by='Importance', ascending=False).head(200)['Gene'].tolist()
    
    print("\n🏆 Top 5 Genes más importantes encontrados:")
    for i, gene in enumerate(top_200_genes[:5]):
        print(f"   {i+1}. {gene}")
        
    # 4. Crear y guardar el nuevo dataset Lite
    print(f"\n💾 Creando dataset Lite con metadata + 200 genes estrella...")
    
    # Mantener el orden: metadata primero, luego los 200 genes seleccionados
    lite_cols = [c for c in metadata_cols if c in df.columns] + top_200_genes
    df_lite = df[lite_cols].copy()
    
    df_lite.to_parquet(output_path, engine='pyarrow')
    
    lite_size_mb = os.path.getsize(output_path) / 1e6
    print(f"🎉 ¡Dataset Lite creado con éxito!")
    print(f"   📦 Ruta: {output_path}")
    print(f"   📐 Dimensiones: {df_lite.shape[0]:,} muestras × {df_lite.shape[1]:,} columnas")
    print(f"   ⚖️  Peso: {lite_size_mb:.1f} MB (Mucho más rápido de subir y procesar)")

if __name__ == '__main__':
    main()
