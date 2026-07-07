# Guía Oficial: Entrenamiento de Modelos Generativos (Forest Diffusion & CTGAN) en Google Colab

**Investigador:** Gary Velásquez Narro  
**Actualización:** Junio 2026

Esta guía detalla los pasos para entrenar tanto el modelo generativo final **Forest Diffusion (Sinergia)** como el modelo de línea de base **CTGAN** en Google Colab, utilizando la cohorte Élite unificada de **9,309 pacientes** y **1,000 genes**.

---

## 1. Requisitos de Google Drive

Asegúrate de tener la siguiente estructura de archivos en tu Drive (ruta recomendada: `/MyDrive/tesis_genetica/`):

| Ruta en Drive | Archivo | Descripción |
| :--- | :--- | :--- |
| `datasets/results/` | `elite_borda_training_table.parquet` | Dataset real de 9,309 pacientes (limpio y saneado). |
| `datasets/scripts/` | `train_fd_colab.py` | Script optimizado para entrenar Forest Diffusion. |
| `datasets/scripts/` | `train_ctgan_colab.py` | Script optimizado para entrenar CTGAN. |

---

## 2. Configuración Inicial en Colab

Abre un nuevo cuaderno en Google Colab, asegúrate de activar el entorno de ejecución con GPU (menú **Entorno de ejecución > Cambiar tipo de entorno de ejecución > GPU T4 o A100**) y ejecuta las siguientes celdas iniciales:

### 📦 CELDA 1: Montar Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')

# Ir al directorio de trabajo en Drive
%cd /content/drive/MyDrive/tesis_genetica/
```

### 🧹 CELDA 2: Limpieza de Historial de Diffusion (CRÍTICO)
Debido a que el nuevo modelo entrena incluyendo la variable `Category` (1,001 características en total), es obligatorio borrar los checkpoints antiguos del modelo anterior para evitar un error de dimensiones (`IndexError`):

```bash
# Eliminar carpeta de checkpoints y cascarón de Forest Diffusion antiguo
!rm -rf datasets/results/checkpoints/steps_elite_borda/
!rm -f datasets/results/checkpoints/fd_shell_elite_borda.joblib
```

### 🔧 CELDA 3: Instalar Dependencias
```bash
!pip install xgboost joblib pandas pyarrow ctgan
```

---

## 3. Entrenamiento SOTA: Forest Diffusion

Ejecuta el comando para entrenar los 50 pasos de difusión. El script guardará automáticamente cada paso entrenado en tu Drive:

```bash
!python -u datasets/scripts/train_fd_colab.py \
    --dataset elite_borda \
    --n_t 50 \
    --device cuda \
    --mode both \
    --data_subpath datasets/results/elite_borda_training_table.parquet \
    --checkpoint_subpath datasets/results/checkpoints
```

*   **Modelo Resultante:** `datasets/results/checkpoints/forest_diffusion_model_elite_borda.joblib`
*   **Muestras Sintéticas:** `datasets/results/synthetic_samples_elite_borda_5000.parquet`
*   **Tiempo estimado:** ~12 mins en A100 | ~45 mins en T4.

---

## 4. Entrenamiento de Línea de Base: CTGAN

Para comparar el rendimiento de Forest Diffusion con modelos clásicos decadales, ejecuta el entrenamiento de CTGAN durante 100 épocas en GPU:

```bash
!python -u datasets/scripts/train_ctgan_colab.py \
    --epochs 100 \
    --batch_size 500 \
    --data_subpath datasets/results/elite_borda_training_table.parquet \
    --output_dir datasets/results
```

*   **Modelo Resultante:** `datasets/results/ctgan_model_elite_borda.pkl`
*   **Muestras Sintéticas:** `datasets/results/synthetic_samples_ctgan_elite_borda_5000.parquet`
*   **Tiempo estimado:** ~10 mins en A100 | ~35 mins en T4.

---

## 💡 Soporte contra Desconexiones
Si Colab te desconecta a mitad de la sesión:
1.  **Para Forest Diffusion:** Vuelve a ejecutar las celdas 1, 3 y la de entrenamiento. El script detectará los checkpoints guardados en Drive y **reanudará automáticamente** desde donde se quedó.
2.  **Para CTGAN:** Vuelve a ejecutar las celdas y corre el entrenamiento. CTGAN no tiene guardado por checkpoints nativo, por lo que iniciará desde cero (al durar poco en GPU, esto no suele ser un problema).
