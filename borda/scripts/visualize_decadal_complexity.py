import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os

def generate_complexity_map(csv_path):
    print(f"📊 Cargando Matriz de Meta-atributos: {csv_path}")
    if not os.path.exists(csv_path):
        print(f"❌ Error: No se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # 1. Preparar datos para PCA
    # Seleccionamos solo las métricas numéricas
    features = df.select_dtypes(include=[np.number])
    
    # Manejar posibles NaNs
    features = features.fillna(0)
    
    # Normalización (Z-score)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(features)
    
    # 2. Ejecutar PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(x_scaled)
    
    df['PCA1'] = components[:, 0]
    df['PCA2'] = components[:, 1]
    
    # 3. Visualización Estilo "High-Impact"
    plt.figure(figsize=(12, 8), dpi=150)
    sns.set_style("darkgrid")
    
    # Separar Históricos vs Moderno
    historic = df[df['dataset'] != 'DATALAKE_2026']
    modern = df[df['dataset'] == 'DATALAKE_2026']
    
    # Dibujar la "nube" histórica
    plt.scatter(historic['PCA1'], historic['PCA2'], 
                alpha=0.5, s=70, c='#3498db', edgecolors='white', label='Datasets Históricos (2021)')
    
    # Dibujar el "punto de referencia" moderno
    if not modern.empty:
        plt.scatter(modern['PCA1'], modern['PCA2'], 
            s=500, c='#e74c3c', marker='*', edgecolors='black', linewidths=1.5,
            label='Datalake Armonizado (2026)', zorder=5)
        
        # Anotación para el Datalake
        plt.annotate('DATALAKE ARMONIZADO (2026)\n(Máxima Densidad)', 
                     xy=(modern['PCA1'].values[0], modern['PCA2'].values[0]),
                     xytext=(20, 20), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                     fontsize=10, fontweight='bold', color='#c0392b',
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#e74c3c", alpha=0.9))
    
    # Estética del gráfico
    plt.title("Evolución del Espacio de Complejidad Genómica (2021-2026)", fontsize=18, fontweight='bold', pad=25)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%) - Componente de Firma Genomica", fontsize=13)
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%) - Componente de Densidad Muestral", fontsize=13)
    
    # Añadir cuadrante de "Zona de Estabilidad"
    plt.axvline(x=0, color='grey', linestyle='--', alpha=0.3)
    plt.axhline(y=0, color='grey', linestyle='--', alpha=0.3)
    
    plt.legend(loc='upper right', frameon=True, facecolor='white', framealpha=1, fontsize=11)
    
    # Pie de gráfico académico
    plt.figtext(0.5, -0.05, "Nota: El PCA se calculó sobre 24 meta-atributos estadísticos que definen la 'huella digital' de cada corpus.", 
                ha="center", fontsize=10, style='italic', color='grey')
    
    output_dir = 'results/plots/'
    os.makedirs(output_dir, exist_ok=True)
    output_img = os.path.join(output_dir, 'DECADAL_COMPLEXITY_MAP.png')
    plt.savefig(output_img, bbox_inches='tight')
    print(f"✅ Mapa de complejidad generado: {output_img}")
    plt.close()

if __name__ == "__main__":
    generate_complexity_map('results/MASTER_METAFEATURES_2021_2026.csv')
