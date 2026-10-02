# Semana 4 — Cuadro técnico consolidado

**Tema:** Librerías para cálculo numérico, análisis y visualización de datos (Pandas, NumPy, SciPy, Matplotlib, Seaborn).
**Datasets de la actividad:** *Netflix TV Shows and Movies* (Soeiro, 2022) — `credits.csv` (77 801 créditos, 5 489 títulos, 54 589 personas) y `titles.csv` (5 850 títulos).

> Todas las cifras de este documento se recalcularon ejecutando el código sobre los CSV del repositorio (Python con SciPy 1.17.1, pandas 3.0.6, `random_state=42` donde hubo muestreo). Las marcadas con ✅ son las que ya aparecen en los notebooks de solución del profesor; las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en esas soluciones.

---

## 1. Procedimientos del taller (de punta a punta)

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la actividad |
|---|---|---|---|---|
| Carga y exploración | Pandas | `read_csv`, `head()`, `shape`, `info()` | Conocer estructura, tipos y tamaño | `credits.csv`: 77 801 × 5. `titles.csv`: 5 850 × 15 (viene en ZIP: `compression="zip"`) |
| Calidad de datos | Pandas | `isnull().sum()`, `duplicated()` | Detectar nulos y repetidos | `credits`: 9 772 nulos en `character` (son los directores), 0 duplicados. `titles`: 2 619 nulos en `age_certification`, 14 filas con `runtime == 0` |
| Limpieza | Pandas | `fillna`, `dropna`, `astype("category")`, `groupby().transform()` | Imputar, eliminar o tipar con criterio | `character` → `"Sin especificar"`; `runtime == 0` → mediana por `type` (película/serie) |
| Variables derivadas | Pandas | `groupby().nunique()`, `agg`, `unstack`, `ast.literal_eval` | Crear numéricas cuando el dataset no las trae | `credits` solo trae identificadores → se construyen `tamano_reparto` y `titulos_por_persona` |
| Arreglos y estadísticos | NumPy | `np.array` / `to_numpy`, `mean`, `median`, `percentile` | Resumir una variable numérica | `tamano_reparto`: media 14.10, mediana 10, P95 = 43 (sesgo a la derecha) |
| Vectorización | NumPy | `(x - x.mean()) / x.std()`, `np.clip`, `np.log1p` | Transformar sin ciclos `for` | z-score manual: 108 títulos con z > 3. Recorte al P99 de `tmdb_popularity` = 273.64 |
| Conteos | NumPy | `np.unique(return_counts=True)`, `np.argsort` | Frecuencias de una categórica | `role`: ACTOR 94.15 % / DIRECTOR 5.85 %. Top 5 géneros: drama, comedia, documentación, thriller, acción |
| Estadística inferencial | SciPy | Ver sección 2 | Decidir si un patrón es real o azar | Shapiro, Pearson/Spearman, t de Welch, z-score |
| Visualización base | Matplotlib | `hist`, `scatter`, `boxplot`, `bar` | Control total de cada elemento | Histograma de `tamano_reparto`; dispersión actores vs. directores |
| Visualización estadística | Seaborn | `histplot(kde=True)`, `violinplot`/`boxplot`, `regplot`, `heatmap` | Gráficas estadísticas con pocas líneas | `regplot` = dispersión + recta; `heatmap` de correlación (en Matplotlib puro sería `imshow` + texto manual) |

---

## 2. Pruebas de SciPy que se pueden aplicar

### 2.1 Cuadro de pruebas

| Pregunta | Prueba (`scipy.stats`) | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Es normal? | **Shapiro-Wilk** · `shapiro` | N ≤ 5 000 (arriba de eso el p-valor se vuelve poco confiable) | `tamano_reparto`: W = 0.719, p = 3.6e-68. `imdb_score`: W = 0.972, p = 2.9e-30 → no normales | ✅ |
| ¿Es normal? (N grande) | **D'Agostino-Pearson** · `normaltest` | Sin tope de N; combina sesgo y curtosis | `imdb_score` (5 849 títulos): K² = 488.9, p = 6.7e-107 | ➕ |
| ¿Qué tan asimétrica? | `skew`, `kurtosis` | Justifica transformar (`log1p`) o usar pruebas por rangos | Sesgo: `tamano_reparto` 3.25 · `tmdb_popularity` 15.03 · `imdb_score` −0.68 | ➕ |
| ¿Hay relación lineal? | **Pearson** · `pearsonr` | Dos numéricas, relación lineal, sin atípicos extremos | Actores vs. directores por título: r = 0.159, p = 1.9e-32. IMDb vs. popularidad: r = 0.017, p = 0.206 (no significativa) | ✅ |
| ¿Hay relación monótona? | **Spearman** · `spearmanr` | Datos sesgados, con atípicos u ordinales (trabaja con rangos) | Actores vs. directores: ρ = 0.229. **IMDb vs. popularidad: ρ = 0.081, p = 4.4e-10** | ✅ / ➕ |
| ¿Relación por concordancia? | **Kendall** · `kendalltau` | Muchos empates o muestras pequeñas | Actores vs. directores: τ = 0.186, p = 2.5e-65 | ➕ |
| ¿Difieren las medias de 2 grupos? | **t de Welch** · `ttest_ind(equal_var=False)` | Aprox. normal o N grande; no exige varianzas iguales | IMDb película vs. serie: 6.28 vs. 6.95, t = −23.37, p = 4.3e-114. Títulos por persona actor vs. director: t = 3.70, p = 0.0002 | ✅ |
| ¿Difieren 2 grupos sin suponer normalidad? | **Mann-Whitney U** · `mannwhitneyu` | Variable sesgada, ordinal o de conteos | IMDb película vs. serie: p = 1.6e-119. Actor vs. director: U = 83 027 144, p = 9.8e-6 | ➕ |
| ¿Tienen igual varianza? | **Levene** · `levene` | Decide entre t de Student y Welch | Película/serie: p = 0.156 (varianzas similares). Actor/director: p = 0.0004 (distintas → Welch es lo correcto) | ➕ |
| ¿Difieren 3 o más grupos? | **ANOVA** · `f_oneway` | Normalidad por grupo y varianzas parecidas | IMDb por género principal (top 5): F = 68.4, p = 3.7e-56. Medias: documentación 7.01, drama 6.72, comedia 6.34, acción 6.30, thriller 6.15 | ➕ |
| ¿Difieren 3 o más grupos (sin normalidad)? | **Kruskal-Wallis** · `kruskal` | Alternativa por rangos a ANOVA | Mismo caso: H = 286.4, p = 9.1e-61 (post hoc posible: `tukey_hsd`) | ➕ |
| ¿Dos categóricas son independientes? | **χ² de independencia** · `chi2_contingency` | Tabla de frecuencias, esperados ≥ 5 | Tipo × estreno desde 2015: χ² = 57.0 (gl = 1), p = 4.3e-14. 77.9 % de las películas vs. 86.0 % de las series | ➕ |
| ¿Quiénes son atípicos? | **z-score** · `zscore` | \|z\| > 3; asume forma más o menos simétrica | `tamano_reparto`: 108 atípicos. `tmdb_popularity`: 61 (1.04 %) | ✅ |
| ¿Atípicos con cola larga? | **IQR / MAD** · `iqr`, `median_abs_deviation` | Robustos ante sesgo | `tamano_reparto`: IQR×1.5 marca 355 y MAD > 3.5 marca 289, frente a 108 del z-score (el z-score subestima con cola larga) | ➕ |
| ¿Hay una tendencia simple? | **Regresión lineal** · `linregress` | Ajuste simple (lo sugiere el Anexo: "algún ajuste simple") | IMDb ~ año de estreno: pendiente −0.0199 puntos/año, r = −0.124, R² = 0.015, p = 1.9e-21 | ➕ |
| ¿Qué tan seguro es el estimado? | **Bootstrap / permutación** · `bootstrap`, `permutation_test` | Sin supuestos de distribución | Actores − directores: diferencia de medias 0.075, IC 95 % [0.035; 0.114]; p de permutación = 0.0004 | ➕ |

### 2.2 Guía rápida para elegir

| Si quiero… | Datos aproximadamente normales | Datos sesgados / ordinales / conteos |
|---|---|---|
| Comparar 2 grupos | t de Welch (`ttest_ind`) | Mann-Whitney (`mannwhitneyu`) |
| Comparar 3+ grupos | ANOVA (`f_oneway`) | Kruskal-Wallis (`kruskal`) |
| Relacionar 2 numéricas | Pearson (`pearsonr`) | Spearman (`spearmanr`) o Kendall |
| Relacionar 2 categóricas | χ² (`chi2_contingency`) | χ² (`chi2_contingency`) |

Regla práctica: ante la duda (colas largas, conteos, calificaciones), correr **las dos** y reportar si coinciden.

---

## 3. Ejemplo guiado: actores vs. directores (`credits.csv`)

**Pregunta:** ¿las personas con rol principal de actor aparecen en más títulos que las de director?

### 3.1 De los promedios de Pandas a la prueba formal

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (Pandas) | `personas.groupby('rol_principal')['titulos_por_persona'].mean()` | Actores 1.422 · Directores 1.347 | Hay diferencia de 0.075 títulos, pero el promedio solo no dice si es azar |
| 2 | Revisar supuestos | `stats.levene(actores, directores)` · `value_counts()` | Levene p = 0.0004. 78.3 % de actores y 81.6 % de directores aparecen en **un solo** título | Varianzas distintas y variable de conteo muy concentrada en 1 → conviene Welch y/o una prueba por rangos |
| 3 | t de Welch | `stats.ttest_ind(actores, directores, equal_var=False)` | t = 3.700, p = 0.0002 | Diferencia estadísticamente significativa |
| 4 | Mann-Whitney | `stats.mannwhitneyu(actores, directores, alternative="two-sided")` | U = 83 027 144, p = 9.8e-6 | Confirma el resultado sin suponer normalidad |
| 5 | Tamaño del efecto | Cohen d = (m₁ − m₂) / s_pooled · CLES = U / (n₁·n₂) · rank-biserial = 2·CLES − 1 | d = 0.065 · CLES = 0.517 · r_rb = 0.034 | Efecto prácticamente nulo: un actor elegido al azar supera a un director elegido al azar el 51.7 % de las veces (50 % sería empate) |
| 6 | Intervalo de confianza | `stats.bootstrap((a, d), ...)` | Dif. de medias 0.075, IC 95 % [0.035; 0.114] | Positiva pero pequeña |

**Conclusión:** la diferencia es estadísticamente significativa porque la muestra es enorme (51 468 actores y 3 121 directores), pero **no es relevante en la práctica**: las medianas son iguales (1 título). Significativo ≠ importante.

### 3.2 Mismo procedimiento con `titles.csv`: película vs. serie (`imdb_score`)

| Prueba | Resultado | Lectura |
|---|---|---|
| Medias | Películas 6.28 · Series 6.95 (medianas 6.5 y 7.0) | Las series tienen mejor calificación |
| Levene | p = 0.156 | Varianzas similares |
| t de Welch | t = −23.37, p = 4.3e-114 | Significativa |
| Mann-Whitney | p = 1.6e-119 | Confirma |
| Tamaño del efecto | Cohen d = −0.63 · r_rb = −0.37 | Efecto **mediano**: aquí la diferencia sí es significativa **y** relevante |

**Contraste didáctico:** mismo flujo, dos conclusiones distintas. Con actores/directores el efecto es casi nulo; con película/serie es moderado. Por eso se reporta siempre el tamaño del efecto junto al p-valor.

### 3.3 Código listo para pegar

```python
import numpy as np
from scipy import stats

actores = personas.loc[personas["rol_principal"] == "ACTOR", "titulos_por_persona"]
directores = personas.loc[personas["rol_principal"] == "DIRECTOR", "titulos_por_persona"]

# 1) Promedios (Pandas)
print(actores.mean(), directores.mean())

# 2) Supuesto de varianzas
print(stats.levene(actores, directores))

# 3) t de Welch y 4) Mann-Whitney
print(stats.ttest_ind(actores, directores, equal_var=False))
u, p = stats.mannwhitneyu(actores, directores, alternative="two-sided")

# 5) Tamaño del efecto
n1, n2 = len(actores), len(directores)
sp = np.sqrt(((n1 - 1) * actores.var() + (n2 - 1) * directores.var()) / (n1 + n2 - 2))
cohen_d = (actores.mean() - directores.mean()) / sp
cles = u / (n1 * n2)            # prob. de que un actor supere a un director (empates = 0.5)
rank_biserial = 2 * cles - 1
print(p, cohen_d, cles, rank_biserial)
```

---

## 4. Salvedades que conviene conocer

1. **Pearson vs. Spearman en `titles.csv`.** La solución del profesor concluye que no hay evidencia de relación entre `imdb_score` y `tmdb_popularity` usando Pearson (r = 0.017, p = 0.21). Con Spearman sí aparece una relación positiva muy débil pero significativa (ρ = 0.081, p = 4.4e-10), porque `tmdb_popularity` tiene sesgo 15 y los valores extremos distorsionan a Pearson. Aun así el efecto es pequeño (ρ² ≈ 0.7 %).
2. **Sensibilidad al desempate en `credits.csv`.** 412 personas tienen créditos como actor *y* como director; `value_counts().idxmax()` resuelve el empate según el tipo de dato. Con `role` como `category` (como en el notebook del profesor) salen 51 468 actores y 3 121 directores; con texto plano salen 51 434 y 3 155 (t = 3.25, p = 0.0012). La conclusión no cambia, pero las n sí.
3. **Cifra desactualizada en la interpretación del notebook.** En `EIARV011_A4_analisis_credits.ipynb` la celda de interpretación (tras la celda 28) dice que los directores promedian 1.36 títulos, pero la salida del propio notebook es 1.347 (≈ 1.35).
4. **La comparación actores/directores del notebook del profesor ya usa t de Welch** (celda 28), no solo promedios. Lo que falta, y lo que este cuadro propone, es verificar supuestos (Levene), contrastar con Mann-Whitney y reportar el tamaño del efecto.
5. **Pruebas múltiples.** No se aplicó corrección (Bonferroni/FDR) porque cada prueba responde una pregunta distinta del taller; si se encadenaran muchas comparaciones sobre los mismos datos habría que corregir.
6. **Shapiro-Wilk con N > 5 000.** Por eso los notebooks toman una muestra de 5 000; con el conjunto completo SciPy advierte que el p-valor puede no ser exacto.
