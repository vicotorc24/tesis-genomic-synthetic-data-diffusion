# Justificación Metodológica: Integración Multi-Tecnológica

Este documento detalla la lógica detrás de la decisión de integrar Microarrays y RNA-seq en un solo corpus unificado, a pesar de la reducción en el volumen total de muestras.

## 1. El Dilema: Volumen vs. Invarianza

Durante el desarrollo del datalake genómico, se identificó que el uso exclusivo de tecnología **RNA-seq** permitiría un volumen de muestras significativamente mayor (~20k muestras de alta densidad). Sin embargo, se optó por una estrategia de **Integración Híbrida** por las siguientes razones:

### A. Robustez Tecnológica (Invarianza)
Al entrenar el modelo generativo (CTGAN) con perfiles de Microarray y RNA-seq simultáneamente, el modelo aprende a distinguir entre:
- **Varianza Biológica:** Diferencias entre tejido normal y tumoral.
- **Varianza Técnica:** Diferencias instrumentales entre plataformas.

Esta capacidad de "armonización latente" hace que los datos sintéticos resultantes sean **universales**, permitiendo que un modelo entrenado con ellos pueda aplicarse a cualquier tipo de dato real, sin importar la tecnología de captura.

### B. Representatividad Histórica
Los Microarrays contienen décadas de investigación clínica valiosa que no están disponibles en RNA-seq moderno. Integrarlos asegura que el modelo generativo capture fenotipos de cáncer documentados extensamente en estudios legados.

## 2. El "Impuesto de Intersección"

La reducción del volumen a un **Core Set de 5,358 muestras** es el resultado de un filtrado riguroso:
1.  **Intersección de Genes:** Se limitó el análisis a los **2,500 genes** con mayor frecuencia en ambas plataformas para garantizar una matriz densa.
2.  **Purga de Sparsity:** Se eliminaron las muestras de microarrays antiguos que presentaban fallas de mapeo o baja integridad génica (>10% de ceros).

## 3. Conclusión para la Tesis

La metodología aplicada prioriza la **calidad de la señal biológica** sobre el **volumén bruto**. 
En la IA generativa para salud, un dataset de 5,000 muestras densas y multi-tecnológicas es superior a uno de 20,000 muestras ruidosas de una sola fuente, ya que previene el sobreajuste (overfitting) a sesgos tecnológicos específicos y garantiza una validación **TSTR (Train Synthetic, Test Real)** mucho más exigente y valiosa.

---
*Preparado para la sustentación de Tesis - 2026*
