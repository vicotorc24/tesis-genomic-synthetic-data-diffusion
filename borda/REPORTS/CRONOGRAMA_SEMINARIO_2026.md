# Cronograma de Avances: Seminario de Investigación 2 / 2026-1

**Asesor:** Dr. Edwin Rafael Villanueva Talavera
**Investigador:** Gary Alberto Velásquez Narro

Este documento contiene la planificación semanal oficial a reportar a lo largo del periodo académico. Está diseñado para ser copiado directamente en las plantillas de seguimiento de curso.

## Planificación de Semanas (Entregables)

### 1 – Hasta el 11/04/2026
* **Fecha de envío:** 19/04/2026
* **Avance:** Propuesta de Modernización: Transición del estudio preliminar 2021 hacia un Datalake Generativo. Definición de objetivos para la armonización multi-plataforma (Microarray + RNA-seq).

### 2 – Hasta el 18/04/2026
* **Fecha de envío:** 19/04/2026
* **Avance:** Ingesta y Curaduría de Datos: Armonización de nomenclatura HGNC y consolidación del Core Set (5,358 muestras de alta densidad). Implementación del split científico 80/20 para validación TSTR.

### 3 – Hasta el 25/04/2026
* **Fecha de envío:** PENDIENTE
* **Avance:** Ejecución de la *Prueba de Estrés*: Demostración empírica del "Colapso de Generalización" de la técnica legada frente al Efecto Lote. Inicio del pre-entrenamiento de los modelos anatómicos generativos SOTA (CTGAN y Forest Diffusion) invirtiendo +4,000 horas de CPU acumuladas.
* **Nota técnica:** El entrenamiento de Forest Diffusion sobre el Master Set (28k×2503) enfrentó un cuello de botella de compresión exponencial (`joblib compress=9` sobre modelo acumulado) que bloqueó el progreso en el paso 3/50 durante ~3 días. Resuelto con refactorización a checkpoints individuales por paso.

### 4 – Hasta el 02/05/2026
* **Avance:** Finalización de la Inferencia Generativa: Sistematización de los resultados matemáticos de Forest Diffusion. Ejecución de la generación masiva para sintetizar el subconjunto de "Gemelos Sintéticos" de alta dimensión espacial.

### 5 – Hasta el 09/05/2026
* **Avance:** Evaluación del Rendimiento Predictivo (Protocolo TSTR): Aplicación del "Arsenal de Algoritmos Modernos" (TabPFN, XGBoost) sobre los datos sintéticos frente a la partición de prueba ciega real (1,072 muestras) para el cruce de métricas AUC/F1-Score.

### 6 – Hasta el 16/05/2026
* **Avance:** Auditoría de Explicabilidad Causal y Fidelidad Biológica: Aplicación de la técnica de Valores de Shapley (SHAP) sobre oráculos predictivos para verificar el Índice de Jaccard y confirmar que las firmas oncológicas reales se preservaron sin alucinación estadística.

### 7 – Hasta el 23/05/2026
* **Avance:** Redacción del Manuscrito Final (Capítulos 3 y 4): Volcado metódico de las Fases del Duelo Decadal, la metodología SOTA, y discusión cruzada de tablas de rendimiento, argumentando el salto a la Invarianza Tecnológica.

### 8 – Hasta el 30/05/2026 *(semana en curso)*
* **Avance:** Diagramación y Revisión de Literatura: Elaboración de mapas de calor (Heatmaps) referenciales y curvas de rendimiento (ROC) en Alta Resolución. Revisión cruzada con la bibliografía de frontera de 2025/2026. Revisión parcial enviada al asesor.
* **Nota técnica:** Refactorización completa del pipeline de checkpoints de Forest Diffusion para guardar cada paso XGBoost individualmente (`compress=0`) eliminando el cuello de botella O(N²) de compresión. Reinicio del entrenamiento de 50 pasos sobre el Master Set (28,048 muestras × 2,503 features).

### 9 – Hasta el 06/06/2026
* **Avance:** Consolidación Documental y Re-entrenamiento Menor: Corrección de observaciones del asesor sobre sesgo biológico o justificación de hiperparámetros. 

### 10 – Hasta el 13/06/2026
* **Avance:** Conclusiones y Anexos Metodológicos: Redacción del Capítulo de Conclusiones sobre la democratización en LATAM, y desarrollo formal de los Anexos detallando el Efecto Lote y las métricas complejas de escalabilidad de CPU/RAM.

### 11 – Hasta el 20/06/2026
* **Avance:** Revisión Tipográfica y Auditoría Antiplagio: Adaptación pulida del formato académico requerido (Tablas, Índices y Referencias según estandarización institucional) y elaboración del *Abstract* final bilingüe.

### 12 – Hasta el 27/06/2026
* **Avance:** Orquestación de la Presentación de Defensa: Extracción de los hallazgos críticos de la tesis en diseño y flujos de soporte visual (Diapositivas) para justificar los argumentos frente al jurado. 

### 13 – Hasta el 04/07/2026
* **Avance:** Entrega Final del Manuscrito: Cierre orgánico de los procesos, consolidación del repositorio de replicación de código, y Simulacro Analítico para la defensa doctoral/magíster.
