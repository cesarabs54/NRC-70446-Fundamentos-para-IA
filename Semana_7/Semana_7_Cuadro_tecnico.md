# Semana 7 — Cuadro técnico consolidado

**Tema:** Estadística inferencial II: regresión lineal. Ecuación por mínimos cuadrados (`b0`, `b1`), prueba de hipótesis sobre la pendiente, R², RMSE y MAE, revisión de supuestos (residuos), regresión múltiple y comparación de modelos, variable *dummy* (t de Student = regresión), entrenamiento y prueba con scikit-learn, y cuándo conviene (o no) usar el modelo.
**Dataset de la semana:** `StudentsPerformance.csv` — 1 000 estudiantes × 8 columnas: tres notas de 0 a 100 (`math score`, `reading score`, `writing score`) y cinco variables categóricas (`gender`, `race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`). Sin nulos y sin duplicados. Las copias de `Semana_6/`, `Semana_7/` y `Semana_8/` son idénticas byte a byte, y `StudentsPerformance.xlsx` (una sola hoja, encabezado en la primera fila) tiene exactamente los mismos 1 000 registros. El Taller 1 trabaja con otro conjunto: 6 estudiantes ficticios (horas de estudio → nota) para calcular todo a mano.
**Actividad calificada:** ninguna. La presentación del profesor (`Presentación Semana 7 Profesor.pptx`) dice «Actividad Semana 7 (No hay actividad) - Semana 8» y la metodología de la clase es un debate (regresión lineal vs. logística). Este cuadro es, por tanto, una referencia técnica para los talleres, la actividad en clase `03_Regresion_lineal.ipynb`, el debate y la Semana 8.

> Todas las cifras de este documento se recalcularon ejecutando el código sobre el CSV del repositorio (Python 3.11.9 con SciPy 1.17.1, pandas 3.0.6, NumPy 2.4.6, statsmodels 0.15.0 y scikit-learn 1.9.1; semillas fijas donde hubo remuestreo). Las marcadas con ✅ son las que ya aparecen en las guías `01` y `02`, en los talleres (`Taller_01` y `Taller_02`, con sus claves), en el notebook `03_Regresion_lineal` (con su clave) o en las presentaciones; las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en esos materiales. Cuando una cifra solo aparece en la salida de `summary()` sin comentario, se indica «(salida sin comentar)».
>
> **Archivos ignorados por Git que se usaron** (`*profesor*` está en `.gitignore`, así que son solo locales): `Taller_01_…_profesor.md` y `.pdf`, `Taller_02_…_profesor.md` y `.ipynb`, `03_Regresion_lineal_profesor.ipynb` y `.pdf`, `01_Regresion_lineal_conceptos_basicos_profesor.pptx`, y en `Profesor/`: `01_Regresion_lineal_conceptos_basicos.pptx`, `Presentación Semana 7 Profesor.pptx` y `Promt.md` (el prompt para generar código con IA: cargar y explorar el dataset, aplicar al menos dos pruebas inferenciales, comentar cada bloque; la sección 9 lo resuelve). También las tres imágenes de `Genially_assets_profesor/` (dispersión lectura–escritura, predicción sobre prueba y residuos), que corresponden a los gráficos del Ejercicio 1 del Taller 2 y de los Ejercicios 4 y 6 del notebook `03`.

---

## 1. Procedimientos de la semana (de punta a punta)

Siguen los 7 pasos de `01` (explorar, plantear, ajustar, evaluar coeficientes, evaluar el ajuste global, revisar supuestos, predecir) más el paso de entrenamiento y prueba del notebook `03`. Los marcados con (➕) no están en los materiales.

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la semana |
|---|---|---|---|---|
| Carga y exploración | Pandas | `read_csv`, `shape`, `describe()` | Conocer rango y dispersión de las notas | 1 000 × 8. `reading` media 69.17 (s = 14.60, rango 17 a 100); `writing` 68.05 (s = 15.20, rango 10 a 100) |
| Calidad de datos | Pandas | `isnull().sum()`, `duplicated().sum()` | Detectar nulos y repetidos antes de ajustar | 0 nulos y 0 duplicados |
| ¿Regresión es la herramienta? | — | Las tres preguntas de `02`: Y numérica, X mayormente numérica, pocas categóricas | Evitar usar el modelo donde no corresponde | `writing` ← `reading`: Y numérica, X numérica, una sola variable → sí (sección 10) |
| Gráfico de dispersión | Matplotlib | `plt.scatter(x, y, alpha=0.3)` | Ver si la nube sube en línea recta | Nube diagonal estrecha (sección 2) |
| Correlación | Pandas / SciPy | `df.corr()`, `stats.pearsonr` | Medir la fuerza y la dirección lineal | `reading`–`writing` r = 0.9546, IC 95 % [0.949; 0.960] · `math`–`reading` 0.8176 · `math`–`writing` 0.8026 |
| Ajuste por mínimos cuadrados | SciPy / statsmodels / scikit-learn | `stats.linregress`, `sm.OLS`, `LinearRegression().fit` | Calcular `b0` y `b1` que minimizan la suma de errores al cuadrado | `writing` = −0.6676 + 0.9935 · `reading`. Las seis formas de ajustar dan lo mismo (diferencia máxima 3e-14) |
| Hipótesis sobre la pendiente | SciPy / statsmodels | t = b1 / SE(b1), p-value | Decidir si la relación es real o azar | H0: β1 = 0 · H1: β1 ≠ 0. t = 101.23, gl = 998, p = 3.5e-527 → se rechaza H0 |
| Intervalo de la pendiente (➕) | statsmodels | `conf_int()`, bootstrap | Responder "¿cuánto?": el p-value no lo dice | IC 95 % de β1 [0.974; 1.013] · bootstrap [0.975; 1.012] |
| Ajuste global | statsmodels | R² = 1 − SSres / SStot, `rsquared_adj`, `fvalue` | Qué parte de la variación explica el modelo | R² = 0.9113 (SSres 20 470.86 de 230 677.08) · R² ajustado 0.9112 · F = 10 248.0 = t² |
| Error de predicción | scikit-learn | `mean_absolute_error`, `mean_squared_error` | Medir el error en puntos de nota | En los 1 000: MAE 3.61 · RMSE 4.52 · error estándar residual (n − 2) 4.53 |
| Supuestos (residuos) | SciPy / statsmodels | `shapiro`, `levene` (✅) · `normaltest`, `het_breuschpagan`, `durbin_watson`, Cook (➕) | Confirmar que el modelo lineal es razonable | Shapiro p = 0.0368 (rechaza, leve); D'Agostino p = 0.362; Breusch-Pagan p = 0.108; Durbin-Watson 1.97; Cook máximo 0.018 |
| Predicción | NumPy / statsmodels | `b0 + b1 * x`, `get_prediction` (➕ para los intervalos) | Estimar la nota de un estudiante nuevo | `reading` = 80 → 78.81 (IC de la media [78.46; 79.16]; intervalo de predicción [69.92; 87.71]) |
| Regresión múltiple | statsmodels / scikit-learn | `sm.OLS` con `add_constant`; `LinearRegression` con 2 columnas | Sumar variables, cada una con su pendiente | + `math`: R² 0.9127 (de 0.9113); coeficiente de `math` 0.0670, t = 4.118 |
| Comparación de modelos (➕) | statsmodels | `compare_f_test`, AIC / BIC, R² ajustado | Decidir si una variable extra "vale la pena" | `math`: F = 16.96, p = 4.1e-5, pero ΔR² = 0.0015 |
| Multicolinealidad (➕) | statsmodels | `variance_inflation_factor` | Detectar predictoras que repiten información | VIF = 3.0 (`reading` y `math`) · 11.3 (`reading` y `writing`) |
| Variable dummy | SciPy / statsmodels | `ttest_ind`, `linregress` sobre 0/1 | Comparar dos grupos como regresión | `writing` por género: b0 = 63.3112 (hombres), b1 = 9.1560, t = 9.98 = el de `ttest_ind` (salvo el signo) |
| Entrenamiento y prueba | scikit-learn | `train_test_split(test_size=0.2, random_state=42)` | Evaluar con estudiantes que el modelo no vio | 800 / 200 · R² de prueba 0.9010 · MAE 3.84 · RMSE 4.89 · R² de entrenamiento 0.9137 |
| Validación cruzada (➕) | scikit-learn | `cross_validate`, `RepeatedKFold` | No depender de una sola partición | 5 × 20 pliegues: R² 0.9100 (simple) y 0.9113 (con `math`) |
| Interpretación | — | Pendiente + intervalo + R² + advertencia de causalidad y de rango | Redactar la conclusión en función del problema | "Asociado con", nunca "causa"; solo dentro del rango 17 a 100 de `reading` |

---

## 2. Qué gráfico usar (Matplotlib / Seaborn)

| Pregunta | Gráfico (función) | Ejemplo con el dataset | Cuidado al leerlo | Uso |
|---|---|---|---|---|
| ¿Hay relación y es lineal? | Dispersión · `plt.scatter(alpha=0.3)` | `reading` vs. `writing`: nube diagonal estrecha (r = 0.9546). `math` vs. `reading`: más abierta (r = 0.8176) | Las notas son enteras: hay puntos superpuestos, por eso `alpha` | ✅ |
| ¿Cómo se ve la recta ajustada? | `plt.plot(x, b0 + b1·x)` sobre la dispersión | Notebook `03`, Ejercicio 4: recta roja sobre `X_test` (200 estudiantes) | Con una recta se puede graficar `X_test` sin ordenar; con un modelo curvo saldría en zigzag | ✅ |
| ¿Qué tan seguro es lo que predice? | Banda de la media y banda de predicción · `sns.regplot` / `get_prediction` | En `reading` = 80: media 78.81 ± 0.35; un estudiante individual 78.81 ± 8.9 | `regplot` solo dibuja la banda de la *media*; los estudiantes individuales caen en la ancha | ➕ |
| ¿Los residuos tienen patrón? | Residuos contra predichos · `plt.scatter(pred, resid)` + `axhline(0)` | Todo el conjunto: desviación de los residuos 4.65 · 4.65 · 4.38 · 4.38 por cuartil de la predicción. En prueba: de −11.9 a +15.1 | Un abanico (varianza que crece) o una curva delatan que el modelo lineal no basta. Aquí no aparecen | ✅ |
| ¿Los residuos son normales? | Histograma de residuos y gráfico Q-Q · `stats.probplot` | r del Q-Q = 0.9985; sesgo 0.092; curtosis 2.871 (la normal tiene 3) | Con n = 1 000 Shapiro rechaza (p = 0.0368) por diferencias mínimas; el Q-Q muestra que casi no hay | ➕ |
| ¿Qué tan bien predice sobre datos nuevos? | Real contra predicho con la diagonal · `plt.scatter(y_te, pred)` | R² de prueba 0.9010; RMSE 4.89 | Un solo conjunto de prueba es una sola partición (salvedad 8) | ➕ |
| ¿Qué variables se parecen entre sí? | Matriz de correlación · `df.corr()` y `sns.heatmap(annot=True)` | 0.82 (`math`–`reading`), 0.80 (`math`–`writing`), **0.95** (`reading`–`writing`) | Correlación alta entre predictoras = posible multicolinealidad (sección 6.3) | ✅ (tabla) / ➕ (mapa de calor) |
| ¿Algún estudiante pesa demasiado en la recta? | Distancia de Cook · `get_influence()`, `influence_plot` | Máximo 0.0176 (índice 596); 36 con Cook > 4/n pero ninguno cerca de 1 | Un residuo grande no es lo mismo que un punto influyente: hay que mirar también el apalancamiento | ➕ |
| ¿Cómo se ve una variable dummy? | Boxplot por grupo + los dos puntos de la recta | Hombres 63.31 (= b0) y mujeres 72.47 (= b0 + b1) | La "recta" solo existe en X = 0 y X = 1 | ➕ |
| ¿Cuánto mejora cada variable que se agrega? | Barras de ΔR² por variable | `math` +0.0015 · curso +0.0072 · género +0.0049 · educación de los padres +0.0040 | Una mejora estadísticamente significativa puede ser pequeña (salvedad 9) | ➕ |
| ¿Cuánto cambia el R² de prueba con la semilla? | Histograma del R² de 2 000 particiones | R² de prueba 0.910 ± 0.011 (de 0.864 a 0.939); la semilla 42 da 0.9010 | Comparar dos modelos con una sola semilla engaña (salvedad 8) | ➕ |

---

## 3. Pruebas y funciones que se pueden aplicar (SciPy / statsmodels / scikit-learn)

### 3.1 Cuadro de herramientas

| Pregunta | Función | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Qué tan fuerte es la relación lineal? | **Pearson** · `stats.pearsonr` | Dos numéricas, relación lineal. H0: ρ = 0. Su t es el mismo que el de la pendiente | `reading`–`writing`: r = 0.9546, t = 101.23, IC 95 % [0.949; 0.960]. Spearman 0.949, Kendall 0.820 | ✅ (r a mano en el Taller 1 y tabla de `02`) / ➕ (IC, Spearman) |
| ¿Cuál es la recta? | **Mínimos cuadrados** · `stats.linregress(x, y)` | Una predictora. Devuelve pendiente, intercepto, r, p y error estándar | b1 = 0.9935, b0 = −0.6676, SE(b1) = 0.0098 | ✅ |
| ¿La pendiente es distinta de cero? | **t de la pendiente** · t = b1 / SE(b1) | Residuos aprox. normales y varianza constante | t = 101.23, gl = 998. `linregress` imprime p = 0.0: el valor real es 3.5e-527 (salvedad 5) | ✅ |
| ¿Cuánto vale la pendiente? | IC de β1 · `sm.OLS(...).fit().conf_int()` · bootstrap | El IC t exige los mismos supuestos; el bootstrap no | [0.974; 1.013] (t) · [0.975; 1.012] (bootstrap, 9 999 remuestreos) · SE robusto HC3 0.0093 frente a 0.0098 | ➕ |
| ¿La pendiente es distinta de un valor (1)? | `ols.t_test("reading score = 1")` | Útil cuando la hipótesis natural no es 0 | β1 = 1: t = −0.659, p = 0.510 (no se rechaza) | ➕ |
| ¿La recta es la identidad (`writing` = `reading`)? | **F conjunta** · `ols.f_test((np.eye(2), [0, 1]))` | Contrasta b0 = 0 y b1 = 1 a la vez | F = 30.52 (gl 2 y 998), p = 1.4e-13 → se rechaza: en promedio `writing` queda 1.1 puntos por debajo | ➕ |
| ¿Cuánto explica el modelo? | **R²** · `rvalue ** 2`, `r2_score` | Con una predictora R² = r². R² ajustado penaliza variables extra | R² = 0.9113; ajustado 0.9112. Con `math`: 0.9127 y 0.9126 | ✅ (R²) / ✅ salida sin comentar (ajustado) |
| ¿Cuántos puntos se equivoca? | **MAE, RMSE** · `mean_absolute_error`, `mean_squared_error` | Misma escala que la nota. RMSE castiga más los errores grandes | MAE 3.61 y RMSE 4.52 (relación 1.25, la de una normal). Con n − 2: error estándar residual 4.53 | ✅ |
| ¿Se pueden sumar variables? | **OLS múltiple** · `sm.OLS(y, sm.add_constant(X))` | Predictoras numéricas o dummies | `writing` = −1.1608 + 0.9366·`reading` + 0.0670·`math`, R² 0.9127 | ✅ |
| ¿Una variable extra mejora de verdad? | **F de modelos anidados** · `m2.compare_f_test(m1)` · AIC / BIC | m1 está contenido en m2 | `math`: F = 16.956 (= 4.118²), p = 4.1e-5; AIC 5860.9 → 5846.0; BIC 5870.7 → 5860.7. AIC y BIC aparecen en el `summary()` sin comentar | ➕ (prueba) / ✅ salida sin comentar (AIC, BIC) |
| ¿Los residuos son normales? | **Shapiro-Wilk** · `stats.shapiro(resid)` | N ≤ 5 000; con n grande detecta desviaciones diminutas | W = 0.9967, p = 0.0368 (modelo simple). Modelo con `math`: p = 0.680 | ✅ |
| ¿Normales? (alternativas) | **D'Agostino** · `stats.normaltest` · **Jarque-Bera** | Combinan sesgo y curtosis | Modelo simple: K² = 2.031, p = 0.362; JB = 2.094, p = 0.351. Con `math`: JB p = 0.426 (salida sin comentar) | ➕ |
| ¿Varianza constante? | **Levene** · `stats.levene` (entre grupos) · **Breusch-Pagan** · `het_breuschpagan` (en la regresión) | Levene compara grupos; Breusch-Pagan, el tamaño del residuo contra X | Género → `writing`: Levene W = 0.0069, p = 0.9336. Reading → writing: Breusch-Pagan LM = 2.590, p = 0.108 | ✅ (Levene) / ➕ (Breusch-Pagan) |
| ¿Hay curvatura que se escapa? | **RESET** · `linear_reset` | Agrega el cuadrado de la predicción | F = 1.921, p = 0.166 → no hay evidencia de curvatura | ➕ |
| ¿Los residuos son independientes? | **Durbin-Watson** · `durbin_watson` | Cerca de 2 = sin autocorrelación; solo tiene sentido si las filas tienen un orden | 1.970 (simple), 1.974 (con `math`; salida sin comentar) | ➕ / ✅ salida sin comentar |
| ¿Alguna fila pesa demasiado? | **Distancia de Cook** · `get_influence().cooks_distance` | Regla práctica: Cook > 4/n merece mirarse, > 1 es grave | Máximo 0.0176; ninguna fila ≥ 0.02 | ➕ |
| ¿Las predictoras se repiten entre sí? | **VIF** · `variance_inflation_factor` | VIF > 5 (o 10) es señal de alerta | `reading`–`math`: 3.02. `reading`–`writing`: 11.27 | ➕ |
| ¿Cuánto puedo confiar en una predicción? | **Intervalos** · `ols.get_prediction(X).summary_frame()` | Intervalo de la media (confianza) o de un individuo (predicción) | `reading` = 65 → 63.91 [IC 63.62; 64.20] [IP 55.02; 72.80]. Cobertura real del IP al 95 %: 95.6 % en los 1 000 y 95.3 % fuera de muestra | ➕ |
| ¿Difieren dos grupos? | **t de Student** · `stats.ttest_ind(equal_var=True)` | Varianzas homogéneas (Levene). Equivale a regresar sobre una variable 0/1 | Género → `writing`: t = −9.9796, gl = 998, p = 2.02e-22. Regresión dummy: mismo p | ✅ |
| ¿Difieren dos grupos sin exigir varianzas iguales? | **Welch** · `ttest_ind(equal_var=False)` · **Mann-Whitney** | Opción segura por defecto; obligatoria si Levene rechaza | Género → `writing`: Welch t = −9.998, gl = 997.5, p = 1.7e-22; Mann-Whitney p = 4.7e-23 | ➕ |
| ¿Difieren 3 o más grupos? | **ANOVA** · `stats.f_oneway` = F global de `smf.ols("y ~ C(grupo)")` | Es el mismo modelo con k − 1 dummies | Etnia → `math`: F = 14.594, p = 1.4e-11 en ambas | ➕ (aquí; en la Semana 6 ✅) |
| ¿Cómo evalúo con datos no vistos? | **División** · `train_test_split` · `LinearRegression().fit` / `.predict` | `random_state` fija la partición | 800 / 200: b1 = 0.9971, b0 = −0.8960; R² de prueba 0.9010 | ✅ |
| ¿Y sin depender de una sola partición? | **Validación cruzada** · `cross_validate(RepeatedKFold)` | Promedia varias particiones | 5 pliegues con semilla 42: R² 0.9097 (simple) y 0.9112 (con `math`); 5 × 20: 0.9100 y 0.9113 | ➕ |

### 3.2 Guía rápida para elegir

| Si quiero… | Herramienta | Verificación |
|---|---|---|
| Describir la relación entre dos numéricas | `pearsonr` o `linregress` | Dispersión + residuos |
| Predecir una nota a partir de otra | `LinearRegression` o `sm.OLS` | R², MAE / RMSE en datos de prueba |
| Saber si una variable aporta | t del coeficiente + `compare_f_test` | ΔR² y validación cruzada (¿vale el tamaño de la mejora?) |
| Comparar dos grupos | `ttest_ind` ≡ regresión con dummy | Levene; si rechaza, Welch |
| Comparar 3 o más grupos | `f_oneway` ≡ OLS con k − 1 dummies | Levene; Kruskal-Wallis si no hay normalidad |
| Predecir una categoría (sí / no) | No es regresión lineal: regresión logística (Semana 8) | Sección 10 |
| Saber si el modelo generaliza | `train_test_split` y validación cruzada | R² de entrenamiento ≈ R² de prueba |

### 3.3 Cómo revisar los supuestos de la recta (reading → writing)

| Supuesto | Cómo revisarlo | Resultado | Si falla |
|---|---|---|---|
| Linealidad | Dispersión, residuos contra predichos, RESET | Sin curva; RESET p = 0.166. Media de los residuos por cuartil: −0.37, +0.52, +0.13, −0.28 | Transformar, agregar un término cuadrático u otro modelo |
| Normalidad de los residuos | Shapiro, D'Agostino, Q-Q, sesgo y curtosis | Shapiro rechaza (p = 0.0368); D'Agostino y Jarque-Bera no (p = 0.362 y 0.351); Q-Q r = 0.9985; sesgo 0.092, curtosis 2.871 | Con n grande el t de la pendiente es robusto (TLC); reportar la limitación o usar bootstrap |
| Varianza constante | Residuos contra predichos, Breusch-Pagan | p = 0.108; desviación 4.65 · 4.65 · 4.38 · 4.38 por cuartil | Errores robustos (HC3: SE 0.0093) o mínimos cuadrados ponderados |
| Independencia | Diseño del estudio; Durbin-Watson | 1.970. Los estudiantes se tratan como independientes, aunque comparten institución o aula | Modelos de efectos mixtos (fuera del alcance) |
| Sin puntos influyentes | Cook, apalancamiento | Cook máximo 0.0176, apalancamiento máximo 0.0138; 39 residuos estandarizados con valor absoluto > 2 (esperados ≈ 46) y 2 con valor absoluto > 3 | Revisar el dato; ajustar con y sin él |
| Sin multicolinealidad (solo múltiple) | Correlación entre predictoras, VIF | `reading`–`math` VIF 3.0 (moderado) | Dejar una de las dos (sección 6.3) |

Umbrales que usa el material: α = 0.05; R² "alto" ≈ 0.9; en correlación, |r| ≥ 0.7 es "fuerte". Reglas prácticas del cuadro: VIF > 5 alerta, Cook > 4/n merece revisión, Durbin-Watson cerca de 2 es lo esperado. Regla general: con n = 1 000 las pruebas de normalidad rechazan casi siempre; conviene mirar el Q-Q y el sesgo, y no decidir solo con p.

---

## 4. Ejemplo guiado 1: lectura → escritura (regresión simple, Taller 2 Ejercicios 1 a 5)

**Pregunta:** ¿se relaciona la nota de lectura con la de escritura y cuánto cambia `writing score` por cada punto de `reading score`?

### 4.1 Del gráfico a la predicción

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Descriptiva (✅) | `df[["reading score","writing score"]].describe()` | `reading` media 69.17, s = 14.60 · `writing` 68.05, s = 15.20 | Promedios y dispersiones parecidos (diferencia de 1.1 puntos) |
| 2 | Gráfico (✅) | `plt.scatter(x, y, alpha=0.3)` | Nube diagonal estrecha | Relación lineal creciente |
| 3 | Correlación (➕ IC) | `stats.pearsonr(x, y)` | r = 0.9546, IC 95 % [0.949; 0.960] | Relación lineal muy fuerte y positiva |
| 4 | Hipótesis (✅) | — | H0: β1 = 0 · H1: β1 ≠ 0 · α = 0.05, dos colas | β1 es la pendiente *poblacional* |
| 5 | Ajuste (✅) | `stats.linregress(x, y)` | b1 = Sxy / Sxx = 211 574.87 / 212 952.44 = 0.9935 · b0 = ȳ − b1·x̄ = 68.054 − 0.9935 · 69.169 = −0.6676 | Un punto más de lectura se asocia con ≈ 0.99 puntos más de escritura (casi 1 a 1). La pendiente **no** es r |
| 6 | Prueba t (✅) | t = b1 / SE(b1) | SE(b1) = 0.0098 → t = 101.23, gl = 998, p = 3.5e-527. F = t² = 10 248.0 | Se rechaza H0. Mismo t que el de `pearsonr` |
| 7 | Intervalo (➕) | `ols.conf_int()` | β1 en [0.974; 1.013] · b0 en [−2.03; 0.69] | El intervalo de β1 incluye 1: no se distingue de "un punto por punto" (p = 0.510) |
| 8 | Intercepto (✅) | — | b0 = −0.668 cuando `reading` = 0 (SE 0.694, t = −0.962, p = 0.336) | Sin sentido práctico: el mínimo observado es 17. Centrando `reading` en su media, el intercepto pasa a ser 68.054 (= la media de `writing`) |
| 9 | Ajuste global (✅) | `rvalue ** 2` | R² = 1 − 20 470.86 / 230 677.08 = 0.9113 = r² | Explica el 91.1 %; el 8.9 % restante no lo capta `reading` |
| 10 | Error típico (✅ RMSE aprox.) | `np.sqrt(SSres / n)` | RMSE 4.52 · error estándar residual (n − 2) 4.53 · MAE 3.61 | Un estudiante individual se aleja de la recta unos 3.6 puntos en promedio y 4.5 en términos cuadráticos |
| 11 | Supuestos (✅ Shapiro) | `stats.shapiro(resid)` + (➕) otras | Shapiro p = 0.0368 · D'Agostino 0.362 · Jarque-Bera 0.351 · Breusch-Pagan 0.108 · RESET 0.166 · Durbin-Watson 1.97 · Cook máx. 0.018 | Salvo Shapiro (leve, con n = 1 000), todo cumple. Ver sección 3.3 |
| 12 | Predicción dentro del rango (✅) | `b0 + b1 * 80` | `reading` = 80 → 78.81 (IC de la media [78.46; 79.16]; IP [69.92; 87.71]) · 65 → 63.91 (IP [55.02; 72.80]) · 50 → 49.01 | La diferencia entre 80 y 50 es 29.81 = b1 · 30 (relación lineal) |
| 13 | Fuera del rango (➕) | `get_prediction` | `reading` = 100 → 98.69 (IP hasta 107.60) · 150 → 148.36 (IP [139.34; 157.39]) · −5 → −5.64 | Imposibles (> 100 o < 0): el modelo no conoce los topes de la escala |

**Conclusión:** con α = 0.05 se rechaza H0. Existe una asociación lineal muy fuerte (R² = 0.911): cada punto de lectura se asocia con 0.99 puntos de escritura (IC 95 % [0.974; 1.013]). Es una asociación, no una prueba de que leer mejor *cause* escribir mejor: ambas son habilidades del mismo ámbito, y la recta de `reading` sobre `writing` tiene otra pendiente (0.917, no 1 / 0.9935 = 1.007). La recta tampoco es la identidad: en promedio `writing` queda 1.1 puntos por debajo de `reading` (F conjunta p = 1.4e-13).

### 4.2 Código listo para pegar

```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

df = pd.read_csv("StudentsPerformance.csv")
x, y = df["reading score"], df["writing score"]

# 1) Calidad de datos y correlación
print(df.shape, df.isnull().sum().sum(), df.duplicated().sum())
r = stats.pearsonr(x, y)
print(r.statistic, r.confidence_interval())

# 2) Recta con SciPy (Taller 2, Ejercicio 2): t = b1 / SE(b1)
res = stats.linregress(x, y)
print(res.slope, res.intercept, res.stderr, res.slope / res.stderr, res.rvalue ** 2)

# 3) Lo mismo con statsmodels: intervalos, R² ajustado, F, AIC y BIC
ols = sm.OLS(y, sm.add_constant(x)).fit()
print(ols.conf_int())
print(ols.rsquared_adj, ols.fvalue, ols.aic, ols.bic)
resid = ols.resid
print("Error estándar residual (n - 2):", np.sqrt(ols.mse_resid))
print("RMSE (n):", np.sqrt((resid ** 2).mean()), "MAE:", resid.abs().mean())

# 4) Supuestos sobre los residuos
print(stats.shapiro(resid), stats.normaltest(resid))
print(het_breuschpagan(resid, ols.model.exog)[:2], durbin_watson(resid))
cook = ols.get_influence().cooks_distance[0]
print("Cook máximo:", cook.max(), "| filas con Cook > 4/n:", (cook > 4 / len(df)).sum())

# 5) Predicción: intervalo de la media (confianza) y de un estudiante (predicción)
nuevos = pd.DataFrame({"const": 1.0, "reading score": [65, 80, 100]})
print(ols.get_prediction(nuevos).summary_frame(alpha=0.05).round(2))

# 6) ¿La pendiente es 1? ¿La recta es la identidad (b0 = 0 y b1 = 1)?
print(ols.t_test("reading score = 1"))
print(ols.f_test((np.eye(2), [0, 1])))

# 7) IC bootstrap de la pendiente (no supone normalidad)
rng = np.random.default_rng(42)
xs, ys = x.to_numpy(float), y.to_numpy(float)
pend = []
for _ in range(9999):
    i = rng.integers(0, len(df), len(df))
    pend.append(np.polyfit(xs[i], ys[i], 1)[0])
print(np.percentile(pend, [2.5, 97.5]))
```

---

## 5. Ejemplo guiado 2: entrenamiento y prueba con scikit-learn (notebook `03`)

**Pregunta:** ¿qué tan bien predice el modelo a estudiantes que **no** se usaron para ajustarlo?

### 5.1 De la partición al estudiante nuevo

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Preparar X e y (✅) | `X = df[["reading score"]]`, `y = df["writing score"]` | X (1000, 1) · y (1000,) | Doble corchete = tabla 2D, lo que pide scikit-learn |
| 2 | Dividir (✅) | `train_test_split(X, y, test_size=0.2, random_state=42)` | 800 de entrenamiento y 200 de prueba | La semilla hace la partición reproducible |
| 3 | Entrenar (✅) | `LinearRegression().fit(X_tr, y_tr)` | b1 = 0.9971, b0 = −0.8960 (con los 1 000: 0.9935 y −0.6676) | Muestra distinta, recta ligeramente distinta |
| 4 | Predecir (✅) | `modelo.predict(X_te)` | Recta roja sobre los puntos de prueba | Sigue la nube; es una recta porque ŷ = b0 + b1·x |
| 5 | Evaluar (✅) | `r2_score`, `mean_absolute_error`, `mean_squared_error` | Prueba: R² 0.9010 · MAE 3.8374 · RMSE 4.8857. Entrenamiento: R² 0.9137 (RMSE 4.43, MAE 3.56) | Diferencia de 0.013 entre entrenamiento y prueba: no hay sobreajuste |
| 6 | Residuos (✅) | `y_te - pred` | Media −0.09, desviación 4.90, de −11.95 a +15.07 (ninguno llega a 20) | Nube pareja alrededor de cero, sin abanico |
| 7 | Regresión múltiple (✅) | `LinearRegression` con `reading` y `math` | Coeficientes 0.9375 y 0.0704, intercepto −1.4321. Prueba: R² 0.9018 · MAE 3.8380 · RMSE 4.8647. Entrenamiento: R² 0.9153 | Mejora de 0.0008 en el R² de prueba |
| 8 | Estudiante nuevo (✅) | `predict(pd.DataFrame({"reading score":[78], "math score":[82]}))` | 77.46 (con el modelo simple y `reading` = 78: 76.88) | El DataFrame deja explícito qué número es cada variable |
| 9 | ¿Depende de la semilla? (➕) | 2 000 particiones 80 / 20 con semillas aleatorias | R² de prueba simple: media 0.9097, desviación 0.0112, rango 0.8638 a 0.9394, 95 % central [0.885; 0.929]. RMSE medio 4.535 (de 3.930 a 5.240) | La semilla 42 es una partición algo pesimista (percentil 20) |
| 10 | Comparación pareada (➕) | Mismas 2 000 semillas para ambos modelos | Con `math`: media 0.9110. Diferencia +0.0013 (desviación 0.0015); gana en 1 671 de las 2 000 particiones (83.6 %) | La mejora existe, pero su promedio (0.0013) es solo ≈ 12 % de la desviación del R² de prueba entre particiones (0.0112) |
| 11 | Validación cruzada (➕) | `cross_validate(RepeatedKFold(5, n_repeats=20))` | Simple: R² 0.9100 · RMSE 4.529 · MAE 3.623. Con `math`: 0.9113 · 4.496 · 3.600. 5 pliegues, semilla 42: simple [0.9010, 0.9265, 0.9070, 0.8973, 0.9168] y con `math` [0.9018, 0.9275, 0.9093, 0.8983, 0.9192] | Bajar 0.03 puntos de RMSE no justifica una variable más por sí solo |

**Conclusión:** el modelo generaliza: R² de prueba ≈ 0.90 a 0.91 y error típico ≈ 4.5 puntos, igual al de entrenamiento. La recta calculada con scikit-learn es la misma que la de `scipy` y `statsmodels` (cambia solo la muestra con la que se entrena).

### 5.2 Código listo para pegar

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, KFold, RepeatedKFold

df = pd.read_csv("StudentsPerformance.csv")
X, y = df[["reading score"]], df["writing score"]
X_multi = df[["reading score", "math score"]]

# 1) Modelo simple: partición 80 / 20 con semilla (notebook 03)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = LinearRegression().fit(X_tr, y_tr)
pred = modelo.predict(X_te)
print(len(X_tr), len(X_te), modelo.coef_[0], modelo.intercept_)
print(r2_score(y_te, pred), mean_absolute_error(y_te, pred), np.sqrt(mean_squared_error(y_te, pred)))
print("R² entrenamiento:", r2_score(y_tr, modelo.predict(X_tr)))
res = y_te - pred
print(res.mean(), res.std(), res.min(), res.max())

# 2) Modelo múltiple y estudiante nuevo
Xm_tr, Xm_te, ym_tr, ym_te = train_test_split(X_multi, y, test_size=0.2, random_state=42)
multi = LinearRegression().fit(Xm_tr, ym_tr)
pred_m = multi.predict(Xm_te)
print(multi.coef_, multi.intercept_, r2_score(ym_te, pred_m))
print(multi.predict(pd.DataFrame({"reading score": [78], "math score": [82]})))

# 3) ¿Cuánto depende el R² de prueba de la semilla? 2 000 particiones
rng = np.random.default_rng(0)
r2_s, r2_m = [], []
for _ in range(2000):
    semilla = int(rng.integers(0, 2**31 - 1))
    a = train_test_split(X, y, test_size=0.2, random_state=semilla)
    b = train_test_split(X_multi, y, test_size=0.2, random_state=semilla)
    r2_s.append(r2_score(a[3], LinearRegression().fit(a[0], a[2]).predict(a[1])))
    r2_m.append(r2_score(b[3], LinearRegression().fit(b[0], b[2]).predict(b[1])))
r2_s, r2_m = np.array(r2_s), np.array(r2_m)
print(r2_s.mean(), r2_s.std(), r2_s.min(), r2_s.max(), (r2_s < 0.9010).mean())
print((r2_m - r2_s).mean(), (r2_m - r2_s).std(), (r2_m > r2_s).mean())

# 4) Validación cruzada: 5 pliegues con semilla 42, y 5 pliegues repetidos 20 veces
kf = KFold(5, shuffle=True, random_state=42)
print(cross_val_score(LinearRegression(), X, y, cv=kf, scoring="r2").round(4))
print(cross_val_score(LinearRegression(), X_multi, y, cv=kf, scoring="r2").round(4))
cv = RepeatedKFold(n_splits=5, n_repeats=20, random_state=1)
for nombre, datos in [("simple", X), ("con math", X_multi)]:
    s = cross_validate(LinearRegression(), datos, y, cv=cv,
                       scoring=("r2", "neg_root_mean_squared_error", "neg_mean_absolute_error"))
    print(nombre, s["test_r2"].mean(), -s["test_neg_root_mean_squared_error"].mean(),
          -s["test_neg_mean_absolute_error"].mean())
```

---

## 6. Ejemplo guiado 3: regresión múltiple, comparación de modelos y multicolinealidad

### 6.1 ¿Vale la pena agregar `math score`? (Taller 2 Ejercicio 4)

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Ajuste (✅) | `sm.OLS(y, sm.add_constant(X)).fit()` | `writing` = −1.1608 + 0.9366·`reading` + 0.0670·`math`. SE: 0.699, 0.017, 0.016. t de `math` = 4.118, IC 95 % [0.035; 0.099] | Cada pendiente se interpreta "dejando la otra variable fija". El intercepto no difiere de 0 (p = 0.097) |
| 2 | R² (✅) | `rsquared`, `rsquared_adj` | 0.9113 → 0.9127 (ajustado 0.9112 → 0.9126) | Sube 0.0015: `reading` ya explica casi todo |
| 3 | Prueba de la mejora (➕) | `m2.compare_f_test(m1)` | F = 16.956 (= 4.118²), p = 4.1e-5. `math` explica el 1.7 % de la variación que `reading` dejaba sin explicar | Estadísticamente significativa; prácticamente pequeña |
| 4 | Criterios de información (➕) | `aic`, `bic` | AIC 5860.9 → 5846.0 · BIC 5870.7 → 5860.7 | Ambos prefieren el modelo con `math` (menor es mejor) |
| 5 | Coeficientes estandarizados (➕) | OLS sobre variables en z | `reading` 0.900 · `math` 0.067 | En unidades comparables, `math` pesa 13 veces menos |
| 6 | Supuestos del modelo múltiple (✅ salida sin comentar) | `summary()` | Sesgo 0.087 · curtosis 2.896 · Durbin-Watson 1.974. Con ➕: Shapiro p = 0.680 · Breusch-Pagan p = 0.450 | Los residuos del modelo múltiple sí pasan Shapiro; los del simple, no (salvedad 4) |
| 7 | Error en datos nuevos (➕) | Validación cruzada 5 × 20 | RMSE 4.529 → 4.496 (−0.03 puntos) · MAE 3.623 → 3.600 | Ganancia real, pero mínima |

### 6.2 Qué variables aportan más (sobre `reading`)

| Variable agregada a `reading` | Columnas nuevas | R² | R² ajustado | ΔR² | p de la F anidada | AIC |
|---|---|---|---|---|---|---|
| (modelo base) | 0 | 0.9113 | 0.9112 | — | — | 5860.9 |
| `lunch` | 1 | 0.9120 | 0.9118 | 0.0007 | 0.0037 | 5854.4 |
| `math score` | 1 | 0.9127 | 0.9126 | 0.0015 | 4.1e-5 | 5846.0 |
| `race/ethnicity` | 4 | 0.9138 | 0.9134 | 0.0026 | 6.4e-6 | 5839.3 |
| `parental level of education` | 5 | 0.9153 | 0.9147 | 0.0040 | 9.9e-9 | 5824.8 |
| `gender` | 1 | 0.9162 | 0.9160 | 0.0049 | 4.8e-14 | 5805.9 |
| `test preparation course` | 1 | 0.9184 | 0.9183 | 0.0072 | 5.2e-20 | 5778.7 |
| Las cinco categóricas + `math` | 12 + 1 | 0.9479 | 0.9472 | 0.0366 | — | 5353.7 |

Con validación cruzada 5 × 20: `reading` solo → R² 0.9100, RMSE 4.53 · `reading` + `math` → 0.9113, 4.50 · `reading` + las cinco categóricas (13 columnas) → 0.9315, 3.95 · todas (14 columnas) → **0.9455, 3.52**. Con `reading` controlado, los hombres puntúan 2.20 puntos menos en escritura que las mujeres (la diferencia cruda era 9.16) y quienes no tomaron el curso 2.76 menos: la mayor parte de la brecha por género ya la explica la lectura.

### 6.3 Multicolinealidad (`02`, sección 2.3)

| Caso | Modelo | Resultado | Lectura |
|---|---|---|---|
| Correlación entre predictoras | `reading`–`math` 0.82 · `reading`–`writing` 0.95 | VIF 3.02 y 11.27 | El 0.82 es moderado (VIF < 5); el 0.95 sí es alto |
| `writing` ← `reading` (+ `math`) | `reading` solo: 0.9935 (SE 0.0098). Con `math`: 0.9366 (SE 0.017) | Desviación bootstrap del coeficiente de `reading`: 0.0092 → 0.0150 | El error estándar sube ×1.7 (√3.02), el coeficiente cambia poco |
| `math` ← `reading` | 0.8491 (SE 0.0189), R² 0.6684 | — | Línea base |
| `math` ← `writing` | 0.8009 (SE 0.0188), R² 0.6442 | — | Casi igual de buena que `reading` |
| `math` ← `reading` + `writing` | `reading` 0.6013 (SE 0.0630) · `writing` 0.2494 (SE 0.0606) · R² 0.6740 (ajustado 0.6733) | Desviación bootstrap de `reading`: 0.0195 → 0.0632 (×3.2) | El efecto se "reparte" entre las dos: el error estándar casi se triplica, el R² sube solo 0.0056 |
| ¿Cambian de signo? | 2 000 remuestreos del modelo anterior | 0 coeficientes negativos; `reading` en [0.469; 0.723] y `writing` en [0.131; 0.371] | La inestabilidad es de tamaño, no de signo, en estos datos |

**Conclusión:** la multicolinealidad no daña la predicción (R² = 0.674) sino la interpretación individual de cada coeficiente. Para `writing` ← `reading` + `math` no es un problema (VIF = 3); para `math` ← `reading` + `writing` sí (VIF = 11.3).

### 6.4 Código listo para pegar

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import RepeatedKFold, cross_validate, train_test_split
from sklearn.metrics import r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("StudentsPerformance.csv")
y = df["writing score"]
m1 = sm.OLS(y, sm.add_constant(df[["reading score"]])).fit()
m2 = sm.OLS(y, sm.add_constant(df[["reading score", "math score"]])).fit()

# 1) Coeficientes y comparación de modelos anidados
print(m2.params, m2.bse, m2.conf_int(), sep="\n")
print(m1.rsquared, m2.rsquared, m1.rsquared_adj, m2.rsquared_adj)
print(m1.aic, m2.aic, m1.bic, m2.bic)
print(m2.compare_f_test(m1))   # (F, p, gl): F es el t² de math

# 2) Qué aporta cada variable categórica sobre reading
for col in ["lunch", "race/ethnicity", "parental level of education", "gender", "test preparation course"]:
    dummies = pd.get_dummies(df[col], drop_first=True, dtype=float)
    mc = sm.OLS(y, sm.add_constant(pd.concat([df["reading score"], dummies], axis=1))).fit()
    print(col, dummies.shape[1], round(mc.rsquared - m1.rsquared, 4),
          mc.compare_f_test(m1)[1], round(mc.aic, 1))

# 3) VIF y el caso de alta colinealidad (math ← reading + writing)
Xv = sm.add_constant(df[["reading score", "math score"]])
print([variance_inflation_factor(Xv.values, i) for i in (1, 2)])
Xw = sm.add_constant(df[["reading score", "writing score"]])
print([variance_inflation_factor(Xw.values, i) for i in (1, 2)])
mm = sm.OLS(df["math score"], Xw).fit()
print(mm.params, mm.bse, mm.rsquared, mm.rsquared_adj)

# 4) Validación cruzada: ¿mejoran las categóricas la predicción?
cat = pd.get_dummies(df[["gender", "race/ethnicity", "parental level of education",
                         "lunch", "test preparation course"]], drop_first=True, dtype=float)
cv = RepeatedKFold(n_splits=5, n_repeats=20, random_state=1)
for nombre, datos in [("reading", df[["reading score"]]),
                      ("reading + math", df[["reading score", "math score"]]),
                      ("reading + 5 categóricas", pd.concat([df[["reading score"]], cat], axis=1)),
                      ("todas (14 columnas)", pd.concat([df[["reading score", "math score"]], cat], axis=1))]:
    s = cross_validate(LinearRegression(), datos, y, cv=cv,
                       scoring=("r2", "neg_root_mean_squared_error"))
    print(nombre, datos.shape[1], s["test_r2"].mean(), -s["test_neg_root_mean_squared_error"].mean())

# 5) Cuando sí hay sobreajuste: 30 estudiantes y 14 columnas
chico = df.sample(30, random_state=1)
Xc = pd.concat([chico[["reading score", "math score"]],
                pd.get_dummies(chico[["gender", "race/ethnicity", "parental level of education",
                                      "lunch", "test preparation course"]], drop_first=True, dtype=float)], axis=1)
a = train_test_split(Xc, chico["writing score"], test_size=0.3, random_state=0)
f = LinearRegression().fit(a[0], a[2])
print("14 columnas: entrenamiento", r2_score(a[2], f.predict(a[0])), "prueba", r2_score(a[3], f.predict(a[1])))
b = train_test_split(Xc[["reading score"]], chico["writing score"], test_size=0.3, random_state=0)
g = LinearRegression().fit(b[0], b[2])
print("solo reading: entrenamiento", r2_score(b[2], g.predict(b[0])), "prueba", r2_score(b[3], g.predict(b[1])))
```

---

## 7. Ejemplo guiado 4: comparar grupos es una regresión con variable dummy (Taller 2 Ejercicio 7)

**Pregunta:** ¿difiere `writing score` entre hombres (n = 482) y mujeres (n = 518)? Es el ejemplo de `01` §5 y del Ejercicio 7.

### 7.1 Tres formas de la misma prueba

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Promedios (✅) | `df.groupby("gender")["writing score"].mean()` | Hombres 63.31 (s = 14.11) · mujeres 72.47 (s = 14.84) | Diferencia de 9.16 puntos |
| 2 | Homogeneidad (✅) | `stats.levene(h, m)` | W = 0.0069, p = 0.9336 (centrado en la media: 0.8647) | Varianzas homogéneas → Student es válido |
| 3 | t de Student (✅) | `stats.ttest_ind(h, m, equal_var=True)` | t = −9.9796, gl = 998, p = 2.02e-22 | El signo depende del orden (salvedad 3) |
| 4 | Regresión con dummy (✅) | `stats.linregress(mujer, writing)` | b0 = 63.3112 (= media de hombres) · b1 = 9.1560 (= diferencia) · p = 2.02e-22 | Mismo p que el paso 3: es la misma prueba |
| 5 | Detalle de la regresión (➕) | `smf.ols(...).fit()` | SE(b1) = 0.9175 · t = 9.9796 · IC 95 % de b1 [7.36; 10.96] · R² = 0.0907 · F = 99.59 = t² | Género explica el 9.1 % de la variación de `writing`: pequeño frente al 91.1 % de `reading` |
| 6 | Sin varianzas iguales (➕) | `ttest_ind(equal_var=False)`, `mannwhitneyu` | Welch t = −9.998, gl = 997.5, p = 1.7e-22 · Mann-Whitney U = 79 719.5, p = 4.7e-23 · SE robusto HC3 0.917, p = 1.7e-23 | Cuatro caminos, una conclusión |
| 7 | Tamaño del efecto (➕) | d = b1 / s_pooled | s_pooled = 14.497 (= el error estándar residual de la regresión) · d = 0.632 | Efecto mediano a grande |

**Conclusión:** el intercepto es la media del grupo de referencia y la pendiente es la diferencia de medias; el t de la prueba es exactamente el de la regresión. Hay una diferencia de 9.16 puntos a favor de las mujeres; es una asociación con el género, no una explicación de su causa.

### 7.2 Mismo procedimiento con otras variables binarias

R² de la regresión = η² (porcentaje de variación que explica el grupo). "Student" se usa si Levene ≥ 0.05; si no, Welch.

| Contraste | b0 (referencia) | b1 (diferencia) | t | p | R² | Levene p | p de Welch |
|---|---|---|---|---|---|---|---|
| Curso → `math` (`completed` − `none`) | 64.078 | 5.618 | 5.705 | 1.5e-8 | 0.0316 | 0.4655 | 1.0e-8 |
| Almuerzo → `math` (`standard` − `free/reduced`) | 58.921 | 11.113 | 11.837 | 2.4e-30 | 0.1231 | 0.0742 | 5.5e-28 |
| Género → `math` (`male` − `female`) | 63.633 | 5.095 | 5.383 | 9.1e-8 | 0.0282 | 0.5563 | 8.4e-8 |
| Género → `writing` (`female` − `male`) | 63.311 | 9.156 | 9.980 | 2.0e-22 | 0.0907 | 0.9336 | 1.7e-22 |
| Curso → `writing` (`completed` − `none`) | 64.505 | 9.914 | 10.409 | 3.7e-24 | 0.0979 | **0.0147** | **2.7e-25** |
| Almuerzo → `writing` (`standard` − `free/reduced`) | 63.023 | 7.801 | 8.010 | 3.2e-15 | 0.0604 | 0.1051 | 1.7e-14 |

Curso → `math` coincide con la Semana 6 (t = 5.705, p = 1.5e-8). Curso → `writing` es el único caso en que Levene rechaza: ahí corresponde Welch.

### 7.3 Con 3 o más grupos: ANOVA = regresión con k − 1 dummies

| Contraste | F de la regresión | F de `f_oneway` | R² (= η²) | Lectura |
|---|---|---|---|---|
| Etnia → `math` (5 grupos) | 14.594, p = 1.4e-11 | 14.594, p = 1.4e-11 | 0.0554 (ajustado 0.0516) | b0 = 61.629 = media del grupo A; pendientes B +1.823, C +2.835, D +5.733, E +12.192 (= medias 63.453, 64.464, 67.363, 73.821 menos la de A) |
| Etnia → `writing` | 7.162, p = 1.1e-5 | 7.162, p = 1.1e-5 | 0.0280 | Efecto pequeño |
| Educación de los padres → `math` (6 grupos) | 6.522, p = 5.6e-6 | 6.522, p = 5.6e-6 | 0.0318 | Igual que la Semana 6 |
| Educación de los padres → `writing` | 14.442, p = 1.1e-13 | 14.442, p = 1.1e-13 | 0.0677 | Educación pesa más sobre `writing` que sobre `math` |

### 7.4 Código listo para pegar

```python
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

df = pd.read_csv("StudentsPerformance.csv")
h = df.loc[df["gender"] == "male", "writing score"]
m = df.loc[df["gender"] == "female", "writing score"]

# 1) Supuesto y prueba t clásica
print(stats.levene(h, m), stats.levene(h, m, center="mean"))
print(stats.ttest_ind(h, m, equal_var=True))
print(stats.ttest_ind(h, m, equal_var=False), stats.mannwhitneyu(h, m))

# 2) La misma prueba como regresión con una variable 0 / 1
df["mujer"] = (df["gender"] == "female").astype(int)
ols = smf.ols("Q('writing score') ~ mujer", df).fit()
print(ols.params, ols.bse, ols.tvalues, ols.pvalues, ols.conf_int().loc["mujer"], sep="\n")
print(ols.rsquared, ols.fvalue)   # F = t²
print(smf.ols("Q('writing score') ~ mujer", df).fit(cov_type="HC3").bse)

# 3) Tamaño del efecto: d = b1 / desviación combinada (= error estándar residual)
print(ols.params["mujer"] / ols.mse_resid ** 0.5)

# 4) Varios grupos: ANOVA = regresión con k - 1 dummies
for col in ["race/ethnicity", "parental level of education"]:
    for nota in ["math score", "writing score"]:
        mo = smf.ols(f"Q('{nota}') ~ C(Q('{col}'))", df).fit()
        grupos = [g[nota].to_numpy(float) for _, g in df.groupby(col)]
        print(col, nota, mo.fvalue, mo.f_pvalue, mo.rsquared, stats.f_oneway(*grupos).statistic)
```

---

## 8. Ejemplo guiado 5: el Taller 1 a mano (6 estudiantes)

Horas de estudio X = 2, 3, 5, 6, 8, 9 y nota Y = 48, 58, 63, 72, 78, 88. La clave dice que usa precisión completa y redondea a 2 decimales solo para mostrar; por eso al repetir la aritmética con los valores redondeados que se ven, algunos resultados difieren en el segundo decimal (salvedad 11).

| Paso | Cálculo | Valor exacto | Lo que muestra la clave | Observación |
|---|---|---|---|---|
| 1. Medias | x̄ = 33 / 6 · ȳ = 407 / 6 | 5.5 · 67.8333 | 5.5 · 67.83 | La suma de las desviaciones es 0 |
| 2. Sumas | Sxy · Sxx · Syy | 194.5 · 37.5 · 1 040.833 | 194.5 · 37.5 · 1 040.83 | ✅ |
| 3. Correlación | r = Sxy / √(Sxx · Syy) | 0.98449 | 0.98 | Relación lineal muy fuerte |
| 4. Pendiente e intercepto | b1 = Sxy / Sxx · b0 = ȳ − b1·x̄ | 5.18667 · 39.3067 | 5.19 · 39.31 | Cada hora adicional ≈ 5.19 puntos |
| 5. R² | r² | **0.96923** | «0.98² ≈ 0.9692» | 0.98² = 0.9604; con el r completo sí da 0.9692 (96.9 %) |
| 6. Predicciones | X = 7 · X = 10 | 75.613 · 91.173 | 75.61 · 91.17 | Con los coeficientes redondeados (39.31 + 5.19·X) saldría 75.64 y 91.21 |
| 7. Residuos | Y − Ŷ | −1.68, +3.13, −2.24, +1.57, −2.80, +2.01 (suma ≈ 0) | Igual | ✅ |
| 8. SSE y MSE | Σ residuos² · SSE / (n − 2) | 32.0267 · 8.0067 (error estándar residual 2.83) | 32.03 · 8.01 | La suma de los sumandos que se muestran (2.82 + 9.80 + 5.02 + 2.46 + 7.84 + 4.04) da 31.98 |
| 9. Error estándar y t | SE(b1) = √(MSE / Sxx) · t = b1 / SE(b1) | 0.46207 · **11.225** | 0.46 · 11.23 | gl = 4, p = 3.6e-4 |
| 10. Decisión | t contra el crítico 2.776 (gl = 4, α = 0.05) | 11.22 > 2.776 | Se rechaza H0 | IC 95 % de β1: [3.90; 6.47]. Equivale al test de r: r crítico con n = 6 es 0.811 |
| 11. Extrapolación | IC de la media y IP | X = 7: IP [66.91; 84.31] · X = 10: IC [84.57; 97.78], **IP [80.91; 101.44]** | «X = 10 es una extrapolación» | El IP ya sobrepasa 100, el máximo de la nota |

```python
import numpy as np
import statsmodels.api as sm
from scipy import stats

X = np.array([2, 3, 5, 6, 8, 9.0])
Y = np.array([48, 58, 63, 72, 78, 88.0])
n = len(X)
dx, dy = X - X.mean(), Y - Y.mean()
Sxy, Sxx, Syy = (dx * dy).sum(), (dx ** 2).sum(), (dy ** 2).sum()
r = Sxy / np.sqrt(Sxx * Syy)
b1 = Sxy / Sxx
b0 = Y.mean() - b1 * X.mean()
res = Y - (b0 + b1 * X)
sse = (res ** 2).sum()
se = np.sqrt(sse / (n - 2) / Sxx)
t = b1 / se
print(Sxy, Sxx, Syy, r, r ** 2, b1, b0)
print(sse, sse / (n - 2), se, t, 2 * stats.t.sf(t, n - 2), stats.t.ppf(0.975, n - 2))
modelo = sm.OLS(Y, sm.add_constant(X)).fit()
print(modelo.conf_int()[1])
print(modelo.get_prediction(np.array([[1, 7], [1, 10]])).summary_frame(alpha=0.05).round(2))
```

---

## 9. Un solo script para el `Promt.md`

El prompt de `Profesor/Promt.md` pide: (1) cargar y explorar el dataset con pandas, (2) aplicar al menos dos pruebas inferenciales relevantes (t-test y ANOVA como ejemplo), (3) comentarios en cada bloque y (4) interpretaciones breves en español. Este script lo cumple y añade la regresión, que une las dos pruebas (secciones 7.1 y 7.3).

```python
# --- 1) Cargar y explorar --------------------------------------------------
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

df = pd.read_csv("StudentsPerformance.csv")           # 1 000 estudiantes
print("Filas y columnas:", df.shape)
print("Nulos:", df.isnull().sum().sum(), "| Duplicados:", df.duplicated().sum())
print(df[["math score", "reading score", "writing score"]].describe().round(2))
print(df[["math score", "reading score", "writing score"]].corr().round(3))

# --- 2) Prueba t: ¿difiere la nota de escritura entre hombres y mujeres? ---
h = df.loc[df["gender"] == "male", "writing score"]
m = df.loc[df["gender"] == "female", "writing score"]
lev = stats.levene(h, m)                               # ¿varianzas parecidas?
t = stats.ttest_ind(h, m, equal_var=lev.pvalue >= 0.05)  # Student si Levene no rechaza, Welch si rechaza
print(f"Levene p = {lev.pvalue:.3f} | t = {t.statistic:.2f}, p = {t.pvalue:.2e}")
print("Interpretación:", "las notas de escritura SÍ difieren entre géneros (p < 0.05)."
      if t.pvalue < 0.05 else "no hay evidencia de diferencia entre géneros.")

# --- 3) ANOVA: ¿difiere la nota de matemáticas entre los 5 grupos de etnia? -
grupos = [g["math score"] for _, g in df.groupby("race/ethnicity")]
f = stats.f_oneway(*grupos)
print(f"ANOVA: F = {f.statistic:.2f}, p = {f.pvalue:.2e}")
print("Interpretación:", "al menos un grupo tiene un promedio distinto (p < 0.05)."
      if f.pvalue < 0.05 else "no hay evidencia de que los promedios difieran.")

# --- 4) Regresión lineal: ¿cuánto sube escritura por cada punto de lectura? -
ols = smf.ols("Q('writing score') ~ Q('reading score')", df).fit()
b0, b1 = ols.params
print(f"writing = {b0:.4f} + {b1:.4f} * reading | R² = {ols.rsquared:.4f}")
print("IC 95 % de la pendiente:", ols.conf_int().iloc[1].round(3).tolist())
print(f"Interpretación: cada punto de lectura se asocia con {b1:.2f} puntos más de escritura; "
      f"el modelo explica el {ols.rsquared:.1%} de la variación (asociación, no causalidad).")
```

---

## 10. Cuándo usar (y cuándo no) la regresión lineal: las evidencias de `02`

| Criterio de `02` | Qué dice | Evidencia recalculada | Lectura |
|---|---|---|---|
| 1.1 ¿Y es numérica? | Para sí/no hay que usar clasificación | `writing` ≥ 60 (719 sí, 281 no) con un modelo lineal sobre `reading` y `math`: **231 de las 1 000 predicciones caen fuera de [0, 1]** (19 menores que 0 y 212 mayores que 1; rango −0.51 a 1.44). Una logística con `math` da probabilidades entre 0.0001 y 0.9994 (84.2 % de aciertos con umbral 0.5) | Confirma el Ejercicio 6b del Taller 2. Es el punto de partida del debate y de la Semana 8 |
| 1.2 ¿Las X son numéricas? | Las categóricas se convierten en dummies | Género 1 columna, etnia 4, educación 5, almuerzo 1, curso 1 (12 en total con las cinco) | Una categórica de 2 niveles es barata; una de 6, cinco columnas |
| 1.3 ¿Pocas variables / pocos niveles? | Muchas columnas aumentan el riesgo de sobreajuste | Las cuatro categóricas del Ejercicio 1c, solas, dan R² = 0.235 (ajustado 0.226, validación cruzada 0.207, RMSE 13.5). Sumar las cinco categóricas a `reading` y `math` sube el R² de validación de 0.910 a **0.9455** | Con n = 1 000 y 14 columnas (≈ 71 estudiantes por columna) no hay sobreajuste. Sí lo hay con n = 30: R² 0.990 en entrenamiento y 0.738 en prueba (solo `reading`: 0.915 y 0.864) |
| 2.1 Empezar simple | La regresión lineal es la línea base | R² de validación 0.910 con una sola variable | Cumple: el modelo simple ya es casi todo |
| 2.2 Reducir variables | `math` sube el R² de 0.9113 a 0.913 (poco) | ΔR² = 0.0015, pero significativo (p = 4.1e-5). Curso sube 0.0072 con una sola columna | El criterio correcto es el ΔR² de validación, no "cuántas columnas" (salvedad 9) |
| 2.3 Multicolinealidad | `reading` y `writing` correlacionan 0.95 | VIF = 11.3: el error estándar del coeficiente de `reading` se multiplica por 3.3 (√VIF); el coeficiente baja de 0.849 a 0.601 | Cierto, aunque ningún coeficiente cambia de signo (sección 6.3) |
| 2.4 No extrapolar | Predecir solo dentro de 17 a 100 | `reading` = 100 → 98.69, IP hasta 107.60; 150 → 148.36; −5 → −5.64 (Ejercicio 2b de `02`); `reading` = 0 → −0.67 | Todas absurdas fuera del rango o en los bordes. 14 estudiantes ya tienen `writing` = 100 |

---

## 11. Salvedades que conviene conocer

1. **La Semana 7 no tiene actividad calificada.** La presentación dice «(No hay actividad)» y propone un debate de regresión lineal vs. logística. Los materiales (talleres y notebook `03`) son de práctica en clase; este cuadro sirve para esa práctica, no para un portafolio. Además, `Promt.md` habla de «regresión lineal» pero lista t-test y ANOVA: están cubiertos porque son casos particulares de la regresión (secciones 7 y 9).
2. **Redondeo que cambia el resultado en `01`, Ejercicio 3b.** Con `b0 = −0.67` y `b1 = 0.99`, `−0.67 + 0.99 × 80 = 78.53`, no 78.8. La clave de `01` dice «aproximadamente 78.8 puntos (el cálculo exacto con los coeficientes completos da 78.81)»: el 0.28 de diferencia sale de redondear `b1` a dos decimales y multiplicar por 80. Con `b1 = 0.9935` da 78.81 (Taller 2, Ejercicio 3).
3. **Signo del estadístico t en la dummy.** `01` §5 y Taller 2 (Ejercicio 7) definen `t = (ȳ_mujeres − ȳ_hombres) / SE ≈ −9.98`, pero esa resta da **+9.98**. El código `stats.ttest_ind(hombres, mujeres)` da −9.98 porque resta *hombres − mujeres*, y la clave del Ejercicio 7b dice lo contrario («el t-test resta mujeres − hombres»). La regresión con `mujer = 1` da +9.98 (b1 = +9.156). Solo cambia el signo; el p es el mismo (2.02e-22).
4. **Normalidad de residuos: la clave del Taller 2, Ejercicio 5b, mezcla dos modelos.** El Shapiro p = 0.0368 es del modelo *simple*, pero la «asimetría ≈ 0.087 y curtosis ≈ 2.90» que lo matizan son del modelo *múltiple* del Ejercicio 4 (en el simple: 0.092 y 2.871). En el modelo múltiple Shapiro da p = 0.680, y en el simple D'Agostino (0.362) y Jarque-Bera (0.351) no rechazan. La conclusión de la clave («desviación leve») es correcta, pero conviene citar el modelo de cada cifra.
5. **«p = 0» y «≈ 10⁻³⁰⁰».** `linregress` imprime `pvalue = 0.0` porque el valor real (3.5e-527, calculado con precisión arbitraria) está por debajo del mínimo de un número de coma flotante (≈ 1e-308). La clave del Ejercicio 2 lo explica bien; en el informe conviene escribir «p < 1e-300» y no «p = 0». En la tabla del `summary()` de statsmodels, «0.000» significa «menor que 0.0005».
6. **RMSE no es el «error promedio».** Las diapositivas dicen que el modelo «se equivoca, en promedio, por unos 4.5 puntos»: eso es el RMSE (4.52); el error absoluto *promedio* es el MAE (3.61); la relación 1.25 es la de una distribución normal. `01` llama al RMSE «error estándar de los residuos», pero este usa n y el error estándar residual usa n − 2: 4.524 frente a 4.529 (sin efecto con n = 1 000).
7. **La clave del notebook `03` tiene comentarios que no coinciden con sus propias salidas.** (a) Ejercicio 3a: «b1 ≈ 0.99, b0 ≈ −0.6», pero la salida es 0.9971 y −0.8960. (b) Ejercicio 5b: «RMSE ≈ 4.5», pero la salida es 4.8857 (4.5 es el RMSE de los 1 000 completos). (c) Ejercicio 6b: habla de un residuo de +25, que no existe; el mayor es +15.07. (d) Ejercicio 7a: «de ≈ 0.91 a ≈ 0.91–0.92», pero lo que sale es 0.9010 → 0.9018 en prueba. Las conclusiones cualitativas sí son correctas.
8. **Una sola partición no sirve para comparar modelos.** La diferencia de 0.0008 entre 0.9010 (simple) y 0.9018 (con `math`) en el notebook `03` es unas 14 veces menor que lo que varía el propio R² de prueba entre particiones (desviación 0.011; rango 0.864 a 0.939). La semilla 42 cae en el percentil 20. La conclusión de la clave («mejora muy poco») es correcta por otra vía: la diferencia pareada media es 0.0013 (desviación 0.0015) y la validación cruzada da 0.9100 contra 0.9113.
9. **«Significativo» no es «útil», y «reducir variables» depende del tamaño de muestra.** `math` es significativo (F anidada p = 4.1e-5; AIC y BIC lo prefieren) pero suma 0.0015 de R² y baja 0.03 puntos de RMSE. `02` (§1.3 y §2.2) justifica reducir variables con el riesgo de sobreajuste, pero con 1 000 estudiantes y 14 columnas el R² de validación sube de 0.910 a 0.9455 al sumar las categóricas, y la variable más rentable es el curso (+0.0072 con una columna), no `math`. El sobreajuste real aparece con n pequeño (n = 30: 0.990 frente a 0.738), de modo que la regla debe expresarse como estudiantes por predictora y validación, no como un número fijo de columnas.
10. **Multicolinealidad: el umbral y el alcance de la advertencia.** `02` §2.3 y su Ejercicio 2a tratan la correlación de 0.82 entre `reading` y `math` como señal de alerta; su VIF es 3.0 (moderado, bajo el umbral común de 5) y el coeficiente de `reading` apenas se mueve (0.9935 → 0.9366). El caso realmente colineal es `reading`–`writing` (r = 0.95, VIF = 11.3). Tampoco es cierto en estos datos que los coeficientes «puedan cambiar de signo»: en 2 000 remuestreos del modelo colineal ninguno fue negativo; lo que crece es el error estándar (×3.3).
11. **Taller 1: la aritmética con los números redondeados que se muestran no reproduce los resultados.** (a) «R² = r² = 0.98² ≈ 0.9692»: 0.98² es 0.9604; el r completo (0.98449) da 0.9692. Un estudiante que siga la cuenta literal obtiene 96.0 %, no 96.9 %. (b) 39.31 + 5.19 × 7 = 75.64 y 39.31 + 5.19 × 10 = 91.21, no 75.61 y 91.17. (c) Los seis sumandos de SSE que se muestran suman 31.98, no 32.03. (d) El t exacto es 11.22, no 11.23. (e) La nota pedagógica del Ejercicio 6 («con muestras pequeñas el valor crítico es más exigente (más grados de libertad libres = menos)») es confusa: con pocos grados de libertad el valor crítico de t es *mayor* (2.776 con gl = 4 frente a 1.96 con gl infinitos). Conviene pedir a los estudiantes 4 decimales en los pasos intermedios. (f) Con n = 6 no se pueden revisar los supuestos (Shapiro de los residuos: p = 0.250, sin potencia), y la predicción para 10 horas tiene un intervalo de predicción hasta 101.44, por encima de la nota máxima.
12. **La recta no es simétrica ni causal.** La regresión de `reading` sobre `writing` tiene pendiente 0.917, no 1 / 0.9935 = 1.007; solo coinciden si r = 1. La pendiente 0.9935 es casi 1 (p = 0.510 contra β1 = 1), pero la recta no es la identidad: el intercepto y la pendiente juntos rechazan b0 = 0 y b1 = 1 (F conjunta p = 1.4e-13) porque `writing` está 1.1 puntos por debajo de `reading` en promedio.
13. **Dos flujos distintos en las diapositivas y en la guía.** La presentación (diapositiva 19) lista recolección, limpieza, división en entrenamiento y prueba, entrenamiento, evaluación, *ajuste de hiperparámetros* e implementación; `01` lista siete pasos de inferencia sin división de datos. El notebook `03` es el puente. Con mínimos cuadrados ordinarios (`LinearRegression`) no hay hiperparámetros que ajustar: ese paso aplicaría a variantes como Ridge o Lasso.
14. **Referencias y enlaces que fallan.** (a) `02` §1.2 cita «el Ejercicio 7 de `01_...md`», pero `01` solo tiene 6 ejercicios: la dummy está en su «Ejemplo aplicado» (§5) y en el Ejercicio 7 de los talleres. (b) El notebook de estudiante `Taller_02_Regresion_lineal_conceptos_basicos.ipynb` termina con un enlace a la clave `..._profesor.ipynb`, que está ignorada por Git: el enlace falla en GitHub y apunta a las respuestas. (c) Los materiales dicen «NRC 94103», la presentación del profesor «NRC 8683» y la carpeta del repositorio es `NRC-70446`: hay que confirmar cuál va en los entregables. (d) El recurso interactivo de la Semana 7 vive en un repositorio aparte (GitHub Pages) y este cuadro no lo revisó.
15. **Datos acotados entre 0 y 100.** Un modelo lineal no conoce los topes: con `reading` = 100 predice 98.69 y su intervalo de predicción llega a 107.60. Hay 14 estudiantes con `writing` = 100, 17 con `reading` = 100 y 1 con `math` = 0. La regresión lineal es una buena aproximación en el centro de la escala, no en los bordes.
