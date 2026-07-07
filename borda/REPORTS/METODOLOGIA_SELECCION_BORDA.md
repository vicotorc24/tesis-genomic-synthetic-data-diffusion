# Metodología de Consenso: Ensemble Borda Count (Selección de Genes Élite)

**Autor:** Gary Velásquez Narro  
**Fecha:** Junio 2026  
**Proyecto:** Datalake Armonizado Oncológico - Tesis Doctoral 2026

Este documento detalla el fundamento teórico, la formulación matemática, la implementación en código y los resultados empíricos del algoritmo de votación **Ensemble Borda Count** utilizado para seleccionar la cohorte Élite de **1,000 genes** para el entrenamiento de los modelos generativos.

---

## 1. Justificación del Enfoque Híbrido

En la minería de datos genómicos de alta dimensionalidad ($N \ll D$), los selectores individuales de características presentan sesgos inherentes:
*   Los **métodos univariados (como F-Test)** son rápidos pero ignoran por completo las interacciones de co-expresión o correlaciones cruzadas no lineales entre genes.
*   Los **modelos basados en impurezas de árboles (como RandomForest)** capturan interacciones complejas pero favorecen sesgos hacia características continuas de alta cardinalidad.
*   Los **métodos de explicabilidad local (como SHAP)** son extremadamente precisos pero pueden verse afectados por colinealidades severas si no se regularizan.

El método **Ensemble Borda Count** actúa como un sistema electoral ponderado que neutraliza las limitaciones individuales mediante consenso de rango (voting rule).

---

## 2. Formulación Matemática de la Votación Borda

Sea $G = \{g_1, g_2, \dots, g_D\}$ el conjunto de $D$ genes ($D=2,500$ en nuestro espacio) y $V = \{v_1, v_2, v_3\}$ el conjunto de los 3 "votantes" de importancia de atributos:
1.  $v_1$: Univariante Paramétrico (F-Test de Fisher).
2.  $v_2$: Impureza de Ensamble de Árboles (Random Forest Feature Importance).
3.  $v_3$: Aditividad Marginal Local (SHAP Mean Absolute Values en XGBoost).

Para cada votante $v_j$, se calcula la importancia de cada gen y se asigna un rango ordinal $\text{rank}_j(g_i)$, donde el gen con mayor score de importancia recibe el rango $1$, y el gen menos importante recibe el rango $D$.

La puntuación final Borda (Mean Rank) de un gen $g_i$ se define como el promedio aritmético de sus rangos individuales:

$$B(g_i) = \frac{1}{|V|} \sum_{j=1}^{|V|} \text{rank}_j(g_i) = \frac{\text{rank}_{\text{F-Test}}(g_i) + \text{rank}_{\text{RF}}(g_i) + \text{rank}_{\text{SHAP}}(g_i)}{3}$$

El conjunto final de $K$ genes seleccionados es el subconjunto $G^* \subset G$ de tamaño $K$ que minimiza la puntuación Borda:

$$G^* = \operatorname{argmin}_{g \in G, |G^*|=K} B(g)$$

---

## 3. Implementación en Código (`feature_selection.py`)

La lógica electoral se ejecuta bajo el método `'ensemble'` en el módulo de selección del repositorio:

```python
# 1. F-Test Ranking
selector = SelectKBest(f_classif, k='all')
selector.fit(X_clean, y)
f_scores = np.nan_to_num(selector.scores_, nan=0.0)
f_ranks = pd.Series(f_scores, index=X.columns).rank(ascending=False, method='min')

# 2. Random Forest Importance Ranking
rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
rf.fit(X_clean, y)
rf_ranks = pd.Series(rf.feature_importances_, index=X.columns).rank(ascending=False, method='min')

# 3. SHAP Ranking (Fast XGBoost)
model = xgb.XGBClassifier(n_estimators=50, max_depth=3, random_state=42, n_jobs=-1)
model.fit(X_clean, y)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_clean)
import_scores = np.abs(shap_values).mean(axis=0)
shap_ranks = pd.Series(import_scores, index=X.columns).rank(ascending=False, method='min')

# 4. Borda Count (Promedio de rangos, menor es mejor)
borda_df = pd.DataFrame({
    'F_Test': f_ranks,
    'RF': rf_ranks,
    'SHAP': shap_ranks
})
borda_df['Mean_Rank'] = borda_df.mean(axis=1)
selected_features = borda_df.sort_values(by='Mean_Rank', ascending=True).head(k).index.tolist()
```

---

## 4. Resultados del Consenso: Top 15 Genes Oncológicos

Al correr la auditoría Borda sobre los **9,309 pacientes**, se obtuvo la siguiente matriz de consenso:

| Gen Selector | Rango F-Test | Rango RF | Rango SHAP | Borda Mean Rank |
| :--- | :--- | :--- | :--- | :--- |
| **SDHA** | 2.0 | 1.0 | 3.0 | **2.00** |
| **FOXP3** | 4.0 | 14.0 | 8.0 | **8.67** |
| **CKMT2** | 37.0 | 22.0 | 2.0 | **20.33** |
| **S100A9** | 15.0 | 55.0 | 82.0 | **50.67** |
| **KLF4** | 172.0 | 7.0 | 10.0 | **63.00** |
| **CXCL9** | 26.0 | 163.0 | 9.0 | **66.00** |
| **SNCA** | 119.0 | 10.0 | 72.0 | **67.00** |
| **ABLIM1** | 170.0 | 50.0 | 17.0 | **79.00** |
| **CCR7** | 55.0 | 41.0 | 148.0 | **81.33** |
| **PDCD1LG2** | 3.0 | 3.0 | 257.0 | **87.66** |
| **CD247** | 17.0 | 9.0 | 257.0 | **94.33** |
| **MXD1** | 22.0 | 6.0 | 257.0 | **95.00** |
| **CSF2** | 35.0 | 15.0 | 257.0 | **102.33** |
| **IL18** | 88.0 | 25.0 | 203.0 | **105.33** |
| **CASP1** | 6.0 | 53.0 | 257.0 | **105.33** |

### 🔬 Demostración de Rescate Clínico (Ejemplo: Gen KLF4)
El gen **`KLF4`** (Kruppel-like factor 4) es un factor de transcripción crítico en la regulación de la diferenciación celular y un conocido supresor tumoral en múltiples carcinomas. 
*   **Fallo de Selección Clásica:** El F-Test de Fisher (métrica univariada paramétrica clásica) lo ubó en el puesto **172**, lo que en muchos estudios tradicionales habría causado que quedara descartado.
*   **Rescate del Consenso:** Debido a su alta no linealidad explicada por la estructura de árboles de RandomForest (puesto **7**) y XGBoost+SHAP (puesto **10**), el algoritmo Borda lo colocó en el puesto **5** global. Esto valida que la metodología electoral evita la pérdida de marcadores altamente predictivos complejos.

---

## 🖼️ Visualización del Mapa de Consenso
El mapa de calor de rangos está exportado localmente en:
`results/metrics/consenso_borda_heatmap.png`

Esta figura mapea visualmente la homogeneidad de votos sobre los genes candidatos y constituye un respaldo gráfico de alta calidad para la defensa oral del Capítulo 4.
