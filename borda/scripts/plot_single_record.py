import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

def plot_single_record():
    path_real = 'results/elite_borda_training_table.parquet'
    path_synth = 'results/synthetic_samples_elite_borda_5000.parquet'
    
    if not os.path.exists(path_real) or not os.path.exists(path_synth):
        print("❌ Error: Faltan los archivos de datos real o sintéticos.")
        return
        
    df_real = pd.read_parquet(path_real)
    df_synth = pd.read_parquet(path_synth)
    
    # Identificar columna de target
    target_col = 'Category' if 'Category' in df_real.columns else 'target'
    
    # Extraer sólo genes
    meta_cols = ['GSE_ID', target_col, 'Technology_Label']
    genes = [c for c in df_real.columns if c not in meta_cols]
    
    # Tomar el primer paciente de tipo Tumor (Target = 1) de cada dataset
    real_patient = df_real[df_real[target_col] == 1.0].iloc[0][genes].values.astype(float)
    synth_patient = df_synth[df_synth[target_col] == 1.0].iloc[0][genes].values.astype(float)
    
    # Seleccionamos los primeros 50 genes para una visualización limpia
    n_genes_to_plot = 50
    genes_subset = genes[:n_genes_to_plot]
    real_profile = real_patient[:n_genes_to_plot]
    synth_profile = synth_patient[:n_genes_to_plot]
    
    # Generar el gráfico de perfil
    plt.figure(figsize=(14, 6))
    plt.plot(genes_subset, real_profile, label='Paciente Real (GEO)', color='#1f77b4', linewidth=2.5, marker='o')
    plt.plot(genes_subset, synth_profile, label='Paciente Sintético (Forest Diffusion)', color='#ff7f0e', linewidth=2, linestyle='--', marker='x')
    
    plt.title('Perfil de Expresión Génica (Primeros 50 Genes): Paciente Real vs Clon Sintético', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Identificador del Gen', fontsize=11, fontweight='bold')
    plt.ylabel('Nivel de Expresión (Log2 Normalizado)', fontsize=11, fontweight='bold')
    plt.xticks(rotation=90, fontsize=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    
    os.makedirs('results/metrics', exist_ok=True)
    output_png = 'results/metrics/comparativa_registro_paciente.png'
    plt.savefig(output_png, dpi=300)
    plt.close()
    
    print(f"✅ ¡Gráfica de perfil de registro completada con éxito!")
    print(f"   Real patient mean: {real_profile.mean():.3f} | Synth patient mean: {synth_profile.mean():.3f}")
    print(f"   Imagen guardada en: {output_png}")

if __name__ == "__main__":
    plot_single_record()
