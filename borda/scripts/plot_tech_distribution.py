import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de estilo
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#121212", "figure.facecolor": "#121212", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})

def create_tech_plots():
    print("Generando visualización de estructura de datos...")
    
    try:
        # Cargar los datos validados
        df = pd.read_csv('results/verified_samples.csv')
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return

    # Datos oficiales unificados y limpios (Datalake Harmonizado)
    categories = ['Microarray', 'RNA-seq']
    patient_values = [1463, 26585]  # Total: 28,048 limpios
    dataset_values = [249, 33]     # Total: 282 independientes
    
    # Crear la figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#121212')
    
    # Colores SOTA: Rojo para Microarray (Legacy), Azul para RNA-seq (Moderno)
    colors = ['#FF4B4B', '#4B4BFF']
    
    # Subplot 1: Cantidad de Pacientes (Limpio)
    bars1 = ax1.bar(categories, patient_values, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
    ax1.set_title('Volumen de Pacientes por Tecnología\n(N = 41,202 brutos → 28,048 limpios)', fontsize=14, pad=15, color='white', weight='bold')
    ax1.set_ylabel('Número de Muestras (Pacientes)', fontsize=12)
    
    # Añadir etiquetas de valor
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{int(height):,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='white', weight='bold', fontsize=11)

    # Subplot 2: Cantidad de Datasets (Estudios)
    bars2 = ax2.bar(categories, dataset_values, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
    ax2.set_title('Estudios Clínicos Integrados\n(N = 282 Datasets Independientes)', fontsize=14, pad=15, color='white', weight='bold')
    ax2.set_ylabel('Número de Datasets (GSE)', fontsize=12)
    
    # Añadir etiquetas de valor
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='white', weight='bold', fontsize=11)

    plt.tight_layout()
    
    # Guardar el gráfico
    output_path = 'results/ESTRUCTURA_CORPUS_MULTIPLATAFORMA.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#121212')
    print(f"✅ Gráfico guardado en {output_path}")

if __name__ == "__main__":
    create_tech_plots()
