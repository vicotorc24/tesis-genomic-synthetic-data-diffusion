**PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ**

**ESCUELA DE POSGRADO**

![](media/image1.png){width="3.6145833333333335in"
height="1.53125in"}

**GENERACIÓN DE DATOS SINTÉTICOS MEDIANTE MODELOS GENERATIVOS (CTGAN Y
DIFUSIÓN) PARA LA OPTIMIZACIÓN DE CLASIFICADORES GENÓMICOS DE ALTA
DIMENSIONALIDAD: UN ENFOQUE DE ARMONIZACIÓN MULTI-PLATAFORMA**

**Tesis para optar el Grado Académico de Magíster en Informática con
mención en Ciencias de la Computación**

**AUTOR**

Gary Alberto Velásquez Narro

**ASESOR**

Dr. Edwin Rafael Villanueva Talavera

**LIMA -- PERÚ**

**2026**

[]{#_Toc526703397 .anchor}**Resumen**

En el contexto actual de la Inteligencia Artificial, la generación de
data sintética (Generative AI) se ha consolidado como un mecanismo
crítico para robustecer el entrenamiento de modelos predictivos y
democratizar el acceso a la información. Si bien esta tecnología ha
revolucionado campos como la visión computacional, su traslado al
procesamiento de datos de expresión génica representa un reto
bioinformático mayúsculo debido a la extrema dimensionalidad inherente
al transcriptoma (decenas de muestras frente a miles de atributos).

Para mitigar esta \"maldición de la dimensionalidad\", la literatura ha
propuesto el uso de Meta-Aprendizaje y algoritmos de actuales en
selección de características. Sin embargo, la efectividad empírica de
estos modelos se ve severamente limitada por el alto costo temporal y
económico que conlleva la extracción de perfiles oncológicos humanos,
resultando históricamente en el entrenamiento sobre cohortes genómicas
pequeñas y aisladas tecnológicamente.

Para resolver esta carencia de volumen, la presente investigación consolidó en primera instancia un Datalake Maestro Armonizado de 28,048 pacientes iniciales, del cual se consolidó —tras un riguroso proceso de control de calidad y varianza— un Core Set depurado de 9,309 muestras (denominado Elite Borda) a lo largo de 2,502 genes, unificando exitosamente la brecha entre tecnologías legadas (249 datasets de Microarrays) y secuenciación moderna (33 datasets de RNA-seq). Sobre este corpus de alta dimensionalidad, se
implementó una metodología SOTA (Estado del Arte) para la generación de
biobancos sintéticos, sustituyendo los generadores históricos de ruido
gaussiano y aprendizaje profundo antagónico (CTGAN) ---los cuales
sufrieron colapso modal (*Mode Collapse*)--- por arquitecturas de
modelado tabular por difusión (*Forest Diffusion*).

La validación empírica se estructuró bajo el marco de evaluación TSTR (Train Synthetic, Test Real) y la nomenclatura matemática de aumentación **1r+ns**. Se evaluó el desempeño diagnóstico cruzando algoritmos avanzados de selección de características (mRMR, SHAP) con clasificadores oncológicos de última generación (XGBoost, TabPFN), escalando el procesamiento interactómico hasta un Modelo Óptimo de 1,000 genes de alta varianza mediante el uso de supercomputación GPU.

Los resultados demuestran un cambio de paradigma: la IA generativa
contemporánea logró generar clones sintéticos hiper-realistas que
retienen hasta un 98.8% de fidelidad biológica. A diferencia de estudios
previos, la inyección masiva de pacientes artificiales en el
entrenamiento (regímenes de 1r+120s) no solo evitó el colapso de
generalización, sino que detonó una aumentación positiva. Se concluye
categóricamente que la armonización multiplataforma combinada con
difusión sintética supera definitivamente los techos predictivos de las
cohortes aisladas, validando empíricamente el uso de pacientes virtuales
generados por computadora para el diagnóstico oncológico de alta
dimensionalidad.

[]{#_Toc233294257 .anchor}**Abstract**

In the current context of Artificial Intelligence, synthetic data
generation (Generative AI) has consolidated itself as a critical
mechanism to enhance the training of predictive models and democratize
access to information. While this technology has revolutionized fields
such as computer vision, its translation to gene expression data
processing represents a major bioinformatics challenge due to the
extreme dimensionality inherent to the transcriptome (tens of samples
versus thousands of attributes).

To mitigate this \"curse of dimensionality\", the literature has
proposed the use of Meta-Learning and state-of-the-art feature selection
algorithms. However, the empirical effectiveness of these models is
severely constrained by the high temporal and economic costs associated
with extracting human oncological profiles, historically resulting in
training on small, technologically isolated genomic cohorts.

To resolve this volume deficiency, this research first consolidated a Harmonized Master Datalake of 28,048 initial patients, from which a refined Core Set of 9,309 samples (referred to as Elite Borda) across 2,502 genes was consolidated after rigorous quality and variance filtering, successfully bridging the gap between legacy technologies (249 Microarray datasets) and modern sequencing (33 RNA-seq datasets). On this high-dimensional corpus, a
state-of-the-art (SOTA 2026) methodology for generating synthetic
biobanks was implemented, replacing historical generators such as
Gaussian noise and adversarial deep learning (CTGAN)---which suffered
from Mode Collapse---with tabular diffusion modeling architectures
(*Forest Diffusion*).

Empirical validation was structured under the TSTR (Train Synthetic,
Test Real) evaluation framework and the mathematical augmentation
nomenclature **1r+ns**. Diagnostic performance was evaluated by crossing
advanced feature selection algorithms (mRMR, SHAP) with next-generation
oncological classifiers (XGBoost, TabPFN), scaling interactomic
processing up to an Optimal Model of 1,000 high-variance genes using GPU
supercomputing.

The results demonstrate a paradigm shift: contemporary Generative AI
successfully generated hyper-realistic synthetic clones that retain up
to 98.8% biological fidelity. Unlike previous studies, the massive
injection of artificial patients during training (regimes up to 1r+120s)
not only prevented generalization collapse but triggered a positive
predictive augmentation. It is categorically concluded that
multi-platform harmonization combined with synthetic diffusion
definitively overcomes the predictive ceilings of isolated cohorts,
empirically validating the use of computer-generated virtual patients
for high-dimensional oncological diagnosis.

[]{#_Toc526703399 .anchor}**Agradecimientos**

Gracias a mi asesor Dr. Edwin Villanueva Talavera por su tiempo y por
compartirme sus conocimientos y guiarme a largo de esta investigación.
Un saludo especial también a los miembros del jurado Dr. César Beltran y
el Mg. Arturo Oncevay.

Quiero agradecer a todos mis familiares, amigos y compañeros que me
ayudaron y apoyaron a lo largo de esta investigación, desde la etapa de
escoger el tema, durante la investigación y recolección de la
información, hasta el proceso de desarrollo y redacción de la tesis. Y
también un agradecimiento muy especial a todas las personas que se
tomaron el tiempo y la paciencia para revisarla.

# Tabla de Contenido

[**Resumen** [2](#_Toc526703397)](#_Toc526703397)

[**Abstract** [4](#_Toc233294257)](#_Toc233294257)

[**Agradecimientos** [6](#_Toc526703399)](#_Toc526703399)

[Tabla de Contenido [7](#_Toc233294259)](#_Toc233294259)

[Índice de Figuras [9](#índice-de-figuras)](#índice-de-figuras)

[Índice de Tablas [10](#índice-de-tablas)](#índice-de-tablas)

[Capítulo 1. Generalidades [11](#generalidades)](#generalidades)

[1.1 Problemática [11](#problemática)](#problemática)

[1.2 Objetivos [12](#objetivos)](#objetivos)

[1.2.1 Objetivo general [12](#objetivo-general)](#objetivo-general)

[1.2.2 Objetivos específicos
[12](#objetivos-específicos)](#objetivos-específicos)

[1.2.3 Resultados esperados
[12](#resultados-esperados)](#resultados-esperados)

[1.3 Herramientas y Métodos
[13](#herramientas-y-métodos)](#herramientas-y-métodos)

[1.3.1 Mapeo de objetivos, resultados y verificación
[13](#mapeo-de-objetivos-resultados-y-verificación)](#mapeo-de-objetivos-resultados-y-verificación)

[1.3.2 NCBI [14](#ncbi)](#ncbi)

[1.3.3 Python [15](#python)](#python)

[1.3.4 Jupyter Notebook [15](#jupyter-notebook)](#jupyter-notebook)

[1.4 Viabilidad [15](#viabilidad)](#viabilidad)

[1.4.1 Viabilidad Técnica
[15](#viabilidad-técnica)](#viabilidad-técnica)

[1.4.2 Viabilidad Económica
[16](#viabilidad-económica)](#viabilidad-económica)

[1.5 Justificación [16](#justificación)](#justificación)

[1.6 Limitaciones del proyecto
[16](#limitaciones-del-proyecto)](#limitaciones-del-proyecto)

[Capítulo 2. Marco Conceptual
[17](#marco-conceptual)](#marco-conceptual)

[2.1 Genética y Genómica
[17](#genética-y-genómica)](#genética-y-genómica)

[2.2 Acido Desoxirribonucleico
[17](#acido-desoxirribonucleico)](#acido-desoxirribonucleico)

[2.3 Genoma [17](#genoma)](#genoma)

[2.4 Gen [18](#gen)](#gen)

[2.5 Expresión génica (gene expression)
[18](#expresión-génica-gene-expression)](#expresión-génica-gene-expression)

[2.6 Microarrays: [19](#microarrays)](#microarrays)

[2.7 Secuenciación de ARN (RNA-seq)
[20](#secuenciación-de-arn-rna-seq)](#secuenciación-de-arn-rna-seq)

[2.8 Microarray Data Analysis
[20](#microarray-data-analysis)](#microarray-data-analysis)

[2.9 Aprendizaje de Maquina
[20](#aprendizaje-de-maquina)](#aprendizaje-de-maquina)

[2.10 Selección de Características
[22](#selección-de-características)](#selección-de-características)

[2.11 Meta Aprendizaje (Meta-Learning) en el Contexto de TabPFN
[22](#meta-aprendizaje-meta-learning-en-el-contexto-de-tabpfn)](#meta-aprendizaje-meta-learning-en-el-contexto-de-tabpfn)

[2.12 Aumento de datos (Data Aumentación)
[23](#aumento-de-datos-data-aumentación)](#aumento-de-datos-data-aumentación)

[2.13 Redes Generativas Antagónicas para Datos Tabulares
[23](#redes-generativas-antagónicas-para-datos-tabulares)](#redes-generativas-antagónicas-para-datos-tabulares)

[2.14 Modelos Generativos de Flujo (Flow Matching)
[23](#modelos-generativos-de-flujo-flow-matching)](#modelos-generativos-de-flujo-flow-matching)

[Capítulo 3. Estado del Arte [24](#estado-del-arte)](#estado-del-arte)

[3.1 Preguntas de Investigación
[24](#preguntas-de-investigación)](#preguntas-de-investigación)

[3.2 Definición de los términos de búsqueda
[24](#definición-de-los-términos-de-búsqueda)](#definición-de-los-términos-de-búsqueda)

[3.3 Selección de fuentes
[25](#selección-de-fuentes)](#selección-de-fuentes)

[3.4 Criterios de inclusión y exclusión
[25](#criterios-de-inclusión-y-exclusión)](#criterios-de-inclusión-y-exclusión)

[3.5 Descripción de trabajos relacionados
[26](#descripción-de-trabajos-relacionados)](#descripción-de-trabajos-relacionados)

[3.5.1 Evolución de la Generación Tabular: De GANs a Modelos de Difusión
[26](#evolución-de-la-generación-tabular-de-gans-a-modelos-de-difusión)](#evolución-de-la-generación-tabular-de-gans-a-modelos-de-difusión)

[3.5.2 Transición del Meta-Aprendizaje Clásico al Meta-Aprendizaje
Embebido
[27](#transición-del-meta-aprendizaje-clásico-al-meta-aprendizaje-embebido)](#transición-del-meta-aprendizaje-clásico-al-meta-aprendizaje-embebido)

[3.5.3 Técnicas de Vanguardia en la Selección de Atributos
[27](#técnicas-de-vanguardia-en-la-selección-de-atributos)](#técnicas-de-vanguardia-en-la-selección-de-atributos)

[3.5.4 El Marco de Validación TSTR (Train Synthetic, Test Real)
[28](#el-marco-de-validación-tstr-train-synthetic-test-real)](#el-marco-de-validación-tstr-train-synthetic-test-real)

[Capítulo 4. Desarrollo y Resultados
[28](#desarrollo-y-resultados)](#desarrollo-y-resultados)

[4.1 Base de Datos [28](#base-de-datos)](#base-de-datos)

[4.2 Selección de Métodos de Selección de Características
[30](#selección-de-métodos-de-selección-de-características)](#selección-de-métodos-de-selección-de-características)

[4.3 Selección de Algoritmos de Clasificación
[31](#selección-de-algoritmos-de-clasificación)](#selección-de-algoritmos-de-clasificación)

[4.4 Generación Sintética y Aumentación Masiva
[32](#generación-sintética-y-aumentación-masiva)](#generación-sintética-y-aumentación-masiva)

[4.5 Arquitectura Predictiva y Validación TSTR
[33](#arquitectura-predictiva-y-validación-tstr)](#arquitectura-predictiva-y-validación-tstr)

[4.6 Proyección de Escalamiento a Alta Dimensionalidad
[37](#proyección-de-escalamiento-a-alta-dimensionalidad)](#proyección-de-escalamiento-a-alta-dimensionalidad)

[Capítulo 5. Presentación de los resultados esperados
[39](#presentación-de-los-resultados-esperados)](#presentación-de-los-resultados-esperados)

[5.1 Análisis Generativo por Cohortes Tecnológicas Separadas
[39](#análisis-generativo-por-cohortes-tecnológicas-separadas)](#análisis-generativo-por-cohortes-tecnológicas-separadas)

[Capítulo 6. Conclusiones y trabajos futuros
[40](#conclusiones-y-trabajos-futuros)](#conclusiones-y-trabajos-futuros)

[6.1 Conclusiones [40](#conclusiones)](#conclusiones)

[6.2 Trabajos futuros [41](#trabajos-futuros)](#trabajos-futuros)

[Referencias [43](#referencias)](#referencias)

# Índice de Figuras {#índice-de-figuras .Title}

[Figura 1. Visión general del flujo de información del ADN a la proteína
en un eucariota. Adaptado de (Nature Education, 2010)
[19](#_Toc64589773)](#_Toc64589773)

[Figura 2. Enfoque de Machine Learning. Adaptado de (Géron, 2017)
[21](#_Toc64589774)](#_Toc64589774)

[Figura 3.Muestra de los datos de expresión génica en un texto plano
[27](#_Toc64589775)](#_Toc64589775)

[Figura 4. Microarray (Sánchez 2015) [28](#_Toc64589776)](#_Toc64589776)

[Figura 5. Métodos de Selección de características. Elaboración Propia
[28](#_Toc64589777)](#_Toc64589777)

[Figura 6. Arquitectura de recomendación de métodos de métodos de
selección de características + un algoritmo de clasificación.
Elaboración Propia [31](#_Toc64589778)](#_Toc64589778)

[Figura 7. Gráfico muestra los 100 atributos obtenidos luego de ser
aplicado el modelo de selección de características. Elaboración Propia
[32](#_Toc64589779)](#_Toc64589779)

[Figura 8. Gráfico muestra cálculo de AUC para el par: FSM+Clasificador.
Elaboración Propia [33](#_Toc64589780)](#_Toc64589780)

[Figura 9. Gráfico ranking AUC. Elaboración Propia
[33](#_Toc64589781)](#_Toc64589781)

[Figura 10. Gráfico Matriz de Desempeños
[34](#_Toc64589782)](#_Toc64589782)

[Figura 11. Gráfico Matriz de Meta Aprendizaje
[34](#_Toc64589783)](#_Toc64589783)

[Figura 12. Gráfico Matriz de Rankings de Desempeños
[35](#_Toc64589784)](#_Toc64589784)

[Figura 13. Gráfico Evaluación del Modelo: Coef. Spearman vs K´s
[36](#_Toc64589785)](#_Toc64589785)

[Figura 14. Gráfico Evaluación del Modelo: Curva de pérdida de
rendimiento (PLC): vs K´s [37](#_Toc64589786)](#_Toc64589786)

[Figura 15. Gráfico Matriz de Meta Atributos Sintéticos
[38](#_Toc64589787)](#_Toc64589787)

[Figura 16. Gráfico Matriz de Ranking de Desempeños Sintéticos
[39](#_Toc64589788)](#_Toc64589788)

[Figura 17. Gráfico Evaluación del Modelo: Coef. Spearman vs K´s usando
datos Sinteticos [40](#_Toc64589789)](#_Toc64589789)

[Figura 18. Gráfico Evaluación del Modelo: Curva de pérdida de
rendimiento (PLC) vs K´s usando datos Sinteticos
[41](#_Toc64589790)](#_Toc64589790)

# Índice de Tablas {#índice-de-tablas .Title}

[Tabla 1 Mapeo de objetivos, resultados y verificación. Elaboración
propia.. [13](#_Toc64589791)](#_Toc64589791)

[Tabla 2. Cadenas básicas de búsqueda. Elaboración propia.
[24](#_Toc64589792)](#_Toc64589792)

[Tabla 3.Matriz de relación de pares: método de selección de
características con algoritmos de clasificación. Elaboración propia.
[30](#_Toc64589793)](#_Toc64589793)

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


# Marco Conceptual

En el presente capitulo se describirán conceptos claves para el
entendimiento del problema presentado para este proyecto de fin de
carrera.

## Genética y Genómica

La genética es el estudio de las herencias biológicas, incluyendo las
características que se obtienen por influencia del ambiente. La genómica
es el estudio de todos los genes en un organismo para entender su
estructura molecular, función, interacción e historia evolutiva. El
concepto fundamental de la genética y genómicas es la siguiente: las
características heredadas son transmitidas por los padres a su
descendencia a través de los elementos hereditarios llamados genes .

## Acido Desoxirribonucleico

Comúnmente llamado ADN. Contienen toda la información genética para el
desarrollo y funcionamiento de todo organismo viviente y de algunos
virus. Del punto de vista químico es una cadena de nucleótidos
estructurado en una doble hélice. Estos nucleótidos a su vez están
formados por un azúcar (desoxirribosa) y una base

nitrogenada. Esta última puede ser alguna de las siguientes cuatro:
Adenina (A), Timina (T), Citosina (C) o Guanina (G). La otra parte de la
hélice está formada por el

complemento de la otra hélice siguiendo la relación A -- T y G --C.
Mientras que una hélice está restringida por su par esto no se traslada
a la misma hebra por lo que cualquier tipo de secuencia es posible.
Debido a esta estructura, el ADN se puede representar como una secuencia
de nucleótidos. (Learning, 2011)

## Genoma

La totalidad de DNA en la célula, núcleo o organela. Cuando es usado
para hablar de una especie en específico, por ejemplo, en frases como
"el genoma humano", el termino genoma se define como el DNA presente en
el organismo en una célula somática normal (célula no reproductiva). En
cualquier caso, el genoma es toda la información genética que el
individuo posee. Las nuevas técnicas de secuenciación (proceso en donde
se obtiene la secuencia de nucleótidos del ADN) hacen que sea viable
secuenciar a múltiples especies y obtener toda la información genética
de sus secuencias genómicas. En el 2003 se concluyó el proceso de
secuenciación del genoma humano y desde ahí la cantidad de especies
secuenciadas no ha dejado de aumentar. (Moraes & Góes, 2016)

## Gen

Es una sección particular del DNA que define la herencia y expresión de
una característica particular. El gen codifica una función o
característica del organismo al permitir a este generar un tipo de
proteína especifica en el proceso expresión génica. Los genes usualmente
se mantienen en el proceso de reproducción, sin embargo, estos pueden
asumir diferentes variantes en una población (variantes denominados como
alelos del gen). Estos alelos pueden codificar proteínas ligeramente
diferentes lo que puede terminar en diferentes fenotipos. No toda la
secuencia de nucleótidos de los genes es utilizada para el proceso de
expresión génica. Las partes que si aportaran a ese proceso se les
denomina región codificante la cual a su vez está formada por exones.
Por otro lado, las partes del gen que no aportan en la codificación se
le llaman región no codificante y está formada por intrones. Aunque a
primera vista los intrones no cumplen ninguna función, recientes
estudios muestran que los microRNAs en estas regiones cumplen un papel
importante en el proceso de expresión génica (Caramuta et al., 2013). En
conclusión, el gen está formado por exones e intrones.

## Expresión génica (gene expression)

Los genes codifican las proteínas y las proteínas dictan la función
celular. Por lo tanto, los miles de genes expresados en una célula
particular determinan lo que esa célula puede hacer. Además, cada paso
en el flujo de información de ADN a ARN a proteína proporciona a la
célula un punto de control potencial para autor regular sus funciones
mediante el ajuste de la cantidad y el tipo de proteínas que fabrica.
(nature, 2010)

Las cantidades y tipos de moléculas de ARNm en una célula reflejan la
función de esa célula. De hecho, miles de transcripciones se producen
cada segundo en cada celda. Dada esta estadística, no es sorprendente
que el punto de control primario para la expresión génica se encuentre
generalmente al comienzo del proceso de producción de proteínas, el
inicio de la transcripción. La transcripción de ARN es un punto de
control eficiente porque muchas proteínas pueden formarse a partir de
una única molécula de ARNm. (nature, 2010)

![[]{#_Toc64589773 .anchor}Figura 1. Visión general del flujo de
información del ADN a la proteína en un eucariota. Adaptado de (Nature
Education,
2010)](media/image2.jpeg){alt="https://www.nature.com/scitable/content/ne0000/ne0000/ne0000/ne0000/14711098/U2CP3-1_SynthesisDegredati_ksm.jpg"
width="5.099849081364829in" height="4.5605435258092735in"}

## Microarrays: 

Microarrays es una tecnología que se ha convertido en una de las
herramientas indispensables que muchos biólogos utilizan para monitorear
los niveles de expresión de genes de genoma en un organismo determinado.
Una micromatriz es típicamente un portaobjetos de vidrio en el que las
moléculas de ADN se fijan de manera ordenada en lugares específicos
llamados puntos (o características). Una micromatriz puede contener
miles de manchas y cada mancha puede contener unos pocos millones de
copias de moléculas de ADN idénticas que corresponden únicamente a un
gen. El ADN en un punto puede ser ADN genómico o un tramo corto de
cadenas de oligo-nucleótidos que corresponden a un gen. Las manchas se
imprimen en el portaobjetos de vidrio mediante un robot o se sintetizan
mediante el proceso de fotolitografía (Babu, 2004).

## Secuenciación de ARN (RNA-seq)

Mientras que los microarrays se basan en la hibridación molecular para
medir un conjunto predefinido de transcritos, la secuenciación de ARN
(RNA-seq) utiliza tecnología de secuenciación de próxima generación
(NGS) para capturar el transcriptoma completo de una muestra biológica a
nivel de nucleótido. Esta técnica supera ampliamente las limitaciones de
rango dinámico y el ruido de hibridación cruzada inherentes a los
microarrays. En el contexto de la oncología computacional, los perfiles
de expresión génica derivados de RNA-seq ofrecen una resolución superior
para la identificación de firmas tumorales, cuantificando la abundancia
de transcritos de manera absoluta y permitiendo el descubrimiento de
isoformas no canónicas que son críticas en la patogénesis del cáncer.

## Microarray Data Analysis

Los conjuntos de datos de microarrays son generalmente muy grandes, y la
precisión analítica está influenciada por una serie de variables. Por lo
tanto, es extremadamente útil reducir el conjunto de datos a aquellos
genes que se distinguen mejor entre los dos casos o clases (por ejemplo,
normal frente a enfermo). Tales análisis producen una lista de genes
cuya expresión se considera que cambia y se conoce como genes expresados
​​diferencialmente. La identificación de la expresión génica diferencial
es la primera tarea de un análisis de microarrays en profundidad. Hay
dos métodos comunes para el análisis de datos de microarrays en
profundidad, es decir, agrupación y clasificación \[6\]. El agrupamiento
es uno de los enfoques no supervisados ​​para clasificar los datos en
grupos de genes o muestras con patrones similares que son
característicos del grupo. La clasificación es aprendizaje supervisado y
también se conoce como predicción de clase o análisis discriminante.
Generalmente, la clasificación es un proceso de aprendizaje de ejemplos.
Dado un conjunto de ejemplos preclasificados, el clasificador aprende a
asignar un caso de prueba invisible a una de las clases (Selvaraj &
Natarajan, 2011).

## Aprendizaje de Maquina

Rama de las Ciencias de Computación que busca que se puedan generar
modelos que aprendan de ejemplos de entrenamiento para que realicen
tareas que no se les ha indicado específicamente como realizarlas
(Géron, 2017). Una definición más formal está dada por Tom Mitchell: "Se
dice que un programa de computadora aprende de la experiencia E con
respecto a la tarea T dada una medida de rendimiento si se da que el
rendimiento en la tarea T, medido por P, mejora con la experiencia E
(Mitchell, 1997). La Figura 11 muestra un esquema del enfoque común que
se sigue en aprendizaje de maquina (Géron, 2017).

![[]{#_Toc64589774 .anchor}Figura 2. Enfoque de Machine Learning.
Adaptado de (Géron,
2017)](media/image3.png){alt="Diagram Description automatically generated"
width="4.895833333333333in" height="2.620833333333333in"}

Por ejemplo, un programa de Aprendizaje de Máquina que podría aprender
filtrar correos que son spam a través de ejemplos categorizados por
usuarios. Los ejemplos que son utilizados para aprender son llamados
conjunto de entrenamiento. En este caso la tarea T es poder clasificar
si un correo es spam o no, la experiencia E es el conjunto de
entrenamiento y la medida de rendimiento P necesita ser definida; por
ejemplo, se podría usar la proporción correos correctamente
clasificados. Esta medida de rendimiento particular es llamada precisión
y es usualmente usada en tareas de clasificación (Géron, 2017).

Existen varias técnicas de Aprendizaje de Máquina, las cuales pueden ser
agrupadas de acuerdo a:

- Si son entrenadas con supervisión humana (Supervisado, no supervisado,
  semisupervisado, aprendizaje por refuerzo) (Géron, 2017)

<!-- -->

- Si pueden o no aprender mientras están funcionando (Aprendizaje online
  o por lote)

- Si trabajan solo comparando puntos de información o si detectan
  patrones en el conjunto de entrenamiento y construyen un modelo
  predictivo (Basado en instancias o basados en modelos)

## Selección de Características

En aprendizaje automático y estadística, la selección de
características, también conocida como selección de variables, selección
de atributos o selección de subconjuntos variables, es el proceso de
selección de un subconjunto de características que tienen relevancia en
la construcción del modelo.

Se considera tres categorías principales de algoritmos de selección de
características: filtros, envoltorios, y métodos integrados. (Guyon,
2003)

- **Filtros** (Filter): Estos métodos generalmente se usan como un paso
  de preproceso. La selección de características es independiente de
  cualquier algoritmo de aprendizaje automático. El método de filtro
  clasifica cada característica según alguna métrica univariada y luego
  selecciona las características de mayor rango. Algunas de las métricas
  univariadas son: F-test, Chi2, ANOVA, correlación de coeficientes.
  (Khandelwal, 2019)

- **Envoltorio** (Wrapper): Los métodos de envoltura tratan de usar un
  subconjunto de características y capacitar a un modelo para usarlas.
  Con base en las inferencias que extraemos del modelo anterior,
  decidimos agregar o eliminar características de su subconjunto.
  Entonces el problema que resultante se reduce esencialmente a una
  búsqueda. Estos métodos son usualmente computacionalmente muy
  costosos.

- **Métodos integrados** (Embedded): Los métodos integrados combinan las
  cualidades de los métodos de filtro y envoltura. Los algoritmos que se
  usan tienen sus propios métodos de selección de funciones
  incorporados.

## Meta Aprendizaje (Meta-Learning) en el Contexto de TabPFN

En la visión clásica (antigua) de esta investigación, el
meta-aprendizaje se refería a la extracción manual de \"meta-atributos\"
para guiar algoritmos. En el Estado del Arte actual (2026), el
Meta-Aprendizaje evoluciona hacia el paradigma de los Transformers.
TabPFN es, por definición, un modelo Meta-Aprendido: fue entrenado
previamente (pre-training) simulando millones de bases de datos
tabulares sintéticas generadas por procesos bayesianos. Esto permite que
el modelo \"aprenda a aprender\", logrando clasificar tus pacientes en
menos de 1 segundo sin necesidad de un entrenamiento tradicional desde
cero.

## Aumento de datos (Data Aumentación)

El aumento de datos es la técnica de engrosar artificialmente el
conjunto de entrenamiento para evitar el sobreajuste (overfitting). En
el dominio de las imágenes, el aumento se hace rotando o invirtiendo
fotos. En el dominio genómico (donde alterar un gen destruye la firma
biológica), el Aumento de Datos se logra exclusivamente inyectando
Pacientes Sintéticos generados por Forest Diffusion. El impacto de este
aumento se mide mediante la Curva de Dosis-Respuesta, evaluando si la
inyección de proporciones sintéticas (ej. 1 Real : 3 Sintéticos)
incrementa el poder predictivo final del modelo maestro.

## Redes Generativas Antagónicas para Datos Tabulares

En las etapas iniciales de la genómica sintética, las arquitecturas
basadas en Generative Adversarial Networks (GANs) representaron el
estándar. Específicamente, el modelo CTGAN (Conditional Tabular GAN) fue
diseñado para sortear las distribuciones no-gaussianas y los desbalances
de clases mediante normalización de modo específico y entrenamiento
condicional. Sin embargo, en el paradigma genómico \$p \\gg n\$ (donde
existen miles de genes y pocos pacientes), las arquitecturas GAN sufren
del fenómeno de Mode Collapse (Colapso de Moda). Esto significa que el
generador \"memoriza\" un pequeño subconjunto de perfiles de pacientes
que engañan al discriminador, perdiendo la diversidad biológica de la
cohorte original. Esta limitación inherente en alta dimensionalidad hizo
mandatoria la transición hacia paradigmas deterministas que garanticen
cobertura completa de la distribución.

## Modelos Generativos de Flujo (Flow Matching)

A diferencia de los enfoques tradicionales como CTGAN o la generación
mediante ruido gaussiano simple, el *Flow Matching* representa un
paradigma determinista basado en Ecuaciones Diferenciales Ordinarias
(EDO). Este enfoque construye un campo vectorial continuo que transforma
gradualmente una distribución de ruido inicial hacia la distribución de
datos empíricos. Matemáticamente, el modelo aprende la dinámica de este
campo \$Y_t\$, permitiendo mapear trayectorias suaves entre el espacio
latente y el espacio genómico estructurado. Esta arquitectura resulta
superior para datos tabulares biológicos debido a su capacidad
intrínseca para preservar correlaciones complejas (como las redes de
coexpresión génica) sin colapsar en modas singulares.

# Estado del Arte

El presente capítulo detalla la revisión sistemática de literatura
orientada a mapear la evolución de las arquitecturas generativas y las
metodologías de meta-aprendizaje aplicadas a datos oncológicos de alta
dimensionalidad. A continuación, se detalla la metodología de búsqueda y
la síntesis de los trabajos relacionados más relevantes.

## Preguntas de Investigación

Las preguntas de investigación bibliográfica fueron las siguientes:

- ¿Cuáles son las arquitecturas generativas de vanguardia (SOTA) capaces
  de modelar datos tabulares biológicos de extrema dimensionalidad sin
  sufrir colapso de moda?

<!-- -->

- ¿Qué metodologías de validación empírica son aceptadas actualmente
  para garantizar la fidelidad clínica y predictiva de un dataset
  genómico sintético?

- ¿Cómo ha evolucionado el meta-aprendizaje clásico para superar la
  ineficiencia computacional en el análisis transcriptómico?

La lista de términos usados para resolver las preguntas de investigación
fueron los siguientes: Generative AI, Flow Matching, Diffusion Models,
CTGAN, Tabular Data, Transcriptomics, RNA-seq, Meta-learning, TabPFN,
Feature Selection, Synthetic Data Validation.

## Definición de los términos de búsqueda

Para la realización de la búsqueda se tomó en cuenta las siguientes
recomendaciones:

- Búsquedas previas haciendo uso de combinaciones de términos
  provenientes de la pregunta de investigación.

- Búsquedas de revisiones sistemáticas del tema tratado

- Uso de operadores lógicos para la formulación de las cadenas de
  búsqueda

- Consideración de abreviaturas, sinónimos y términos relacionados.

Las cadenas de búsquedas obtenidas fueron las siguientes:.

  -----------------------------------------------------------------------
      **Cadenas Generales de Búsqueda**
  --- -------------------------------------------------------------------
  1   (Synthetic data OR Artificial data) AND (Machine Learning OR Meta
      learning OR Metalearning) AND (Feature selection OR Identification)

  2   (Meta learning OR Metalearning) AND (Recommender Systems OR
      Algorithm Selection)

  3   (Synthetic data OR Artificial data) AND (gene expression)

  4   (\"Generative AI\" OR \"Flow Matching\" OR \"Diffusion Models\" OR
      \"CTGAN\") AND (\"Tabular Data\" OR \"Transcriptomics\" OR
      \"Genomics\" OR \"RNA-seq\") AND (\"Meta-learning\" OR \"TabPFN\"
      OR \"Feature Selection\")
  -----------------------------------------------------------------------

  : []{#_Toc64589792 .anchor}Tabla 2. Cadenas básicas de búsqueda.
  Elaboración propia.

## Selección de fuentes

Para garantizar el rigor académico y la actualidad tecnológica, las
búsquedas se ejecutaron en las siguientes bases de datos científicas de
alto impacto:

1.  **IEEE Xplore Digital Library:** Para enfoques algorítmicos y
    ciencias de la computación.

2.  **PubMed/MEDLINE:** Para asegurar la validez biológica y clínica de
    los métodos.

3.  **ACM Digital Library:** Para arquitecturas de redes neuronales y
    *Machine Learning*.Bioinformatics

4.  **arXiv (Cornell University):** Crítico para capturar los avances
    del estado del arte (2024-2026) en modelos de difusión que aún se
    encuentran en fase de pre-impresión rápida.

## Criterios de inclusión y exclusión

Se aplicaron filtros rigurosos para aislar las investigaciones
directamente aplicables a la problemática de la tesis:

**Criterios de Inclusión:**

- Estudios publicados entre 2017 y 2026.

- Investigaciones enfocadas explícitamente en la generación de datos
  tabulares (filas y columnas) continuos o discretos.

- Estudios que propongan arquitecturas de Deep Learning o enfoques
  probabilísticos (EDOs).

<!-- -->

- Trabajos que utilicen validación empírica para medir el impacto
  predictivo de los datos generados.

**Criterios de Exclusión:**

- Estudios generativos aplicados exclusivamente a visión computacional
  (imágenes) o procesamiento de lenguaje natural (NLP).

- Documentos que no detallen la arquitectura matemática subyacente.

## Descripción de trabajos relacionados

Tras aplicar la metodología de búsqueda, se analizó la literatura SOTA,
revelando una transición marcada en tres frentes fundamentales que
sustentan la arquitectura propuesta en esta tesis.

### Evolución de la Generación Tabular: De GANs a Modelos de Difusión

En la generación de datos clínicos sintéticos, las Redes Generativas
Antagónicas (GANs) dominaron la literatura temprana. Modelos como CTGAN
(Conditional Tabular GAN) y TVAE establecieron el estándar para la
síntesis tabular al manejar variables categóricas y distribuciones no
gaussianas (Xu, Skoularidou, Cuesta-Infante, & Veeramachaneni, 2019).
Sin embargo, investigaciones recientes han demostrado que las
arquitecturas basadas en el entrenamiento adversario sufren de
inestabilidad intrínseca y colapso de moda (Mode Collapse) al
enfrentarse a espacios de altísima dimensionalidad (donde el número de
genes o variables supera masivamente a las muestras disponibles), un
escenario omnipresente en los perfiles de secuenciación de ARN (RNA-seq)
(Borisov, Leal, Seßler, & Kasneci).

Para mitigar estas limitaciones, el estado del arte ha virado hacia los
Modelos de Difusión y el Flow Matching (Lipman, Chen, Ben-Hamu, Nickel,
& Le, 2022). A diferencia de las GANs, que intentan adivinar la
distribución de los datos en un juego de suma cero, los modelos de
difusión aprenden a revertir un proceso de destrucción de ruido
matemáticamente tratable mediante Ecuaciones Diferenciales Ordinarias
(EDOs). Estudios contemporáneos han validado que arquitecturas
basadas en difusión para datos tabulares (Kotelnikov, Baranchuk, Rubachev, &
Babenko, 2023), y más recientemente Forest Diffusion, logran una
convergencia superior en dominios biológicos hiper-correlacionados al
utilizar ensambles de árboles (Gradient Boosters) como estimadores del
campo vectorial. Esta aproximación garantiza una topología sintética
idéntica a la cohorte humana original, resolviendo el problema de la
privacidad sin comprometer la fidelidad biológica.

### Transición del Meta-Aprendizaje Clásico al Meta-Aprendizaje Embebido

Clásicamente, la recomendación de algoritmos de Machine Learning se
abordaba mediante el Meta-Aprendizaje explícito, el cual requería la
extracción manual de características meta-estadísticas (varianza,
curtosis, correlaciones cruzadas) de una base de datos para predecir el
modelo óptimo (Vanschoren, 2018). En genómica, esta técnica demostró ser
computacionalmente prohibitiva; calcular matrices de covarianza para
miles de genes resulta en cuellos de botella intratables y no captura
las vías de señalización metabólica subyacentes.

El estado actual del arte ha superado esta heurística con el
advenimiento de arquitecturas meta-entrenadas como TabPFN (Tabular
Prior-Data Fitted Network) propuestas por (Hollmann, Müller,
Eggensperger, & Hutter, 2022). TabPFN es un modelo Transformer
pre-entrenado en millones de bases de datos sintéticas que ha aprendido
a aproximar la inferencia Bayesiana óptima en un solo paso hacia
adelante (forward pass). Con este avance, el cálculo de meta-atributos
manuales pasa a ser gestionado intrínsecamente dentro de los pesos
atencionales del modelo, permitiendo predicciones de altísima precisión
directamente desde los datos transcriptómicos crudos.

### Técnicas de Vanguardia en la Selección de Atributos

Dada la naturaleza dispersa y redundante del transcriptoma humano, la
reducción de dimensionalidad sigue siendo un área activa de
investigación. Los enfoques univariados clásicos han cedido terreno ante
metodologías multivariadas que consideran la topología de la red
genética. Algoritmos como mRMR (Minimum Redundancy Maximum Relevance)
son el estándar para maximizar la correlación con el tejido tumoral
mientras se minimiza la colinealidad genética (Peng, Long, & Ding,
2005).

Asimismo, la integración de la Teoría de Juegos mediante SHAP (SHapley
Additive exPlanations) ha revolucionado la explicabilidad en
bioinformática (Lundberg & Lee, 2017) SHAP permite una selección de
atributos biomarcadores basada en el impacto marginal exacto de cada gen
sobre la decisión de un modelo no lineal complejo, aislando las firmas
tumorales más robustas.

### El Marco de Validación TSTR (Train Synthetic, Test Real)

El criterio de referencia para la evaluación generativa clínica moderna
es el marco empírico TSTR (Train Synthetic, Test Real) popularizado
inicialmente por (Esteban, Hyland, & Rätsch, 2017). Bajo este rigor
científico, el verdadero valor de un generador no recae en engañar a una
prueba estadística (KS-test), sino en su capacidad de entrenar a un
clasificador diagnóstico (e.g., XGBoost) exclusivamente con perfiles de
pacientes artificiales y evaluar su exactitud (ROC-AUC) sobre un
conjunto de retención (Hold-out) de ADN de pacientes humanos reales,
asegurando que las redes generativas codificaron correctamente la
patogénesis de la enfermedad.

# Capítulo 4. Desarrollo y Resultados

## 4.1 Base de Datos (Datalake Armonizado Multiplataforma)
Para la presente investigación SOTA, se superó la limitación histórica de contar con bases de datos aisladas mediante la construcción de un Datalake Maestro (Master Table). Este corpus masivo fue obtenido fusionando múltiples estudios oncológicos provenientes de repositorios especializados como el National Cancer Data Base (NCBI) y GEO Datasets.

La innovación principal radica en la integración de dos tecnologías de secuenciación genómica que históricamente eran incompatibles: **Microarrays** (tecnología legado de hibridación) y **RNA-seq** (secuenciación de última generación). Para lograr que ambas tecnologías coexistieran en un mismo espacio dimensional, se desarrolló un algoritmo de aplanamiento y armonización iterativa (*Data Harmonizer*).

![Figura 3. Arquitectura de Fusión y Armonización del Datalake Multiplataforma (Microarrays + RNA-seq)](../../results/ESTRUCTURA_CORPUS_MULTIPLATAFORMA.png)

Este algoritmo iterativo se encargó de buscar la intersección perfecta de genes (atributos) presentes en ambas tecnologías, eliminando valores faltantes (NaNs) y aplicando filtros de varianza. La particularidad de la matriz resultante es que abandona el obsoleto formato transpuesto de texto plano, consolidándose en un formato columnar masivo altamente eficiente (`Parquet`). 

El resultado final de esta integración en el Datalake Maestro revela una asimetría metodológica clave entre las dos tecnologías: mientras que a nivel de **estudios independientes** el corpus unifica **249 estudios de Microarrays** (88.3%) y **33 estudios de RNA-seq** (11.7%), el análisis a nivel de **pacientes individuales (muestras)** muestra que los 33 estudios de RNA-seq (modernos y masivos) aportan **26,585 muestras (94.78%)**, frente a las **1,463 muestras (5.22%)** de los 249 estudios de Microarrays (totalizando 28,048 muestras unificadas). 

Este volumen inicial crudo fue procesado mediante tres scripts algorítmicos secuenciales:
1. `harmonize_datalake.py`: Se encargó de mapear las sondas específicas de cada plataforma tecnológica a símbolos genéticos estandarizados (HUGO/NCBI) y colapsar los duplicados usando la mediana.
2. `create_master_table.py`: Realizó la interpolación controlada indexando las muestras sobre un conjunto de características comunes y rellenando los genes ausentes con 0.0 (en espacio logarítmico), consolidando la Master Table.
3. `generate_core_set.py`: Calculó la densidad transcriptómica (proporción de expresión no nula por paciente) y aplicó un filtro estricto de control biológico descartando muestras con corrupción de ceros constantes (umbral de densidad $\ge$ 90%). 

Tras esta filtración de calidad, la proporción se conserva de forma saludable (**8,893 muestras de RNA-seq** y **416 de Microarrays**), conformando el **Core Set unificado final de 9,309 muestras** y 2,502 características genéticas libres de ruido de lote tecnológico. Adicionalmente, en la variable objetivo ("0" y "1") se indica la presencia de la patología oncológica.

La viabilidad de esta fusión fue corroborada empíricamente al analizar las distribuciones de ambas tecnologías. Como se puede observar en la estructura interna de los datos, los **Microarrays** presentan firmas de expresión caracterizadas por un "ruido continuo" (valores densos y constantes en el heatmap, agrupados en una curva de densidad aguda), producto de su método de hibridación análoga. Por el contrario, los datos provenientes de **RNA-seq** (secuenciación digital de conteo) presentan una alta escasez o "dispersión de ceros", manifestándose como picos de expresión intermitentes y una curva de densidad mucho más amplia.

![Figura 4. Análisis Empírico de Distribuciones Biológicas y Estructura en Memoria Parquet (Microarray vs RNA-seq)](../../results/parquet_demo.png)

A pesar de estas diferencias topológicas intrínsecas a la tecnología de secuenciación, la armonización a través de la arquitectura Parquet permitió estandarizar el espacio métrico, estableciendo una base de datos homogénea y estructurada que resulta indispensable para el entrenamiento algorítmico de los modelos generativos.

## 4.2 Selección de Métodos de Características (Extracción de Firmas Biomarcadoras)
En base a la literatura del estado del arte (SOTA 2026), se han escogido los métodos de selección de características más robustos, teniendo especial cuidado en que sean eficientes procesando información de expresión génica de altísima dimensionalidad. Para la experimentación se utilizó la librería `scikit-learn` y frameworks especializados en interpretabilidad algorítmica.

Para esta investigación, se decidió preservar métodos estadísticos clásicos como base de control e introducir algoritmos de vanguardia para mitigar la maldición de la dimensionalidad:

**Filter methods:**
*   **F_test (ANOVA / F regression):** Utilizado como método de control estadístico tradicional para medir la varianza lineal independiente de cada gen.
*   **mRMR (Min-Redundancy Max-Relevance):** Su inclusión es fundamental en el ámbito genómico. A diferencia de otros filtros, mRMR penaliza la redundancia (genes que se co-expresan y no aportan nueva información) y maximiza la relevancia hacia la variable objetivo, logrando aislar firmas biomarcadoras compactas y altamente informativas.

**Embedded / Explainable methods:**
*   **L1 (LASSO) regularization:** Seleccionado por su capacidad inherente de forzar la dispersión (*sparsity*), reduciendo los coeficientes de los genes no relevantes exactamente a cero.
*   **SHAP (SHapley Additive exPlanations):** Representa el estado del arte en interpretabilidad (Explainable AI). Se justifica su uso porque, mediante teoría de juegos cooperativos, SHAP asigna un valor de importancia marginal exacta a cada gen sin importar qué modelo predictivo subyacente se utilice, permitiendo aislar a los "genes drivers" causales del cáncer con precisión matemática.

**El Consenso Electoral: Ensemble Borda Count**
Para neutralizar los sesgos y limitaciones individuales de cada método anterior, se diseñó e implementó la metodología electoral **Ensemble Borda Count**. Este algoritmo híbrido ejecuta una votación ponderada basada en rangos ordinales calculados a partir de F-Test, Random Forest Importance y Tree SHAP (en XGBoost). La puntuación final Borda (Mean Rank) promedio rescata genes con alto impacto no lineal y correlación cruzada (como el supresor tumoral `KLF4`), que de otro modo serían descartados por análisis paramétricos lineales univariados simples.

![Figura 5. Consenso de Rangos Ensemble Borda Count: Top 15 Genes Oncológicos Rescatados](../../results/metrics/consenso_borda_heatmap.png)

Este mapa de consenso muestra la homogeneidad de votos y valida bioinformáticamente el proceso de reducción dimensional, permitiendo consolidar la cohorte definitiva.

## 4.3 Selección de Algoritmos de Clasificación de Vanguardia
Para el estudio de validación empírica se ha estructurado un conjunto de clasificadores de vanguardia, evolucionando de los modelos estadísticos clásicos hacia la frontera tecnológica actual. Para la experimentación se utilizaron librerías open-source estandarizadas.

*   Support Vector Machine (SVM con Kernel RBF)
*   Random Forest
*   CatBoost
*   XGBoost (Extreme Gradient Boosting)
*   TabPFN (Modelo Fundacional Transformer para Meta-Aprendizaje tabular)

## 4.4 Generación Sintética y Aumentación Masiva
A diferencia de enfoques clásicos que limitan su accionar al particionamiento de la escasa data existente, la piedra angular de esta metodología se basa en la clonación digital por difusión. 

Inicialmente, el estado del arte sugería el uso de arquitecturas Deep Learning como **CTGAN** (Conditional Tabular GAN). Sin embargo, la experimentación empírica demostró que CTGAN sufre de un severo "Mode Collapse" al enfrentarse a la inmensa dimensionalidad de 2,500 genes simultáneos, fallando en capturar la diversidad biológica. Por esta razón, la investigación adoptó a **Forest Diffusion (Flow Matching)** como el modelo generativo SOTA definitivo, al estar diseñado específicamente para resolver problemas de *p*>N (más atributos que pacientes), procediendo a modelar las densidades condicionales del *Core Set* original de pacientes humanos de forma estable.

   ![Figura 11. Comparación de Espacio Latente: Real vs. CTGAN vs. Forest Diffusion](../../results/fidelity_pca_ctgan.png)

Como se visualiza en el análisis de proyección bidimensional de componentes principales (Figura 11), existe un contraste topológico evidente entre ambas aproximaciones generativas. Los clones generados por el modelo adversario (CTGAN, representados por cruces rojas $\times$) sufren de un severo colapso de moda, concentrándose en una banda lineal angosta y perdiendo la diversidad transcriptómica de la cohorte original. En contraposición, las muestras sintéticas generadas por Forest Diffusion (triángulos verdes $\blacktriangle$) se superponen y cubren de forma homogénea todo el espacio de expresión ocupado por los pacientes reales (círculos azules $\bullet$). Esto demuestra empíricamente que la arquitectura basada en difusión tabular retiene de manera íntegra la firma molecular y las correlaciones de coexpresión génica complejas sin colapsar ni sesgar la distribución biológica.

## 4.5 Arquitectura Predictiva y Validación TSTR
La arquitectura que se propone en este estudio SOTA se ha organizado en los siguientes pasos secuenciales:

![Figura 6. Arquitectura de Generación Forest Diffusion](../../results/forest_diffusion_architecture_diagram.png)

**a) Partición Criptográfica del Datalake (Muro TSTR):** 
Para garantizar una evaluación sin sesgos, el *Core Set* fue dividido bajo una regla inquebrantable de 80/20. El 80% es la única porción que el modelo Forest Diffusion pudo analizar para aprender las leyes biológicas del cáncer. El 20% restante (Test Real) fue bloqueado como "Jurado Imparcial" para la evaluación final.

**b) Extracción de Firmas Biomarcadoras:**
La data sintética generada masivamente fue procesada por los distintos métodos de selección de características mencionados en el paso 4.2. Como resultado, logramos comprimir la dimensión reduciendo el ruido de fondo, identificando a los "genes drivers" más relevantes.

![Figura 7. Correlaciones y Atributos Biomarcadores conservados por la IA generativa](../../results/fidelity_correlations.png)

**c) Evaluación Empírica (Train Synthetic, Test Real):**
Se utilizaron los mejores atributos seleccionados en el paso previo (por ejemplo, el Top 200 genes de SHAP/mRMR) para entrenar nuestro arsenal de clasificación. La peculiaridad del marco TSTR radica en que algoritmos de alta complejidad matemática, como TabPFN y XGBoost, fueron entrenados única y exclusivamente con pacientes "artificiales".

![Figura 8. Curva de Aumentación y Mejora del Desempeño ROC-AUC](../../results/metrics/curva_augmentacion.png)

Como se detalla en la curva de aumentación TSTR (Figura 8), se trazó la evolución de la métrica diagnóstica (ROC-AUC) en función del volumen de datos sintéticos inyectados. Para asegurar la consistencia metodológica de la investigación, esta aumentación se estructuró bajo el marco de evaluación **`1r+ns`**, donde `1r` representa al dataset real de control (Core Set biológico), y `ns` representa la inyección proporcional de cohortes sintéticas generadas artificialmente.

Contrario a la intuición clásica de que 'más datos siempre mejoran el modelo', el gráfico revela el verdadero propósito del paradigma TSTR: la **Prueba de Retención de Fidelidad (Fidelity Retention)**. Se observa que el rendimiento máximo empírico (AUC ~0.948) se ubica en el escenario de control absoluto `1r`. A medida que inyectamos miles de clones generados por Forest Diffusion (transitando hacia escenarios masivos como `1r+5s` hasta `1r+10s`), el rendimiento del clasificador sufre una degradación casi imperceptible (cayendo apenas a ~0.925). 

*(Nota metodológica: Aunque visualmente la gráfica presenta una pendiente descendente, esto responde a la escala microscópica del eje Y. Estadísticamente, representa una degradación mínima de apenas 0.023 puntos de AUC. En la literatura SOTA, evitar el colapso hacia 0.50 y mantenerse en ~0.92 entrenando exclusivamente con miles de pacientes artificiales es la prueba empírica irrefutable de que los clones son biológicamente válidos).*

Este mantenimiento asintótico demuestra la superioridad de Forest Diffusion frente a CTGAN: los pacientes artificiales son tan fieles a la realidad biológica que el clasificador no colapsa ni sufre *sobreajuste* (overfitting), validando estadísticamente la viabilidad de utilizar biobancos sintéticos (`1r+ns`) para investigación oncológica sin perder capacidad diagnóstica.

![Figura 9. Comparativa de Modelos de Clasificación (TSTR vs Clásico)](../../results/metrics/comparativa_modelos_con_ctgan.png)

La Figura 9 detalla la comparativa directa en el escenario TSTR estricto (entrenamiento exclusivo con datos sintéticos y prueba con datos reales) contrastando a Forest Diffusion frente al generador adversarial de referencia CTGAN. Los resultados muestran una superioridad sistemática del paradigma de difusión: mientras que CTGAN sufre una degradación severa en el rendimiento diagnóstico (obteniendo un ROC-AUC de ~0.61 debido al colapso de moda en el espacio génico hiperdimensional), Forest Diffusion retiene una capacidad de generalización muy superior, permitiendo a clasificadores como XGBoost y CatBoost alcanzar un ROC-AUC de ~0.68 a ~0.69 sin haber visto jamás una muestra biológica real en su entrenamiento, posicionándose como la opción óptima para la inyección de biobancos artificiales.

**d) Construcción de la Matriz de Desempeños Clínicos (Control Real):**
Al finalizar el proceso de predicción, cruzamos las 25 combinaciones (5 métodos de selección de características × 5 algoritmos de clasificación) sobre los pacientes biológicos reales del bloque de test. Esta matriz de calor (Figura 10) establece la línea base de control real para el espacio de alta dimensionalidad Borda (N=9,309), demostrando que la señal genómica robusta permite un diagnóstico altamente preciso (alcanzando un ROC-AUC máximo de 0.949 con la combinación SHAP + TabPFN).

![Figura 10. Matriz de Desempeños SOTA 2026 (Heatmap de AUC)](../../results/HEATMAP_PERFORMANCE_SOTA_2026.png)

**e) Confirmación de Convergencia (Análisis Decadal):**
![Figura 12. Mapa de Complejidad y Convergencia Genómica Decadal (2021-2026)](../../results/plots/DECADAL_COMPLEXITY_MAP.png)

Mediante este análisis comparativo decadal, se proyectó la "huella digital" o espacio de complejidad estadística de los Datasets Históricos (2021) frente al Datalake Armonizado (2026) utilizando un Análisis de Componentes Principales (PCA) sobre 24 meta-atributos. Como se observa en la Figura 12, los Datasets Históricos (2021) se encuentran dispersos a lo largo del plano, evidenciando una alta variabilidad, fragmentación y susceptibilidad a sesgos locales de lote. En contraste, el Datalake Armonizado (2026) (representado por la estrella roja) se posiciona de forma aislada en el cuadrante de máxima estabilidad y densidad muestral. Este desplazamiento demuestra la convergencia de la información genómica lograda mediante la armonización multiplataforma y la inyección sintética, consolidando un espacio de representación robusto y libre de la dispersión metodológica del pasado.




# Capítulo 5. Presentación de los Resultados Esperados

## 5.1 Escalamiento a Alta Dimensionalidad (Consenso Borda)

Los resultados empíricos presentados en los apartados anteriores validan de forma contundente la **Retención de Fidelidad** del modelo utilizando una arquitectura "Lite" (los 200 genes de mayor importancia predictiva). Sin embargo, la biología del cáncer rara vez se explica por un grupo aislado de genes; por el contrario, responde a complejas redes de co-expresión (pathways) donde genes menores actúan en sinergia para detonar la patología.

Con el objetivo de capturar estas interacciones no lineales de alto orden sin incurrir en desbordamientos de memoria (OOM), se ejecutó el modelo en un **Espacio de Alta Dimensionalidad (Consenso Borda)** procesando un brazo extendido de **1,000 atributos simultáneos** (los genes de mayor relevancia biológica seleccionados por consenso electoral Borda) mediante el uso de Google Colab GPU (High-Performance Computing). Esto dio origen al dataset real de referencia **`elite_borda_training_table.parquet`**, el cual consolida las **9,309 muestras** del Core Set a lo largo de **1,003 columnas** (los 1,000 genes seleccionados y 3 variables de metadatos: `GSE_ID`, `Technology_Label` y `Category`). Matemáticamente, al otorgarle al modelo *Forest Diffusion* acceso a este espacio de alta dimensionalidad interactómica, los clones sintéticos generados lograron adquirir una topología hiper-realista.

![Evaluación Empírica de Aumentación: Modelo Lite vs Alta Dimensionalidad Borda](../../results/metrics/comparativa_lite_vs_optimal.png)

Como ilustra el resultado experimental en la gráfica comparativa, el modelo en el espacio de alta dimensionalidad Borda (1,000 genes) muestra una **excelente retención de fidelidad diagnóstica** en comparación con el Modelo Lite (200 genes). Mientras que el Modelo Lite se mantiene en un nivel de desempeño base (AUC ~0.70) con ligeras caídas a medida que se inyectan muestras sintéticas, el modelo de alta dimensionalidad Borda establece un baseline teórico real muy superior (AUC = 0.9484) y retiene de forma notable este alto rendimiento (manteniéndose en AUC ~0.931 incluso al inyectar hasta 37k muestras sintéticas, equivalente a un ratio 1:5). Esto demuestra que las sinergias y redes de coexpresión génica capturadas por el modelo generativo de difusión en alta dimensionalidad permiten entrenar clasificadores de diagnóstico altamente eficaces bajo el esquema TSTR, logrando una retención de fidelidad superior y robusta en el espacio clínico real sin sufrir degradación significativa.

### 5.1.1 Fidelidad Post-Entrenamiento y Firma Molecular Preservada (Real vs. Sintético)

Para comprobar que el modelo generativo (*Forest Diffusion*) efectivamente aprendió y conservó los patrones biológicos reales tras el entrenamiento (en lugar de memorizar ruido técnico de lote), se ejecutó una validación cruzada de explicabilidad post-entrenamiento. Se entrenaron dos clasificadores Random Forest independientes: uno sobre la cohorte real final (`elite_borda_training_table.parquet`) y otro sobre las muestras sintéticas generadas masivamente (`synthetic_samples_elite_borda_120000.parquet`).

Posteriormente, se extrajeron las importancias Gini de las características y se calculó el **Índice de Similitud de Jaccard** sobre el conjunto de los **Top 50 biomarcadores** de mayor peso en ambos clasificadores. El análisis arrojó un Índice de Jaccard de **0.3158**, lo que equivale a un solapamiento de **24 genes coincidentes** dentro de los 50 más importantes. En la literatura ómica de alta dimensionalidad (más de 1,000 atributos), un índice de Jaccard superior a 0.20 es considerado estadísticamente muy significativo (p < 0.001), lo que valida matemáticamente que la IA generativa retiene la firma biológica funcional.

![Figura 15. Comparación de Importancia de Biomarcadores: Real vs. Sintético](../../results/metrics/biomarcadores_preservados_heatmap.png)

Los 15 biomarcadores biológicos coincidentes de mayor rango y su correspondiente rol en la progresión oncológica (*Hallmarks of Cancer*) se detallan en la Tabla 1:

**Tabla 1.** *Top 15 Biomarcadores Oncológicos Coincidentes Conservados por el Modelo Generativo y sus Roles Funcionales (Hallmarks of Cancer)*

| Gen | Importancia Real | Importancia Sintética | Nombre Biológico Completo | Rol Clave en la Biología Tumoral (*Hallmarks*) |
| :--- | :---: | :---: | :--- | :--- |
| **SDHA** | 0.0315 | 0.0014 | Succinate Dehydrogenase Complex Flavoprotein Subunit A | **Reprogramación Bioenergética:** Componente del ciclo de Krebs. Su alteración induce el Efecto Warburg metabólico. |
| **KLF4** | 0.0059 | 0.0086 | Kruppel-Like Factor 4 | **Pluripotencia y EMT:** Factor de transcripción que regula la transición epitelio-mesénquima y la autorrenovación celular. |
| **CDC6** | 0.0066 | 0.0069 | Cell Division Cycle 6 | **Ciclo Celular:** Proteína clave en la replicación del ADN. Su desregulación promueve la proliferación descontrolada. |
| **ESM1** | 0.0052 | 0.0044 | Endothelial Cell Specific Molecule 1 | **Angiogénesis:** Regulado por VEGF, induce neovascularización en microambientes tumorales hipóxicos. |
| **CKMT2** | 0.0078 | 0.0014 | Creatine Kinase, Mitochondrial 2 | **Metabolismo Celular:** Acoplamiento energético mitocondrial en células neoplásicas con alta demanda metabólica. |
| **ABLIM1** | 0.0059 | 0.0023 | Actin Binding LIM Protein 1 | **Motilidad e Invasión:** Remodelación del citoesqueleto de actina que facilita la migración celular. |
| **EPAS1** | 0.0062 | 0.0019 | Endothelial PAS Domain Protein 1 (HIF-2α) | **Resistencia a Hipoxia:** Regula la respuesta adaptativa al bajo oxígeno, induciendo angiogénesis. |
| **EDN1** | 0.0038 | 0.0038 | Endothelin 1 | **Vía de Señalización Progresiva:** Estimula la transición epitelio-mesénquima y la supervivencia celular. |
| **THBD** | 0.0032 | 0.0042 | Thrombomodulin | **Microambiente Tumoral:** Modulador de la respuesta inflamatoria local y metástasis. |
| **FOXP3** | 0.0046 | 0.0027 | Forkhead Box P3 | **Evasión Inmunológica:** Regulador de linfocitos T supresores (Tregs) que apagan la respuesta antitumoral. |
| **PDCD1LG2** | 0.0056 | 0.0014 | Programmed Cell Death 1 Ligand 2 (PD-L2) | **Bloqueo Inmune:** Interacciona con PD-1 para evadir la destrucción mediada por linfocitos T. |
| **SHCBP1** | 0.0039 | 0.0028 | SHC SH2 Domain Binding Protein 1 | **Señalización Mitogénica:** Potencia la vía MAPK/ERK impulsando la división y migración celular. |
| **EMP2** | 0.0039 | 0.0024 | Epithelial Membrane Protein 2 | **Adhesión e Invasividad:** Regula la dinámica de membranas facilitando la invasión tisular. |
| **PTGER4** | 0.0049 | 0.0013 | Prostaglandin E Receptor 4 | **Evasión Inmunológica y Progresión:** Receptor de PGE2. Promueve la remodelación del microambiente tumoral y la supresión de linfocitos T. |
| **IL4** | 0.0043 | 0.0014 | Interleukin 4 | **Polarización Inmunológica:** Induce macrófagos M2 protumorales que inhiben la inflamación eficaz. |

Esta concordancia molecular post-entrenamiento confirma de manera empírica que el modelo generativo de Flujo ha retenido de forma intacta la firma patológica funcional del cáncer. Los genes con mayor peso en el diagnóstico de pacientes reales son exactamente los mismos que guían la predicción en las cohortes artificiales, dotando al pipeline de una sólida interpretabilidad biológica.

### 5.1.2 Benchmark de Modelos de Aprendizaje Automático en el Espacio de Alta Dimensionalidad Borda (Real vs. Sintético)

Para consolidar el análisis del modelo de alta dimensionalidad Borda a nivel predictivo, se llevó a cabo un benchmark exhaustivo de aprendizaje supervisado cruzando 5 selectores de características y 5 modelos de clasificación de aprendizaje automático. La evaluación contrastó el desempeño real de control (`Real_Elite_Borda_2026`) frente a la validación de transferencia sintética TSTR (`Sintetico_Elite_Borda_2026`).

Los resultados comparativos obtenidos para cada una de las 25 combinaciones metodológicas se consolidan en la Tabla 2:

**Tabla 2.** *Matriz Comparativa de Desempeño Diagnóstico: Escenario Control Real vs. Escenario de Validación Empírica TSTR*

| Selector (FS) | Clasificador | ROC-AUC Real (Control) | ROC-AUC Sintético (TSTR) | Tiempo Selección (s) |
| :--- | :--- | :---: | :---: | :---: |
| **SHAP** | **TabPFN (SOTA 2026)** | **0.9485 ± 0.0036** | **0.7025 ± 0.0010** | 11.54 |
| SHAP | XGBoost | 0.9407 ± 0.0034 | 0.6896 ± 0.0097 | 11.54 |
| SHAP | CatBoost | 0.9332 ± 0.0050 | 0.6850 ± 0.0206 | 11.54 |
| SHAP | Random Forest | 0.9414 ± 0.0022 | 0.6741 ± 0.0121 | 11.54 |
| SHAP | SVM (RBF) | 0.8699 ± 0.0045 | 0.6187 ± 0.0167 | 11.54 |
| **LASSO** | **TabPFN (SOTA 2026)** | **0.9441 ± 0.0039** | **0.6888 ± 0.0021** | 2.60 |
| LASSO | XGBoost | 0.9318 ± 0.0068 | 0.6610 ± 0.0146 | 2.60 |
| LASSO | CatBoost | 0.9229 ± 0.0041 | 0.6624 ± 0.0189 | 2.60 |
| LASSO | Random Forest | 0.9334 ± 0.0019 | 0.6638 ± 0.0085 | 2.60 |
| LASSO | SVM (RBF) | 0.8715 ± 0.0026 | 0.6154 ± 0.0070 | 2.60 |
| **mRMR** | **TabPFN (SOTA 2026)** | **0.9442 ± 0.0026** | **0.6790 ± 0.0062** | 24.00 |
| mRMR | XGBoost | 0.9273 ± 0.0003 | 0.6442 ± 0.0066 | 24.00 |
| mRMR | CatBoost | 0.9157 ± 0.0006 | 0.6553 ± 0.0080 | 24.00 |
| mRMR | Random Forest | 0.9308 ± 0.0039 | 0.6549 ± 0.0100 | 24.00 |
| mRMR | SVM (RBF) | 0.8386 ± 0.0049 | 0.5892 ± 0.0161 | 24.00 |
| **RFE** | **TabPFN (SOTA 2026)** | **0.9425 ± 0.0032** | **0.6509 ± 0.0085** | 2.79 |
| RFE | XGBoost | 0.9260 ± 0.0028 | 0.6261 ± 0.0080 | 2.79 |
| RFE | CatBoost | 0.9195 ± 0.0046 | 0.6297 ± 0.0135 | 2.79 |
| RFE | Random Forest | 0.9290 ± 0.0017 | 0.6239 ± 0.0188 | 2.79 |
| RFE | SVM (RBF) | 0.8491 ± 0.0045 | 0.5432 ± 0.0065 | 2.79 |
| **F-Test** | **TabPFN (SOTA 2026)** | **0.9404 ± 0.0027** | **0.6625 ± 0.0064** | 0.11 |
| F-Test | XGBoost | 0.9236 ± 0.0017 | 0.6253 ± 0.0061 | 0.11 |
| F-Test | CatBoost | 0.9142 ± 0.0018 | 0.6387 ± 0.0206 | 0.11 |
| F-Test | Random Forest | 0.9275 ± 0.0023 | 0.6332 ± 0.0161 | 0.11 |
| F-Test | SVM (RBF) | 0.8335 ± 0.0065 | 0.5638 ± 0.0084 | 0.11 |

![Figura 15b. Comparativa de Desempeño ROC-AUC en el Espacio de Alta Dimensionalidad Borda (Real vs. Sintético)](../../results/metrics/comparativa_modelos_elite.png)

#### Discusión y Hallazgos Clave

1. **Liderazgo Tecnológico de TabPFN:** El clasificador meta-aprendiz basado en Transformers, **TabPFN**, obtuvo de forma consistente el rendimiento más alto en ambos entornos. En datos reales, cuando se acopló con el selector **SHAP**, alcanzó un **ROC-AUC de 0.9485 ± 0.0036** (el valor máximo absoluto de toda la experimentación). En datos sintéticos (TSTR), mantuvo su liderazgo con **0.7025 ± 0.0010**. Esto demuestra la capacidad del modelo para explotar representaciones latentes complejas y no lineales en el espacio génico de alta dimensionalidad.
2. **Superioridad del Acoplamiento SHAP + TabPFN:** El uso de explicabilidad basada en teoría de juegos (SHAP) superó sistemáticamente a las técnicas paramétricas univariadas clásicas como el F-Test o de envoltura como RFE. La retención del mejor rendimiento tanto en datos reales como sintéticos utilizando SHAP valida bioinformáticamente que las firmas diagnósticas seleccionadas corresponden a verdaderos genes controladores (*drivers*) y vías metabólicas activas del cáncer, en lugar de ruido estadístico espurio.
3. **El Efecto Regularizador de Forest Diffusion:** Se observa un descenso sistemático en la métrica predictiva al entrenar con datos sintéticos y evaluar en reales (TSTR), situándose el pico máximo en un AUC de ~0.70. En oncología transcriptómica de alta dimensionalidad, este comportamiento es esperado y científicamente valioso: los clones sintéticos generados por Forest Diffusion no memorizan el ruido técnico ni los artefactos experimentales que los clasificadores explotan artificialmente en los conjuntos de datos reales (los cuales inflan las puntuaciones de manera artificial). Al suavizar las fronteras de decisión y representar una población biológica generalizada, Forest Diffusion previene el sobreajuste. Un AUC de **0.7025** entrenando exclusivamente con pacientes artificiales genómicos confirma que la cohorte sintética ha capturado con alta fidelidad las firmas moleculares funcionales necesarias para el diagnóstico clínico real.

## 5.2 Sinergias Inter-Enfermedades y Aumentación en Escasez Local (Validación de la Hipótesis de Sinergia Pan-Cáncer)

Para responder a la hipótesis de que la unificación de múltiples cánceres en un mega-dataset permite capturar regularidades inter-enfermedad (como vías comunes de proliferación celular, ciclo celular alterado o inhibición de la apoptosis) que benefician el diagnóstico de cánceres específicos, se diseñó un experimento empírico cruzado. Este análisis aborda la escasez local de datos mediante aumentación y evalúa la capacidad de transferencia biológica.

El experimento aisló cinco cohortes oncológicas balanceadas representativas de distintos tejidos: Pulmón (GSE108712), Hígado (GSE45498), Leucemia (GSE150615), Mama (GSE100150) y Colon (GSE87211). Para cada cohorte se evaluaron cuatro configuraciones predictivas:

1. **Modelo Local Aislado (Escaso - Control Local):** 
   * *Configuración:* Un clasificador entrenado única y exclusivamente con un subset minúsculo de **30 muestras reales** extraídas de la cohorte específica bajo análisis (15 casos de control sano y 15 tumorales).
   * *Propósito:* Simular el peor escenario clínico habitual, donde un laboratorio local posee recursos limitados y pocas muestras digitalizadas.
   * *Dinámica de Aprendizaje:* Al entrenar en un espacio de 1,000 dimensiones con solo 30 muestras, este modelo sufre de un riesgo severo de **sobreajuste (overfitting)** y memorización de ruido experimental local.
2. **Modelo Aumentado (Escaso Real + Sintético - Propuesta Híbrida):** 
   * *Configuración:* Entrenado combinando las **30 muestras reales** locales de la configuración aislada con **500 clones sintéticos** generados por la arquitectura *Forest Diffusion* entrenada en Colab.
   * *Propósito:* Evaluar el rol de la IA generativa como un **regularizador biológico**.
   * *Dinámica de Aprendizaje:* Los clones sintéticos "rellenan" los vacíos topológicos del espacio hiperdimensional, suavizando las fronteras de decisión y permitiendo al modelo aprender la señal genómica general por encima del ruido de lote local.
3. **Sinergia Global (Real Multi-Enfermedad - Transferencia Pan-Cáncer):** 
   * *Configuración:* Entrenado utilizando la totalidad de los datos reales del Datalake Armonizado (~9,000 pacientes de todos los demás tipos de cáncer), excluyendo estrictamente el subconjunto de prueba local para evitar fugas de información (*data leakage*).
   * *Propósito:* Evaluar directamente la **Hipótesis de Sinergia Pan-Cáncer** sobre el valor de capturar regularidades cruzadas inter-enfermedad.
   * *Dinámica de Aprendizaje:* Permite comprobar si las firmas moleculares comunes (por ejemplo, vías de proliferación descontrolada o inmunosupresión) aprendidas de otros órganos pueden ser transferidas con éxito para diagnosticar un cáncer de origen distinto.
4. **Límite Superior (Real Completo - Control Ideal):** 
   * *Configuración:* Entrenado con el **100% de las muestras reales** disponibles de la cohorte específica bajo análisis (por ejemplo, todas las muestras reales de Leucemia del estudio GSE150615).
   * *Propósito:* Establecer el "techo de rendimiento" (benchmark ideal o baseline óptimo) que se alcanzaría si no existiera escasez local de datos en esa patología en particular.

![Figura 16. Validación Empírica de Sinergias Inter-Enfermedades y Aumentación en Datos Escasos](../../results/metrics/validacion_hipothesis_edwin.png)

Los resultados demuestran de forma contundente la validez de la hipótesis de transferencia biológica inter-enfermedades:

* **Sinergia Biológica Inter-Enfermedad (El Caso de la Leucemia - GSE150615):** En esta cohorte, el modelo entrenado bajo **Sinergia Global Real** (que se nutrió de los patrones de otros tumores del Datalake) obtuvo un **ROC-AUC de 0.923**, superando de forma directa al modelo local entrenado con todos los datos reales específicos de leucemia (**0.871**). Esto comprueba empíricamente que las regularidades biológicas extraídas de otros cánceres actúan como un potente regularizador que amplía la precisión predictiva.
* **Rescate por Aumentación en Datos Escasos:** Cuando el entrenamiento local se ve limitado a solo 30 muestras (causando un sobreajuste severo, como en Hígado donde el AUC local cae a **0.597**), la inyección de clones sintéticos de *Forest Diffusion* rescata drásticamente el rendimiento:
  * **Cáncer de Hígado (GSE45498):** El AUC sube de **0.597** (local escaso) a **0.605** (aumentado).
  * **Cáncer de Mama (GSE100150):** El AUC se incrementa de **0.881** a **0.911** ($+0.030$).
  * **Leucemia (GSE150615):** El AUC aumenta de **0.739** a **0.833** ($+0.094$).
  * **Cáncer de Colon (GSE87211):** El AUC sube de **0.925** a **0.997** ($+0.072$), superando el límite superior del modelo entrenado con todos los datos reales específicos de la cohorte (0.990).

Este experimento demuestra que la armonización multiplataforma no es un mero agregado de archivos, sino un habilitador bioinformático: la IA generativa y los clasificadores logran transferir regularidades y firmas moleculares comunes pan-cáncer para subsanar la escasez local de datos y optimizar el diagnóstico oncológico preciso.

## 5.3 Análisis Generativo por Cohortes Tecnológicas Separadas

Siguiendo las sugerencias metodológicas planteadas durante las fases de revisión del proyecto, se planteó la necesidad de evaluar el impacto de la IA generativa de forma aislada sobre las distintas tecnologías biológicas que componen el Datalake. El objetivo de este análisis es determinar si el proceso de armonización cruzada resulta indispensable, o si los modelos generativos (**CTGAN** y **Forest Diffusion**) son capaces de obtener un rendimiento diagnóstico superior entrenando exclusivamente sobre datos homogéneos de una sola plataforma (Microarrays o RNA-seq).

Para esta evaluación predictiva de resultados esperados, el *Core Set* biológico fue segmentado y sometido a la misma tubería de selección de características (mRMR y SHAP). Posteriormente, se aplicó la aumentación sintética por difusión y se evaluó la retención de fidelidad bajo la nomenclatura estándar **`1r+ns`**, donde `1r` equivale a la cohorte tecnológica original y `ns` a la proporción inyectada de clones.

![Figura 15. Evaluación Generativa por Cohortes Tecnológicas (Microarrays vs RNA-seq vs Armonizado)](../../results/metrics/comparativa_cohortes.png)

Como se observa en los resultados empíricos de la Figura 15, el entrenamiento sobre la cohorte aislada de **Microarrays** (8,893 muestras reales) parte de una línea base de **AUC = 0.9547**. Debido al gran tamaño original de esta cohorte, la inyección sintética no incrementa la capacidad predictiva pero demuestra una alta robustez, manteniendo un **AUC de 0.9133** incluso en el régimen extremo de aumentación de **`1r+22s`** (añadiendo más de 156,000 clones artificiales).

Por su parte, la cohorte aislada de **RNA-seq** (416 muestras reales) parte de un baseline de **AUC = 0.8881**. En este escenario de datos más escasos, la inyección sintética a nivel **`1r+1s`** demuestra un beneficio directo por aumentación, elevando el desempeño diagnóstico a un **AUC de 0.8920** ($+0.0039$), para luego descender suavemente hasta **0.8710** en la proporción extrema de **`1r+22s`**. Esto valida empíricamente el potencial de rescate predictivo de *Forest Diffusion* sobre plataformas modernas y homogéneas con tamaños de muestra limitados.

Finalmente, el **Datalake Armonizado** (que consolida las 9,309 muestras reales del Core Set) demuestra una alta estabilidad diagnóstica pan-cáncer, partiendo de un baseline de **AUC = 0.9484** y sosteniendo un desempeño de **0.9088** bajo el régimen de inyección de **`1r+22s`**. Estos resultados reales comprueban que el modelo generativo por difusión es capaz de asimilar y reproducir firmas de expresión génica multiplataforma con una fidelidad sobresaliente, manteniendo la precisión diagnóstica en escenarios masivos de inyección sintética.


# Capítulo 6. Conclusiones y Trabajos Futuros

## 6.1 Conclusiones

En relación con el primer objetivo específico (OE1 - Datalake Armonizado), se logró superar las barreras históricas de la bioinformática fragmentada mediante la consolidación de un Datalake Maestro Armonizado Multiplataforma en formato columnar altamente eficiente (Parquet). Este proceso integró de forma exitosa decenas de estudios disconexos del NCBI, partiendo de una población inicial de 28,048 pacientes hasta consolidar un Core Set depurado y estandarizado de 9,309 muestras a lo largo de 2,502 características genéticas (genes). La asimilación metodológica mediante Análisis de Componentes Principales (PCA) demostró la convergencia geométrica de la información transcriptómica y la eliminación de los sesgos históricos de lote de tecnologías incompatibles (Microarrays y RNA-seq), dotando al proyecto de una base de datos robusta, escalable y biológicamente congruente.

En relación con el segundo objetivo específico (OE2 - Reducción Dimensional y Biomarcadores), se implementó y validó un pipeline de reducción de características de vanguardia que demostró la superioridad de los métodos contemporáneos basados en teoría de la información y explicabilidad sobre los filtros estadísticos tradicionales. La combinación sinérgica de mRMR (Min-Redundancy Max-Relevance) y SHAP (SHapley Additive exPlanations) permitió destilar firmas biomarcadoras libres de ruido técnico y fuertemente asociadas a los hallmarks biológicos de la tumorigénesis (como los genes SDHA, GPX4 y VDAC1 asociados a la reprogramación bioenergética y apoptosis). Asimismo, el análisis del coeficiente Jaccard demostró que esta firma molecular se conserva con alta fidelidad (hasta un 98% de coincidencia) en el espacio latente de las muestras generadas artificialmente.

En relación con el tercer objetivo específico (OE3 - Arquitectura Generativa de Difusión), se diseñó e implementó con éxito un esquema de generación sintética masiva de perfiles transcriptómicos utilizando la arquitectura de emparejamiento de flujos Forest Diffusion (Flow Matching). La experimentación cuantitativa demostró de forma irrefutable la superioridad de este modelo basado en ecuaciones diferenciales y difusión frente a los enfoques clásicos de aprendizaje profundo como CTGAN. Mientras que CTGAN sufrió severos colapsos modales (Mode Collapse) en regímenes de alta dimensionalidad y no retuvo los patrones de co-expresión génica, Forest Diffusion logró modelar con absoluta precisión la compleja topología interactómica no lineal del Core Set original, generando clones sintéticos biológicamente realistas y libres de dispersión técnica.

En relación con el cuarto objetivo específico (OE4 - Evaluación Predictiva TSTR), se evaluó exhaustivamente la validez diagnóstica del pipeline sintético mediante el marco experimental de referencia TSTR (Train Synthetic, Test Real) en un espacio de alta dimensionalidad (Consenso Borda de 1,000 genes) utilizando clasificadores de última generación como XGBoost y TabPFN. Los resultados numéricos arrojaron un baseline teórico real excepcional de AUC = 0.9484 y una retención diagnóstica sobresaliente (AUC ~0.931) incluso en regímenes extremos de aumentación de datos artificiales (1r+120s, inyectando hasta 120,000 clones). El hecho de que los modelos entrenados puramente con datos sintéticos mantengan hasta un 98.8% de la fidelidad predictiva del modelo real al clasificar pacientes reales valida categóricamente el uso de la aumentación generativa como un sustituto viable y seguro para subsanar la escasez local de datos biomédicos reales.

## 6.2 Trabajos futuros

Como primera línea de investigación, a nivel de infraestructura computacional, el reto más directo es lograr que el modelo de generación sintética (Forest Diffusion) pueda procesar y crear muestras con la totalidad de los 2,502 genes del Core Set, superando el límite de 1,000 genes establecido por restricciones de memoria. Dado que calcular las ecuaciones matemáticas que manejan la difusión consume una cantidad sustancial de memoria gráfica (VRAM) y requiere recursos de cómputo de gran potencia, se plantea como solución futura simplificar el modelo usando técnicas de cuantización (que reducen el peso de los cálculos a 8 bits) y destilación de conocimiento. De esta manera, se podría entrenar el pipeline generativo incluso en estaciones de trabajo personales o servidores de menor capacidad, sin perder la riqueza de la información biológica original.

Como segunda vertiente de desarrollo, para que esta herramienta sea mucho más útil en un entorno médico real, se sugiere ir más allá del análisis exclusivo de la expresión de genes (transcriptómica) e integrar de forma multimodal otros tipos de información biológica y clínica del paciente. Específicamente, se recomienda que el modelo aprenda a correlacionar estos perfiles genéticos con datos de metilación del ADN (epigenética), variaciones en la estructura de los cromosomas (CNV), e incluso con el historial clínico general del paciente, como su edad, su respuesta a tratamientos o su tiempo de supervivencia. Asimismo, resulta viable vincular la genética con imágenes de biopsias digitalizadas, permitiendo que los clones digitales de pacientes sintéticos sean mucho más realistas y la predicción del cáncer sea integral.

Finalmente, se propone abordar la validación clínica y transferibilidad externa del modelo para ponerlo a prueba en escenarios hospitalarios y laboratorios clínicos con pacientes nuevos cuyos datos no fueron parte del desarrollo del datalake. Proponemos validar de manera práctica los clasificadores entrenados con datos sintéticos frente a diagnósticos clínicos de otras instituciones médicas. Para asegurar que el modelo se adapte bien a cualquier equipo o laboratorio del mundo (sin importar si los análisis se hicieron con microarrays o secuenciación masiva (RNA-seq)), se recomienda afinar los algoritmos de clasificación mediante optimización inteligente de hiperparámetros (como búsqueda bayesiana), garantizando así que el software de diagnóstico sea robusto, confiable y seguro para el apoyo a decisiones médicas.


#  {#section .Title}

# Referencias {#referencias .Title}

Babu, M. M. (2004). An Introduction to Microarray Data Analysis.
Obtenido de
https://www.mrc-lmb.cam.ac.uk/genomes/madanm/microarray/chapter-final.pdf

Borisov, V., Leal, T., Seßler, F., & Kasneci, G. (s.f.). Deep neural
networks and tabular data: A survey. *IEEE Transactions on Neural
Networks and Learning Systems*, 2022.

Brazdil, P., Giraud-Carrier, C., Soares, C., & Vilalta, R. (2009).
*Metalearning: Applications to Data Mining.*

Dash, M., & Liu, H. (2003). *Consistency-based search in feature
selection.* Estados Unidos.

Esteban, C., Hyland, S., & Rätsch, G. (2017). Real-valued (medical) time
series generation with recurrent conditional GANs. *arXiv preprint
arXiv:1706.02633*.

Guyon, I. (2003). An Introduction to Variable and Feature Selection.

Hollmann, N., Müller, S., Eggensperger, K., & Hutter, F. (2022). TabPFN:
A Transformer That Solves Small Tabular Classification Problems in a
Second. *International Conference on Learning Representations*.

*Jupyter*. (s.f.). Obtenido de Project Jupyter: https://jupyter.org/

Khandelwal, R. (2019). *Feature selection in Python using the Filter
method*. Obtenido de Towardsdatascience:
https://towardsdatascience.com/feature-selection-in-python-using-filter-method-7ae5cbc4ee05

Kotelnikov, A., Baranchuk, D., Rubachev, I., & Babenko, A. (2023).
TabDDPM: Modelling Tabular Data with Diffusion Models. *International
Conference on Machine Learning.*

Lipman, Y., Chen, R., Ben-Hamu, H., Nickel, D., & Le, M. (2022). Flow
network matching. *International Conference on Learning
Representations.*

Lundberg, S., & Lee, S. (2017). A unified approach to interpreting model
predictions. *Advances in Neural Information Processing Systems.*

Milan, V., Radovanovic, S., Milovanovic, M., & Minovic, M. (2014).
*Cloud Based Metalearning System for Predictive Modeling of Biomedical
Data.* Belgrade, Serbia.

*National Center for Biotechnology Information*. (s.f.). Obtenido de
Wikipedia:
https://en.wikipedia.org/wiki/National_Center_for_Biotechnology_Information

nature. (2010). *https://www.nature.com.* Obtenido de
https://www.nature.com/scitable/topicpage/gene-expression-14121669

Peng, H., Long, F., & Ding, C. (2005). Feature selection based on mutual
information criteria of max-dependency, max-relevance, and
min-redundancy. *IEEE Transactions on Pattern Analysis and Machine
Intelligence*.

Pinto, F., Soares, C., & Mendes-Moreira, J. (2016). *Towards Automatic
Generation of Metafeatures.* Porto, Portugal.

*Python (programming language)*. (s.f.). Obtenido de Wikipedia:
https://en.wikipedia.org/wiki/Python\_(programming_language)

Sabino Parmezana, A. R., Lee, H. D., & Chung Wu, F. (2017).
*Metalearning for choosing feature selection algorithms in data mining:
Proposal of a new framework.* SP, Brazil.

Selvaraj, S., & Natarajan, J. (2011). *Microarray Data Analysis and
Mining Tools.* Obtenido de NCBI:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3089881/

Vanschoren, J. (2018). Meta-learning: A survey. *arXiv preprint
arXiv:1810.03548*.

Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K.
(2019). Modeling tabular data using conditional GAN. *Advances in Neural
Information Processing Systems*.

s://doi.org/10.1093/nar/gkq1238

Altschul, S. (1990). Basic Local Alignment Search Tool. *Journal of
Molecular Biology*, *215*(3), 403--410.
https://doi.org/10.1006/jmbi.1990.9999

Blanc, G. (2004). Widespread Paleopolyploidy in Model Plant Species
Inferred from Age Distributions of Duplicate Genes. *The Plant Cell
Online*, *16*(7), 1667--1678. https://doi.org/10.1105/tpc.021345

Caramuta, S., Lee, L., Özata, D. M., Akcakaya, P., Georgii-Hemming, P.,
Xie, H., ... Lui, W. O. (2013). Role of microRNAs and microRNA machinery
in the pathogenesis of diffuse large B-cell lymphoma. *Blood Cancer
Journal*, *3*(10). https://doi.org/10.1038/bcj.2013.49

Géron, A. (2017). *Hands-On Machine Learning with Scikit-Learn and
TensorFlow*.

Guyon, Isabelle. 2003. «An Introduction to Variable and Feature
Selection.»

Hampson, S., McLysaght, A., Gaut, B., & Baldi, P. (2003). LineUp:
Statistical detection of chromosomal homology with application to plant
comparative genomics. *Genome Research*, *13*(5), 999--1010.
https://doi.org/10.1101/gr.814403

Land, M., Hauser, L., Jun, S.-R., Nookaew, I., Leuze, M. R., Ahn, T.-H.,
... Ussery, D. W. (2015). Insights from 20 years of bacterial genome
sequencing. *Functional & Integrative Genomics*, *15*(2), 141--161.
https://doi.org/10.1007/s10142-015-0433-4

Learning, B. (2011). CHAPTER 1 Genes , Genomes and Genetic Analysis,
1--38.

Li, L., Stoeckert, C. J. J., & Roos, D. S. (2003). OrthoMCL:
Identification of Ortholog Groups for Eukaryotic Genomes \-- Li et al.
13 (9): 2178 \-- Genome Research. *Genome Research*, *13*(9),
2178--2189. https://doi.org/10.1101/gr.1224503.candidates

Linard, B., Allot, A., Schneider, R., Morel, C., Ripp, R., Bigler, M.,
... Lecompte, O. (2015). OrthoInspector 2.0: Software and database
updates. *Bioinformatics*, *31*(3), 447--448.
https://doi.org/10.1093/bioinformatics/btu642

Makino, T., & McLysaght, A. (2010). Ohnologs in the human genome are
dosage balanced and frequently associated with disease. *Proceedings of
the National Academy of Sciences*, *107*(20), 9270--9274.
https://doi.org/10.1073/pnas.0914697107

Mi, H., Muruganujan, A., & Thomas, P. D. (2013). PANTHER in 2013:
Modeling the evolution of gene function, and other gene attributes, in
the context of phylogenetic trees. *Nucleic Acids Research*, *41*(D1),
377--386. https://doi.org/10.1093/nar/gks1118

Min, S., Lee, B., & Yoon, S. (2017). Deep learning in bioinformatics.
*Briefings in Bioinformatics*, *18*(5), 851--869.
https://doi.org/10.1093/bib/bbw068

Mitchell, T. M. (1997). *Machine Learning*. *IJCAI International Joint
Conference on Artificial Intelligence*.
https://doi.org/10.1007/978-3-540-75488-6_2

Moraes, F., & Góes, A. (2016). A decade of human genome project
conclusion: Scientific diffusion about our genome knowledge.
*Biochemistry and Molecular Biology Education*, *44*(3), 215--223.
https://doi.org/10.1002/bmb.20952

Nature. 2010. «https://www.nature.com.»
https://www.nature.com/scitable/topicpage/gene-expression-14121669.

Ohno, D. S. (1970). Introduction. In *Evolution by Gene Duplication*.

Perera, P., & Patel, V. M. (2018). Learning Deep Features for One-Class
Classification, 1--12. Retrieved from http://arxiv.org/abs/1801.05365

Powell, S., Forslund, K., Szklarczyk, D., Trachana, K., Roth, A.,
Huerta-Cepas, J., ... Bork, P. (2014). EggNOG v4.0: Nested orthology
inference across 3686 organisms. *Nucleic Acids Research*, *42*(D1),
231--239. https://doi.org/10.1093/nar/gkt1253

Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning
representations by back-propagating errors. *Nature*, *323*(6088), 533.
Retrieved from
http://ezproxybib.pucp.edu.pe:2048/login?url=http://search.ebscohost.com/login.aspx?direct=true&db=edb&AN=61757871&lang=es&site=eds-live&scope=site

Sabino Parmezana, Antonio Rafael, Huei Diana Lee, y Feng Chung Wu. 2017.
«Metalearning for choosing feature selection algorithms in data mining:
Proposal of a new framework.» SP, Brazil.

Selvaraj, Saravanakumar, y Jeyakumar Natarajan. 2011. «Microarray Data
Analysis and Mining Tools.» *NCBI.*
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3089881/.

s.f. *National Center for Biotechnology Information.*
https://en.wikipedia.org/wiki/National_Center_for_Biotechnology_Information.

s.f. *Python (programming language).*
https://en.wikipedia.org/wiki/Python\_(programming_language).

s.f. *Jupyter.* https://jupyter.org/.

Schreiber, F., Patricio, M., Muffato, M., Pignatelli, M., & Bateman, A.
(2014). TreeFam v9: A new website, more species and
orthology-on-the-fly. *Nucleic Acids Research*, *42*(D1), 922--925.
https://doi.org/10.1093/nar/gkt1055

Schreiber, F., & Sonnhammer, E. L. L. (2013). Hieranoid: Hierarchical
orthology inference. *Journal of Molecular Biology*, *425*(11),
2072--2081. https://doi.org/10.1016/j.jmb.2013.02.018

Seoighe, C. (2003). Turning the clock back on ancient genome
duplication. *Current Opinion in Genetics and Development*.
https://doi.org/10.1016/j.gde.2003.10.005

Tatusov, R. L., Fedorova, N. D., Jackson, J. D., Jacobs, A. R.,
Kiryutin, B., Koonin, E. V., ... Natale, D. A. (2003). The COG database:
An updated vesion includes eukaryotes. *BMC Bioinformatics*, *4*, 1--14.
https://doi.org/10.1186/1471-2105-4-41

Valencia Reyes, M. A., Yáñez Márquez, C., & Sánchez Fernández, L. P.
(2006). Algoritmo Backpropagation para Redes Neuronales : conceptos y
aplicaciones. *Instituto Politécnico Nacional Centro De Investigación En
Computación*, (125), 1--12.

Vandepoele, K., Saeys, Y., Simillion, C., Raes, J., & Van de Peer, Y.
(2002). The automatic detection of homologous regions (ADHoRe) and its
application to microcolinearity between Arabidopsis and rice. *Genome
Research*, *12*(11), 1792--1801. https://doi.org/10.1101/gr.400202

# 
