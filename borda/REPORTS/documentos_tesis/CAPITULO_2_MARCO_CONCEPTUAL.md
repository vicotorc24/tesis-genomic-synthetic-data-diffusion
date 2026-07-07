# Capítulo 2: Marco Conceptual

> [!NOTE]
> Copia y pega estos apartados en tu archivo DOCX para reemplazar las definiciones antiguas (ruido gaussiano, meta-aprendizaje clásico). Estas definiciones reflejan el Estado del Arte (SOTA) bioinformático de 2026.

> [!IMPORTANT]
> **Añadido Biológico:** Si tu documento ya tiene un concepto sobre Microarrays, debes añadir inmediatamente después este concepto sobre RNA-seq, ya que es el estándar SOTA actual y lo usamos para la sección de Trabajos Futuros.

## 2.X Secuenciación de ARN (RNA-seq)
Mientras que los microarrays se basan en la hibridación molecular para medir un conjunto predefinido de transcritos, la secuenciación de ARN (RNA-seq) utiliza tecnología de secuenciación de próxima generación (NGS) para capturar el transcriptoma completo de una muestra biológica a nivel de nucleótido. Esta técnica supera ampliamente las limitaciones de rango dinámico y el ruido de hibridación cruzada inherentes a los microarrays. En el contexto de la oncología computacional, los perfiles de expresión génica derivados de RNA-seq ofrecen una resolución superior para la identificación de firmas tumorales, cuantificando la abundancia de transcritos de manera absoluta y permitiendo el descubrimiento de isoformas no canónicas que son críticas en la patogénesis del cáncer.

## 2.1 Redes Generativas Antagónicas para Datos Tabulares (CTGAN)
En las etapas iniciales de la genómica sintética, las arquitecturas basadas en *Generative Adversarial Networks* (GANs) representaron el estándar. Específicamente, el modelo **CTGAN (Conditional Tabular GAN)** fue diseñado para sortear las distribuciones no-gaussianas y los desbalances de clases mediante normalización de modo específico y entrenamiento condicional. Sin embargo, en el paradigma genómico $p \gg n$ (donde existen miles de genes y pocos pacientes), las arquitecturas GAN sufren del fenómeno de **Mode Collapse** (Colapso de Moda). Esto significa que el generador "memoriza" un pequeño subconjunto de perfiles de pacientes que engañan al discriminador, perdiendo la diversidad biológica de la cohorte original. Esta limitación inherente en alta dimensionalidad hizo mandatoria la transición hacia paradigmas deterministas que garanticen cobertura completa de la distribución.

## 2.X Modelos Generativos de Flujo (Flow Matching)
A diferencia de los enfoques tradicionales como CTGAN o la generación mediante ruido gaussiano simple, el *Flow Matching* representa un paradigma determinista basado en Ecuaciones Diferenciales Ordinarias (EDO). Este enfoque construye un campo vectorial continuo que transforma gradualmente una distribución de ruido inicial hacia la distribución de datos empíricos. Matemáticamente, el modelo aprende la dinámica de este campo $Y_t$, permitiendo mapear trayectorias suaves entre el espacio latente y el espacio genómico estructurado. Esta arquitectura resulta superior para datos tabulares biológicos debido a su capacidad intrínseca para preservar correlaciones complejas (como las redes de coexpresión génica) sin colapsar en modas singulares.

## 2.X Forest Diffusion y Ecuaciones Diferenciales Ordinarias (EDO)
*Forest Diffusion* es una implementación especializada de *Flow Matching* diseñada específicamente para sortear las ineficiencias computacionales de las redes neuronales profundas en conjuntos de datos tabulares y continuos. En lugar de utilizar arquitecturas densas (como perceptrones multicapa), emplea ensambles masivos de árboles de decisión (como *XGBoost*) para modelar el campo vectorial iterativo. La generación de un perfil transcriptómico sintético se logra mediante la Integración de Euler, un método numérico que resuelve la EDO iterando pasos discretos: $X_{t-1} = X_t - Y_t \cdot \Delta t$. Este ensamblaje iterativo resulta crucial para manejar el paradigma $p \gg n$ (alta dimensionalidad, bajo número de muestras) típico de la genómica.

## 2.X Selección de Características Interpretable (SHAP y mRMR)
En genómica, la maldición de la dimensionalidad exige algoritmos de selección rigurosos. En lugar de filtros univariados estadísticos básicos, el estado del arte utiliza dos vertientes:
*   **SHAP (Shapley Additive exPlanations):** Un enfoque basado en teoría de juegos cooperativos que calcula la contribución marginal exacta de cada gen a la predicción final de un modelo no lineal. Provee interpretabilidad local y global de extrema precisión.
*   **mRMR (Minimum Redundancy Maximum Relevance):** Un selector topológico basado en teoría de la información que penaliza a los genes que aportan información repetida (alta redundancia topológica) y premia aquellos altamente correlacionados con la etiqueta fenotípica (alta relevancia).

## 2.X Clasificadores Tabulares SOTA y Transformers (TabPFN)
La validación de firmas genómicas sintéticas exige algoritmos que modelen fronteras de decisión hiperplanas no lineales.
*   **Gradient Boosting (XGBoost / CatBoost):** Algoritmos de ensamblaje por impulso de gradiente. Construyen árboles secuenciales que corrigen iterativamente los residuos probabilísticos del árbol anterior, siendo actualmente el estándar de oro en datos biológicos estructurados.
*   **TabPFN (Prior-Data Fitted Network):** Una red neuronal basada en la arquitectura *Transformer* (Atención Autoregresiva). A diferencia de los modelos paramétricos que se entrenan desde cero en cada dataset, TabPFN viene pre-entrenado matemáticamente sobre billones de funciones sintéticas. Realiza inferencia directa en una sola pasada de red (O(1)), emulando inferencia bayesiana óptima para conjuntos tabulares pequeños sin necesidad de retropropagación.

## 2.X Validación TSTR (Train Synthetic, Test Real) y Pseudo-Labeling
El marco evaluativo TSTR es la metodología más rigurosa para cuantificar la fidelidad de datos tabulares sintéticos. Implica entrenar un algoritmo clasificador utilizando **únicamente** datos sintéticos, para luego evaluar su rendimiento (Área Bajo la Curva ROC - AUC) sobre un conjunto de datos **estrictamente reales** (Test Hold-out).
Para habilitar esta evaluación en modelos generativos incondicionales, se utiliza la técnica de **Pseudo-Labeling Post-Hoc**, la cual despliega un "Médico Virtual" (un clasificador previamente calibrado con cohortes reales) para diagnosticar de forma automatizada las muestras sintéticas, garantizando que sus etiquetas fenotípicas sean fieles a los dominios biológicos originales.

## 2.X Meta-Aprendizaje (Meta-Learning) en el Contexto de TabPFN
En la visión clásica (antigua) de esta investigación, el meta-aprendizaje se refería a la extracción manual de "meta-atributos" para guiar algoritmos. En el Estado del Arte actual (2026), el Meta-Aprendizaje evoluciona hacia el paradigma de los Transformers. **TabPFN** es, por definición, un modelo Meta-Aprendido: fue entrenado previamente (pre-training) simulando millones de bases de datos tabulares sintéticas generadas por procesos bayesianos. Esto permite que el modelo "aprenda a aprender", logrando clasificar tus pacientes en menos de 1 segundo sin necesidad de un entrenamiento tradicional desde cero. 

## 2.X Aumento de Datos (Data Augmentation) Sintéticos
El aumento de datos es la técnica de engrosar artificialmente el conjunto de entrenamiento para evitar el sobreajuste (overfitting). En el dominio de las imágenes, el aumento se hace rotando o invirtiendo fotos. En el dominio genómico (donde alterar un gen destruye la firma biológica), el Aumento de Datos se logra exclusivamente inyectando **Pacientes Sintéticos** generados por Forest Diffusion. El impacto de este aumento se mide mediante la **Curva de Dosis-Respuesta**, evaluando si la inyección de proporciones sintéticas (ej. 1 Real : 3 Sintéticos) incrementa el poder predictivo final del modelo maestro.
