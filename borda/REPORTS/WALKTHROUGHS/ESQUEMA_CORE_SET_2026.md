# Esquema de Integridad y Evolución del Core Set (2026)

Este documento detalla la estructura oficial del Datalake para la investigación SOTA 2026.

| Fase | Nivel de Integridad | Muestras (N) | Genes | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **1. Scraping Inicial** | Crudo (Raw) | 161 Estudios | 20k - 50k | Datos brutos de GEO y TCGA. |
| **2. Harmonization** | Limpieza Base | 28,048 | 2,500 | Unificación de 161 plataformas a HGNC Symbols. |
| **3. Master Table v2** | Integración | 28,048 | 2,500 | Dataset unificado con ruido residual. |
| **4. Core Set** | Calidad Premium | **5,358** | 2,500 | **Punto de Inflexión**: >90% integridad génica. |
| **5. Split Entrenamiento** | Set Oficial | 4,286 | 2,500 | 80% del Core Set (En entrenamiento Forest Diffusion). |
| **6. Validación Ciega** | Test Final | 1,072 | 2,500 | 20% bloqueado para validación de arquitectura. |

### 🛠️ Archivos Físicos Relacionados:
- Master Table: `results/master_training_table.parquet`
- Training (Fase 5): `results/core_train_final.parquet`
- Test (Fase 6): `results/core_test_final.parquet`
