import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import os

# Configuración de estilo Dark Mode
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#121212", "figure.facecolor": "#121212", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})

def plot_auc_explanation():
    # Simulamos probabilidades de predicción de un modelo bastante bueno (AUC ~ 0.95)
    np.random.seed(42) # Para que siempre salga igual
    
    # Pacientes Sanos (clase 0): El modelo predice probabilidades bajas de tener cáncer
    normal_probs = np.random.normal(loc=0.2, scale=0.15, size=1000)
    normal_probs = np.clip(normal_probs, 0, 1)
    
    # Pacientes con Tumor (clase 1): El modelo predice probabilidades altas de tener cáncer
    tumor_probs = np.random.normal(loc=0.8, scale=0.15, size=1000)
    tumor_probs = np.clip(tumor_probs, 0, 1)
    
    y_true = np.array([0]*1000 + [1]*1000)
    y_scores = np.concatenate([normal_probs, tumor_probs])
    
    # Crear la figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#121212')
    
    # GRÁFICO 1: Las dos distribuciones (Sanos vs Tumores)
    sns.kdeplot(normal_probs, fill=True, color="#4B4BFF", label="Pacientes Sanos (Real)", ax=ax1, linewidth=2)
    sns.kdeplot(tumor_probs, fill=True, color="#FF4B4B", label="Pacientes con Tumor (Real)", ax=ax1, linewidth=2)
    
    # Línea de umbral en 0.5
    threshold = 0.5
    ax1.axvline(x=threshold, color='white', linestyle='--', lw=2, label=f'Umbral Médico Clásico ({threshold})')
    
    ax1.set_title('Paso 1: ¿Qué tan bien separa el modelo a los sanos de los enfermos?', fontsize=14, color='white', weight='bold', pad=15)
    ax1.set_xlabel('Probabilidad (Score) asignada por el Modelo', fontsize=12)
    ax1.set_ylabel('Cantidad de Pacientes', fontsize=12)
    ax1.legend(loc="upper center")
    
    # Textos didácticos
    ax1.text(0.85, 2.0, "Verdaderos Positivos\n(TP: Detectó el Cáncer)", color='#FF4B4B', ha='center', fontsize=10, weight='bold')
    ax1.text(0.15, 2.0, "Verdaderos Negativos\n(TN: Confirmó Salud)", color='#4B4BFF', ha='center', fontsize=10, weight='bold')
    
    # Sombrear errores (Falsos Positivos y Falsos Negativos)
    # No es trivial sombrear solapes exactos en KDE, así que ponemos texto.
    ax1.text(0.4, 0.5, "Falsos Positivos (Sanos alarmados)", color='white', ha='center', fontsize=9, rotation=45)
    ax1.text(0.6, 0.5, "Falsos Negativos (Cáncer ignorado)", color='white', ha='center', fontsize=9, rotation=-45)

    # GRÁFICO 2: La Curva ROC (que resume el Gráfico 1)
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    # Dibujar curva ROC
    ax2.plot(fpr, tpr, color='#00FF00', lw=3, label=f'Curva ROC del Modelo (AUC = {roc_auc:.3f})')
    
    # Dibujar línea base (al azar)
    ax2.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Tirar una moneda (AUC = 0.50)')
    
    # Rellenar el área bajo la curva (¡ESTO ES EL AUC!)
    ax2.fill_between(fpr, tpr, alpha=0.15, color='#00FF00', label='Área Bajo la Curva (AUC)')
    
    # Marcar dónde cae el umbral de 0.5 en la curva ROC
    idx = np.argmin(np.abs(thresholds - threshold))
    ax2.plot(fpr[idx], tpr[idx], marker='o', markersize=10, color='white', 
             label=f'Punto exacto si cortas en {threshold} de probabilidad')
    
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('Tasa de Falsos Positivos (Errores: Sano diagnosticado como Cáncer)', fontsize=11)
    ax2.set_ylabel('Tasa de Verdaderos Positivos (Éxitos: Cáncer detectado)', fontsize=11)
    ax2.set_title('Paso 2: La Curva ROC y su Área (AUC)', fontsize=14, color='white', weight='bold', pad=15)
    ax2.legend(loc="lower right")
    
    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/EXPLICACION_AUC.png', dpi=300, bbox_inches='tight', facecolor='#121212')
    print("Gráfico didáctico generado en results/EXPLICACION_AUC.png")

if __name__ == "__main__":
    plot_auc_explanation()
