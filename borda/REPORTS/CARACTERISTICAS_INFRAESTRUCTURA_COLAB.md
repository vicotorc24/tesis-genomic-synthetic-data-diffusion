# Ficha Técnica de Infraestructura y Cómputo (Google Colab GPU)

Este documento detalla el perfil de hardware, software y rendimiento optimizado para el entrenamiento a gran escala del modelo **Forest Diffusion** (9,309 pacientes × 1,000 genes Borda) y la generación definitiva de 120,000 muestras sintéticas. Es ideal para ser integrado en el **Capítulo de Metodología e Infraestructura** de la tesis.

---

## 1. Perfil de Hardware Recomendado vs. Alternativo

| Componente | Opción Recomendada (A100 High-RAM) | Opción Alternativa (T4 Estándar) |
| :--- | :--- | :--- |
| **GPU** | **NVIDIA A100 Tensor Core** | **NVIDIA T4 Tensor Core** |
| **Memoria VRAM** | 40 GB HBM2 | 16 GB GDDR6 |
| **Ancho de Banda GPU** | 1.6 TB/s | 320 GB/s |
| **RAM del Sistema** | **51.8 GB (High-RAM)** | 12.7 GB (Estándar RAM) |
| **CPU Cores** | 8 o 12 vCPUs (Intel Xeon / AMD EPYC) | 2 vCPUs (Intel Xeon) |
| **Riesgo de OOM (RAM)**| Prácticamente 0% | Alto en generación (120k samples) |
| **Consumo de Créditos**| ~9.2 - 13 créditos/hora | ~1.5 - 2 créditos/hora (o Gratis) |

---

## 2. Métricas de Rendimiento del Entrenamiento (Forest Diffusion)

Estadísticas recopiladas durante las fases piloto y de calibración:

### A. Velocidad por Paso de Difusión ($t$)
*   **En NVIDIA A100:** **~14.4 segundos** por paso.
    *   *Detalle:* Entrena 1,000 XGBoosts en paralelo utilizando el motor GPU Hist.
*   **En NVIDIA T4:** **~72.0 segundos** por paso (5 veces más lento).
    *   *Detalle:* Cuello de botella debido a la menor cantidad de núcleos CUDA y menor ancho de banda de memoria del sistema para el paralelismo de joblib.

### B. Tiempo Total de Ejecución del Pipeline (50 Pasos)
*   **En NVIDIA A100:** **~12 minutos** de entrenamiento neto.
*   **En NVIDIA T4:** **~60 minutos** (1 hora) de entrenamiento neto.

---

## 3. Perfil de Almacenamiento y Checkpoints en Google Drive

Para garantizar la tolerancia a fallos ante desconexiones repentinas de Google Colab, la infraestructura implementa almacenamiento persistente desacoplado en Google Drive bajo las siguientes especificaciones:

*   **Dataset Real de Entrada (`elite_borda_training_table.parquet`):**
    *   *Tamaño:* **~37 MB** en formato Parquet (compresión Snappy).
*   **Cascarón Inicial (`fd_shell_elite_borda.joblib`):**
    *   *Tamaño:* **~20 KB** (inicializa los hiperparámetros y el MinMaxScaler).
*   **Checkpoints de Pasos (`checkpoints/steps_elite_borda/step_t.joblib`):**
    *   *Tamaño:* **~5 MB por paso** (Total de 50 pasos: **~250 MB**).
    *   *Estrategia:* Guardado con `compress=0` (sin compresión) para evitar retardos de CPU en la RAM y asegurar una sincronización inmediata a Drive sin colapsar la cola de I/O.
*   **Modelo Ensamblado Final (`forest_diffusion_model_elite_borda.joblib`):**
    *   *Tamaño:* **~120 MB** (Guardado con `compress=3` para reducir significativamente su peso antes de la descarga local).

---

## 4. Estrategia de Paralelización en Software

*   **Motor Generativo (XGBoost GPU):**
    *   `tree_method='hist'` y `device='cuda'`: Habilita la discretización por histogramas en los núcleos GPU, acelerando el cálculo de gradientes.
    *   `n_jobs=1` por XGBoost individual: Evita conflictos de sobre-suscripción de hilos CPU.
*   **Paralelización de Características (Joblib Parallel):**
    *   `n_jobs=-1` en la envoltura: Lanza el entrenamiento de los 1,000 genes del paso simultáneamente utilizando todos los núcleos virtuales de CPU disponibles en Colab para alimentar eficientemente a la GPU.
*   **Integración de Euler (Generación en Lotes):**
    *   Generación segmentada de la cohorte sintética de 120,000 muestras para evitar picos de uso de memoria RAM que superen el límite físico de la sesión.
