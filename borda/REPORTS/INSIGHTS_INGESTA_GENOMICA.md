# Bitácora Técnica: Expansión de Corpus Genómico (Phase 7)

Este documento centraliza los conocimientos y soluciones técnicas desarrolladas durante la fase de escalamiento del corpus multi-ómico de cáncer.

## 📊 Estado Final del Datalake
- **Datasets Totales:** 190 archivos `.parquet`.
- **Candidatos RNA-seq Validados:** 500 estudios identificados en metadatos.
- **Muestras Totales:** (~31k Normales, ~78k Tumorales) aproximadas.

## 💡 Aprendizajes y "Insights" de Ingesta

### 1. El Puente de Nomenclatura (Nomenclature Bridge)
Uno de los mayores retos fue el desajuste entre los nombres de columnas en las matrices (IDs de laboratorio como `RP14M`, `P116`) y los IDs globales de NCBI (GSMs).
- **Solución:** Implementamos una búsqueda "borrosa" y exhaustiva en el objeto `GEOparse`. El script ahora busca el ID del laboratorio no solo en el título, sino dentro de todas las sub-características (`characteristics_ch1`) de cada muestra.
- **Impacto:** Esto permitió rescatar datasets de alta calidad (como `GSE213862`) que el pipeline automático descartaba inicialmente.

### 2. Robustez en la Carga de Datos
Se detectaron fallos en la detección de separadores (Tab vs Coma) en archivos comprimidos (`.gz`).
- **Insight:** El lector de Python nativo a veces interpreta bytes binarios de GZIP como texto si no se abre específicamente con el módulo `gzip`.
- **Mejora:** Refinamos el script de ingesta manual para manejar streams `gzip` de forma nativa antes de pasar el separador detectado a `pandas`.

### 3. Normalización Universal
Para permitir el entrenamiento multi-etiqueta y multi-estudio (Phase 7.5+), adoptamos el estándar:
$$ \text{Log2}(\text{TPM Proxy} + 1) $$
Esto estabiliza la varianza entre laboratorios que usan diferentes profundidades de lectura.

## 🧠 Justificación Teórica: CTGAN y el Modelo Condicional
*Nota para la Tesis/Asesor:*

**¿Es CTGAN un Conditional GAN?**
Sí, categóricamente. La "C" de CTGAN responde directamente a **"Conditional"**. 

**Estrategia Antibias (Evitando Overfitting Tecnológico):**
Al entrenar el modelo, utilizaremos la columna `Technology` (Microarray vs RNA-seq) como una **Variable Condicional**.
1.  **Independencia de Dominio:** El generador de CTGAN aprenderá a generar perfiles de expresión genética *condicionados* a la tecnología.
2.  **Mitigación de Batch Effects:** Esto permite que el modelo entienda que la diferencia en los valores numéricos entre RNA-seq y Microarray es puramente técnica, mientras que la diferencia entre Normal y Tumor es biológica.
3.  **Defensa de la Tesis:** Estamos utilizando un modelo generativo de vanguardia que separa el ruido instrumental de la señal tumoral mediante etiquetas latentes de tecnología.

## 🛠 Guía de Supervivencia (Scripts Clave)

- **`scripts/ingest_manual_rnaseq.py`**: El conversor universal. Úsalo si encuentras una matriz suplementaria en GEO que el script automático no pudo bajar.
- **`scripts/report_class_balance.py`**: Tu fuente de verdad sobre cuántas muestras tienes por tumor y tecnología.
- **`scripts/find_matrices.py`**: Auditor de suplementos para encontrar directamente las URLs de descarga de matrices de "conteo".

## 🚀 Próximos Pasos Recomendados (Benchmarking)
- **CTGAN:** Usar la librería `sdv` para entrenar el modelo generativo sobre este datalake de 190 parquets.
- **TSTR (Train Synthetic, Test Real):** Entrenar un clasificador SVM sobre los datos sintéticos de CTGAN y validarlo contra los datos reales de este corpus.

---
*Documento generado por Antigravity AI - Abril 2026*
