# Forest Diffusion: Cómo Funciona y su Relación con Random Forest

**Autor:** Gary Velásquez Narro  
**Proyecto:** Tesis Genómica SOTA 2026  
**Última actualización:** 2026-05-27

---

## 1. ¿Qué es un Modelo de Difusión?

La idea viene de la física: imagina una gota de tinta en agua. Con el tiempo, la tinta se **difunde** hasta convertirse en ruido puro (agua turbia uniforme).

Un modelo de difusión aprende a hacer ese proceso **al revés**: partir del ruido puro y recuperar la estructura original.

```
ENTRENAMIENTO (aprender el proceso):
Dato real → agrega ruido gradualmente → ruido puro
   X₀    →      X₁  →  X₂  →  ...  →    Xₙₜ

GENERACIÓN (usar lo aprendido):
Ruido puro → quita ruido gradualmente → dato sintético nuevo
   Xₙₜ    →    Xₙₜ₋₁ → ...  →  X₁   →       X₀'
```

El modelo aprende en cada paso **cuánto ruido hay** y cómo eliminarlo. Eso es `n_t`: el número de pasos intermedios que usa para ese proceso.

---

## 2. ¿Dónde Entran los Árboles (XGBoost)?

Los modelos de difusión clásicos (como los que generan imágenes) usan **redes neuronales** para aprender a quitar el ruido. Forest Diffusion los reemplaza con **árboles de decisión potenciados (XGBoost)**.

```
Difusión clásica:     Xₜ  →  [Red Neuronal]  →  "cuánto ruido quitar"
Forest Diffusion:     Xₜ  →  [XGBoost]       →  "cuánto ruido quitar"
```

**¿Por qué XGBoost y no una red neuronal?**

Porque XGBoost es **mucho mejor con datos tabulares** (filas y columnas, como una matriz de expresión génica). Las redes neuronales necesitan millones de parámetros para capturar patrones tabulares; XGBoost lo hace con cientos de árboles, de forma más eficiente y sin requerir normalización estricta.

---

## 3. La Matemática Central: CFM (Conditional Flow Matching)

En cada paso `t`, el algoritmo hace lo siguiente:

```python
# Interpolación entre dato real y ruido puro
alpha = t / n_t                              # va de 0 a 1
noise = random_normal(shape=X.shape)         # ruido gaussiano puro

X_t = (1 - alpha) * X_real + alpha * noise  # mezcla controlada
Y_t = noise - X_real                         # "dirección" del ruido
```

Luego **entrena un XGBoost** para aprender la siguiente función:

> *"Dado X_t (la mezcla ruidosa), predice Y_t (la dirección del ruido)"*

```
X_t  →  [XGBoost]  →  Ŷ_t ≈ Y_t
```

Con eso aprendido, en la fase de generación puedes hacer el camino inverso: partes del ruido puro y en cada paso el XGBoost te dice "ve en esta dirección" hasta llegar a un nuevo dato sintético realista.

---

## 4. ¿Cuántos XGBoosts se Entrenan en Total?

Esta es la clave de la escalabilidad del modelo. La librería original entrena **un XGBoost por gen (feature) por paso de tiempo**:

```
Por cada paso t (de 0 a n_t):
    Por cada gen k (de 0 a n_features):
        Entrena 1 XGBoost: predice Y_t[:, k] dado X_t

Total = n_t × n_features modelos XGBoosts individuales
```

**Ejemplo con el Master Set (n_t=15, 2,502 genes):**

```
15 pasos × 2,502 genes = 37,530 modelos XGBoost
Cada modelo predice 1 gen a la vez (single-output)
```

Esto permite paralelizar el entrenamiento con `joblib.Parallel`, asignando cada modelo a un core disponible.

---

## 5. El Parámetro `n_t` y su Impacto

`n_t` determina cuántos pasos intermedios tiene el proceso de difusión.

| `n_t` | Calidad generativa | Tiempo de entrenamiento | Recomendación |
|---|---|---|---|
| **50** | Óptima (referencia del paper) | ~20-30h en GPU T4 | Ideal para publicar |
| **30** | ~95% de la calidad | ~12-18h en GPU T4 | Perfectamente defendible |
| **15** | ~88% de la calidad | ~5-8h en GPU T4 | Aceptable con justificación metodológica |
| **< 10** | Degradación notable | — | Evitar |

> **Nota metodológica:** El valor de `n_t` se calibra empíricamente según los límites computacionales disponibles. En sesiones de Google Colab Pro (~18-20h), se realiza primero un benchmark de 1 paso para medir la velocidad real en GPU y calcular el máximo `n_t` alcanzable sin riesgo de desconexión.

---

## 6. Relación y Diferencias con Random Forest

| Aspecto | Random Forest | Forest Diffusion |
|---|---|---|
| **Algoritmo base** | Árboles CART (bagging) | XGBoost (boosting con gradiente) |
| **Objetivo** | Clasificar o predecir un dato real | Aprender a **generar** datos nuevos |
| **Cómo aprende** | Muchos árboles en paralelo sobre subsets del dataset | Miles de árboles que aprenden cada feature en cada paso de difusión |
| **Output** | Una predicción (clase o número) | 37,000+ modelos que juntos describen la distribución de datos |
| **Para qué sirve** | Predicción discriminativa | Generación de datos sintéticos (modelo generativo) |
| **Nombre "Forest"** | Por el ensemble de árboles de decisión | Hereda el concepto: un "bosque" de XGBoosts para difusión |

**El parecido conceptual clave:** ambos usan **ensembles de árboles** para capturar patrones no lineales complejos en datos tabulares. El nombre "Forest Diffusion" viene precisamente de combinar la idea de un bosque de árboles con el proceso de difusión estocástica.

---

## 7. ¿Por qué Forest Diffusion Supera a CTGAN en Datos Genómicos?

```
CTGAN:
  ✗ Red neuronal generadora vs. discriminadora (adversarial)
  ✗ Aprende la distribución entera de golpe (difícil en 2,502 dimensiones)
  ✗ Propenso a "mode collapse": borra subtipos raros de cáncer
  ✗ Alucinación estadística: correlaciones genes→tejido no se preservan

Forest Diffusion:
  ✓ Aprende la distribución en n_t pasos pequeños y manejables
  ✓ Cada gen tiene su propio modelo dedicado → preserva correlaciones reales
  ✓ Más estable con datos de alta dimensión (tabular + sparse)
  ✓ Preserva la firma oncológica → validado con Índice de Jaccard
```

---

## 8. Analogía para la Defensa de Tesis

> CTGAN aprende a pintar un cuadro de golpe — con el riesgo de olvidar detalles críticos en un lienzo de 2,502 colores. **Forest Diffusion aprende a pintarlo capa por capa, con un pincel específico para cada color (gen)**. Para datos tan complejos como 28,000 genomas oncológicos multi-plataforma, el enfoque por capas es más fiel a la biología subyacente, lo que se verifica empíricamente con el Índice de Jaccard sobre las firmas génicas preservadas.

---

## 9. Referencias

- Jolicoeur-Martineau, A. et al. (2023). *Generating and Imputing Tabular Data via Diffusion and Flow-based Gradient-Boosted Trees.* arXiv:2309.09968.
- Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.* KDD 2016.
- Ho, J. et al. (2020). *Denoising Diffusion Probabilistic Models.* NeurIPS 2020.
- Lipman, Y. et al. (2022). *Flow Matching for Generative Modeling.* ICLR 2023.
