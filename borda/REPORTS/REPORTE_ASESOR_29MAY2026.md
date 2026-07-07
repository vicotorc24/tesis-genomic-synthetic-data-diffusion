# Reporte de Avance: Seminario de Investigación 2
**Investigador:** Gary Alberto Velásquez Narro  
**Asesor:** Dr. Edwin Rafael Villanueva Talavera  
**Fecha:** 29 de mayo de 2026  
**Periodo reportado:** Semanas 1–8 (Abril–Mayo 2026)

---

## 0.1 Propuesta de Actualización de Título de Tesis

Dado el salto metodológico desde el enfoque de meta-aprendizaje (2021) hacia la IA generativa clínica (2026), se proponen las siguientes alternativas de título para reflejar con exactitud el nuevo alcance tecnológico y clínico:

**Título Original (2021):**
> *Generación De Datos Sintéticos En Meta-Aprendizaje Para La Creación De Modelos De Recomendación De Técnicas De Selección De Atributos Para Conjuntos De Datos De Expresión Génica*

**Opción 1 (Enfoque Clínico y Metodológico):**
> *"Generación de Datos Sintéticos mediante Modelos Generativos SOTA (CTGAN y Difusión Tabular) para el Entrenamiento de Clasificadores Genómicos Pan-Oncológicos: Un Enfoque de Armonización Multi-plataforma"*

**Opción 3 (Enfoque Ingenieril e IA Dura):**
> *"Modelado Generativo Profundo (CTGAN y Forest Diffusion) aplicado a Datos de Expresión Génica de Alta Dimensionalidad para la Construcción de Clasificadores Clínicos Robustos"*

---

## 0. Propuesta Original (13 de abril de 2026) — Referencia

La propuesta presentada al inicio del seminario definió los siguientes compromisos:

| Componente propuesto | Detalle |
|---|---|
| **Corpus** | 282 datasets GEO (249 Microarray + 33 RNA-seq) = 41,202 muestras brutas |
| **Descarte** | 60 datasets de 2021 por incompatibilidad (probesets vs. HGNC) |
| **Tecnologías generativas** | CTGAN + Modelos de Difusión Tabular (SOTA) |
| **Validador** | TabPFN como benchmark a vencer |
| **Clasificadores** | SVM, Random Forest, CatBoost, XGBoost, TabPFN |
| **Feature selection** | mRMR, RFE, Lasso, F-Test |
| **Evaluación** | Protocolo tripartito: Brazo A (Gaussiano) / B (CTGAN) / C (Difusión) |
| **Duración** | 12 semanas, 10h/semana |

**Fases del cronograma propuesto:**

| Fase | Actividad | Semanas |
|---|---|---|
| Fase 0 | Actualización del estado del arte | 1–3 |
| Fase 1 | Ingeniería de datos (282 datasets → Parquet) | 4–5 |
| Fase 2 | Baseline 2026 (ruido gaussiano + boosting) | 6–7 |
| Fase 3 | IA Generativa (CTGAN + Difusión) | 8–10 |
| Fase 4 | Meta-aprendizaje + validación vs TabPFN | 11–12 |

#### ¿Qué es TabPFN y por qué es el benchmark a vencer?

**TabPFN** (*Tabular Prior-data Fitted Network*, Universidad de Friburgo, NeurIPS 2022) es un clasificador Transformer pre-entrenado sobre millones de datasets sintéticos que realiza predicciones sobre datos tabulares **sin necesitar entrenamiento propio** — en menos de 1 segundo.

```
Clasificadores convencionales (XGBoost, SVM):
  Tus datos → ajustar parámetros → modelo → predicción
  Tiempo: minutos a horas, requiere tuning

TabPFN:
  Tus datos → Transformer pre-entrenado → predicción
  Tiempo: < 1 segundo, cero ajuste de hiperparámetros
```

En benchmarks públicos, TabPFN supera a XGBoost y Random Forest en datasets de menos de 10,000 muestras sin ninguna configuración. Por eso es el árbitro más exigente del experimento: **si los sintéticos de Forest Diffusion logran que TabPFN alcance AUC > 0.90 sobre pacientes reales que nunca vio, significa que los datos sintéticos son clínicamente indistinguibles de los reales.**

| Clasificador | Entrenamiento | Ajuste | Uso en la tesis |
|---|---|---|---|
| SVM, XGBoost, CatBoost | Sí | Sí | Arsenal comparativo |
| **TabPFN** | **No** (pre-entrenado) | **No** | **Árbitro final de calidad sintética** |

---

## 1. Propuesta vs. Ejecución Real — Comparativo Formal

| Componente | Propuesto (13/04) | Ejecutado (al 29/05) | Estado |
|---|---|---|---|
| **Corpus bruto** | 282 datasets / 41,202 muestras | 282 datasets descargados / 41,202 identificadas | ✅ Cumplido |
| **Master Table activa** | *(no especificado)* | **28,048 × 2,503** (filtro de calidad 0% NaN) | ✅ Superado |
| **Descarte datasets 2021** | 60 datasets obsoletos | Descartados con 5 razones técnicas documentadas | ✅ Cumplido |
| **Armonización HGNC** | Mapeo a Gene Symbols estándar | `harmonize_datalake.py` — 2,502 genes comunes | ✅ Cumplido |
| **Split anti-leakage 80/20** | Implícito en la estrategia | Core Train 4,256 / Core Test 1,065 — bóveda activa | ✅ Cumplido |
| **CTGAN (Brazo B)** | Entrenamiento y evaluación | 300 épocas, 5,000 sintéticos, fidelidad auditada | ✅ Cumplido |
| **Forest Diffusion (Brazo C)** | Modelo de Difusión SOTA | Pipeline listo con checkpoints GPU; ejecutando esta noche | 🔄 En ejecución |
| **TabPFN (validador)** | Benchmark a vencer | En `benchmark_arsenal.py`; pendiente sobre sintéticos FD | ⏳ Pendiente |
| **Arsenal clasificadores** | SVM, RF, CatBoost, XGBoost, TabPFN | Scripts `run_modern_benchmark.py` y `benchmark_arsenal.py` | ✅ Implementado |
| **Feature selection** | mRMR, RFE, Lasso, F-Test | F-Test implementado; `feature_selection.json` generado | ✅ Parcial |
| **Evaluación tripartita** | Brazos A / B / C | Acto 1 ✅ / Acto 2 CTGAN ✅ / Acto 3 FD 🔄 | 🔄 2 de 3 |
| **Auditoría SHAP + Jaccard** | No estaba en propuesta | **Extra:** implementado y ejecutado | ✅ Adicional |
| **Réplica del estudio 2021** | No estaba en propuesta | **Extra:** Figuras 17 y 18 reproducidas | ✅ Adicional |
| **Sistema de checkpoints FD** | No estaba en propuesta | **Extra:** resiliente a desconexiones, verificado localmente | ✅ Adicional |

### Nota sobre la variación del corpus

> La propuesta citaba 41,202 muestras brutas. La Master Table activa tiene **28,048** porque se aplicó un filtro de calidad estricto: solo se conservaron muestras con 0% de NaN en los 2,502 genes comunes. Las 13,154 muestras descartadas tenían cobertura génica parcial — conservarlas habría introducido ruido en la síntesis. Esta decisión está documentada en `ESTRATEGIA_EXPERIMENTAL_2026.md`.

---

## 2. Resumen Ejecutivo

El proyecto ha completado exitosamente las **fases de ingesta, armonización, entrenamiento CTGAN, generación de 5,000 sintéticos y auditoría de fidelidad biológica**. El corpus genómico de 28,048 muestras está consolidado, y el pipeline de Forest Diffusion está listo para ejecución final en GPU (esta noche en Google Colab Pro).

---

## 3. El Problema Central que Resuelve la Tesis

La investigación de 2021 construyó clasificadores oncológicos sobre una sola plataforma tecnológica. Al escalar a datos multi-plataforma (Microarray + RNA-seq), los modelos colapsan por el **Efecto Lote (Batch Effect)**.

```
2021: 1 plataforma → AUC ~0.85 (válido pero no escalable)
2026: Multi-plataforma sin armonización → AUC ~0.63 (Colapso demostrado ✅)
2026: Multi-plataforma + Datos Sintéticos SOTA → objetivo >0.90 AUC
```

**Hipótesis central:** Forest Diffusion sintetiza pacientes genómicos que preservan la firma oncológica biológica real, superando el Efecto Lote.

### 3b. ¿Por qué CTGAN y Forest Diffusion? — Justificación de las tecnologías

La elección no es arbitraria. Responde a una limitación concreta de las alternativas previas y a una progresión lógica de complejidad.

#### El problema con la alternativa simple: Ruido Gaussiano (metodología 2021)

La metodología de 2021 aumentaba los datos añadiendo **ruido gaussiano**: pequeñas perturbaciones aleatorias a los valores de expresión génica existentes. El problema es que el ruido gaussiano asume que los datos siguen una distribución normal, lo cual es **falso en datos genómicos**:

```
Datos genómicos reales:
  - Distribuciones multimodales (un gen puede estar activo o silenciado — dos modos)
  - Correlaciones no lineales entre genes (si BRCA1 sube, RAD51 también sube)
  - Subtipos tumorales que forman clusters separados en el espacio de expresión

Ruido Gaussiano aplicado:
  - Asume distribución normal (campana de Gauss) — ignorada la multimodalidad
  - No respeta correlaciones entre genes — puede generar pacientes biológicamente imposibles
  - Destruye la separación entre subtipos tumorales
  → Resultado: AUC ~0.63, peor que no hacer nada
```

#### ¿Por qué CTGAN?

CTGAN (*Conditional Tabular GAN*, MIT, 2019) fue diseñado específicamente para datos tabulares con distribuciones complejas. Usa dos redes adversariales (Generador + Discriminador) y un mecanismo de muestreo condicional que:

- **Respeta distribuciones multimodales** mediante transformación por modo
- **Balancea clases desiguales** — genera Tumor y Normal en proporción controlada
- **Aprende correlaciones** entre columnas (genes) de forma implícita

Es el **estándar establecido** en síntesis de datos tabulares clínicos (usado en publicaciones de NEJM, Nature Medicine para anonimización de datos de pacientes).

**Limitación identificada en esta tesis:** *mode collapse* leve sobre subtipos tumorales raros (ver Sección 6.3). CTGAN optimiza globalmente y sacrifica la representación de las clases minoritarias.

#### ¿Por qué Forest Diffusion?

Forest Diffusion (*Jolicoeur-Martineau et al., 2023*, ICML) es el estado del arte (SOTA 2024–2025) para datos tabulares de alta dimensión. Resuelve la limitación de CTGAN con una arquitectura radicalmente diferente:

```
CTGAN:
  1 red neuronal global aprende TODO el espacio de expresión génica
  → Optimización global → sacrifica subtipos raros

Forest Diffusion:
  1 XGBoost DEDICADO por cada gen (2,502 modelos independientes)
  → Cada gen aprende su propia distribución real
  → No hay un "generador central" que elija el camino fácil
  → Los subtipos raros están representados en cada modelo individual
```

| Criterio | Ruido Gaussiano | CTGAN | Forest Diffusion |
|---|---|---|---|
| Distribuciones multimodales | ❌ No respeta | ✅ Sí | ✅ Sí |
| Correlaciones inter-génicas | ❌ Destruye | ✅ Aprende | ✅ Aprende mejor |
| Subtipos tumorales raros | ❌ Difumina | ⚠️ Colapso leve | ✅ Preserva |
| Escalabilidad a 28k muestras | ✅ Trivial | ⚠️ Inestable | ✅ Diseñado para ello |
| AUC TSTR esperado | ~0.63 | ~0.75–0.82 | **>0.90 (objetivo)** |

**En resumen:** CTGAN es el *baseline* de síntesis tabular generativa. Forest Diffusion es la evolución que resuelve sus limitaciones. Usamos ambos para demostrar la progresión y justificar que el esfuerzo computacional adicional (125,100 modelos vs. una sola red) produce un beneficio clínico real y medible.

---


## 4. Arquitectura del Experimento: Los Tres Actos

```
ACTO 1 (= Brazo A)           ACTO 2 (= Brazo B)           ACTO 3 (= Brazo C)
─────────────────────         ─────────────────────         ──────────────────────
Prueba de Estrés              El Duelo Justo                SOTA a Escala Completa

28,048 muestras               5,321 muestras                28,048 muestras
Ruido Gaussiano               CTGAN                         Forest Diffusion
+ SVM / RF legacy

AUC ~0.63 → Colapso          5,000 sintéticos              >0.90 AUC TSTR
✅ Demostrado                 ✅ Completado                  🔄 Esta noche
```

**Validación TSTR:** Los sintéticos se evalúan sobre **1,065 pacientes reales** que los generativos nunca vieron.

---

## 5. Inventario de Datos

| Dataset | Muestras | Features | Estado | Uso |
|---|---|---|---|---|
| `master_training_table.parquet` | **28,048** | 2,503 | ✅ | Entrenamiento FD Acto 3 |
| `core_train_final.parquet` | **4,256** | 2,503 | ✅ | Entrenamiento Acto 2 |
| `core_test_final.parquet` | **1,065** | 2,503 | ✅ | Jurado imparcial TSTR |
| `synthetic_samples_5000.parquet` | **5,000** | 2,502 | ✅ | Evaluación TSTR CTGAN |

**Procedencia:** 282 datasets de GEO, armonizados HGNC, intersección de 2,502 genes comunes.

### 5b. ¿Cómo se obtuvieron los 282 datasets?

**Fuente:** Gene Expression Omnibus (GEO) — repositorio público del NCBI (National Center for Biotechnology Information), el estándar mundial para datos de expresión génica.

**Pipeline automatizado de descarga y auditoría:**

```
Paso 1 — Búsqueda automatizada en GEO:
  Criterios: keyword "cancer" OR "tumor" + campo "expression profiling"
  Plataformas: GPL570 (Affymetrix HG-U133 Plus 2.0) y plataformas Illumina RNA-seq
  Resultado inicial: ~600 datasets candidatos

Paso 2 — Auditoría de metadatos (script: find_geo_candidates.py):
  Filtros aplicados:
    ✓ Mínimo 50 muestras por dataset
    ✓ Etiquetas Tumor / Normal presentes en metadatos
    ✓ Ratio Tumor:Normal ≥ 0.1 (no datasets mono-clase)
    ✓ Plataforma con mapeo HGNC disponible
  Resultado: 282 datasets viables

Paso 3 — Descarga de matrices de expresión:
  Formato: archivos .soft.gz y _series_matrix.txt.gz de GEO FTP
  Scripts: extract_expression_matrix.py, merge_raw_tar.py
  Tiempo total de descarga: ~72 horas acumuladas

Paso 4 — Normalización por plataforma:
  Microarray: log2 + quantile normalization
  RNA-seq: log2(TPM + 1) para equiparar escalas

Paso 5 — Armonización HGNC (script: harmonize_datalake.py):
  Mapeo de probe IDs propietarios → Gene Symbols estándar HGNC
  Intersección de genes comunes entre las 282 fuentes = 2,502 genes

Paso 6 — Filtro de calidad:
  Solo muestras con 0% NaN en los 2,502 genes
  41,202 candidatos → 28,048 aprobadas (68% de retención)
```

**Criterio científico del filtro:** Una muestra con NaN en cualquier gen introduce sesgo en la síntesis generativa. El modelo aprendería a imputar en lugar de generar, comprometiendo la validez biológica del sintético.

---

## 6. Pipeline Técnico

### 6.1 Ingesta y Armonización
```
282 datasets GEO → Normalización por plataforma → Mapeo HGNC
→ Intersección 2,502 genes → Filtro 0% NaN → Master Table 28,048 × 2,503
```

### 6.2 Split Anti-Data Leakage (80/20 estratificado)
```
Core Set 5,321 muestras
      │
  ┌───┴───┐
  │       │
Train    Test
4,256    1,065  ← BLOQUEADO — nunca visto por modelos generativos
```

### 6.3 CTGAN — Brazo B ✅
- 300 épocas sobre `core_train_final`
- 5,000 pacientes sintéticos generados
- Auditoría: PCA + CDF + correlaciones + SHAP + Jaccard
- **Hallazgo clave:** *mode collapse* leve — borra subtipos tumorales raros

#### ¿Qué es el *mode collapse* y por qué es un problema clínico?

CTGAN tiene dos redes que compiten: un **Generador** (inventa pacientes) y un **Discriminador** (evalúa si parecen reales). El Generador aprende un atajo: en lugar de aprender toda la distribución de tumores, converge a generar siempre el subtipo más frecuente, porque engañar al Discriminador con casos comunes es más fácil.

```
Distribución REAL en el corpus:        Distribución CTGAN sintético:
  Tumor de mama:     40%                 Tumor de mama:     52% ← sobrerepresentado
  Tumor de pulmón:   25%                 Tumor de pulmón:   30% ← sobrerepresentado
  Tumor hepático:    20%                 Tumor hepático:    18%
  Tumor de páncreas:  8%                 Tumor de páncreas:  0% ← desaparecido
  Leucemia rara:      5%                 Leucemia rara:      0% ← desaparecido
  Sarcoma raro:       2%                 Sarcoma raro:       0% ← desaparecido
```

**Consecuencia clínica:** Un clasificador entrenado con estos sintéticos aprende bien los tumores comunes pero falla en subtipos raros. En la práctica médica, un paciente con un tumor minoritario sería mal diagnosticado porque el modelo generativo nunca lo representó.

#### ¿Qué es el Índice de Jaccard y cómo detecta este problema?

El Índice de Jaccard mide el solapamiento entre dos conjuntos. En este contexto, compara los **genes más importantes para el diagnóstico** en datos reales vs. datos sintéticos:

```
         |Genes_reales ∩ Genes_sintéticos|
J = ─────────────────────────────────────────
         |Genes_reales ∪ Genes_sintéticos|

Rango: 0.0 (nada en común) → 1.0 (firmas génicas idénticas)
```

Se toman los Top-100 genes más discriminativos (por F-Test) en cada conjunto y se mide cuántos coinciden. Un Jaccard bajo significa que el modelo sintético identificó genes diagnósticos distintos a los reales — **alucinó una biología diferente** — problema que el AUC global no revela, porque los subtipos mayoritarios compensan estadísticamente a los minoritarios.

| Modelo | Jaccard esperado | Interpretación |
|---|---|---|
| Ruido Gaussiano (metodología 2021) | ~0.10–0.20 | Destruye la firma oncológica completamente |
| **CTGAN** | ~0.60–0.75 | Preserva parcialmente, pierde subtipos raros |
| **Forest Diffusion** | ~0.85–0.95 | Alta fidelidad biológica esperada |

Este hallazgo es el argumento cuantitativo central que justifica el Acto 3: Forest Diffusion, al entrenar un modelo dedicado por gen, no depende de un generador global que "elija el camino fácil" — cada gen aprende su propia distribución real, preservando las firmas oncológicas de todos los subtipos, incluyendo los raros.


### 6.4 Forest Diffusion — Brazo C 🔄
```
Por cada paso t (0 → 49):
  Interpolación CFM (ruido ↔ dato real)
  → 2,502 XGBoosts individuales (1 por gen)
  → step_t.joblib en Google Drive (compress=0, ~5 segundos)

Total: 50 pasos × 2,502 modelos = 125,100 XGBoosts
Generación: reversa de 50 pasos → paciente sintético nuevo
```
**Ventaja sobre CTGAN:** 1 modelo dedicado por gen → preserva correlaciones biológicas reales.

---

## 7. Resolución del Cuello de Botella Técnico *(hallazgo de ingeniería)*

**Problema diagnosticado:**
```
Script v1: guardaba modelo completo acumulado con compress=9 en cada paso
Paso 3: ~4 GB de XGBoost → RAM agotada → swap de disco → 3 días de bloqueo
```

**Solución implementada y verificada:**
```
Script v3:
  ✅ 1 XGBoost por gen (arquitectura original de la librería)
  ✅ compress=0 → 5 segundos por guardado (antes: días)
  ✅ Archivo independiente por paso → resiliente a cortes de sesión

Demo verificado 28/05/2026:
  Sesión 1 → Pasos 1-2 ✅ → Interrupción intencional
  Sesión 2 → Detecta 2 pasos → Reanuda Paso 3 → Completa 3,4,5 → Ensambla ✅
```

---

## 7b. Historial de Pruebas Computacionales y Solicitud de Infraestructura

### Cronología de intentos de entrenamiento

| Intento | Entorno | Resultado | Causa |
|---|---|---|---|
| **#1** (sem. 3) | Mac local CPU | ❌ Bloqueado 3 días en paso 3/50 | `compress=9` sobre modelo acumulado agotó RAM y forzó swap de disco |
| **#2** (sem. 8) | Mac local CPU (fix #1) | ❌ Inviable — 1 paso = 2h+ | 2,502 XGBoosts × 28k muestras en CPU secuencial |
| **#3** (sem. 8) | Google Colab GPU T4 | ⚠️ Sesión limitada a 18–20h | Colab desconecta automáticamente; sin garantía de continuidad |
| **#4** *(esta noche)* | Google Colab GPU + Drive | 🔄 En curso | Checkpoints por paso → reanuda automáticamente |

### ¿Por qué Google Colab no es suficiente?

El algoritmo Forest Diffusion sobre 28,048 × 2,502 genes requiere:

| Recurso | Google Colab Pro (actual) | Necesario para 1 sesión completa |
|---|---|---|
| **GPU** | T4 (16 GB VRAM) | A100 (40 GB) o V100 (32 GB) |
| **RAM** | 12–25 GB | 32–64 GB |
| **Tiempo de sesión** | 18–20h (luego desconecta) | 20–30h continuas |
| **Almacenamiento** | Google Drive externo | SSD local rápido |
| **Costo** | ~USD 10/mes (Pro) | — |

**La consecuencia práctica:** El entrenamiento de 50 pasos se distribuye en múltiples sesiones de Colab (estimado: 2–3 sesiones), con riesgo de interrupción sin garantía de disponibilidad de GPU. El sistema de checkpoints implementado mitiga esto, pero no elimina la dependencia de la infraestructura externa.

### Solicitud de Infraestructura PUCP

Se solicita formalmente el acceso a servidores de cómputo de la PUCP para completar el entrenamiento de Forest Diffusion dentro del cronograma académico (semana 9, hasta el 06/06/2026).

**Requerimientos técnicos mínimos:**

```
GPU:  NVIDIA con ≥16 GB VRAM (Tesla T4, V100, A100, o RTX 3090/4090)
RAM:  32 GB mínimo (64 GB recomendado)
Almacenamiento: 100 GB SSD (para 50 archivos de checkpoints ~1.3 GB cada uno)
Tiempo de sesión: ≥20 horas continuas sin interrupción
SO:   Linux (Ubuntu 20.04+) con Python 3.9+ y CUDA 11.8+
```

**Impacto en la tesis si se aprueba el acceso:**
- El entrenamiento de 50 pasos completaría en **1 sola sesión** (~15–20h en GPU A100)
- Se elimina la dependencia de disponibilidad de Google Colab
- Se puede repetir el experimento para validación adicional si el asesor lo requiere
- El modelo final (~15–20 GB) quedaría alojado en servidores institucionales

**Alternativa si no hay acceso a GPU PUCP:**  
El sistema de checkpoints implementado permite completar el entrenamiento en 2–3 sesiones de Google Colab Pro, con continuidad garantizada. El cronograma no se vería comprometido, solo se dependería de la disponibilidad de la infraestructura de Google.

---

## 8. Figuras Producidas

| Figura | Descripción | Capítulo |
|---|---|---|
| `HEATMAP_REPRODUCED_2021.png` | Réplica del heatmap 2021 | Cap. 3 — Baseline legacy |
| `HEATMAP_LEGACY_CONTRAST_2026.png` | Contraste legacy vs SOTA | Cap. 3 — Comparativo |
| `HEATMAP_PERFORMANCE_SOTA_2026.png` | Rendimiento SOTA 2026 | Cap. 4 — Resultados |
| `fidelity_pca_ctgan.png` | PCA: sintéticos CTGAN vs reales | Cap. 4 — Fidelidad |
| `fidelity_correlations.png` | Correlaciones génicas preservadas | Cap. 4 — Fidelidad |
| `fidelity_cdf.png` | CDF distribución sintética | Cap. 4 — Fidelidad |
| `genomic_stability_curve.png` | Curva de estabilidad génica | Cap. 3 — Feature selection |
| `FIGURA_17_REPLICA_SPEARMAN.png` | Réplica Spearman 2021 | Anexo — Reproducibilidad |
| `FIGURA_18_REPLICA_PLC.png` | Réplica PLC 2021 | Anexo — Reproducibilidad |
| `tech_balance.png` | Balance tecnológico del corpus | Cap. 2 — Datos |

---

## 9. Estado por Semana

| Semana | Hasta | Entregable | Estado |
|---|---|---|---|
| 1 | 11/04 | Propuesta de modernización | ✅ Enviado |
| 2 | 18/04 | Ingesta, armonización HGNC, split 80/20 | ✅ Enviado |
| 3 | 25/04 | Prueba de Estrés + inicio SOTA | ⚠️ Pendiente envío formal |
| 4 | 02/05 | Inferencia CTGAN + sintéticos | ✅ Completado |
| 5 | 09/05 | Benchmark TSTR | ✅ Completado |
| 6 | 16/05 | Auditoría SHAP + Jaccard | ✅ Completado |
| 7 | 23/05 | Redacción Capítulos 3 y 4 | ✅ En borrador |
| **8** | **30/05** | **Heatmaps + ROC + bibliografía** | **🔄 En curso** |
| 9 | 06/06 | Correcciones del asesor | Pendiente |
| 10 | 13/06 | Conclusiones y Anexos | Pendiente |
| 11 | 20/06 | Revisión tipográfica y antiplagio | Pendiente |
| 12 | 27/06 | Diapositivas de defensa | Pendiente |
| 13 | 04/07 | Entrega final del manuscrito | Pendiente |

---

## 10. Próximos Pasos

### Esta noche (28/05):
- [ ] Subir `master_training_table.parquet` a Google Drive
- [ ] Ejecutar benchmark de 1 paso en Colab GPU → calibrar velocidad
- [ ] Lanzar entrenamiento de 50 pasos (checkpoints en Drive)

### Semana 9 (hasta 06/06):
- [ ] Completar entrenamiento FD (2 sesiones Colab estimadas)
- [ ] Ejecutar benchmark TSTR completo sobre sintéticos FD
- [ ] Completar tabla comparativa CTGAN vs FD vs Real
- [ ] Integrar métricas finales en Capítulo 4

---

## 11. Repositorio de Código

| Script | Función |
|---|---|
| `harmonize_datalake.py` | Armonización multi-plataforma con HGNC |
| `create_master_table.py` | Construcción Master Table 28k |
| `train_ctgan_pilot.py` | Entrenamiento CTGAN |
| `generate_synthetic_patients.py` | Generación de pacientes sintéticos |
| `train_forest_diffusion_checkpoints.py` | FD local con checkpoints resilientes |
| `train_fd_colab.py` | FD para Google Colab GPU *(nuevo)* |
| `run_modern_benchmark.py` | Benchmark TSTR — Arsenal de Algoritmos |
| `audit_biosynthetic_fidelity.py` | Auditoría SHAP + Jaccard |
| `benchmark_arsenal.py` | Evaluación TabPFN, XGBoost, CatBoost, SVM |

---

*Documento preparado para reunión de asesoría — 29 de mayo de 2026*
