# Capítulo 1. Generalidades
 
## 1.1 Problemática
Una de las promesas de la bioinformática y la genómica es poder identificar tempranamente la presencia de patologías, tales como el cáncer, a partir del perfil de expresión génica de la persona.
 
La dimensionalidad de los datos de expresión génica es muy alta, es decir, las muestras están en el orden de las centenas mientras que atributos en el orden de los millares. Reducción de la dimensionalidad, es uno de los principales desafíos que se encuentra en el procesamiento de este tipo de datos.
 
Meta aprendizaje ha sido propuesto para la reducción dimensional, en dichos estudios se busca usar la acumulación de experiencias para ayudar a sugerir el mejor conjunto de métodos de reducción de características para estudios futuros. Sin embargo, el cálculo manual de meta-atributos ha quedado obsoleto y propenso a errores frente a las arquitecturas modernas embebidas, evitando de eso modo que se realice nuevamente la extensa experimentación computacional.
 
Sin embargo, se ha identificado también que existe limitada cantidad de corpus de datos de expresión génica, dado que es costoso en tiempo y dinero la obtención de dichos conjuntos de datos. Esto influye en la calidad de los resultados en el contexto del meta aprendizaje, que se basa en los datos acumulados para mejorar sus precisiones.
 
En otros dominios, la generación de data plástica o sintética, también llamada "Data Augmentation", viene siendo usada con mucho éxito. No obstante, en el contexto de datos genómicos de alta dimensionalidad, las redes generativas clásicas (como GANs) sufren colapso de moda (*Mode Collapse*), haciendo necesario el uso de arquitecturas basadas en el paradigma determinista de emparejamiento de flujos como Forest Diffusion (Flow Matching).

La presente investigación propone diseñar e implementar una metodología del Estado del Arte para la generación de datos sintéticos de expresión génica a partir de un Datalake Maestro Armonizado Multiplataforma (que unifica tecnologías de Microarrays y RNA-seq). Estos biobancos sintéticos, generados mediante *Forest Diffusion*, serán integrados en regímenes de aumentación masiva dentro del proceso de meta-aprendizaje embebido (TabPFN), con el fin de evaluar si la inyección de pacientes artificiales incrementa la robustez y precisión diagnóstica del clasificador. Se empleará la arquitectura *Forest Diffusion* para la síntesis de las cohortes virtuales debido a su capacidad única para preservar correlaciones transcriptómicas complejas, complementando el flujo de trabajo con algoritmos multivariados de selección de firmas genómicas relevantes (SHAP, mRMR) para maximizar la interpretabilidad biológica y la precisión predictiva en la oncología computacional.

## 1.2 Objetivos

### 1.2.1 Objetivo general
Elaborar y evaluar una metodología de vanguardia para la generación de datos sintéticos de expresiones génicas mediante Modelos de Difusión en el contexto de meta aprendizaje embebido (TabPFN), con el fin de maximizar la precisión predictiva de los clasificadores en diagnósticos oncológicos.

### 1.2.2 Objetivos específicos
*   **OE1:** Organizar un corpus de conjuntos de datos de expresión génica de diversas patologías humanas.
*   **OE2:** Implementar un modelo de meta aprendizaje sobre el corpus inicial: extracción de las firmas biomarcadoras más robustas mediante métodos de reducción dimensional de vanguardia (como SHAP y mRMR).
*   **OE3:** Diseñar el esquema de generación de datos de expresión génicas sintéticas, usando la arquitectura de emparejamiento de flujos Forest Diffusion (Flow Matching).
*   **OE4:** Evaluar numéricamente la fidelidad biológica y la utilidad clínica de los datos generados mediante el marco de validación **TSTR** (*Train Synthetic, Test Real*) y **regímenes de aumentación híbrida (`1r+ns`)**, determinando si la incorporación de clones virtuales preserva la capacidad de generalización y mejora el rendimiento predictivo de clasificadores avanzados (TabPFN, XGBoost) en el diagnóstico de pacientes reales bajo escenarios de escasez de datos.

### 1.2.3 Resultados esperados
*   R 1. Corpus de expresión génica. (OE1)
*   R 2. Pipeline de métodos de reducción dimensional. (OE2)
*   R 3. Nuevos bancos de datos sintéticos de expresión génica de última generación. (OE3)
*   R 4. Evaluación cuantitativa de la fidelidad biológica y utilidad predictiva mediante validación TSTR y regímenes de aumentación híbrida (`1r+ns`), demostrando la capacidad de los clasificadores entrenados con datos sintéticos para discriminar con precisión entre pacientes reales sanos y oncológicos bajo condiciones de escasez de datos. (OE4)

## 1.3 Herramientas y Métodos
A continuación, se presentarán los métodos y herramientas que serán utilizados para la realización de este proyecto de fin de carrera.

### 1.3.1 Mapeo de objetivos, resultados y verificación
 
**Tabla 1 Mapeo de objetivos, resultados y verificación. Elaboración propia..**

<table border="1" width="100%" style="border-collapse: collapse;">
  <tr>
    <td colspan="4"><strong>Objetivo Específico OE1:</strong> Organizar un corpus de conjuntos de datos de expresión génica de diversas patologías humanas.</td>
  </tr>
  <tr>
    <td><strong>Resultado</strong></td>
    <td><strong>Meta física</strong></td>
    <td><strong>Medio de verificación</strong></td>
    <td><strong>Herramientas o Métodos</strong></td>
  </tr>
  <tr>
    <td>Corpus de conjuntos de datos de expresión génica de diversos estudios patológicos.</td>
    <td>Conjunto de datos.</td>
    <td>Estadísticas descriptivas de conjunto de datos recolectados de estudios realizados a pacientes con presencia de cáncer y No cáncer.</td>
    <td>
      <ul>
        <li>NCBI</li>
        <li>Python</li>
      </ul>
    </td>
  </tr>
  
  <tr>
    <td colspan="4"><strong>Objetivo Específico OE2:</strong> Implementar un modelo de meta aprendizaje sobre el corpus inicial: extracción de las firmas biomarcadoras más robustas mediante métodos de reducción dimensional de vanguardia (como SHAP y mRMR).</td>
  </tr>
  <tr>
    <td><strong>Resultado</strong></td>
    <td><strong>Meta física</strong></td>
    <td><strong>Medio de verificación</strong></td>
    <td><strong>Herramientas o Métodos</strong></td>
  </tr>
  <tr>
    <td>Pipeline de reducción dimensional y meta aprendizaje.</td>
    <td>Documento<br>Modelo</td>
    <td>Reportes describiendo la arquitectura del modelo algorítmico. Pruebas de entrada/salida. Gráficos SHAP/mRMR.</td>
    <td>
      <ul>
        <li>Algoritmos de machine learning (SHAP, mRMR)</li>
        <li>Jupyter Notebook: Python</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td colspan="4"><strong>Objetivo Específico OE3:</strong> Diseñar el esquema de generación de datos de expresión génicas sintéticas, usando la arquitectura de emparejamiento de flujos Forest Diffusion (Flow Matching).</td>
  </tr>
  <tr>
    <td><strong>Resultado</strong></td>
    <td><strong>Meta física</strong></td>
    <td><strong>Medio de verificación</strong></td>
    <td><strong>Herramientas o Métodos</strong></td>
  </tr>
  <tr>
    <td>Nuevos bancos de datos sintéticos de expresión génica.</td>
    <td>Conjunto de archivos conteniendo el conjunto de datos generados sintéticamente.<br>Documento.<br>Modelo.</td>
    <td>Logs de entrenamiento y métricas de convergencia de la difusión.</td>
    <td>
      <ul>
        <li>Forest Diffusion</li>
        <li>Python</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td colspan="4"><strong>Objetivo Específico OE4:</strong> Evaluar numéricamente la fidelidad biológica y la utilidad clínica de los datos generados mediante el marco de validación **TSTR** (*Train Synthetic, Test Real*) y **regímenes de aumentación híbrida (`1r+ns`)**, determinando si la incorporación de clones virtuales preserva la capacidad de generalización y mejora el rendimiento predictivo de clasificadores avanzados (TabPFN, XGBoost) en el diagnóstico de pacientes reales bajo escenarios de escasez de datos.</td>
  </tr>
  <tr>
    <td><strong>Resultado</strong></td>
    <td><strong>Meta física</strong></td>
    <td><strong>Medio de verificación</strong></td>
    <td><strong>Herramientas o Métodos</strong></td>
  </tr>
  <tr>
    <td>Evaluación cuantitativa de la fidelidad biológica y utilidad predictiva mediante validación TSTR y regímenes de aumentación híbrida (`1r+ns`), demostrando la capacidad de los clasificadores entrenados con datos sintéticos para discriminar con precisión entre pacientes reales sanos y oncológicos bajo condiciones de escasez de datos.</td>
    <td>Documento de reporte de resultados.<br>Cuadros y gráficas de métricas TSTR (Curvas ROC-AUC).</td>
    <td>Reporte de experimentación numérica con resultados estadísticos de métricas de desempeño (TSTR).</td>
    <td>
      <ul>
        <li>Jupyter Notebook</li>
        <li>TabPFN / XGBoost</li>
      </ul>
    </td>
  </tr>
</table>

### 1.3.2 NCBI
El Centro Nacional para la Información Biotecnológica o National Center for Biotechnology Information (NCBI) es parte de la Biblioteca Nacional de Medicina de Estados Unidos (National Library of Medicine), una rama de los Institutos Nacionales de Salud (National Institutes of Health o NIH). Se encuentra ubicado en Bethesda, Maryland y fue fundado el 4 de noviembre de 1988. El NCBI alberga una serie de bases de datos relevantes para la biotecnología y la biomedicina y es un recurso importante para herramientas y servicios bioinformáticos. Las principales bases de datos incluyen GenBank para secuencias de ADN y PubMed, una base de datos bibliográfica para literatura biomédica. Otras bases de datos incluyen la base de datos NCBI Epigenomics. Todas estas bases de datos están disponibles en línea a través del motor de búsqueda Entrez. (National Center for Biotechnology Information, s.f.)

### 1.3.3 Python
Python es un lenguaje de programación interpretado, soporta orientación a objetos, usa tipado dinámico y es multiplataforma. Posee una licencia de código abierto, denominada Python Software Foundation License. (Python (programming language), s.f.). Adicionalmente, cuenta con el soporte de librerías del estado del arte para este proyecto como Forest Diffusion, XGBoost y TabPFN.

### 1.3.4 Jupyter Notebook
Jupyter Notebook es una aplicación web de código abierto que le permite crear y compartir documentos que contienen código en vivo, ecuaciones, visualizaciones y texto narrativo. Los usos incluyen: limpieza y transformación de datos, simulación numérica, modelado estadístico, visualización de datos, aprendizaje automático y mucho más. (Jupyter, s.f.). Para este estudio, debido al gran poder computacional requerido, los notebooks también serán orquestados en entornos de nube como Google Colab (GPUs).

## 1.4 Viabilidad
A continuación, se presentará el estudio de viabilidad sobre los ámbitos técnicos, temporales y económicos del presente proyecto de fin de carrera.

### 1.4.1 Viabilidad Técnica
La viabilidad técnica de este proyecto se sustenta por las razones que se mencionarán a continuación. En primer lugar, por la existencia diferentes estudios donde se aplica técnicas de aprendizaje de máquina para ajustar modelos predictivos sobre a datos de expresión génica. Del mismo modo se cuenta con diferentes repositorios de conjuntos de datos de expresión génica de los cuales serán extraídos los datos requeridos. Adicionalmente se cuenta con la arquitectura de Forest Diffusion (Flow Matching) estandarizada en librerías open-source que resuelven los problemas de alta dimensionalidad.

### 1.4.2 Viabilidad Económica
Nuestra investigación busca implementar modelos clasificadores de vanguardia (TabPFN, XGBoost) que nos permitan evaluar la pertinencia clínica del uso de datos generados sintéticamente. La viabilidad económica se justifica dado que ya se cuenta con un datalake maestro de datos reales que supera los 28,000 perfiles genómicos iniciales (consolidados en un Core Set depurado de 9,309 muestras de alta calidad tras el filtrado de varianza y ruido), y mediante la clonación digital masiva ya no tendremos que invertir cuantiosos recursos económicos de laboratorio en la obtención de nuevas muestras.
 
## 1.5 Justificación
Nuestra investigación tiene justificación dado el contexto actual donde para muchos ámbitos de la investigación se viene generando data sintética para poder ayudar a mejorar la precisión de los modelos, es allí que nuestra investigación cobra relevancia; pues en el campo los datos de expresión génica todavía se vienen experimentando de manera incipiente; es sabido que la obtención de los bancos de datos de expresión génica es costosa, puede rondar el orden de los millones de dólares.
 
Desde el punto de vista técnico, se busca implementar un pipeline diagnóstico con meta aprendizaje embebido (TabPFN) que nos permita validar la viabilidad clínica de los datos generados sintéticamente. Dado que se cuenta con pocos bancos de datos de expresión génica y, a su vez la obtención de uno nuevo demanda de mucho tiempo y esfuerzo.

## 1.6 Limitaciones del proyecto
En nuestro proyecto vamos a implementar una metodología diagnóstica donde intervienen un conjunto de 4 métodos de selección de características (F_test, Lasso, SHAP, mRMR) y algoritmos de clasificación de vanguardia (CatBoost, XGBoost, SVM, RandomForest, TabPFN). La obtención de información relevante para la investigación demanda de un gran poder computacional (uso de GPUs y memoria RAM intensiva para resolver las Ecuaciones Diferenciales de Forest Diffusion), al no contar con máquinas que puedan procesar rápidamente los modelos, estaremos limitados a pocas ejecuciones de los modelos o lotes en la nube.
 
Otras de las limitaciones de esta investigación son que si bien se cuenta con mucha información sobre datos de expresión génica, en algunos documentos se mencionan términos muy propios de la biología y genética.
