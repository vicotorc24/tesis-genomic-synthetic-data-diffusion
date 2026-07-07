# Estrategia Experimental y Metodología (2026)
**Registro Oficial de Decisiones Técnicas para el Benchmarking SOTA**

Este documento funge como evidencia metodológica para la tesis, justificando la estructura de los conjuntos de datos, el flujo de validación cruzada y el marco comparativo entre algoritmos generativos.

---

## 1. Topología del Datalake y Prevención de Fuga de Datos (Data Leakage)

El escalamiento hacia el "Big Data" ha requerido una trazabilidad estricta para garantizar que la generación sintética sea evaluada sin sesgos.

### 1.1. Los Números del Datalake
*   **Datalake Total (Master Table): `28,048` muestras.** Este es el universo concatenado de datos de Microarrays y RNA-seq.
*   **Filtro Operativo:** Durante iteraciones iniciales (pilotos), el log imprimió `26,207` muestras debido a los procesos automáticos de `.dropna()` sobre metadatos incompletos de *Category* o *Technology_Label*. 
*   **Biobanco Armonizado (Master Core Set): `5,358` muestras.** Es el subconjunto de máxima densidad, armonizado perfectamente con 0% de valores faltantes (NaNs) en los 2,500 genes comunes. Representa el espacio más "puro" de la cohorte.

### 1.2. El Muro del TSTR (Train Synthetic, Test Real)
Para la fase de comparación ("El Duelo Justo"), el Master Core Set de 5,358 muestras ha sido dividido bajo una regla inquebrantable de 80/20 estratificada:
1.  **Core Train (4,286 pacientes):** La única porción del mundo que las IAs generativas (CTGAN y Forest Diffusion) tienen permitido ver durante el entrenamiento base.
2.  **Core Test (1,072 pacientes):** Una bóveda criptográfica. Estos pacientes reales están bloqueados. Los algoritmos no pueden aprender de ellos. Su único propósito es servir como "Jurado Imparcial" contra los pacientes sintéticos generados para evaluar la fidelidad diagnóstica.

---

## 2. Marco Experimental: "Los Tres Actos"

Para defender la modernización algorítmica, la tesis se estructura en tres fases demostrativas:

### Acto 1: La Caída del Paradigma 2021 (Prueba de Estrés)
*   **El Experimento:** Lanzar métodos de Machine Learning Clásico (SVM, Random Forest) acompañados de Perturbación Estocástica Lineal (Ruido Blanco) directamente contra la tabla maestra de 28,048 muestras.
*   **El Resultado Demostrado:** Colapso de Generalización. Los métodos antiguos fracasan al intentar modelar las varianzas multimodales (*Batch Effects*) introducidas por las distintas tecnologías de secuenciación masiva.

### Acto 2: "El Duelo Justo" (El Core Set)
*   **El Experimento:** Entrenar CTGAN (Red Neuronal) y Forest Diffusion (Flow Matching SOTA 2025) en igualdad de condiciones sobre el `Core Train` de 4,286 muestras.
*   **Objetivo Científico:** Evaluar qué arquitectura captura mejor la geometría latente (PCA) y las redes interactómicas (Correlaciones) de los tumores en un ambiente purificado. En este terreno estable, CTGAN no sufre colapso de modo destructivo, permitiendo generar métricas de *Baseline* limpias.

### Acto 3: La Verdadera Fortaleza y la "Estrategia Dual" (Escalamiento a 28k)
*   **El Experimento:** Demostrar por qué Forest Diffusion es el estándar absoluto de la bioinformática SOTA frente al "Batch Effect" masivo. Debido a las limitaciones físicas extremas que conlleva entrenar 2,502 características sobre 28,048 pacientes, la experimentación se dividió en una **Estrategia Dual**:
    *   **Brazo Maestro (Fuerza Bruta Computacional):** Forest Diffusion alimentado con la tabla total de 2,502 genes. Este es el experimento definitivo de máxima resolución biológica, procesado en supercomputadoras en la nube (GPU A100).
    *   **Brazo Lite (Feature Selection & Optimización):** Experimento paralelo donde se utiliza Inteligencia Artificial predictiva (`XGBClassifier` con `tree_method='hist'`) para pre-evaluar la matriz y extraer los **Top 200 genes** con mayor *Feature Importance* predictiva respecto a la categoría de la enfermedad. Al reducir la dimensionalidad un 92%, el proceso generativo se ejecuta en fracciones del tiempo en GPUs estándar (T4).
*   **Objetivo Científico:** Demostrar que la inteligencia condicional puede absorber el ruido técnico del *Batch Effect* y esculpir un espacio biológico perfecto, resolviendo el problema del Acto 1. Adicionalmente, el Brazo Lite validará si la calidad generativa se mantiene al concentrarse únicamente en la "señal" genética principal (los 200 genes top), sentando un precedente de optimización para futuros trabajos.

---

## 3. Consideraciones de Infraestructura Computacional
El fracaso en la compilación local de Forest Diffusion (129 horas de procesamiento estancadas en memoria Swap local) sirve como hallazgo tecnológico colateral. El proceso de *Flow Matching* con ensamble de miles de árboles requiere un diseño tolerante a fallos:
1.  **Modelo Maestro (A100):** El ensamblaje de 2,502 árboles XGBoost paralelos por paso exige Hardware de Centro de Datos (GPU A100 con 80GB VRAM y >160GB RAM) mediante Google Colab Pro, totalizando más de 100 horas de cálculo repartidas en sesiones a través de un sistema de "Checkpoints" que guarda el progreso en Google Drive paso a paso.
2.  **Modelo Lite (T4):** Al aislar los 200 genes estrella mediante selección de características, el cálculo del *Flow Matching* se reduce drásticamente, encajando perfectamente en una GPU T4 convencional (12GB VRAM), democratizando el acceso a estos modelos generativos masivos sin perder significancia estadística.
