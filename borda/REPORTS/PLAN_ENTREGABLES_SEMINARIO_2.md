# Plan de Entregables SOTA: Seminario de Investigación 2 / Seminario de Tesis 2
**Periodo Académico:** 2026-1
**Investigador:** Gary Velasquez

---

Este documento funciona como hoja de ruta técnica indispensable para dar por concluida la Tesis y entregarla formalmente al jurado en el presente periodo académico.

## 🟩 FASE 1: Resolución de Cuellos de Botella Computacionales (SOTA)
Estas tareas requieren la finalización de los procesos matemáticos de infraestructura en segundo plano.

- [ ] **1. Consolidación de Forest Diffusion (Brazo C):** Finalizar el pre-entrenamiento de las ~4,600 horas de CPU acumuladas sobre las 26,000 muestras híbridas.
- [ ] **2. Stress Test Generativo: Escalar CTGAN (Brazo B):** Ejecutar CTGAN sobre las 5,358 muestras del Core-Set (vs los 2,500 previos) para demostrar empíricamente frente al jurado la incapacidad por "Underfitting Geométrico" (N \approx D) de la familia GAN.
- [ ] **3. Inferencia de Gemelos Sintéticos Finales:** Usar los `.pkl` finales para sintetizar los 28k pacientes sintéticos SOTA que se usarán en las auditorías.

## 🟨 FASE 2: Auditorías Biológicas y Benchmark
Pruebas de fuego que probarán la eficacia del Brazo C sobre los Legados.

- [ ] **1. Ejecución del Benchmark Decadal:** Correr el script `run_modern_benchmark.py` con estimadores modernos (TabPFN, XGBoost) sobre los datos de Forest Diffusion, apuntando a asegurar la métrica por encima de **>0.90 AUC**.
- [ ] **2. Auditoría Causal de Explicabilidad (SHAP):** Pasar `audit_biosynthetic_fidelity.py` para calcular el Índice Jaccard. Requisito vital: Comprobar que los "top-genes" (*Ej: TP53, BRCA1*) no se alucinaron sino que se preservaron.

## 🟦 FASE 3: Consolidación Documental y Redacción (El Manuscrito)
- [x] **1. Portada, Abstract y Anexos Metodológicos:** Listos y blindados en el Borrador Maestro.
- [ ] **2. Inyección de Resultados Duros:** Sustituir estimaciones narrativas por los resultados categóricos (ej. "Forest Diffusion logró exactamente un AUC de X.XXX").
- [ ] **3. Anexo Gráfico Final:** Insertar versiones en alta resolución de la Curva ROC comparativa (2021 vs 2026) y de las distribuciones de Batch-Effect.
- [ ] **4. Preparación de Memoria USB/Repositorio Anexo:** Armar la carpeta `.zip` con los códigos para que el comité de evaluación SOTA pueda replicarlo localmente (evidenciando las 4000 horas invertidas).
