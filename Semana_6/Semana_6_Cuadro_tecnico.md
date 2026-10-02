# Semana 6 — Cuadro técnico consolidado

**Tema:** Estadística inferencial y prueba de hipótesis (portafolio de evidencias): población y muestra, H0/H1, p-value, errores tipo I y II, supuestos (normalidad y homogeneidad de varianzas), t de Student / Welch / Mann-Whitney, ANOVA / Kruskal-Wallis, correlación y regresión lineal simple.
**Dataset de la actividad:** `StudentsPerformance.csv` — 1 000 estudiantes × 8 columnas: tres notas de 0 a 100 (`math score`, `reading score`, `writing score`) y cinco variables categóricas (`gender`, `race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`). Sin nulos y sin duplicados. Las cuatro copias del archivo (`Semana_6/`, `Semana_6_Actividad/`, `Semana_6_Actividad_desarrollo/` y `Semana_6_Actividad_solucion_profesor/`) son idénticas byte a byte. El Anexo también permite `BostonHousing.csv` y Netflix (`titles.csv`, `credits.csv`): ver sección 8.

> Todas las cifras de este documento se recalcularon ejecutando el código sobre el CSV del repositorio (Python 3.11.9 con SciPy 1.17.1, pandas 3.0.6, NumPy 2.4.6 y statsmodels 0.15.0; semillas fijas donde hubo remuestreo). Las marcadas con ✅ son las que ya aparecen en el notebook de la actividad (`EIARV011_A6_Notebook.ipynb`), en las claves y notebooks de los talleres (`Taller_01` a `Taller_03`, versión profesor), en `Explicacion/`, en `03_Regla_definir_tamaño_muestra_optima.md` o en las plantillas Excel del ZIP «Material inferencia estadística»; las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en esos materiales.
>
> **Archivos ignorados por Git que se usaron** (`*profesor*` está en `.gitignore`, así que son solo locales): las dos presentaciones `.pptx`, los tres `Taller_0X_…_profesor.md` y `.ipynb`, y en `Semana_6_Actividad_solucion_profesor/`: `EIARV011_A6_Notebook.ipynb`, `Desarrollo_Actividad_Explicado.md`, `Promts.md`, `StudentsPerformance.xlsx`, `zoom_check.png` (captura del notebook del Taller 1) y el ZIP con las plantillas Excel «Anexo1-Plantilla Fase 2, 3 y 4» (sección 9).

---

## 1. Procedimientos del portafolio (de punta a punta)

Siguen los 9 pasos del Anexo. Los procedimientos marcados con (➕) no están en el notebook del profesor.

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la actividad |
|---|---|---|---|---|
| Carga y exploración | Pandas | `read_csv`, `head()`, `shape`, `info()`, `describe()` | Conocer estructura, tipos y rango de cada nota | 1 000 × 8. `math` media 66.09 (0 a 100), `reading` 69.17 (17 a 100), `writing` 68.05 (10 a 100) |
| Calidad de datos | Pandas | `isnull().sum()`, `duplicated().sum()` | Decidir si hay que excluir registros (el Anexo pide declarar el criterio) | 0 nulos y 0 duplicados → no se excluye ninguna fila |
| Pregunta e hipótesis | — | Pregunta investigable + H0/H1 en palabras y en notación; α = 0.05, dos colas | Dejar escrito qué se pone a prueba *antes* de calcular. El Anexo admite tres tipos de pregunta: diferencia entre grupos, relación entre variables, promedio frente a un valor objetivo | "¿Difiere `math score` entre quienes completaron el curso y quienes no?" H0: μ_completed = μ_none · H1: μ_completed ≠ μ_none |
| Variables | Pandas | `dtypes`, `unique()`, `nunique()` | Dependiente (numérica) e independiente (categórica de 2+ grupos; numérica si es correlación) | Dependiente: `math score` (numérica, 0 a 100). Independiente: `test preparation course` (2 grupos) |
| Muestra y grupos | Pandas | `len`, `value_counts()`, `groupby().size()` | Reportar n total y n₁, n₂, … | n = 1 000. `none` 642 (64.2 %) y `completed` 358 (35.8 %) |
| Estadística descriptiva | Pandas | `groupby().describe()` | Media, mediana, desviación, mín/máx y cuartiles por grupo | `completed`: media 69.70, mediana 69, s = 14.44, Q1–Q3 60 a 79. `none`: media 64.08, mediana 64, s = 15.19, Q1–Q3 54 a 74.75 |
| Visualización mínima | Seaborn / Matplotlib | `histplot(kde=True)`, `boxplot`, `scatterplot` | Histograma de la numérica, boxplot por grupo, dispersión si es numérica contra numérica | Ver sección 2 |
| Normalidad (obligatoria) | SciPy | `shapiro` por grupo o sobre la muestra completa | p < 0.05 = evidencia contra la normalidad; p ≥ 0.05 = no se rechaza (con cautela) | `none`: W = 0.9921, p = 0.0018. `completed`: W = 0.9937, p = 0.139. Muestra completa: W = 0.9932, p = 1.5e-4 |
| Homogeneidad de varianzas | SciPy | `levene` | Decidir entre t de Student y t de Welch | W = 0.5330, p = 0.4655 (desviaciones 15.19 y 14.44, razón 1.05) |
| Selección de la prueba | — | Tipo de variables + normalidad + homogeneidad + tamaño de muestra (tabla 3.3) | Justificar la prueba: es lo que evalúa la rúbrica | 2 grupos independientes; normalidad falla en `none`; varianzas homogéneas; n = 642 y 358 → Mann-Whitney principal y t de Student de verificación (clave) |
| Aplicación | SciPy | `mannwhitneyu`, `ttest_ind` | Obtener estadístico y p-value | Mann-Whitney U = 91 424 (orden `none`, `completed`), p = 8.0e-8. t = −5.705, gl = 998, p = 1.5e-8 |
| Decisión | Python | `if p < alpha` (función `decidir`) | Aplicar la regla de forma uniforme | Ambos p < 0.05 → se rechaza H0 |
| Tamaño del efecto e intervalo (➕) | NumPy / SciPy | d de Cohen, CLES, `stats.bootstrap` | Responder "¿cuánta diferencia?": el p-value no lo dice | d = 0.376 (IC 95 % [0.25; 0.51]) · CLES = 0.602 · diferencia 5.62 puntos, IC 95 % [3.76; 7.53] |
| Potencia y tamaño de muestra (➕) | statsmodels | `TTestIndPower` | Saber si n alcanza y qué efecto mínimo detecta | Con 358 y 642 se detecta d ≥ 0.185 (potencia 80 %); para d = 0.376 bastan ≈ 243 estudiantes en total |
| Interpretación | — | Estadístico + p-value + decisión + tamaño del efecto + advertencia de causalidad | Redactar la conclusión en función del problema | "Asociado con", nunca "causa": son datos observacionales |
| Alternativa en Excel (➕ para el portafolio) | Excel | `NORM.S.INV`, `STDEV.S`, "Análisis de varianza de un factor", muestreo sistemático | Mismo flujo (muestra, intervalos, prueba Z, ANOVA) con las plantillas Fase 2 a 4 del ZIP del profesor | Calidad del aire en Medellín (N = 8 030, muestra de 706): ver sección 9 |
| Conclusiones y referencias | — | Qué se aprendió de los supuestos, limitaciones del dataset, análisis futuros; APA | Cerrar el portafolio (paso 9 del Anexo y criterios de la rúbrica) | Ver sección 10 |

---

## 2. Qué gráfico usar (Seaborn / Matplotlib)

| Pregunta | Gráfico (función) | Ejemplo con el dataset | Cuidado al leerlo | Uso |
|---|---|---|---|---|
| ¿Cómo se distribuye la numérica? | Histograma + KDE · `sns.histplot(kde=True)` | `math score`: media 66.09 y mediana 66.0 casi pegadas; sesgo −0.28 y curtosis 0.27 → campana casi simétrica con leve cola hacia notas bajas | La curva no prueba normalidad: Shapiro rechaza (p = 1.5e-4). Es la imagen que acompaña al test | ✅ |
| ¿Cómo se compara entre grupos? | Boxplot · `sns.boxplot(x=grupo, y=numérica)` | `none`: Q1 54, mediana 64, Q3 74.75, 5 atípicos bajos (0, 8, 18, 19, 22). `completed`: Q1 60, mediana 69, Q3 79, 2 atípicos bajos (23, 29) | Cajas de alturas parecidas (IQR 20.75 y 19) → dispersión similar. La caja no prueba que la diferencia sea real | ✅ |
| ¿Forma y comparación a la vez? | *Violin plot* · `sns.violinplot` | Mismo caso | Igual que el boxplot, pero muestra además la densidad. El Anexo lo admite en lugar del boxplot | ➕ |
| ¿Hay relación entre dos numéricas? | Dispersión · `sns.scatterplot(alpha=0.5)` | Lectura vs. escritura: nube diagonal estrecha (r = 0.955). Matemáticas vs. lectura: más abierta (r = 0.818) | Las notas son enteras: hay puntos superpuestos, por eso conviene `alpha` | ✅ |
| ¿Cómo se ve la recta ajustada y su extrapolación? | `plt.plot(x, b0 + b1·x)` sobre `sns.scatterplot`; `ax.axvspan` para el rango real; (`sns.regplot` trae banda) | Notebook del Taller 1: recta roja y punto de predicción en `reading` = 80 (Ejercicio 4); recta punteada hasta 160 con el rango 17–100 sombreado y la predicción imposible 148.36 (Ejercicio 6) | `regplot` dibuja la banda de confianza de la *media* (± 0.35 puntos en `reading` = 80); los estudiantes individuales caen en el intervalo de predicción (± 8.9) | ✅ (recta y extrapolación) / ➕ (bandas) |
| ¿Se parece a una normal? | Gráfico Q-Q · `stats.probplot` | r del Q-Q: `none` 0.9959, `completed` 0.9974, muestra completa 0.9966 | Complementa a Shapiro cuando n es grande y el p-value rechaza por diferencias mínimas | ➕ |
| ¿Qué tan seguro es el promedio de cada grupo? | Puntos con intervalo de confianza · `plt.errorbar` | `none` [62.90; 65.26] y `completed` [68.19; 71.20] (no se solapan). `master's degree` (n = 59, s = 15.15) [65.80; 73.69] frente a `some college` (n = 226, s = 14.31) [65.25; 69.00] | Es el error estándar s/√n del Taller 2: con s parecida, el grupo pequeño tiene un intervalo del doble de ancho | ➕ |
| ¿Se cumplen los supuestos de la recta? | Residuos contra ajustados · `plt.scatter(pred, resid)` | Error estándar residual 4.53 puntos; 3.9 % de los residuos cae fuera de ± 2 errores estándar (≈ 4.6 % esperado) | Detecta curvatura o varianza que cambia con el nivel de `reading` | ➕ |
| ¿Cómo se comparan 3 o más grupos? | Boxplot o puntos con IC por grupo | Etnia → `math`: A 61.63, B 63.45, C 64.46, D 67.36, E 73.82 | Una variable ordinal (`parental level of education`) hay que declararla con `pd.Categorical(..., ordered=True)` para que no salga en orden alfabético | ➕ |

---

## 3. Pruebas de SciPy que se pueden aplicar

### 3.1 Cuadro de pruebas

| Pregunta | Prueba (`scipy.stats`) | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Es normal? | **Shapiro-Wilk** · `shapiro` | N ≤ 5 000; con n grande detecta desviaciones diminutas | `math`: W = 0.9932, p = 1.5e-4 · `reading`: W = 0.9929, p = 1.1e-4 · `writing`: W = 0.9920, p = 2.9e-5 | ✅ |
| ¿Es normal en cada grupo? | Shapiro por grupo | El t de Student y el ANOVA asumen normalidad en cada grupo (o residuales) | Curso → `math`: `none` W = 0.9921, p = 0.0018; `completed` W = 0.9937, p = 0.139. Género → `math`: hombres p = 0.038; mujeres p = 0.0035 | ✅ |
| ¿Es normal? (alternativa) | **D'Agostino-Pearson** · `normaltest` | Combina sesgo y curtosis; sin tope de N | `none`: K² = 14.70, p = 6.4e-4 · `completed`: K² = 1.67, p = 0.43 | ➕ |
| ¿Qué tan asimétrica? | `skew`, `kurtosis` | Mide *cuánto* se aparta de la normal, no solo si se aparta | `none`: sesgo −0.33, curtosis 0.39 · `completed`: −0.15 y −0.18 → desviaciones leves | ➕ |
| ¿Igual varianza (2 grupos)? | **Levene** · `levene` | SciPy centra en la mediana (variante Brown-Forsythe). Decide entre Student y Welch | Curso → `math`: W = 0.5330, p = 0.4655 · Género → `writing`: W = 0.0069, p = 0.934 · Curso → `writing`: p = 0.0147 (**rechaza** → usar Welch) | ✅ |
| ¿Igual varianza (3+ grupos)? | Levene / **Bartlett** · `bartlett` | Bartlett exige normalidad; con datos enteros falla en SciPy 1.17.1 (salvedad 5) | Etnia → `math`: Levene W = 0.5903, p = 0.6697; Bartlett p = 0.396. Educación → `math`: Levene p = 0.458; Bartlett p = 0.749 | ➕ |
| ¿Difieren las medias de 2 grupos? | **t de Student** · `ttest_ind(equal_var=True)` | Aprox. normal o n grande; varianzas homogéneas | Curso → `math`: t = −5.705 (orden `none`, `completed`), gl = 998, p = 1.5e-8 · Género → `math`: t = 5.383, p = 9.1e-8 · Género → `writing`: t = −9.980, p = 2.0e-22 · Almuerzo → `writing`: t = 8.010, p = 3.2e-15 | ✅ |
| ¿Difieren las medias (sin exigir varianzas iguales)? | **t de Welch** · `ttest_ind(equal_var=False)` | Opción segura por defecto; obligatoria si Levene rechaza | Curso → `writing`: Student t = 10.409, p = 3.7e-24 frente a Welch t = 10.753, gl = 811.1, p = 2.7e-25 · Curso → `math`: t = 5.787, gl = 770.1, p = 1.0e-8 | ✅ |
| ¿Difieren 2 grupos sin suponer normalidad? | **Mann-Whitney U** · `mannwhitneyu` | Variable sesgada u ordinal. Contrasta P(X > Y) = 0.5, no las medias (salvedad 2) | Curso → `math`: U = 91 424 (orden `none`, `completed`) o 138 412 (orden inverso), p = 8.0e-8 · Género → `math`: U = 147 907.5, p = 4.3e-7 · Almuerzo → `writing`: p = 5.1e-14 | ✅ |
| ¿La media es distinta de un valor objetivo? | **t de una muestra** · `ttest_1samp` | Un solo grupo contra μ₀: es el tercer tipo de pregunta del Anexo. En la plantilla Excel «PH media U» se hace con Z (misma estadística, referencia normal). Valores de μ₀ ilustrativos | `math` vs. μ₀ = 70: t = −8.156, gl = 999, p = 1.0e-15 (rechaza H0). Vs. μ₀ = 66: t = 0.186, p = 0.853 (no rechaza). IC 95 % de la media [65.15; 67.03]. Excel (temperatura, n = 706, μ₀ = 10): Z = t = 5.948 | ➕ en Python · ✅ en Excel |
| ¿Una proporción es distinta de π₀? | **Z de una proporción** · `statsmodels.stats.proportion.proportions_ztest` o `stats.binomtest` | Variable categórica; esperados ≥ 5. Está en la plantilla Excel «PH proporción P» | Medellín, mes 6: 68 de 706 = 9.63 % frente a π₀ = 0.07: Z = 2.741, p (1 cola) = 0.0031; binomial exacta p = 0.0053. La plantilla da Z = 2.780 (salvedad 14) | ✅ (Excel) |
| ¿Dos proporciones difieren? | **Z de dos proporciones** · `proportions_ztest`; **Fisher** · `stats.fisher_exact` | Muestras independientes; Fisher si los conteos son pequeños | `Tipo de estación` = 2 en julio 38/73 vs. diciembre 17/47: Z agrupado = 1.705, p (1 cola) = 0.044; Fisher p = 0.064. La plantilla da Z = 3.386 y p = 3.6e-4 (salvedad 14) | ✅ (Excel) |
| ¿Lo mismo, sin normalidad? | **Wilcoxon** · `wilcoxon(x - mu0)` | Alternativa por rangos a la t de una muestra | μ₀ = 70: p = 1.3e-13 · μ₀ = 66: p = 0.485 | ➕ |
| ¿Difieren dos mediciones del mismo estudiante? | **t pareada** · `ttest_rel` / `wilcoxon(a, b)` | Datos emparejados (no independientes) | Lectura vs. escritura: diferencia media 1.115, t = 7.787, gl = 999, p = 1.7e-14, IC 95 % [0.834; 1.396]; Wilcoxon p = 3.8e-14 | ➕ |
| ¿Difieren 3 o más grupos? | **ANOVA** · `f_oneway` | Normalidad por grupo y varianzas parecidas | Etnia → `math`: F = 14.594, p = 1.4e-11 · Educación de los padres → `math` (6 grupos): F = 6.522, p = 5.6e-6 | ✅ |
| ¿Difieren 3 o más grupos (sin normalidad)? | **Kruskal-Wallis** · `kruskal` | Alternativa por rangos a ANOVA | Etnia: H = 57.079, p = 1.2e-11 (✅) · Educación: H = 26.506, p = 7.1e-5 (➕) | ✅ / ➕ |
| ¿Cuáles grupos son distintos? | **Tukey HSD** · `tukey_hsd` | *Post hoc* tras un ANOVA significativo; controla el error por comparaciones múltiples. La clave lo nombra, pero no lo ejecuta | Educación → `math`: 6 de 15 pares significativos. Etnia → `math`: 6 de 10 pares | ➕ |
| ¿Hay relación lineal? | **Pearson** · `pearsonr` | Dos numéricas, relación lineal, sin atípicos extremos. H0: ρ = 0 | Matemáticas–lectura: r = 0.8176, t = 44.855, gl = 998, p = 1.8e-241, IC 95 % [0.796; 0.837]. Lectura–escritura: r = 0.9546, p < 1e-300 (SciPy imprime 0.0) | ✅ |
| ¿Hay relación monótona? | **Spearman** / **Kendall** · `spearmanr`, `kendalltau` | Datos sesgados, atípicos u ordinales | Matemáticas–lectura: ρ = 0.804, τ = 0.617. Lectura–escritura: ρ = 0.949, τ = 0.820 | ➕ |
| ¿Hay una tendencia simple? | **Regresión lineal** · `linregress` | Una predictora: pendiente, intercepto y R² | `writing` = −0.668 + 0.9935 · `reading`, R² = 0.911, error estándar de la pendiente 0.0098 (t = 101.2) | ✅ |
| ¿Dos categóricas son independientes? | **χ² de independencia** · `chi2_contingency` | Tabla de frecuencias, esperados ≥ 5 | Género × curso: χ² = 0.016, gl = 1, p = 0.90 (V de Cramér 0.004) → no se rechaza H0. Almuerzo × curso: χ² = 0.221, p = 0.64 | ➕ |
| ¿Qué tan seguro es el estimado? | **Bootstrap / permutación** · `bootstrap`, `permutation_test` | Sin supuestos de distribución | Curso → `math`: diferencia de medias 5.62, IC 95 % [3.76; 7.53]; p de permutación = 0.0002 | ➕ |

### 3.2 Guía rápida para elegir

| Si quiero… | Datos aproximadamente normales | Datos sesgados / ordinales |
|---|---|---|
| Comparar 2 grupos independientes | t de Student (Levene OK) o t de Welch (`ttest_ind`) | Mann-Whitney (`mannwhitneyu`) |
| Comparar 3+ grupos | ANOVA (`f_oneway`) + Tukey | Kruskal-Wallis (`kruskal`) |
| Comparar 2 mediciones del mismo estudiante | t pareada (`ttest_rel`) | Wilcoxon pareado (`wilcoxon`) |
| Comparar un promedio con un valor fijo | t de una muestra (`ttest_1samp`) | Wilcoxon (`wilcoxon`) |
| Relacionar 2 numéricas | Pearson (`pearsonr`) | Spearman (`spearmanr`) o Kendall |
| Relacionar 2 categóricas | χ² (`chi2_contingency`) | χ² (`chi2_contingency`) |

### 3.3 Cómo decidir con los resultados de los supuestos (2 grupos independientes)

| Shapiro por grupo | Levene | Prueba principal | Verificación |
|---|---|---|---|
| Se cumple en ambos | Se cumple | t de Student | Mann-Whitney |
| Se cumple en ambos | No se cumple | t de Welch | Mann-Whitney |
| Falla en alguno (n grande, desviación leve) | Se cumple | Mann-Whitney (criterio de la actividad) o Student (criterio del ejemplo género → `math` de `02_Pruebas_Hipotesis_conceptos.md`): hay que elegir **un** criterio y declararlo (salvedad 1) | La otra |
| Falla en alguno | No se cumple | Mann-Whitney o Welch (clave del Taller 3, Ejercicio 4) | La otra |

Umbrales que usa el material: α = 0.05; d de Cohen 0.2 pequeño, 0.5 mediano, 0.8 grande; en correlación, el taller llama "fuerte" a |r| ≥ 0.7 (Cohen usa 0.1, 0.3 y 0.5 para pequeña, mediana y grande). Regla práctica: con n alto los tests de normalidad rechazan casi siempre; conviene mirar histograma, Q-Q y sesgo, y correr **las dos** pruebas (paramétrica y por rangos) para reportar si coinciden.

---

## 4. Ejemplo guiado 1: curso de preparación vs. nota de matemáticas (la actividad)

**Pregunta:** ¿los estudiantes que completaron el curso de preparación tienen, en promedio, una nota de matemáticas distinta de quienes no lo tomaron?

### 4.1 De los promedios a la prueba formal

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (Pandas) | `df.groupby('test preparation course')['math score'].agg(['count','mean','median','std'])` | `completed`: n = 358, media 69.70, mediana 69, s = 14.44. `none`: n = 642, media 64.08, mediana 64, s = 15.19 | Diferencia de 5.62 puntos; el promedio solo no dice si es azar |
| 2 | Gráficos | `sns.histplot`, `sns.boxplot` | Histograma: media 66.09 ≈ mediana 66, sesgo −0.28. Boxplot: `none` Q1 54 · mediana 64 · Q3 74.75; `completed` 60 · 69 · 79 | La caja de `completed` queda unos 5 puntos más arriba; dispersión parecida |
| 3 | Hipótesis | — | H0: μ_completed = μ_none · H1: μ_completed ≠ μ_none · α = 0.05 | Prueba de dos colas |
| 4 | Normalidad | `stats.shapiro` por grupo | `none`: p = 0.0018. `completed`: p = 0.139. Apoyo: Q-Q r = 0.9959 y 0.9974; sesgo −0.33 y −0.15 | Rechaza en `none`, pero con n = 642 la desviación es leve |
| 5 | Homogeneidad | `stats.levene` | W = 0.5330, p = 0.4655. (Bartlett p = 0.282; Levene centrado en la media p = 0.476) | Varianzas homogéneas → Student es válido |
| 6 | Prueba principal (clave) | `stats.mannwhitneyu(none, completed)` | U = 91 424, p = 8.0e-8 | Rechaza H0 sin suponer normalidad |
| 7 | Verificación (clave) | `stats.ttest_ind(none, completed, equal_var=True)` | t = −5.705, gl = 998, p = 1.5e-8 | Misma decisión. El signo depende del orden de los grupos |
| 8 | t de Welch (➕) | `stats.ttest_ind(completed, none, equal_var=False)` | t = 5.787, gl = 770.1, p = 1.0e-8 | Igual conclusión |
| 9 | Tamaño del efecto (➕) | d = (m₁ − m₂) / s_pooled · CLES = U / (n₁·n₂) · r_rb = 2·CLES − 1 | d = 0.376 (IC 95 % [0.25; 0.51]) · CLES = 0.602 · r_rb = 0.204 | Efecto de pequeño a mediano: un estudiante con curso supera a uno sin curso el 60.2 % de las veces (50 % sería empate) |
| 10 | Intervalo de confianza (➕) | Fórmula t, `stats.bootstrap`, `stats.permutation_test` | Diferencia 5.62: t clásica [3.69; 7.55] · Welch [3.71; 7.52] · bootstrap [3.76; 7.53] · p de permutación = 0.0002 | El intervalo no incluye 0 |
| 11 | Potencia (➕) | `TTestIndPower.solve_power` | Con 358 y 642: efecto mínimo detectable d = 0.185 (80 %). Para d = 0.376 bastan ≈ 243 estudiantes (con el reparto 36 / 64) | El tamaño de muestra alcanza de sobra |

**Conclusión:** con α = 0.05 se rechaza H0. Hay evidencia estadísticamente significativa de que `math score` difiere según el curso: 69.70 frente a 64.08, unos 5.6 puntos (0.38 desviaciones estándar), efecto **pequeño a mediano**. Es una asociación, no una prueba de que el curso *cause* la mejora (datos observacionales, curso no asignado al azar).

### 4.2 Mismo procedimiento, otras comparaciones del dataset

"Prueba que corresponde" = Student si Levene ≥ 0.05; Welch si Levene < 0.05. La columna *p* es la de esa prueba.

| Contraste | Medias | Levene p | Prueba que corresponde | p | p Mann-Whitney | d | Lectura |
|---|---|---|---|---|---|---|---|
| Curso → `math` (`completed` vs. `none`) | 69.70 vs. 64.08 | 0.4655 | Student | 1.5e-8 | 8.0e-8 | 0.376 | Pequeño a mediano |
| Curso → `reading` | 73.89 vs. 66.53 | 0.299 | Student | 9.1e-15 | 1.7e-14 | 0.519 | Mediano |
| Curso → `writing` | 74.42 vs. 64.50 | **0.0147** | **Welch** | 2.7e-25 | 1.2e-23 | 0.687 | Mediano a grande |
| Género → `math` (hombres vs. mujeres) | 68.73 vs. 63.63 | 0.556 | Student | 9.1e-8 | 4.3e-7 | 0.341 | Pequeño, **a favor de los hombres** |
| Género → `reading` | 65.47 vs. 72.61 | 0.891 | Student | 4.7e-15 | 5.4e-15 | −0.504 | Mediano, a favor de las mujeres |
| Género → `writing` | 63.31 vs. 72.47 | 0.934 | Student | 2.0e-22 | 4.7e-23 | −0.632 | Mediano a grande, a favor de las mujeres |
| Almuerzo → `math` (`standard` vs. `free/reduced`) | 70.03 vs. 58.92 | 0.074 | Student | 2.4e-30 | 1.5e-26 | 0.782 | Casi grande: el mayor del dataset |
| Almuerzo → `reading` | 71.65 vs. 64.65 | 0.158 | Student | 2.0e-13 | 3.7e-12 | 0.492 | Mediano |
| Almuerzo → `writing` | 70.82 vs. 63.02 | 0.105 | Student | 3.2e-15 | 5.1e-14 | 0.529 | Mediano |
| Etnia B vs. C → `math` | 63.45 vs. 64.46 | 0.578 | Student | 0.465 | 0.527 | −0.067 | **No se rechaza H0**. IC 95 % de la diferencia [−3.73; 1.70] |

**Contraste didáctico:** con n = 1 000, nueve de las diez comparaciones dan p entre 1e-8 y 1e-30, así que el p-value no sirve para ordenarlas; el tamaño del efecto sí. La pregunta de la actividad (curso → `math`, d = 0.376) es la segunda de menor efecto de las nueve; el almuerzo pesa más sobre `math` (≈ 11 puntos) que el curso (≈ 5.6). El caso B vs. C sí da p ≥ α, pero "no se rechaza" no prueba igualdad: el intervalo todavía admite diferencias de hasta 3.7 puntos, y con 190 y 319 estudiantes solo se detectan efectos d ≥ 0.26.

### 4.3 Código listo para pegar

```python
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("StudentsPerformance.csv")
completed = df.loc[df["test preparation course"] == "completed", "math score"]
none = df.loc[df["test preparation course"] == "none", "math score"]

def decidir(p, alpha=0.05):
    return "se rechaza H0" if p < alpha else "no se rechaza H0"

# 1) Descriptiva por grupo
print(df.groupby("test preparation course")["math score"].agg(["count", "mean", "median", "std"]))

# 2) Supuestos: normalidad por grupo y homogeneidad de varianzas
print(stats.shapiro(none), stats.shapiro(completed))
print(stats.levene(none, completed))

# 3) Prueba principal (Mann-Whitney) y verificaciones (Student y Welch)
mw = stats.mannwhitneyu(none, completed, alternative="two-sided")
student = stats.ttest_ind(none, completed, equal_var=True)
welch = stats.ttest_ind(completed, none, equal_var=False)
print(mw, decidir(mw.pvalue))
print(student, decidir(student.pvalue))
print(welch)

# 4) Tamaño del efecto
n1, n2 = len(completed), len(none)
sp = np.sqrt(((n1 - 1) * completed.var() + (n2 - 1) * none.var()) / (n1 + n2 - 2))
cohen_d = (completed.mean() - none.mean()) / sp
u_completed = stats.mannwhitneyu(completed, none).statistic
cles = u_completed / (n1 * n2)   # prob. de que un estudiante con curso supere a uno sin curso (empates = 0.5)
rank_biserial = 2 * cles - 1
print(cohen_d, cles, rank_biserial)

# 5) Intervalo de confianza de la diferencia de medias (bootstrap)
dif = lambda a, b, axis: np.mean(a, axis=axis) - np.mean(b, axis=axis)
res = stats.bootstrap((completed.to_numpy(), none.to_numpy()), dif,
                      n_resamples=9999, method="percentile", random_state=42)
print(res.confidence_interval)
```

---

## 5. Ejemplo guiado 2: nivel educativo de los padres vs. nota de matemáticas (6 grupos)

**Pregunta:** ¿el promedio de `math score` es distinto entre los seis niveles de `parental level of education`? (Taller 3, Ejercicio 2; con 5 grupos de `race/ethnicity` es el Ejercicio 8 del Taller 2.)

### 5.1 Nivel educativo de los padres → `math`

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (Pandas), en orden natural | `df.groupby('parental level of education')['math score'].agg(['count','mean','std'])` | `some high school` 63.50 (n = 179) · `high school` 62.14 (196) · `some college` 67.13 (226) · `associate's` 67.88 (222) · `bachelor's` 69.39 (118) · `master's` 69.75 (59) | 7.61 puntos entre el grupo más bajo (`high school`) y el más alto. No es monótona: `some high school` supera a `high school` |
| 2 | Hipótesis | — | H0: μ₁ = … = μ₆ · H1: al menos una distinta | "Al menos una" no es "todas distintas" |
| 3 | Supuestos | `stats.levene(*grupos)` · `stats.shapiro` por grupo | Levene: W = 0.9333, p = 0.458 (desviaciones entre 14.31 y 15.93). Shapiro: rechaza en 3 de 6 grupos (`associate's` 0.045, `master's` 0.032, `some high school` 0.005) | Varianzas homogéneas; normalidad dudosa en 3 grupos |
| 4 | ANOVA | `stats.f_oneway(*grupos)` | F = 6.522 (SSB = 7 295.6, SSW = 222 393.5, gl 5 y 994), p = 5.6e-6 | Rechaza H0 |
| 5 | Kruskal-Wallis (➕) | `stats.kruskal(*grupos)` | H = 26.506, p = 7.1e-5 | Confirma sin suponer normalidad |
| 6 | Tamaño del efecto (➕) | η² = SSB / SST · ε² = H / ((N² − 1) / (N + 1)) | η² = 0.032 · ε² = 0.027 | La educación de los padres explica ≈ 3.2 % de la variación de la nota: efecto pequeño aunque p sea 5.6e-6 |
| 7 | *Post hoc* (➕) | `stats.tukey_hsd(*grupos)` | 6 de 15 pares significativos (lista debajo de la tabla) | Los seis enfrentan a `high school` o `some high school` contra un nivel superior; los otros nueve pares no se distinguen |

Pares significativos del paso 7 (diferencia de medias, p de Tukey): `associate's`–`high school` 5.75 (0.0013) · `associate's`–`some high school` 4.39 (0.042) · `bachelor's`–`high school` 7.25 (0.0005) · `bachelor's`–`some high school` 5.89 (0.012) · `master's`–`high school` 7.61 (0.0084) · `some college`–`high school` 4.99 (0.0086).

### 5.2 Etnia → `math` (Taller 2, Ejercicio 8)

| Paso | Prueba | Resultado | Lectura |
|---|---|---|---|
| Supuestos | Levene · Shapiro por grupo | Levene W = 0.5903, p = 0.6697. Shapiro: A 0.855, B 0.010, C 0.017, D 0.059, E 0.019 | Varianzas homogéneas; normalidad dudosa en 3 grupos con n ≥ 89 |
| ANOVA (✅) | `f_oneway` | F = 14.594, p = 1.4e-11 | Rechaza H0 |
| Kruskal-Wallis (✅) | `kruskal` | H = 57.079, p = 1.2e-11 | Confirma |
| Tamaño del efecto (➕) | η², ε² | η² = 0.055 · ε² = 0.057 | Efecto de pequeño a mediano |
| *Post hoc* (➕) | `tukey_hsd` | Significativos: A–D, A–E, B–D, B–E, C–E, D–E (6 de 10) | E se distingue de todos; A, B y C no se distinguen entre sí |

**Conclusión:** ANOVA y Kruskal solo dicen que *alguna* media difiere; Tukey dice cuáles. Con n = 1 000, ambos efectos son pequeños (η² de 0.03 y 0.06) aunque los p-values sean minúsculos. Las etiquetas "group A–E" son anónimas, así que la diferencia no se puede atribuir a un origen étnico en sí.

---

## 6. Ejemplo guiado 3: correlación y regresión lineal (Taller 1)

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Gráfico | `sns.scatterplot(x='reading score', y='writing score', alpha=0.5)` | Nube diagonal, estrecha y creciente | Relación lineal positiva evidente |
| 2 | Hipótesis | — | H0: ρ = 0 · H1: ρ ≠ 0 | Prueba de dos colas |
| 3 | Pearson matemáticas–lectura (✅) | `stats.pearsonr(m, r)`; t = r·√(n−2) / √(1−r²) | r = 0.8176, t = 44.855, gl = 998, p = 1.8e-241, IC 95 % [0.796; 0.837], r² = 0.668 | Se rechaza H0: relación fuerte y positiva |
| 4 | Pearson lectura–escritura (✅) | `stats.pearsonr(r, w)` | r = 0.9546, t = 101.23, p < 1e-300, IC 95 % [0.949; 0.960], r² = 0.911 | El 91.1 % de la variación de una se comparte con la otra |
| 5 | Spearman y Kendall (➕) | `spearmanr`, `kendalltau` | Lectura–escritura: ρ = 0.949, τ = 0.820 · Matemáticas–lectura: ρ = 0.804, τ = 0.617 | Coinciden con Pearson: ningún atípico distorsiona la relación |
| 6 | Recta de mínimos cuadrados (✅) | `stats.linregress(reading, writing)` | b₁ = Sxy / Sxx = 211 574.87 / 212 952.44 = 0.9935 · b₀ = ȳ − b₁·x̄ = 68.054 − 0.9935 · 69.169 = −0.6676 · error estándar de b₁ = 0.0098 | Un punto más en lectura se asocia con ≈ 0.99 puntos más en escritura. La pendiente **no** es r |
| 7 | Intercepto | — | −0.668 cuando `reading` = 0 | Sin sentido práctico: el mínimo observado es 17 |
| 8 | R² (✅) | 1 − SSres / SStot | 1 − 20 470.86 / 230 677.08 = 0.9113 = r² | Con un predictor R² = r²; el modelo explica el 91.1 % |
| 9 | Predicción dentro del rango (✅) | `b0 + b1 * 80` | `reading` = 80 → `writing` = 78.81 (IC de la media [78.46; 79.16]; intervalo de predicción [69.92; 87.71]) | El error típico de un estudiante individual es 4.53 puntos |
| 10 | Extrapolación (✅) | `b0 + b1 * 150` | `reading` = 150 → `writing` = 148.36 (intervalo de predicción [139.33; 157.39]) | Imposible (> 100): fuera del rango 17 a 100 con el que se ajustó la recta |
| 11 | Correlación con muestra chica (✅, Ejercicio 2c) | t = r·√(n−2) / √(1−r²) | Con n = 5, r = 0.8 → t = 2.31, gl = 3, p = 0.104; el valor crítico de r (en valor absoluto) es 0.878 | Un r alto con pocos datos puede ser azar; con n = 1 000 un r = 0.818 no |

**Conclusión:** asociación lineal muy fuerte y positiva entre lectura y escritura. Ambas son habilidades del mismo ámbito, así que la fuerza de la relación no dice cuál influye en cuál. Matemáticas sobre lectura: `math` = 7.358 + 0.8491 · `reading`, R² = 0.668.

---

## 7. Ejemplo guiado 4: error tipo I y II, potencia y tamaño de muestra

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Error tipo I (➕) | Permutar 5 000 veces las etiquetas de curso y aplicar Welch con α = 0.05 | Rechaza H0 en 4.84 % de las permutaciones | α es la tasa de falsas alarmas cuando H0 es verdadera |
| 2 | Submuestra de 50 (✅, Taller 2 Ejercicio 6) | `df.sample(n=50, random_state=42)` | 30 `none` y 20 `completed`. Mann-Whitney p = 0.6274 (t de Student p = 0.435) → no se rechaza H0 | Error tipo II: el efecto existe en los 1 000 pero no se detecta con 50 |
| 3 | ¿Es típico ese resultado? (➕) | 5 000 submuestras aleatorias de 50 | Mann-Whitney rechaza H0 en 19.9 % (t de Student 21.7 %); potencia teórica con d = 0.376: 24 % | Con n = 50 lo normal es no rechazar; la semilla 42 no es una excepción |
| 4 | Curva de potencia (➕) | `TTestIndPower.power` (reparto 36 / 64, d = 0.376) | N total 20 → 12 % · 50 → 24 % · 100 → 43 % · 200 → 72 % · 400 → 95 % · 1 000 → ≈ 100 % | 80 % de potencia exige ≈ 243 estudiantes (≈ 325 para 90 %) |
| 5 | Muestras de 10 (✅, Taller 3 Ejercicio 7) | `grupo_a.head(10)`, `grupo_e.head(10)` | Primeros 10: 57.50 vs. 66.70, t = −1.167, p = 0.2585. Grupos completos (89 y 140): 61.63 vs. 73.82, t = −5.936, p = 1.1e-8, d = 0.805 | Con n = 10 por grupo y d = 0.80 la potencia es 40 %: el error tipo II es lo más probable |
| 6 | Tamaño de muestra necesario (✅, `03_Regla…`) | `TTestIndPower.solve_power(effect_size=d, alpha=0.05, power=0.80)` | d = 0.341 (género → `math`): 136 por grupo (80 %) y 182 (90 %). Aprox. normal: 135.2 y 181.0. d = 0.5: 64 y 85 · d = 0.2: 393 y 526 · d = 0.8: 26 y 34. Bonus del notebook del Taller 1: d = 0.632 (género → `writing`): 39.4 por grupo (aprox. normal) y 40.3 (statsmodels); 53.7 para 90 % | Los 482 y 518 reales son ≈ 3.5 a 3.8 veces lo necesario para `math` y ≈ 12 a 13 veces para `writing` |
| 7 | Tamaño de muestra para una correlación (✅) | Fisher: n = ((z₁₋α/₂ + z₁₋β) / atanh r)² + 3 | r = 0.3: 84.9 · r = 0.1: 782.7 (simulación: potencia 80.3 % con n = 84 y 79.9 % con n = 782) | Un efecto pequeño cuesta ≈ 9 veces más muestra que uno mediano |
| 8 | Efecto mínimo detectable con los n reales (➕) | `solve_power(nobs1=n1, ratio=n2/n1, power=0.80)` | Género 482 / 518: d = 0.177 · curso 358 / 642: 0.185 · almuerzo 645 / 355: 0.185 · etnia A vs. E 89 / 140: 0.381 | Entre subgrupos de ≈ 100 estudiantes, un "no se rechaza" dice poco |

### Código listo para pegar (pasos 3 y 8; requiere `pip install statsmodels`)

```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower

df = pd.read_csv("StudentsPerformance.csv")
P = TTestIndPower()

# Tamaño de muestra por grupo para detectar d = 0.341 con 80 % de potencia (≈ 136)
print(P.solve_power(effect_size=0.3407, alpha=0.05, power=0.80))
# Efecto mínimo detectable con 358 y 642 estudiantes (≈ 0.185)
print(P.solve_power(nobs1=358, alpha=0.05, power=0.80, ratio=642 / 358))

# Qué tan seguido se rechaza H0 con submuestras aleatorias de 50 (≈ 0.20)
rng = np.random.default_rng(0)
R, rechazos = 5000, 0
for _ in range(R):
    s = df.sample(n=50, random_state=int(rng.integers(0, 2**31 - 1)))
    a = s.loc[s["test preparation course"] == "none", "math score"]
    b = s.loc[s["test preparation course"] == "completed", "math score"]
    rechazos += stats.mannwhitneyu(a, b).pvalue < 0.05
print(rechazos / R)
```

---

## 8. Mismo flujo con los otros datasets del Anexo

| Dataset | Pregunta y prueba | Resultado | Cuidado |
|---|---|---|---|
| Boston Housing (506 × 14) | `chas` (junto al río: 35 viviendas vs. 471) → `medv` (miles de USD) | Medias 28.44 vs. 22.09. Shapiro rechaza en ambos (p = 1.1e-4 y 3.1e-14). Levene p = 0.0326 → **Welch**: t = 3.113, gl = 36.9, p = 0.0036. Mann-Whitney p = 0.0016. d = 0.700 | Grupos muy desbalanceados: Student daría t = 3.996 y p = 7.4e-5, casi 50 veces menor que el de Welch y engañoso |
| Boston Housing | `rm` (habitaciones) → `medv`: Pearson, Spearman, `linregress` | n = 501 (se excluyen 5 nulos de `rm`). r = 0.6962, p = 7.6e-74, IC 95 % [0.648; 0.739]. ρ = 0.636. `medv` = −34.68 + 9.109 · `rm`, R² = 0.485 | Sin `dropna`, `pearsonr` y `shapiro` devuelven `nan`. Declarar la exclusión (el Anexo lo pide) |
| Boston Housing | `lstat` → `medv` | r = −0.738 (p = 5.1e-88), pero ρ = −0.853. R² = 0.544 | Un ρ más grande que r (en valor absoluto) indica curvatura: la recta lineal subestima la relación |
| Boston Housing | `rad` agrupada (1–4: 192 · 5–8: 182 · 24: 132) → `medv`: ANOVA y Kruskal | Medias 23.67, 25.78 y 16.40. Levene p = 0.598. F = 50.32, p = 1.2e-20; H = 122.79, p = 2.2e-27 | Los cortes de `rad` son una decisión propia; `medv` está truncada en 50 (16 viviendas) |
| Netflix `titles.csv` | Película (3 429) vs. serie (1 939) → `imdb_score`: Welch y Mann-Whitney | Medias 6.25 vs. 6.98. Levene p = 0.0047 → Welch: t = −23.48, gl = 4 176, p = 1.2e-114. Mann-Whitney p = 3.4e-120. d = −0.659 | Hay 482 títulos sin `imdb_score` (aquí excluidos). Imputándolos con la mediana global, como en la Semana 4, salen 6.28 vs. 6.95 y t ≈ −23.4 |

---

## 9. Ruta en Excel: plantillas del ZIP «Material inferencia estadística»

El ZIP (ignorado por Git, en `Semana_6_Actividad_solucion_profesor/`) trae tres libros: **Fase 2** (problemática, población, tamaño de muestra, tipo de muestreo, intervalos de confianza, respuestas a interrogantes), **Fase 3** (muestreo, PH media, PH proporción, PH diferencia de medias, PH diferencia de proporciones, ANOVA, ficha técnica) y **Fase 4** (Fase 3 más portada y referencias). Usan otro dataset, calidad del aire en Medellín (N = 8 030 registros × 16 variables: rango horario, día, mes, marca, tipo de estación, zona, dirección del viento, precipitación, temperatura, radiación, humedad, SO₂, PM10, O₃ y CO), y un flujo en Excel con muestreo sistemático (k = ⌊N / n⌋ = 11, inicio 6 para n = 706). Reproduje esa muestra en Python (`P.loc[[6 + 11*i for i in range(706)]]`) y obtuve las mismas cifras guardadas en las celdas (x̄, s y Z).

| Procedimiento (Excel) | Fórmula de la plantilla | Equivalente en Python | Resultado recalculado | Observación |
|---|---|---|---|---|
| Tamaño de muestra, media (población finita) | n = ⌈Z²σ²N / ((N−1)e² + Z²σ²)⌉ | `np.ceil(z**2*s**2*N / ((N-1)*e**2 + z**2*s**2))` con `stats.norm.ppf` | σ = 3.7521, N = 8 030, e = 0.3, 97 %: con Z bilateral = 2.170 → n = 675. La plantilla usa Z = 1.881 → n = 518 | Salvedad 14 |
| Tamaño de muestra, proporción | n = Z²N / (4e²(N−1) + Z²) (p = 0.5) | igual | e = 0.06, 97 %: Z = 2.170 → 314.3 → 315. Con la Z de la plantilla: 238.4 (la celda no usa `ROUNDUP`) | Salvedad 14 |
| Muestreo sistemático | k = ⌊N / n⌋; inicio `RANDBETWEEN(1, k)` | `P.loc[[inicio + k*i for i in range(n)]]` | N = 8 030, n = 706 → k = 11 | Fijar el inicio con una semilla para que sea reproducible |
| IC de la media | x̄ ± Z·s/√n | `stats.t.interval(conf, n-1, loc=m, scale=s/np.sqrt(n))` | x̄ = 11.2, s = 3.7605, n = 518, 97 %: plantilla (Z = 1.881) [10.89; 11.51] · Z bilateral [10.84; 11.56] · t [10.84; 11.56] | No lleva corrección por población finita; el IC de la proporción sí |
| IC de la proporción | p ± √(p(1−p)(N−n) / (n(N−1))) | `statsmodels.stats.proportion.proportion_confint` | Las celdas B26:B27 calculan Z (B25) pero no lo multiplican | Salvedad 14: queda un intervalo de ± 1 error estándar (≈ 68 %) |
| PH de una media (Z) | Z = (x̄ − μ₀) / (s/√n); p con `NORM.S.DIST` | `stats.ttest_1samp(x, mu0, alternative=…)` | Temperatura, n = 706: x̄ = 10.862, s = 3.852, μ₀ = 10 → Z = t = 5.948 (gl = 705). H1: μ < 10 (la de la plantilla) → p = 0.9999999986 (no rechaza); H1: μ > 10 → p = 2.1e-9; bilateral 4.3e-9 | Con n grande Z y t coinciden; con n chica usar t. Los datos van en sentido contrario a la H1 de la plantilla |
| PH de una proporción | Z = (p̂ − π₀) / √(π₀·(1 − p̂)/n) | `proportions_ztest(x, n, π₀, prop_var=π₀)`; `stats.binomtest` | Mes 6: 68 de 706 = 0.0963 frente a π₀ = 0.07: plantilla Z = 2.780 (p = 0.0027); con el denominador π₀(1 − π₀): Z = 2.741 (p = 0.0031); binomial exacta p = 0.0053 | Salvedad 14 |
| PH de diferencia de medias | Z = (x̄ − ȳ) / √(sₓ²/nₓ + sᵧ²/nᵧ) | `stats.ttest_ind(a, b, equal_var=False)` | Temperatura, mes 4 (n = 61) vs. mes 11 (n = 59): 12.81 vs. 12.63. Z = t de Welch = 0.2689 (gl = 117.0), p = 0.788; Mann-Whitney p = 0.939 | Es un Welch con referencia normal; la plantilla no pide revisar supuestos |
| PH de diferencia de proporciones | Z = (p̂ₓ − p̂ᵧ) / √(p̂ₓ(1−p̂ₓ)/nₓ + p̂ᵧ(1−p̂ᵧ)/nᵧ) | `proportions_ztest`, `stats.fisher_exact` | `Tipo de estación` = 2: julio 38/73 = 0.521 vs. diciembre 17/47 = 0.362 (la plantilla calcula 17/73 = 0.233). Plantilla Z = 3.386, p = 3.6e-4. Corregido: Z = 1.740 (no agrupado, p = 0.041) o 1.705 (agrupado, p = 0.044); Fisher p = 0.064 | Salvedad 14: pasa de "muy significativo" a "en el límite" |
| ANOVA de un factor | Herramienta «Análisis de varianza de un factor» | `stats.f_oneway(*grupos)` | Temperatura por día de la semana (2, 3 y 7; n = 102, 91 y 111): F = 0.0414, p = 0.9595 (Kruskal p = 0.783; Levene p = 0.094). La hoja guarda F = 0.0202 y p = 0.980 | Salvedad 15 |

Otros dos archivos locales de la carpeta del profesor: `StudentsPerformance.xlsx` (hoja de datos con un título encima del encabezado, por lo que `pd.read_excel` necesita `header=1`; `Hoja1` es una tabla dinámica con el promedio de `math` 63.63 y 68.73, de `reading` 72.61 y 65.47 y la desviación de `writing` 14.84 y 14.11 por género; `Hoja2` suma `reading` por cada nota de `math`) y `zoom_check.png` (captura del notebook del Taller 1). Todas esas cifras coinciden con el CSV.

---

## 10. Salvedades que conviene conocer

1. **Dos criterios opuestos para el mismo síntoma.** En la actividad (notebook y `Desarrollo_Actividad_Explicado.md`) Shapiro rechaza en un grupo (`none`, p = 0.0018) y por eso Mann-Whitney es la prueba principal y Student la verificación. En el ejemplo género → `math` de `02_Pruebas_Hipotesis_conceptos.md` (§5) Shapiro rechaza en **los dos** grupos (p = 0.038 y 0.0035) y se hace al revés: Student principal y Mann-Whitney de verificación, por el Teorema del Límite Central. En ambos casos las dos pruebas coinciden (p entre 1.5e-8 y 4.3e-7), así que la conclusión no cambia, pero en el portafolio hay que justificar un único criterio y decirlo (tabla 3.3).
2. **Mann-Whitney no contrasta medias.** El notebook plantea H0: μ_completed = μ_none y usa Mann-Whitney como prueba principal, que pone a prueba P(X > Y) = 0.5 (para el caso, CLES = 0.602). Equivale a una diferencia de medias solo si las dos distribuciones tienen forma parecida; aquí sí (s = 14.44 y 15.19, sesgo −0.15 y −0.33). Conviene redactar la H0 de Mann-Whitney como "las distribuciones son iguales" o reportar también Welch.
3. **El notebook decide solo con p-values.** No reporta tamaño del efecto ni intervalos: los dos p (8.0e-8 y 1.5e-8) no dicen qué tan grande es la diferencia. Con d = 0.376, IC 95 % de la diferencia [3.7; 7.5] puntos y CLES = 0.602 la lectura es "pequeño a mediano". Entre las nueve comparaciones de la tabla 4.2, la pregunta de la actividad es la segunda de menor efecto. La rúbrica pide "interpretación rigurosa del estadístico y del p-value" y la guía del portafolio recomienda agregar el tamaño del efecto. Tampoco se explican los intervalos de confianza en `01`, `02`, `Semana_6_Resumen.md` ni en los talleres (0 menciones), aunque el tercer prompt de `Promts.md` pide cubrirlos y las plantillas Excel de la Fase 2 sí los calculan.
4. **El p-value se explica de forma imprecisa en la prosa informal.** `01_Estadistica_inferencial_conceptos.md` §5 dice que se le cree a H1 "si la probabilidad de que sea pura casualidad es menor al 5 %", pero dos párrafos después define bien p = P(datos | H0), y el Ejercicio 6 de `02` señala justamente esa confusión como error. `Semana_6_Resumen.md` habla de una "diferencia real … en esta muestra", pero en la muestra la diferencia de 5.1 puntos existe por definición: lo que se infiere es la población. Redacción segura: "si H0 fuera cierta, un resultado tan extremo ocurriría con probabilidad p".
5. **Detalles de SciPy y de versiones.** (a) El orden de los grupos cambia el signo de t y el valor de U: `ttest_ind(none, completed)` da t = −5.705 y U = 91 424; con el orden inverso, t = +5.705 y U = 138 412 (suman 229 836 = 642 × 358); el p es el mismo. (b) `levene` usa la mediana como centro (Brown-Forsythe); con el Levene clásico (`center="mean"`) el p es 0.476 en vez de 0.4655, misma decisión. (c) `bartlett` lanza `ValueError: cannot convert float NaN to integer` con datos enteros en SciPy 1.17.1 / NumPy 2.4.6; se arregla con `.to_numpy(dtype=float)` (p = 0.282 para curso → `math`). (d) Las salidas del notebook muestran `dtype: str`, que es de pandas 3.x; con pandas 2.x se ve `object`, sin efecto sobre los resultados.
6. **Taller 2, Ejercicio 6 (n = 50, `random_state=42`).** El p = 0.6274 es un resultado típico, no una rareza: en 5 000 submuestras aleatorias de 50 estudiantes Mann-Whitney solo rechaza H0 el 19.9 % de las veces (potencia teórica 24 %). La lección de la clave es correcta, pero conviene decir que depende de la semilla solo en el valor exacto del p.
7. **Taller 3, Ejercicio 7 usa las primeras 10 filas de cada grupo (`head(10)`), no una muestra aleatoria.** Con n = 10 tampoco se puede revisar normalidad. Mann-Whitney da p = 0.173 y Welch p = 0.260 (la clave solo corre Student, p = 0.2585). La potencia para el efecto real de ese par (d = 0.805) es 40 %, por eso el "no se rechaza" es un error tipo II más probable que no.
8. **La frase sobre ANOVA en `03_Regla_definir_tamaño_muestra_optima.md` no es general.** Dice que con 3 o más grupos "generalmente necesitas más muestra por grupo". Con el mismo f de Cohen (0.25), el n por grupo **baja** al subir los grupos (2: 63.8 · 3: 52.4 · 4: 44.6 · 5: 39.2 · 6: 35.1) y lo que sube es el total (127.5 → 157.2 → 178.4 → 195.8 → 210.8). Solo es "más por grupo" si se quiere detectar la misma diferencia entre un par mientras los demás grupos no difieren, o si se hacen comparaciones *post hoc* corregidas. El resto de las cifras de ese archivo (136 y 182 por grupo, 393, 64, 84 y 782) se reproducen.
9. **ANOVA y Kruskal sin *post hoc*, y `parental level of education` tratada como nominal.** Los Talleres 2 y 3 se detienen en "al menos una difiere" y declaran el *post hoc* fuera de alcance; Tukey identifica 6 de 15 pares. Además, con p = 5.6e-6 el efecto es pequeño (η² = 0.032). La variable es ordinal, pero `groupby` la ordena alfabéticamente; en su orden natural el promedio no crece de forma estrictamente monótona (`some high school` 63.50 > `high school` 62.14). Hay que declararla con `pd.Categorical(..., ordered=True)`.
10. **Regresión: la extrapolación se puede cuantificar y el rango no basta.** En el Ejercicio 6 la predicción 148.36 (para `reading` = 150) tiene intervalo de predicción [139.33; 157.39], todo fuera de 0 a 100. Incluso dentro del rango observado, con `reading` = 100 la recta da 98.69 y el intervalo llega a 107.60: un modelo lineal no conoce el tope de la escala.
11. **Si el equipo usa Boston Housing.** El archivo trae 5 nulos en `rm` (filas 10, 35, 63, 96 y 135), `medv` está truncada en 50 (16 viviendas), `chas` está muy desbalanceada (35 vs. 471) y la columna `b` es problemática: scikit-learn retiró `load_boston` (v1.2) por esa variable, así que conviene no usarla ni interpretarla.
12. **Deslices menores en el material.** `Explicacion/10 Hipotesis ejemplo paso 5.md` da s_p² = 223.24; el valor correcto es 223.66 (el SE = 0.947 y t = 5.3832 sí cuadran). `03_Regla…` usa s_p = 14.94 para d = 0.341; s_p es 14.96 (d = 0.3407 es correcto). Todos los materiales y el notebook dicen "NRC 94103", pero la carpeta del repositorio es `NRC-70446`: hay que confirmar cuál va en la portada. En el notebook, el comentario de la celda de carga dice que busca y descarta una fila "basura" al inicio, pero el código solo une todas las líneas (`"".join(lineas)`); funciona porque el CSV está limpio y el resultado es idéntico a un `pd.read_csv` simple. (El título sobrante sí existe en `StudentsPerformance.xlsx`, no en el CSV.)
13. **Archivos del repositorio.** (a) Dos enlaces de archivos versionados apuntan a archivos ignorados por `.gitignore` (`*profesor*`), así que fallan en GitHub: `02_Pruebas_Hipotesis_conceptos.md` → `02_Prueba_Hipotesis_conceptos_profesor.pptx` y `Taller_01_Estadistica_inferencial.md` → `Taller_01_Estadistica_inferencial_profesor.md`. (b) Varias etiquetas de enlace quedaron con numeración vieja: `02_Pruebas…` muestra `Taller_02_Prueba_Hipotesis.md` y enlaza a `Taller_03_…`; el notebook muestra `Desarrollo_Actividad_Explicado_Nino.md` y enlaza a `Desarrollo_Actividad_Explicado.md`. (c) Los PDF `EIARV011_A6_Desarrollo_actividad.pdf` y `EIARV011_A6_Notebook.pdf` están versionados en `Semana_6_Actividad_desarrollo/` (el nombre no coincide con `*profesor*`) y contienen la solución completa de la actividad. Los talleres de estudiante (`Taller_01` a `Taller_03`, `.md`) sí están sin resolver. (d) Las plantillas Excel del ZIP traen el nombre completo de un estudiante en la hoja de tamaño de muestra: están ignoradas por Git y no conviene publicarlas tal cual.
14. **Plantillas Excel: cuantiles y fórmulas que cambian los resultados (sección 9).** (a) El tamaño de muestra y el IC de la media usan Z = −`NORM.S.INV`(1 − confianza), un cuantil unilateral: con "97 %" sale Z = 1.881, que equivale a 94 % bilateral (la hoja «TIPO DE MUESTREO» sí usa (1 − confianza)/2 y por eso guarda 0.94 para obtener ese mismo Z). Con el Z bilateral el n del ejemplo pasa de 518 a 675 (media) y de 238 a 315 (proporción), y el IC de la media se ensancha de [10.89; 11.51] a [10.84; 11.56]. (b) Los límites del IC de la proporción no multiplican por Z. (c) La PH de una proporción usa (1 − p̂) en el error estándar en lugar de (1 − π₀): Z = 2.780 en vez de 2.741. (d) La PH de diferencia de proporciones divide el conteo del segundo grupo entre el n del primero (17/73 en vez de 17/47): da Z = 3.386 y p = 3.6e-4, cuando lo correcto es Z ≈ 1.70 a 1.74 y p ≈ 0.041 a 0.044 (Fisher 0.064). A α = 0.05 la decisión sobrevive en la aproximación normal, pero la evidencia pasa de muy fuerte a límite. Además, el enunciado y la conclusión hablan de "dirección del viento norte" mientras la prueba usa `Tipo de estación`. (e) Las pruebas Z de media y de diferencia de medias usan la s muestral con la normal; con n chica corresponde t.
15. **Plantilla Excel, hoja ANOVA.** El rango de entrada incluye la fila de códigos de los grupos (2, 3 y 7) como si fueran datos: la hoja cuenta 103, 92 y 112 observaciones y suma 1 108.8, 982.2 y 1 194.4, cuando los datos reales son 102, 91 y 111 (sumas 1 106.8, 979.2 y 1 187.4; la diferencia es exactamente el código de cada grupo). Con los datos correctos F = 0.0414 y p = 0.9595, no 0.0202 y 0.980. La conclusión escrita llama "tamaños de muestra" a esas sumas y la ficha técnica habla de "nivel de confianza del 99 %" mientras usa α = 0.05 (z crítico −1.645). La decisión (no se rechaza H0) no cambia.
16. **Notebooks del profesor desincronizados con los `.md`.** (a) `Taller_03_…_profesor.ipynb` no tiene salidas guardadas en 5 de sus 9 celdas de código (Ejercicios 2, 4, 5, 6 y 7), justo las que producen los resultados; al ejecutarlo corre sin errores y reproduce las cifras de la clave `.md`. Como el Anexo exige "salidas visibles", conviene reejecutarlo y guardarlo antes de compartirlo. (b) `Taller_01_…_profesor.ipynb` trae un *Bonus* de potencia (n = 39.4 por grupo con aproximación normal y 40.3 con statsmodels, para `writing` por género), los gráficos de la recta y de la extrapolación y la fila "Tamaño de muestra óptimo" en el resumen; ni la clave `.md` ni el taller de estudiante `.md` los tienen.
