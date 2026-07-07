# Evolución del Arsenal Algorítmico (2021 vs 2026)

Esta tabla comparativa documenta la evolución tecnológica de tu tesis. Puedes usarla directamente en una diapositiva o en el Capítulo 3 de tu manuscrito.

## 1. Modelos de Síntesis / Generación de Datos

| Modelo / Algoritmo | Año de Uso | Paradigma | Ventaja Principal (Por qué se usó) | Limitación Descubierta |
| :--- | :---: | :--- | :--- | :--- |
| **Ruido Gaussiano** | 2021 | Perturbación Estocástica Lineal | Muy rápido computacionalmente. Ideal para regularizar matrices diminutas (N < 100). | Destruye la biología compleja (Colapso Geométrico). AUC cae a 0.63 en bases masivas. |
| **CTGAN** | 2026 | Redes Generativas Adversariales (Deep Learning) | Excelente para entender el "Efecto Lote" (Batch Effect) y variables categóricas. | "Techo de Cristal": Colapsa con alta dimensionalidad (>1,000 genes) causando asfixia de hardware. |
| **Forest Diffusion** | 2026 | Difusión Tabular SOTA (Bosques Aleatorios / Flujos) | Inmune al Colapso de Modo. Preserva los biomarcadores genéticos al 100%. Soporta genómica ancha. | Demanda alta memoria en procesamiento paralelo (Resuelto con el despacho secuencial en A100). |

---

## 2. Modelos de Diagnóstico / Clasificación (El Jurado Clínico)

| Modelo / Algoritmo | Año de Uso | Arquitectura | Rol en la Investigación | Estado Actual en la Tesis |
| :--- | :---: | :--- | :--- | :--- |
| **SVM (Kernel RBF)** | 2021 / 2026 | Margen Máximo (Geométrico) | Fue el rey en 2021 por su resistencia natural al sobreajuste en bases pequeñas. | **Línea Base (Legacy):** Se mantiene hoy solo para probar que los datos sintéticos mejoran hasta a los algoritmos antiguos. |
| **Random Forest** | 2021 | Ensamble Paralelo (Bagging) | Utilizado en 2021 para extraer la importancia de los genes (Feature Importance). | **Desplazado:** Superado abrumadoramente por los algoritmos de gradiente moderno. |
| **CatBoost** | 2026 | Gradient Boosting Simétrico | Clasificador moderno resistente al ruido. Maneja categorías sin necesidad de *One-Hot Encoding*. | **Clasificador Avanzado:** Parte del "Arsenal de Auditoría" para probar datos SOTA. |
| **XGBoost** | 2021 / 2026 | Extreme Gradient Boosting | En 2021 era secundario. En 2026 es el motor central tanto predictivo como del motor de *Forest Diffusion*. | **Estándar Industrial:** El clasificador SOTA por excelencia de tu biobanco masivo. |
| **TabPFN** | 2026 | Transformer Fundacional (Zero-Shot) | El **Juez Supremo**. Entrenado previamente con millones de datasets sintéticos. No necesita sintonización. | **Frontera del Conocimiento:** Representa el límite absoluto del rendimiento (AUC máximo) para la auditoría final. |

---

## 3. Selectores de Características / Reducción de Dimensionalidad

| Modelo / Algoritmo | Año de Uso | Paradigma | Rol Original (2021) | Evolución SOTA (2026) |
| :--- | :---: | :--- | :--- | :--- |
| **mRMR / F-Test / Lasso** | 2021 | Selectores Clásicos (Filtro / Wrapper) | **El Núcleo:** El objetivo de la tesis era usar Meta-Learning para recomendar el mejor selector para cada dataset. | **Auditoría de Identidad (Jaccard):** Ya no se usan para entrenar, sino como "Jueces" para comprobar si los datos sintéticos conservan los mismos genes importantes que los reales. |
| **PCA / Autoencoders** | -- | Extracción de Características | (No centrales en la investigación) | **Descartados por Diseño:** Comprimen la matriz y destruyen la interpretabilidad biológica. El médico pierde el nombre del gen. |
| **XGBoost (Feature Importance)** | 2026 | Selección Embebida (Árboles) | -- | **El Brazo Lite (Fallido pero Revelador):** Se usó para aislar los 200 genes de mayor importancia predictiva. Demostró empíricamente que una compresión dimensional extrema (reducción del 92% del transcriptoma) colapsa la firma inter-génica de la enfermedad, resultando en la pérdida de viabilidad diagnóstica (AUC 0.56). |
| **Filtro de Varianza Máxima** | 2026 | Selección No Supervisada | -- | **El Brazo Óptimo (El Éxito SOTA):** Solución matemática cruda y elegante. Retiene los 1,000 genes de mayor varianza biológica, evitando el sesgo predictivo y estabilizando la GPU A100. |

---

> [!TIP]
> **El Argumento para la Defensa:**
> Observa cómo evolucionó tu investigación. Pasaste de usar herramientas matemáticas "ciegas" y simples (Ruido Gaussiano y SVM) en 2021, a utilizar arquitecturas que simulan la física cuántica (Difusión) y el lenguaje humano (Transformers / TabPFN) en 2026 para dominar el Big Data Oncológico. Además, el rol de la selección de atributos mutó: pasó de ser "el fin de la tesis" a ser una "herramienta de auditoría" para validar IA Generativa.
