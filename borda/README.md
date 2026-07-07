# Ecosistema de Validación de Tesis: Consenso de Borda (Élite)

Este repositorio contiene los códigos, datos y documentos oficiales que sustentan la investigación sobre la **Aumentación Transcripcional con Modelos de Difusión en el Contexto de Meta-Aprendizaje**. Este espacio ha sido aislado específicamente para facilitar la revisión del Asesor y del Jurado de Tesis.

---

## 📂 Estructura de Directorios

El espacio de trabajo se organiza de la siguiente manera:

*   **`scripts/`**: Algoritmos de entrenamiento, simulación, predicción y graficación.
    *   `run_extreme_audit.py`: Algoritmo de auditoría bioinformática extrema que realiza el filtrado de varianza (>0) sobre el datalake de 28k para aislar la cohorte Élite, además de evaluar el batch effect (Silhouette) y generalización cruzada.
    *   `run_modern_benchmark_elite.py` / `run_modern_benchmark_elite_cpu.py`: Batería de clasificación multi-modelo (TabPFN, XGBoost, CatBoost, etc.) entrenados con TSTR (Train Synthetic, Test Real).
    *   `evaluate_edwin_hypothesis.py`: Validación cruzada pan-cáncer inter-enfermedad y rescate predictivo ante escasez de datos.
    *   `analyze_borda_feature_importance.py`: Extracción y comparación de la importancia Gini de biomarcadores (Real vs. Sintético).
    *   `train_fd_colab.py` / `train_ctgan_colab.py`: Scripts de entrenamiento de los modelos generativos en Google Colab (A100 GPU).
    *   `generate_low_memory.py`: Implementación optimizada de la integración de Euler para la inferencia de difusión en CPU locales (< 2 GB de RAM).
*   **`results/`**: Archivos binarios de pesos de modelos, datasets en formato columnar optimizado y métricas cuantitativas.
    *   `master_training_table.parquet`: Dataset crudo inicial unificado de la cohorte completa (N=28,048).
    *   `elite_borda_training_table.parquet`: Dataset real consolidado de la cohorte Élite (N=9,309) tras aplicar el filtro de varianza.
    *   `synthetic_samples_elite_borda_120000.parquet`: Colección de 120,000 perfiles sintéticos generados por Forest Diffusion.
    *   `forest_diffusion_model_elite_borda.joblib`: Modelo de difusión final entrenado.
    *   `metrics/`: Gráficas y tablas CSV que validan la fidelidad y el desempeño del pipeline.
*   **`REPORTS/`**: Borrador del manuscrito oficial y reportes de calidad.
    *   `documentos_tesis/`: Capítulos del 1 al 6 alineados con el Core Set de 9,309 pacientes.
    *   `documentos_tesis/BORRADOR_TESIS_OFICIAL_ACTUALIZACION.md`: Bloques de texto redactados con estilo técnico doctoral listos para integrar en el documento final.
    *   `PIPELINE_SOTA_2026.md`: Descripción arquitectónica del pipeline de alta dimensionalidad.
*   **`simulador_forest_diffusion.html`**: Simulador web interactivo (diseño premium responsivo) que permite explorar visualmente y jugar con los parámetros del modelo generativo Forest Diffusion.

---

## 🚀 Guía de Ejecución Local

Para reproducir los resultados clave del manuscrito, ejecute los siguientes comandos en su entorno virtual de Python:

### 1. Auditoría Bioinformática Extrema (Generación del Core Set y Calidad)
Para verificar la depuración de las 28,048 muestras a las 9,309 de la cohorte Élite y correr las pruebas de batch effect:
```bash
python scripts/run_extreme_audit.py
```
* **Salidas:** Reporte formal de auditoría guardado en `REPORTS/REPORT_AUDIT_9K_ELITE.md`.

### 2. Validación de la Hipótesis de Sinergia Pan-Cáncer (Transferencia e Inyección Sintética)
Para comprobar cómo los clones sintéticos rescatan el desempeño de clasificadores locales y validar la transferencia biológica inter-órganos, ejecute:
```bash
python scripts/evaluate_edwin_hypothesis.py \
  --real_path results/elite_borda_training_table.parquet \
  --synth_path results/synthetic_samples_elite_borda_120000.parquet
```
* **Salidas:** Resultados detallados de ROC-AUC guardados en `results/metrics/edwin_hypothesis_results.csv` y gráfica guardada en `results/metrics/validacion_hipothesis_edwin.png`.

### 3. Análisis de Preservación de Biomarcadores (Heatmap y Similitud)
Para verificar la coincidencia biológica en la selección de genes utilizando los clasificadores entrenados con datos reales vs. sintéticos:
```bash
python scripts/analyze_borda_feature_importance.py
```
* **Salidas:** Gráfica comparativa de importancia en `results/metrics/biomarcadores_preservados_heatmap.png` y listado de consistencia en `results/metrics/top_15_preserved_biomarkers.csv`.

### 4. Matriz de Benchmarking SOTA
Para entrenar y evaluar el arsenal completo de clasificación (XGBoost, RandomForest, SVM, TabPFN, etc.) bajo la metodología TSTR en CPU:
```bash
python scripts/run_modern_benchmark_elite_cpu.py
```
* **Salidas:** Matriz de desempeño diagnóstica guardada en `results/metrics/MODERN_BENCHMARK_RESULTS_ELITE_2026.csv`.

---

## 🏆 Resumen de Hitos Científicos del Brazo Élite Borda
*   **Fidelidad de Redes Génicas:** El análisis de co-expresión arrojó un **Índice de Jaccard de 0.3158** (24 genes coincidentes en los Top 50), validando que la IA generativa aprende y retiene las rutas de regulación del cáncer.
*   **Rescate de Datos Escasos:** La inyección proporcional de 500 pacientes artificiales incrementa la capacidad diagnóstica en entornos con solo 30 muestras reales, subiendo el AUC de **0.597 a 0.605** en Hígado y de **0.881 a 0.911** en Mama.
*   **Sinergia Global Pan-Cáncer:** El modelo entrenado con datos tumorales de otros órganos diagnosticó la Leucemia con un **ROC-AUC de 0.923**, superando al modelo local entrenado solo con datos reales de leucemia (**0.871**).
