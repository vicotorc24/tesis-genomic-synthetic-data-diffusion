# Resultados Experimentales: Validación TSTR (Train Synthetic, Test Real)

Este documento es una plantilla para los resultados finales del benchmark "Arsenal de Algoritmos". Los valores marcados con `[ ]` serán completados al finalizar el entrenamiento de la CTGAN y la ejecución del script `benchmark_arsenal.py`.

## 1. Resumen de Poder Predictivo (Top 100 Genes)

**Target:** Tumor vs. Normal (Category)  
**Hold-out Set:** $N=1,072$ (Core Test 20% - Real)

| Clasificador | Métrica | Brazo A (Control Real) | Brazo B (TSTR Sintético) | Diferencia ($\Delta$) | Fidelidad (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **SVM (Linear)** | Macro-F1 | [ ] | [ ] | [ ] | [ ] |
| **Random Forest**| Macro-F1 | [ ] | [ ] | [ ] | [ ] |
| **XGBoost** | Macro-F1 | [ ] | [ ] | [ ] | [ ] |
| **CatBoost** | Macro-F1 | [ ] | [ ] | [ ] | [ ] |
| **TabPFN** | Macro-F1 | [ ] | [ ] | [ ] | [ ] |
| --- | --- | --- | --- | --- | --- |
| **PROMEDIO** | **Macro-F1** | **[ ]** | **[ ]** | **[ ]** | **[ ]** |

---

## 2. Fórmulas de Análisis Sugeridas

Para la discusión de resultados en la tesis, utilizaremos las siguientes definiciones:

1.  **Fidelidad de la Síntesis ($F_s$):**
    $$ F_s = \frac{F1_{TSTR}}{F1_{Real}} \times 100 $$
    *Interpretación:* Indica qué porcentaje de la utilidad clínica de los datos reales fue capturado por el modelo generativo.

2.  **Pérdida de Utilidad ($U_p$):**
    $$ U_p = F1_{Real} - F1_{TSTR} $$
    *Interpretación:* El costo marginal de utilizar datos anónimos sintéticos en lugar de datos reales sensibles.

## 3. Notas Técnicas del Experimento
- **Feature Selection:** Se utilizó `F-Test` sobre cada set de entrenamiento de forma independiente para evitar fuga de información.
- **Volumen Sintético:** 5,000 pacientes generados por CTGAN (300 Epochs).
- **Consistencia:** Todos los modelos fueron evaluados con el mismo set de test real (`core_test.parquet`).

---
*Documento generado para el capítulo de Resultados - 2026*
