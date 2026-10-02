# Semana 5 — Cuadro técnico consolidado

**Tema:** Estadística básica y visualización de datos (estadística descriptiva, gráficos con Matplotlib, correlación y primer contacto con la prueba de hipótesis).
**Dataset de la actividad:** `StudentsPerformance.csv` — 1 000 estudiantes × 8 columnas: tres notas de 0 a 100 (`math score`, `reading score`, `writing score`) y cinco variables categóricas (`gender`, `race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`). Sin nulos y sin duplicados. Las dos copias del archivo (carpetas de la guía y del taller) son idénticas byte a byte.

> Todas las cifras de este documento se recalcularon ejecutando el código sobre el CSV del repositorio (Python con SciPy 1.17.1, pandas 2.3.3, NumPy 2.4.6 y Matplotlib 3.11.2; `random_state=42` donde hubo remuestreo). Las marcadas con ✅ son las que ya aparecen en el notebook y en la clave del profesor (`02_Ejercicios_aplicacion_profesor.ipynb` y `Taller_01_Visualizacion_de_datos_profesor`); las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en esos materiales (incluye las pruebas que la guía menciona pero el notebook no ejecuta).

---

## 1. Procedimientos del taller (de punta a punta)

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la actividad |
|---|---|---|---|---|
| Carga y exploración | Pandas | `read_csv`, `head()`, `shape`, `dtypes`, `describe()` | Conocer estructura, tipos y rango de cada nota | 1 000 × 8. Mínimos: math 0, reading 17, writing 10; máximo 100 en las tres |
| Calidad de datos | Pandas | `isnull().sum()`, `duplicated()` | Detectar nulos y repetidos (el notebook no lo revisa) | 0 nulos y 0 duplicados |
| Tipos de variables | Pandas | `select_dtypes`, `nunique()`, `astype("category")` | Decidir qué operaciones y qué pruebas tienen sentido | 3 cuantitativas y 5 cualitativas: `gender` 2 categorías, `race/ethnicity` 5, `parental level of education` 6 (ordinal), `lunch` 2, `test preparation course` 2 |
| Tamaño de muestra y de grupos | Pandas | `len`, `value_counts()`, `groupby().size()` | Reportar n total y n por grupo | n = 1 000. Curso: `none` 642 / `completed` 358. Etnia: A 89, B 190, C 319, D 262, E 140 |
| Tendencia central | Pandas | `mean`, `median`, `mode` | Resumir el dato típico | math 66.09 / 66.0 / 65 · reading 69.17 / 70.0 / 72 · writing 68.05 / 69.0 / 74 |
| Dispersión | Pandas | `std` (ddof = 1), `min`/`max`, `quantile` | Ver qué tan parejos son los datos | math: rango 100, s = 15.16, Q1 = 57, Q2 = 66, Q3 = 77, IQR = 20. El 69.6 % cae entre 50.9 y 81.3 (media ± 1 s) |
| Valores atípicos | Pandas | Regla 1.5 × IQR | Marcar casos a revisar antes de concluir | math: límites [27, 107] → 8 atípicos (0, 8, 18, 19, 22, 23, 24, 26) |
| Visualización | Matplotlib | `bar`, `hist`, `boxplot`, `scatter`, `pie`, `axvline`, `ylim` | Ver la forma, la comparación y la relación | Ver sección 2 |
| Correlación | Pandas | `corr()` | Medir la asociación lineal entre las tres notas | Lectura–escritura 0.955 · matemáticas–lectura 0.818 · matemáticas–escritura 0.803 |
| Hipótesis | — | H0 / H1 en palabras y en notación (μ₁ = μ₂) | Dejar por escrito qué se pone a prueba | H0: el promedio de `math score` es igual con y sin curso; H1: es distinto. α = 0.05 |
| Supuestos | SciPy | `shapiro`, `levene` | Decidir entre prueba paramétrica y no paramétrica | Shapiro `math score`: W = 0.9932, p = 0.000145. Levene por curso: W = 0.5330, p = 0.4655 |
| Prueba inferencial | SciPy | `ttest_ind`, `f_oneway`, `kruskal`, `pearsonr` | Decidir si un patrón es real o azar | Ver sección 3 |
| Decisión | Python | `if p < alpha` (función `decidir_H0`) | Aplicar la regla de decisión de forma uniforme | Las cuatro pruebas del notebook tienen p < 0.05 → se rechaza H0 |
| Interpretación | — | Estadístico + p-value + decisión + advertencia de causalidad | Redactar la conclusión del portafolio | "Asociado con", nunca "causa" |

---

## 2. Qué gráfico usar (Matplotlib)

| Pregunta | Gráfico (función) | Ejemplo con el dataset | Cuidado al leerlo | Uso |
|---|---|---|---|---|
| ¿Cuántos casos hay de cada categoría? | Barras · `plt.bar` | Curso: 642 `none` vs. 358 `completed`. Almuerzo: 645 `standard` vs. 355 `free/reduced` | Con una numérica continua (`math score`) saldrían decenas de barras: ahí va un histograma | ✅ |
| ¿Cómo se distribuye una numérica? | Histograma · `plt.hist` + `axvline` | `math score`: media 66.09 y mediana 66.0 casi pegadas → distribución simétrica | El número de *bins* cambia la historia: con 5 *bins* (ancho 20) el pico concentra 484 estudiantes y se pierde la forma; con 20 (ancho 5) el máximo es 144; con 50 (ancho 2) hay 8 cajones vacíos y el gráfico se vuelve dentado | ✅ |
| ¿Cómo se compara una numérica entre grupos? | Boxplot · `plt.boxplot` | `none`: Q1 54, mediana 64, Q3 74.75, 5 atípicos bajos. `completed`: Q1 60, mediana 69, Q3 79, 2 atípicos bajos | La caja es el IQR; sirve para comparar de un vistazo, pero no prueba que la diferencia sea real | ✅ |
| ¿Hay relación entre dos numéricas? | Dispersión · `plt.scatter` | Lectura vs. escritura: nube diagonal estrecha (r = 0.955). Lectura vs. matemáticas: más dispersa (r = 0.818) | Usar `alpha` si hay muchos puntos superpuestos | ✅ |
| ¿Qué proporción es cada parte? | Pastel · `plt.pie` | Almuerzo: 64.5 % `standard` / 35.5 % `free/reduced` | Con 6 categorías (`parental level of education`: 22.6 %, 22.2 %, 19.6 %, 17.9 %, 11.8 %, 5.9 %) se vuelve ilegible: mejor barras | ✅ |
| ¿Cómo se compara un promedio entre grupos? | Barras de promedios · `plt.bar` sobre `groupby().mean()` | Etnia → `math score`: A 61.63, B 63.45, C 64.46, D 67.36, E 73.82 | El eje de `plt.bar` parte de 0 por defecto (ver salvedad 1); un eje truncado exagera la diferencia | ✅ |
| ¿Se parece la distribución a una normal? | Gráfico Q-Q · `stats.probplot` | `math score`: r = 0.9966 (casi una recta) | Complementa a Shapiro cuando n es grande y el p-value rechaza por diferencias mínimas | ➕ |
| ¿Cómo se ven forma y comparación a la vez? | *Violin plot* · `seaborn.violinplot` | `math score` por curso, por género o por etnia | Igual que el boxplot, pero muestra además la densidad | ➕ |
| ¿Qué tan fuertes son todas las correlaciones juntas? | Mapa de calor · `seaborn.heatmap(df.corr())` | Matriz 3 × 3 de las notas (0.803 a 0.955) | Con solo 3 variables una tabla alcanza; útil si se suman más | ➕ |
| ¿Qué tan seguro es el promedio de cada grupo? | Barras con intervalo de confianza · `plt.errorbar` | IC 95 % de la media de `math` por curso: `none` [62.90; 65.26] y `completed` [68.19; 71.20] (no se solapan) | Dos intervalos que no se solapan sugieren diferencia; si se solapan un poco, no basta para concluir lo contrario | ➕ |

---

## 3. Pruebas de SciPy que se pueden aplicar

### 3.1 Cuadro de pruebas

| Pregunta | Prueba (`scipy.stats`) | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Es normal? | **Shapiro-Wilk** · `shapiro` | N ≤ 5 000; con n grande detecta desviaciones diminutas | `math`: W = 0.9932, p = 1.5e-4. `reading`: W = 0.9929, p = 1.1e-4. `writing`: W = 0.9920, p = 2.9e-5 → ninguna normal en sentido estricto | ✅ (math) / ➕ |
| ¿Es normal dentro de cada grupo? | Shapiro por grupo | El t de Student asume normalidad en cada grupo (o residuales) | `math` por curso: `none` W = 0.9921, p = 0.0018; `completed` W = 0.9937, p = 0.139. Residuales: p = 0.0005 | ➕ |
| ¿Es normal? (alternativa) | **D'Agostino-Pearson** · `normaltest` | Combina sesgo y curtosis | `math` K² = 15.41, p = 4.5e-4 · `reading` K² = 11.12, p = 3.9e-3 · `writing` K² = 13.61, p = 1.1e-3 | ➕ |
| ¿Qué tan asimétrica? | `skew`, `kurtosis` | Mide *cuánto* se aparta de la normal, no solo si se aparta | Sesgo: math −0.28, reading −0.26, writing −0.29. Curtosis (exceso): 0.27, −0.07, −0.04 → leve cola hacia notas bajas | ➕ |
| ¿Igual varianza (2 grupos)? | **Levene** · `levene` | Decide entre t de Student y Welch | Curso → `math`: W = 0.5330, p = 0.4655 (homogéneas). Género → `writing`: p = 0.934 | ✅ / ➕ |
| ¿Igual varianza (3+ grupos)? | Levene / **Bartlett** · `bartlett` | Antes de un ANOVA (Bartlett exige normalidad) | Etnia → `math`: Levene W = 0.5903, p = 0.6697; Bartlett p = 0.396 | ➕ |
| ¿Difieren las medias de 2 grupos? | **t de Student** · `ttest_ind(equal_var=True)` | Aprox. normal o n grande; varianzas homogéneas | Curso → `math`: 64.08 (`none`) vs. 69.70 (`completed`), t = −5.705, gl = 998, p = 1.5e-8 (el signo depende del orden de los grupos) | ✅ |
| ¿Difieren las medias de 2 grupos (sin exigir varianzas iguales)? | **t de Welch** · `ttest_ind(equal_var=False)` | Opción más segura por defecto | Mismo caso: t = −5.787, gl = 770.1, p = 1.0e-8 | ➕ |
| ¿Difieren 2 grupos sin suponer normalidad? | **Mann-Whitney U** · `mannwhitneyu` | Variable sesgada u ordinal | Mismo caso: U = 138 412, p = 8.0e-8 | ➕ |
| ¿La media es distinta de un valor de referencia? | **t de una muestra** · `ttest_1samp` | Un solo grupo contra μ₀ (la guía la menciona; el notebook no la ejecuta). Valores de μ₀ ilustrativos | `math` vs. μ₀ = 70: t = −8.156, gl = 999, p = 1.0e-15 (rechaza H0). Vs. μ₀ = 66: t = 0.186, p = 0.853 (no rechaza). IC 95 % de la media: [65.15; 67.03] | ➕ |
| ¿Lo mismo, sin normalidad? | **Wilcoxon** · `wilcoxon(x - mu0)` | Alternativa por rangos a la t de una muestra | μ₀ = 70: p = 1.3e-13. μ₀ = 66: p = 0.485 | ➕ |
| ¿Difieren dos mediciones del mismo estudiante? | **t pareada** · `ttest_rel` / `wilcoxon(a, b)` | Datos emparejados (no independientes) | Lectura vs. escritura: diferencia media 1.115, t = 7.787, gl = 999, p = 1.7e-14, IC 95 % [0.834; 1.396]. Tratándolas como independientes daría t = 1.673, p = 0.094 | ➕ |
| ¿Difieren 3 o más grupos? | **ANOVA** · `f_oneway` | Normalidad por grupo y varianzas parecidas | Etnia → `math`: F = 14.594, p = 1.4e-11 | ✅ |
| ¿Difieren 3 o más grupos (sin normalidad)? | **Kruskal-Wallis** · `kruskal` | Alternativa por rangos a ANOVA | Mismo caso: H = 57.079, p = 1.2e-11. Nivel educativo de los padres → `reading` (6 grupos): ANOVA F = 9.289, p = 1.2e-8; Kruskal H = 38.665, p = 2.8e-7 | ✅ / ➕ |
| ¿Cuáles grupos son distintos? | **Tukey HSD** · `tukey_hsd` | *Post hoc* tras un ANOVA significativo; controla el error por comparaciones múltiples | Etnia → `math`: 6 de 10 pares significativos (A–D, A–E, B–D, B–E, C–E, D–E) | ➕ |
| ¿Hay relación lineal? | **Pearson** · `pearsonr` | Dos numéricas, relación lineal, sin atípicos extremos | Lectura–escritura: r = 0.955 (IC 95 % [0.949; 0.960]), p = 0.0 (ver salvedad 4). Mate–lectura: r = 0.818, p = 1.8e-241. Mate–escritura: r = 0.803, p = 3.4e-226 | ✅ |
| ¿Hay relación monótona? | **Spearman** · `spearmanr` | Datos sesgados, atípicos u ordinales | ρ = 0.949 (lectura–escritura), 0.804 (mate–lectura), 0.778 (mate–escritura). Nivel educativo (codificado de 0 a 5) vs. `reading`: ρ = 0.172, p = 4.3e-8 | ➕ |
| ¿Relación por concordancia? | **Kendall** · `kendalltau` | Muchos empates o muestras pequeñas | τ = 0.820, 0.617 y 0.591 en los mismos tres pares | ➕ |
| ¿Hay una tendencia simple? | **Regresión lineal** · `linregress` | Ajuste de una recta (anticipa la Semana 7) | `writing` = −0.668 + 0.9935 · `reading`, R² = 0.911, error estándar de la pendiente 0.0098. Con `reading` = 80 la recta predice `writing` = 78.8 | ➕ |
| ¿Dos categóricas son independientes? | **χ² de independencia** · `chi2_contingency` | Tabla de frecuencias, esperados ≥ 5 | Género × curso: χ² = 0.016, gl = 1, p = 0.90 (V de Cramér 0.004). Almuerzo × curso: χ² = 0.221, p = 0.64. Etnia × almuerzo: χ² = 3.442, gl = 4, p = 0.49 | ➕ |
| ¿Quiénes son atípicos? | **IQR 1.5×** (✅) · `zscore` · `median_abs_deviation` (➕) | IQR y MAD son robustos; z-score asume forma simétrica | `math`: IQR marca 8; z > 3 marca 4; MAD modificado > 3.5 marca 2 | ✅ / ➕ |
| ¿Qué tan seguro es el estimado? | **Bootstrap / permutación** · `bootstrap`, `permutation_test` | Sin supuestos de distribución | Curso → `math`: diferencia de medias 5.62, IC 95 % [3.76; 7.53]; p de permutación = 0.0002 | ➕ |

### 3.2 Guía rápida para elegir

| Si quiero… | Datos aproximadamente normales | Datos sesgados / ordinales |
|---|---|---|
| Comparar 2 grupos independientes | t de Student (Levene OK) o t de Welch (`ttest_ind`) | Mann-Whitney (`mannwhitneyu`) |
| Comparar 2 mediciones del mismo estudiante | t pareada (`ttest_rel`) | Wilcoxon pareado (`wilcoxon`) |
| Comparar 3+ grupos | ANOVA (`f_oneway`) + Tukey | Kruskal-Wallis (`kruskal`) |
| Comparar un promedio con un valor fijo | t de una muestra (`ttest_1samp`) | Wilcoxon (`wilcoxon`) |
| Relacionar 2 numéricas | Pearson (`pearsonr`) | Spearman (`spearmanr`) o Kendall |
| Relacionar 2 categóricas | χ² (`chi2_contingency`) | χ² (`chi2_contingency`) |

Regla práctica: con n = 1 000 los tests de normalidad rechazan casi siempre, aunque la forma sea aceptable. Conviene mirar histograma, Q-Q y sesgo, y ante la duda correr **las dos** pruebas (paramétrica y por rangos) y reportar si coinciden.

---

## 4. Ejemplo guiado 1: curso de preparación vs. nota de matemáticas (2 grupos)

**Pregunta:** ¿los estudiantes que completaron el curso de preparación obtienen, en promedio, una nota de matemáticas distinta de quienes no lo tomaron?

### 4.1 De los promedios a la prueba formal

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (Pandas) | `df.groupby('test preparation course')['math score'].agg(['count','mean','median','std'])` | `completed`: n = 358, media 69.70, mediana 69, s = 14.44. `none`: n = 642, media 64.08, mediana 64, s = 15.19 | Diferencia de 5.62 puntos; el promedio solo no dice si es azar |
| 2 | Gráfico | `plt.boxplot([none, completed])` | `none`: Q1 54 · mediana 64 · Q3 74.75. `completed`: Q1 60 · mediana 69 · Q3 79 | La caja de `completed` queda unos 5 puntos más arriba |
| 3 | Hipótesis | — | H0: μ_completed = μ_none · H1: μ_completed ≠ μ_none · α = 0.05 | Prueba de dos colas |
| 4 | Revisar supuestos | `stats.shapiro` por grupo · `stats.levene` | Shapiro: `none` p = 0.0018, `completed` p = 0.139. Levene: p = 0.4655 (Bartlett p = 0.28) | Normalidad estricta dudosa en `none`, pero con 642 y 358 datos el t es robusto; varianzas homogéneas → Student es válido |
| 5 | t de Student | `stats.ttest_ind(completed, none, equal_var=True)` | t = 5.705, gl = 998, p = 1.5e-8 | Rechaza H0 |
| 6 | t de Welch | `stats.ttest_ind(completed, none, equal_var=False)` | t = 5.787, gl = 770.1, p = 1.0e-8 | Igual conclusión |
| 7 | Mann-Whitney | `stats.mannwhitneyu(completed, none)` | U = 138 412, p = 8.0e-8 | Confirma sin suponer normalidad |
| 8 | Tamaño del efecto | Cohen d = (m₁ − m₂) / s_pooled · CLES = U / (n₁·n₂) · rank-biserial = 2·CLES − 1 | d = 0.376 · CLES = 0.602 · r_rb = 0.204 | Efecto de pequeño a mediano: un estudiante con curso supera a uno sin curso el 60.2 % de las veces (50 % sería empate) |
| 9 | Intervalo de confianza | `stats.bootstrap(...)`, `stats.permutation_test(...)` | Diferencia 5.62, IC 95 % [3.76; 7.53] (con la fórmula t clásica: [3.69; 7.55]); p de permutación = 0.0002 | La diferencia es positiva y el intervalo no incluye 0 |

**Conclusión:** con un nivel de significancia del 5 % se rechaza H0. La diferencia es estadísticamente significativa y de tamaño **pequeño a mediano**: unos 5.6 puntos sobre 100, es decir, 0.38 desviaciones estándar. Es una asociación, no una prueba de que el curso *cause* la mejora (ver salvedad 9).

### 4.2 Mismo procedimiento, otras comparaciones del dataset

| Contraste | Medias | p (Welch o χ²) | Tamaño del efecto | Lectura |
|---|---|---|---|---|
| Curso → `math` | 69.70 vs. 64.08 | 1.0e-8 | d = 0.376 | Pequeño a mediano |
| Curso → `reading` | 73.89 vs. 66.53 | 4.4e-15 | d = 0.519 | Mediano |
| Curso → `writing` | 74.42 vs. 64.50 | 2.7e-25 | d = 0.687 | Mediano a grande |
| Género → `writing` (mujeres vs. hombres) | 72.47 vs. 63.31 | 1.7e-22 | d = 0.632 | Mediano a grande |
| Género → `reading` | 72.61 vs. 65.47 | 4.4e-15 | d = 0.504 | Mediano |
| Género → `math` | 63.63 vs. 68.73 | 8.4e-8 | d = −0.341 | Pequeño, **a favor de los hombres** |
| Almuerzo → `math` (`standard` vs. `free/reduced`) | 70.03 vs. 58.92 | 5.5e-28 | d = 0.782 | Casi grande: el mayor del dataset |
| Lectura vs. escritura (mismos estudiantes, pareada) | Diferencia 1.115 | 1.7e-14 | d_z = 0.246 | Significativa, pero ≈ 1 punto: efecto pequeño |
| Género × curso (χ²) | 35.5 % de mujeres vs. 36.1 % de hombres completó el curso | 0.90 | V = 0.004 | Sin asociación: **no se rechaza H0** |

**Contraste didáctico:** con n = 1 000, casi toda diferencia sale "significativa" (p entre 1e-8 y 1e-28), así que el p-value no sirve para ordenarlas; el tamaño del efecto sí. El almuerzo pesa más sobre la nota de matemáticas (≈ 11 puntos) que el curso de preparación (≈ 5.6). La única comparación que no rechaza H0 es la de género × curso.

### 4.3 Código listo para pegar

```python
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("StudentsPerformance.csv")
completed = df.loc[df["test preparation course"] == "completed", "math score"]
none = df.loc[df["test preparation course"] == "none", "math score"]

# 1) Promedios (Pandas)
print(df.groupby("test preparation course")["math score"].agg(["count", "mean", "median", "std"]))

# 2) Supuestos
print(stats.shapiro(completed), stats.shapiro(none))
print(stats.levene(completed, none))

# 3) t de Student, Welch y Mann-Whitney
print(stats.ttest_ind(completed, none, equal_var=True))
print(stats.ttest_ind(completed, none, equal_var=False))
u, p = stats.mannwhitneyu(completed, none, alternative="two-sided")

# 4) Tamaño del efecto
n1, n2 = len(completed), len(none)
sp = np.sqrt(((n1 - 1) * completed.var() + (n2 - 1) * none.var()) / (n1 + n2 - 2))
cohen_d = (completed.mean() - none.mean()) / sp
cles = u / (n1 * n2)            # prob. de que un estudiante con curso supere a uno sin curso (empates = 0.5)
rank_biserial = 2 * cles - 1
print(u, p, cohen_d, cles, rank_biserial)

# 5) Intervalo de confianza de la diferencia de medias (bootstrap)
dif = lambda a, b, axis: np.mean(a, axis=axis) - np.mean(b, axis=axis)
res = stats.bootstrap((completed.to_numpy(), none.to_numpy()), dif,
                      n_resamples=9999, method="percentile", random_state=42)
print(res.confidence_interval)
```

---

## 5. Ejemplo guiado 2: etnia vs. nota de matemáticas (5 grupos)

**Pregunta:** ¿el promedio de `math score` es distinto entre los cinco grupos de `race/ethnicity`?

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (Pandas) | `df.groupby('race/ethnicity')['math score'].mean()` | A 61.63 (n = 89) · B 63.45 (190) · C 64.46 (319) · D 67.36 (262) · E 73.82 (140) | Hay 12.19 puntos entre el grupo más bajo y el más alto |
| 2 | Hipótesis | — | H0: las cinco medias son iguales · H1: al menos una es distinta | Con 3 o más grupos se usa ANOVA, no varias pruebas t |
| 3 | Revisar supuestos | `stats.levene(*grupos)` · `stats.shapiro` por grupo | Levene: W = 0.5903, p = 0.6697 (desviaciones entre 13.77 y 15.53). Shapiro: A 0.85, B 0.010, C 0.017, D 0.059, E 0.018 | Varianzas homogéneas; normalidad estricta dudosa en 3 grupos, con n ≥ 89 por grupo |
| 4 | ANOVA | `stats.f_oneway(*grupos)` | F = 14.594, p = 1.4e-11 | Rechaza H0 |
| 5 | Kruskal-Wallis | `stats.kruskal(*grupos)` | H = 57.079, p = 1.2e-11 | Confirma sin suponer normalidad |
| 6 | Tamaño del efecto | η² = SSB / SST · ε² = H / ((N² − 1) / (N + 1)) | η² = 0.055 · ε² = 0.057 | La etnia explica ≈ 5.5 % de la variación de la nota: efecto de pequeño a mediano |
| 7 | *Post hoc* | `stats.tukey_hsd(*grupos)` | Significativos: A–D (5.73, p = 0.014), A–E (12.19, p = 1.6e-8), B–D (3.91, p = 0.044), B–E (10.37, p = 4.3e-9), C–E (9.36, p = 6.0e-9), D–E (6.46, p = 3.1e-4). No significativos: A–B, A–C, B–C, C–D | E se distingue de todos los demás; A, B y C no se distinguen entre sí |

**Conclusión:** el ANOVA solo dice que *alguna* media es distinta; Tukey dice cuáles. El patrón es E > D > {A, B, C}. Las etiquetas "group A–E" son anónimas en el archivo, por lo que la diferencia no se puede atribuir a un origen étnico en sí: puede reflejar otras variables (por ejemplo, el tipo de almuerzo).

---

## 6. Ejemplo guiado 3: lectura vs. escritura (correlación y recta)

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Gráfico | `plt.scatter(df['reading score'], df['writing score'], alpha=0.4)` | Nube diagonal, estrecha y creciente | Relación lineal positiva evidente |
| 2 | Matriz | `df[['math score', 'reading score', 'writing score']].corr()` | Lectura–escritura 0.955 · mate–lectura 0.818 · mate–escritura 0.803 | La pareja lectura–escritura es la más fuerte |
| 3 | Pearson | `stats.pearsonr(lectura, escritura)` | r = 0.955, IC 95 % [0.949; 0.960], R² = 0.911 | El 91.1 % de la variación de una se comparte con la otra |
| 4 | Spearman y Kendall | `stats.spearmanr`, `stats.kendalltau` | ρ = 0.949 · τ = 0.820 | Coinciden con Pearson: ningún atípico distorsiona la correlación |
| 5 | Recta | `stats.linregress(lectura, escritura)` | `writing` = −0.668 + 0.9935 · `reading` (error estándar de la pendiente 0.0098) | Un punto más en lectura se asocia con ≈ 1 punto más en escritura |
| 6 | Predicción | `intercepto + pendiente * 80` | `reading` = 80 → `writing` = 78.8 | Interpolación dentro del rango observado (17 a 100) |

**Conclusión:** asociación lineal muy fuerte y positiva. Ambas son habilidades del mismo ámbito, así que la fuerza de la relación no dice cuál influye en cuál.

---

## 7. Salvedades que conviene conocer

1. **El eje Y de `plt.bar` sí parte de 0 (error en la clave del taller, Ejercicio 6b-6c).** La clave dice que, sin `plt.ylim`, Matplotlib ajusta el eje a los valores mínimo y máximo (≈ 61 a 74) y por eso las diferencias "se ven exageradas". Al ejecutarlo, `plt.bar` deja `ylim = (0, 77.51)` por defecto, porque las barras fijan su base en 0. El gráfico original ya parte de 0 y `plt.ylim(0, 100)` solo lo aplasta (la razón entre la barra más alta y la más baja es 1.20 en ambos casos). El efecto que el ejercicio quiere mostrar aparece al revés: hay que *forzar* un eje truncado, por ejemplo `plt.ylim(60, 75)`.
2. **La normalidad se revisa solo sobre la muestra completa.** El notebook aplica Shapiro a los 1 000 `math score` (p = 1.5e-4). Por grupo: `none` p = 0.0018 y `completed` p = 0.139; sobre los residuales, p = 0.0005. Con n = 1 000 se rechaza por una desviación mínima (sesgo −0.28, curtosis 0.27, Q-Q con r = 0.9966). El t de Welch y Mann-Whitney coinciden con el t de Student, así que la conclusión no depende de este supuesto.
3. **ANOVA sin Levene y sin *post hoc*.** El notebook verifica varianzas solo en los 2 grupos del curso. En los 5 grupos de etnia se cumple (Levene p = 0.6697), pero conviene mostrarlo. Además, ANOVA y Kruskal solo dicen que "alguna" media difiere; Tukey identifica los 6 pares distintos de 10. No se corrigió por comparaciones múltiples entre las pruebas del taller porque cada una responde una pregunta distinta; Tukey sí corrige internamente.
4. **`p-value = 0.000e+00` en Pearson no es cero exacto.** Para lectura–escritura el estadístico t equivalente es ≈ 101 con 998 gl y el p real es menor que el mínimo que representa `float64` (≈ 1e-308), que SciPy redondea a 0. En el portafolio conviene escribir "p < 0.001" (o "p < 1e-300"), no "p = 0".
5. **El signo de t depende del orden de los grupos.** `ttest_ind(none, completed)` da −5.705; `ttest_ind(completed, none)` da +5.705. La dirección del efecto se lee en las medias, no en el signo.
6. **Los atípicos dependen del criterio y de la referencia.** Con 1.5 × IQR sobre toda la muestra salen 8 (0, 8, 18, 19, 22, 23, 24, 26). Por grupo (Ejercicio 3 de la clave) salen 5 en `none` (0, 8, 18, 19, 22) y 2 en `completed` (23, 29): 7 en total y no son los mismos (24 y 26 dejan de serlo y aparece 29). Con z > 3 salen 4 y con MAD 2. Un atípico no es un error: el 0 de `math score` es un único estudiante y debe revisarse antes de eliminarlo.
7. **Cuartiles: la fórmula de la guía y la de pandas no son idénticas.** La guía da la posición k(n+1)/4 (en NumPy, `method="weibull"`); pandas usa interpolación lineal. En `math` y `reading` coinciden; en `writing` el Q1 es 57.25 con la fórmula y 57.75 con pandas. Las cifras del notebook son las de pandas.
8. **El notebook decide solo con p-values.** No reporta tamaño del efecto: los cuatro p son < 0.05 (desde 1.5e-8 hasta uno que se desborda a 0) y esa cifra no distingue qué tan grande es cada efecto (ver tabla 4.2). Conviene reportar d, η² o r² junto al p.
9. **Causalidad y muestra.** El curso de preparación no fue asignado al azar. Los dos grupos son parecidos en género (35.5 % vs. 36.1 % completó el curso; χ² p = 0.90) y en almuerzo (36.9 % vs. 35.2 %; p = 0.64), lo que reduce, pero no elimina, el riesgo de confusión por variables no observadas. El CSV tampoco documenta cómo se obtuvo la muestra, así que generalizar a "todos los estudiantes" tiene un límite.
10. **`parental level of education` es ordinal, pero el notebook la trata como nominal.** `value_counts()` y `groupby` la ordenan alfabéticamente. En su orden natural (`some high school` < `high school` < `some college` < `associate's` < `bachelor's` < `master's`), el promedio de `reading` no crece de forma estrictamente monótona: `some high school` (66.94) supera a `high school` (64.70). Con la codificación ordinal, Spearman da ρ = 0.172 (p = 4.3e-8). Para que Pandas respete el orden hay que declarar `pd.Categorical(..., ordered=True)`.
11. **Compatibilidad de Matplotlib.** `plt.boxplot(..., tick_labels=[...])` exige Matplotlib ≥ 3.9; en versiones anteriores el parámetro se llama `labels`. Una instalación antigua (por ejemplo, un Anaconda sin actualizar) falla con el código del taller.
12. **Archivos del repositorio.** (a) `02_Ejercicios_aplicacion.md`, que está versionado en git, es la versión **resuelta** (no tiene ningún `TODO`), mientras que el notebook de estudiante `02_Ejercicios_aplicacion.ipynb` trae los `TODO`: la solución queda versionada junto al material de los estudiantes. Además sus imágenes apuntan a `02_Ejercicios_aplicacion_files_profesor/`, carpeta que `.gitignore` excluye (`*profesor*`), por lo que esas imágenes no llegan al repositorio y se ven rotas. (b) El taller y el notebook de estudiante enlazan a `01_Estadistica_Basica.md` (con B mayúscula) pero el archivo se llama `01_Estadistica_basica.md`: funciona en Windows y falla en servidores que distinguen mayúsculas.
