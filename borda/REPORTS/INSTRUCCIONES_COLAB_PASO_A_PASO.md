# Guía Paso a Paso: Ejecución de Experimentos en Google Colab con GPU

Esta guía describe detalladamente cada paso para ejecutar la generación masiva de 120,000 muestras y evaluar las métricas definitivas utilizando tus créditos de GPU en Google Colab.

---

## Paso 1: Subir archivos a Google Drive

Para comenzar, debes subir la carpeta completa de tu proyecto (`datasets`) a la raíz de tu Google Drive. Asegúrate de tener la siguiente estructura en tu Drive:

*   `/My Drive/datasets/results/elite_borda_training_table.parquet` (El dataset real)
*   `/My Drive/datasets/scripts/train_fd_colab.py` (Script de entrenamiento FD)
*   `/My Drive/datasets/scripts/train_ctgan_colab.py` (Script de entrenamiento CTGAN)
*   `/My Drive/datasets/scripts/generate_low_memory.py` (Script de generación)
*   `/My Drive/datasets/scripts/run_modern_benchmark_elite.py` (Script de Benchmarks)
*   `/My Drive/datasets/scripts/evaluate_edwin_hypothesis.py` (Validación de Edwin)
*   `/My Drive/datasets/scripts/analyze_borda_feature_importance.py` (Fidelidad Jaccard)

---

## Paso 2: Configurar Google Colab

1.  Abre [Google Colab](https://colab.research.google.com/).
2.  Crea un nuevo cuaderno vacío (**Archivo > Bloc de notas nuevo**).
3.  Cambia el entorno a GPU de alto rendimiento:
    *   Ve al menú **Entorno de ejecución > Cambiar tipo de entorno de ejecución**.
    *   En **Acelerador de hardware**, selecciona **GPU A100** (para máxima velocidad y evitar desconexiones).
    *   En **Perfil de entorno de ejecución**, selecciona **High-RAM**.
    *   Haz clic en **Guardar**.

---

## Paso 3: Ejecución de Celdas en el Cuaderno de Colab

Crea y ejecuta una celda de código para cada uno de los siguientes pasos:

### 📦 Celda 1: Montar Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')

# Ir a la carpeta de trabajo en Drive
%cd /content/drive/MyDrive/datasets/
```

### 🧹 Celda 2: Instalar dependencias requeridas
```bash
!pip install xgboost joblib pandas pyarrow ctgan tabpfn matplotlib seaborn scikit-learn tqdm
```

### 🧹 Celda 3: Limpiar checkpoints anteriores (Seguridad)
```bash
# Limpiar cascarones y carpetas viejas de pilotos para evitar conflictos
!rm -rf results/checkpoints/steps_elite_borda/
!rm -f results/checkpoints/fd_shell_elite_borda.joblib
```

### 🌲 Celda 4: Entrenar el modelo Forest Diffusion
Este comando iniciará el entrenamiento del modelo generativo sobre los 1,000 genes Borda de los 9,309 pacientes.
```bash
!python -u scripts/train_fd_colab.py \
    --dataset elite_borda \
    --n_t 50 \
    --device cuda \
    --mode train \
    --data_subpath datasets/results/elite_borda_training_table.parquet \
    --checkpoint_subpath datasets/results/checkpoints
```
*Tiempo estimado en A100:* **~12 minutos**.

### 🤖 Celda 5: Entrenar el modelo de Línea de Base CTGAN
Este comando entrena la red neuronal generativa adversaria para tener una línea de base clásica.
```bash
!python -u scripts/train_ctgan_colab.py \
    --epochs 100 \
    --batch_size 500 \
    --data_subpath datasets/results/elite_borda_training_table.parquet \
    --output_dir datasets/results
```
*Tiempo estimado en A100:* **~10 minutos**.

### 🎲 Celda 6: Generación Definitiva de 120,000 Pacientes Sintéticos (Forest Diffusion)
Generamos la cohorte masiva definitiva utilizando la integración de Euler optimizada.
```bash
!python -u scripts/generate_low_memory.py \
    --dataset elite_borda \
    --n_samples 120000 \
    --n_t 50
```
*Tiempo estimado:* **~8 minutos** en GPU de Colab.
*Salida:* `results/synthetic_samples_elite_borda_120000.parquet`.

### 🎲 Celda 7: Generación Definitiva de 120,000 Pacientes Sintéticos (CTGAN)
Generamos las muestras para el modelo de comparación clásica.
```python
import joblib
import pandas as pd
import os

print("🎲 Generando muestras con CTGAN...")
model_path = 'results/ctgan_model_elite_borda.pkl'
output_path = 'results/synthetic_samples_ctgan_elite_borda_120000.parquet'

model = joblib.load(model_path)
synthetic_df = model.sample(120000)

# Asegurar tipo de datos de Category y Label
for col in ['Technology_Label', 'Category']:
    if col in synthetic_df.columns:
        synthetic_df[col] = synthetic_df[col].round().clip(0, 1).astype(int)

synthetic_df.to_parquet(output_path)
print(f"✅ Completado. Guardado en {output_path}")
```

### 📊 Celda 8: Ejecutar la Explicabilidad Post-Entrenamiento (Fidelidad Jaccard)
Calculamos la similitud Jaccard de los 50 biomarcadores más importantes entre la data Real y la data Sintética definitiva de 120k.
```bash
!python scripts/analyze_borda_feature_importance.py \
    --real_path results/elite_borda_training_table.parquet \
    --synth_path results/synthetic_samples_elite_borda_120000.parquet
```
*Esto actualizará el gráfico `results/metrics/biomarcadores_preservados_heatmap.png`.*

### 🔀 Celda 9: Ejecutar la Validación de la Hipótesis de Edwin
Validamos la hipótesis de sinergia cruzada con el dataset masivo definitivo.
```bash
!python scripts/evaluate_edwin_hypothesis.py \
    --real_path results/elite_borda_training_table.parquet \
    --synth_path results/synthetic_samples_elite_borda_120000.parquet
```
*Esto actualizará el gráfico `results/metrics/validacion_hipothesis_edwin.png` y el CSV `results/metrics/edwin_hypothesis_results.csv`.*

### 🏆 Celda 10: Ejecutar el Benchmark SOTA de Clasificadores (TSTR)
Evaluamos XGBoost, CatBoost, TabPFN, SVM y RF entrenados con la data sintética de 120,000 muestras frente a test real.
```bash
!python scripts/run_modern_benchmark_elite.py \
    --real_path results/elite_borda_training_table.parquet \
    --synth_path results/synthetic_samples_elite_borda_120000.parquet
```
*Salida:* `results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv`.

---

## Paso 4: Descarga de Resultados a tu Computadora Local

Una vez finalizado, puedes descargar los archivos resultantes desde tu Google Drive para incluirlos en tu tesis doctoral:

1.  **Gráfica Jaccard:** `/datasets/results/metrics/biomarcadores_preservados_heatmap.png`
2.  **Gráfica Hipótesis de Edwin:** `/datasets/results/metrics/validacion_hipothesis_edwin.png`
3.  **Resultados Edwin (.csv):** `/datasets/results/metrics/edwin_hypothesis_results.csv`
4.  **Resultados del Benchmark TSTR (.csv):** `/datasets/results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv`
