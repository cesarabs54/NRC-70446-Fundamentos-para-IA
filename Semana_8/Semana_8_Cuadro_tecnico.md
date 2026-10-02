# Semana 8 — Cuadro técnico consolidado

**Tema:** Estadística inferencial III: regresión logística. De predecir un número a predecir una categoría: variable respuesta binaria (`aprueba_mate` = 1 si `math score >= 60`), predictor lineal `z = b0 + b1·X` (el *logit*), función sigmoide, ajuste por máxima verosimilitud, prueba de Wald y prueba chi-cuadrado del modelo, razón de momios (*odds ratio*), umbral de decisión, matriz de confusión (exactitud, precisión, sensibilidad), colinealidad con dos predictoras y comparación con la regresión lineal.
**Dataset de la semana:** `StudentsPerformance.csv` — idéntico byte a byte al de las Semanas 6 y 7 (1 000 estudiantes × 8 columnas, sin nulos y sin duplicados). Se crea `aprueba_mate`: 677 aprueban (67.7 %) y 323 no. Predictor del caso guía: `reading score` (media 69.17, s = 14.60, rango 17 a 100). Otros conjuntos de la semana: el ejemplo de la enfermedad de las diapositivas (36 personas, tabla de clasificación 11 / 5 / 5 / 15, sin datos), el caso de «riesgo de deserción» del quiz de Canvas (sin datos) y `Taller_regresion_logistica_calculos.xlsx` (6 hojas con las fórmulas del taller en papel).
**Actividad calificada:** «MA Evaluación 8» en Canvas: una presentación de 18 diapositivas seguida de 5 preguntas (opción múltiple, verdadero / falso, completar espacios, arrastrar palabras y marcar palabras entre «estadística» y «aprendizaje automático»). Todo lo demás es práctica previa: el taller en papel (`02`), el taller en Python (`03`), el refuerzo de `Evaluacion/` y el debate de `04` (regresión lineal vs. logística, que la Semana 7 dejó anunciado). La clave de la evaluación habla de 4 criterios de «Revisión», pero no hay un enunciado oficial ni rúbrica en el repositorio. No existe un `Promt.md` para esta semana.

> Todas las cifras de este documento se recalcularon ejecutando el código sobre el CSV del repositorio (Python 3.11.9 con SciPy 1.17.1, pandas 3.0.6, NumPy 2.4.6, statsmodels 0.15.0 y scikit-learn 1.9.1; semilla fija donde hubo remuestreo). Las marcadas con ✅ ya aparecen en los materiales (guías `01` y `04`, talleres `02` y `03` con sus claves, refuerzo de `Evaluacion/`, notebooks de `Matematicas/`, diapositivas o Excel); las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en ellos. Cuando una cifra solo aparece en la salida de `summary()` sin comentario, se indica «(salida sin comentar)».
>
> **Archivos ignorados por Git que se usaron** (`*profesor*` está en `.gitignore`, así que son solo locales): `02_Taller_regresion_logistica_profesor.md`, `03_Taller_regresion_logistica_profesor.md` y `.ipynb`, y en `Evaluacion/`: `02_Evaluacion_desarrollo_profesor.md`, `02_Evaluacion_taller_profesor.ipynb`, `02_Evaluacion_8_clave_respuestas_profesor.md` y `Semana_8_Evaluacion_profesor.docx` (tarjetas de la evaluación: solo transcriben las preguntas 1, 2 y 5). Las diapositivas `00_Regresion_Logistica_Diapositivas.pptx` no están ignoradas.

---

## 1. Procedimientos de la semana (de punta a punta)

Siguen los 7 pasos de `01` §5 (explorar, plantear, ajustar, evaluar coeficientes, elegir umbral y clasificar, evaluar el clasificador, predecir). Los marcados con (➕) no están en los materiales.

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la semana |
|---|---|---|---|---|
| Carga y calidad | Pandas | `read_csv`, `shape`, `isnull().sum()`, `duplicated().sum()` | Conocer el archivo antes de modelar | 1 000 × 8, 0 nulos, 0 duplicados. `reading` media 69.17 (s = 14.60) |
| Crear la variable binaria | Pandas | `(df["math score"] >= 60).astype(int)` | Convertir una nota en un sí / no | 677 aprueban (67.7 %) y 323 no. El 60 es una decisión del taller (salvedad 9) |
| ¿La logística es la herramienta? | — | Y binaria → logística; Y numérica → lineal (`01` §6, `04` §1) | Elegir el modelo según el tipo de Y | Una recta sobre 0 / 1 predice fuera de [0, 1] para 165 de los 1 000 estudiantes (sección 12) |
| Descriptiva por grupo | Pandas / Matplotlib | `groupby("aprueba_mate")["reading score"].describe()`, `boxplot(by=...)` | Ver si `reading` separa a los dos grupos | Aprueban: media 75.64, mediana 75 · No aprueban: 55.61, mediana 56. Las cajas se solapan (42 a 85) |
| Contraste sin modelo (➕) | SciPy | `ttest_ind(equal_var=False)`, `mannwhitneyu` | Hacer la pregunta de otra forma | Welch t = 26.48, gl = 637, p = 9.1e-105 · Mann-Whitney p = 3.1e-93 · el AUC de `reading` sola es U / (n1·n0) = 0.8999 |
| Hipótesis | — | H0: β1 = 0 · H1: β1 ≠ 0 | Decidir si la variable ayuda a clasificar | β1 es el coeficiente *poblacional* del logit |
| Ajuste por máxima verosimilitud | statsmodels / scikit-learn | `sm.Logit(y, add_constant(x)).fit()`, `LogisticRegression().fit` | Hallar b0 y b1 que hacen más creíbles los datos (no hay fórmula cerrada) | b0 = −10.2254, b1 = 0.1672 (7 iteraciones). scikit-learn por defecto (C = 1): −10.2241 y 0.16719; con `penalty=None` coincide con statsmodels |
| Prueba de Wald | statsmodels | `tvalues`, `pvalues`, `conf_int()` | Contrastar cada coeficiente | z = 15.334, p = 4.5e-53 (el `summary()` imprime 0.000). IC 95 % de b1 [0.1458; 0.1886] |
| Razón de momios | NumPy | `np.exp(b1)`, `np.exp(conf_int())` | Traducir b1 a «cuántas veces se multiplican los momios» | OR = 1.1820, IC 95 % [1.157; 1.208]. Por 5 puntos 2.31 · por 10 puntos 5.32 |
| Modelo completo contra el nulo | statsmodels | `llr`, `llr_pvalue`, `prsquared`, `aic`, `bic` | Es la prueba chi-cuadrado de las diapositivas: ¿el modelo aporta algo? | χ² = 524.46, gl = 1, p = 4.5e-116 · pseudo R² de McFadden 0.4168 · AIC 737.76 · BIC 747.58 |
| De z a probabilidad | NumPy | `z = b0 + b1*x` y `1 / (1 + np.exp(-z))` | Calcular la probabilidad de aprobar | `reading` 40 → 2.8 % · 50 → 13.4 % · 60 → 45.2 % · 70 → 81.4 % · 80 → 95.9 % · 90 → 99.2 % |
| Punto de corte | NumPy | `-b0 / b1` | `reading` donde P = 0.5 | 61.15 (a mano con los coeficientes redondeados, 61.157): de 62 en adelante se clasifica «aprueba» |
| Umbral y decisión | NumPy | `(p >= 0.5).astype(int)` | Pasar de probabilidad a sí / no | Con t = 0.5 es lo mismo que la regla `reading ≥ 62`: las mismas 168 equivocaciones |
| Matriz de confusión y métricas | scikit-learn | `confusion_matrix`, `accuracy_score`, `precision_score`, `recall_score` | Evaluar el clasificador | [[227, 96], [72, 605]] · exactitud 0.832 · precisión 0.863 · sensibilidad 0.894 |
| Línea base | Pandas | `y.mean()` | Comparar con el modelo «tonto» que siempre dice «aprueba» | 0.677: el modelo gana 15.5 puntos de exactitud |
| Otras métricas (➕) | scikit-learn | `f1_score`, `balanced_accuracy_score`, `matthews_corrcoef` | Mirar los dos tipos de error a la vez | Especificidad 0.703 · F1 0.878 · exactitud balanceada 0.798 · MCC 0.609 · kappa 0.608 |
| Cambiar el umbral | NumPy | Barrido de t de 0.3 a 0.9 | Ver cómo se intercambian precisión y sensibilidad | t = 0.8: precisión 0.930, sensibilidad 0.705, exactitud 0.764 (sección 6.2) |
| Discriminación y calidad de la probabilidad (➕) | scikit-learn | `roc_auc_score`, `brier_score_loss`, `log_loss` | Medir sin depender de un umbral | AUC 0.8999 · Brier 0.1181 (base 0.2187) · log-loss 0.3669 (base 0.6291) |
| Calibración (➕) | SciPy / Pandas | Tasa real por tramo, Hosmer-Lemeshow | ¿Las probabilidades se parecen a las frecuencias? | χ² = 6.89, gl = 8, p = 0.549 (no rechaza) |
| Entrenamiento y prueba (➕) | scikit-learn | `train_test_split`, `cross_validate(RepeatedStratifiedKFold)` | Evaluar con estudiantes que el modelo no vio | 80 / 20 con semilla 42: exactitud de prueba 0.835 · 5 × 20 pliegues: 0.8307 y AUC 0.8998 |
| Segunda predictora y colinealidad | statsmodels | `sm.Logit` con dos columnas, `variance_inflation_factor` | Ver qué pasa con variables muy correlacionadas | `reading` + `writing`: b de `reading` baja de 0.1672 a 0.1280 y su error estándar se duplica (×2.03). VIF 11.27 |
| Categóricas como *dummies* | Pandas / statsmodels | `(df["gender"] == "female").astype(int)` | Meter columnas de texto al modelo | `reading` + género + curso: exactitud 0.883, AUC 0.9476; OR de género (mujer) 0.033 |
| Predicción | NumPy / statsmodels | `sigmoide(b0 + b1*x)`, `get_prediction` (➕ el intervalo) | Estimar la probabilidad de un estudiante nuevo | `reading` = 65 → 65.5 % (IC 95 % [61.3; 69.6]) → «aprueba» |
| Interpretación | — | OR + IC + exactitud frente a la línea base + advertencia de causalidad | Redactar la conclusión | «Asociado con», no «causa»; solo dentro del rango observado (17 a 100) |

---

## 2. Qué gráfico usar (Matplotlib / Seaborn)

| Pregunta | Gráfico (función) | Ejemplo con el dataset | Cuidado al leerlo | Uso |
|---|---|---|---|---|
| ¿`reading` separa a los dos grupos? | Boxplot por grupo · `df.boxplot(column="reading score", by="aprueba_mate")` | Mediana 75 (aprueban) contra 56 (no aprueban), con las cajas solapadas | No muestra el tamaño de cada grupo (677 contra 323) | ✅ |
| ¿Qué forma tiene la relación? | Dispersión 0 / 1 con la curva · `plt.scatter(x, y, alpha=0.15)` + `plt.plot(x_rango, p_rango)` | S casi plana en 40 (2.8 %), empinada entre 50 y 75 (de 13 % a 91 %) y casi plana desde 80 (más de 95 %); cruza 0.5 en 61.15 | Los puntos solo existen en 0 y 1: la curva es la probabilidad estimada, no un promedio de los datos | ✅ |
| ¿Cómo se ve la sigmoide en abstracto? | `plt.plot(zs, sigmoide(zs))` con z de −6 a 6 | Cruza 0.5 en z = 0; vale 0.0025 en z = −6 y 0.9975 en z = 6 | El eje horizontal es z (el logit), no una nota | ✅ |
| ¿Cuánto cambia la probabilidad por punto de `reading`? | Curva de P y su pendiente, `P·(1−P)·b1` | +0.5 puntos porcentuales entre 40 y 41; **+4.2** entre 60 y 61; el máximo, b1 / 4 = 4.18, está en el punto de corte | El OR es constante; el efecto en probabilidad no (salvedad 4) | ✅ (la idea; las cifras de la clave tienen un error) |
| ¿Cuántos aciertos y errores de cada tipo? | Matriz de confusión · `ConfusionMatrixDisplay(matriz).plot()` | 227 · 96 · 72 · 605 | Filas = lo real, columnas = lo predicho; el positivo es «aprueba» | ✅ |
| ¿Dónde se equivoca? | Histograma de `reading` de los mal clasificados | 168 errores: 108 con `reading` entre 55 y 67. Falsos positivos: 62 a 85 (media 68.0). Falsos negativos: 42 a 61 (media 56.4) | Con una sola predictora el error es de frontera: se pega al punto de corte (la clave lo propone como verificación opcional) | ✅ / ➕ |
| ¿Las probabilidades son creíbles? | Calibración: tasa real contra probabilidad media por tramo · `groupby(pd.cut(...))` | 60–64: real 57.1 %, modelo 54.1 % · 70 o más: 93.0 % y 93.7 % | Con pocos estudiantes por tramo el cociente es ruidoso | ➕ |
| ¿Qué pasa al mover el umbral? | Precisión, sensibilidad y especificidad contra t | t = 0.5: 0.863 / 0.894 / 0.703 · t = 0.8: 0.930 / 0.705 / 0.889 | La clave lo afirma, pero ningún notebook lo calcula (salvedad 7) | ➕ |
| ¿Qué tan bien separa sin fijar umbral? | Curva ROC · `roc_curve`, `roc_auc_score` | AUC 0.8999; el umbral de Youden es 0.692 | Con clases desbalanceadas conviene mirar también la precisión | ➕ |
| ¿Cómo desplaza una *dummy* la curva? | Dos sigmoides (hombre y mujer) con las demás variables fijas | Con `reading` = 65 y sin curso: 93.6 % (hombre) contra 32.4 % (mujer) | La *dummy* desplaza la S, no cambia su forma | ✅ |
| ¿Cuánto varía un coeficiente al remuestrear? | Histograma del coeficiente en 1 000 bootstraps | `reading`: desviación 0.0106 (sola) y 0.0240 (con `writing`); el de `writing` es negativo en el 3.1 % de las muestras | Se ve la colinealidad: los dos coeficientes se compensan (correlación −0.90) | ➕ |
| ¿Qué variables se parecen? | Matriz de correlación · `df[[...]].corr()` | `math`–`reading` 0.82 · `math`–`writing` 0.80 · `reading`–`writing` **0.95** | Correlación alta entre predictoras = posible colinealidad | ✅ |

---

## 3. Pruebas y funciones que se pueden aplicar (statsmodels / scikit-learn / SciPy)

### 3.1 Cuadro de herramientas

| Pregunta | Función | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Cuál es el modelo? | **Logit** · `sm.Logit(y, X).fit()` | Y con valores 0 / 1; máxima verosimilitud por iteraciones (Newton). No converge si una variable separa perfectamente | b0 = −10.2254, b1 = 0.1672, 7 iteraciones | ✅ |
| ¿Lo mismo con scikit-learn? | `LogisticRegression().fit(X, y)` | Aplica una penalización L2 (C = 1) por defecto; `penalty=None` la quita | C = 1: −10.2241 y 0.16719 · sin penalización: −10.2254 y 0.16721, idéntico a statsmodels | ✅ (la diferencia está comentada en el notebook) |
| ¿El coeficiente es distinto de cero? | **Wald** · `tvalues`, `pvalues` | Muestras grandes; poco fiable si hay casi separación | z = 15.334, p = 4.5e-53 (en el `summary()`, «0.000») | ✅ |
| ¿Cuánto vale el coeficiente? | IC de b1 · `conf_int()` · bootstrap | El de Wald supone normalidad asintótica; el bootstrap no | Wald [0.1458; 0.1886] · bootstrap (1 000 remuestreos) [0.1487; 0.1891] | ✅ (Wald) / ➕ (bootstrap) |
| ¿Cuántas veces se multiplican los momios? | **Razón de momios** · `np.exp(b1)` | Es multiplicativa y constante; el cambio en probabilidad no | 1.1820 [1.157; 1.208] · por 5 puntos 2.31 · por 10 puntos 5.32 · por una desviación (14.6 puntos) 11.49 | ✅ (OR) / ➕ (IC y escalas) |
| ¿El modelo es mejor que no tener variables? | **Razón de verosimilitud** · `llr`, `llr_pvalue` | Modelos anidados: 2·(ll − ll nula) sigue una chi-cuadrado | 524.46, gl = 1, p = 4.5e-116. El z² de Wald vale 235.13: son pruebas distintas | ✅ (p en la nota del profesor; chi-cuadrado en la diapositiva 23) |
| ¿Cuánto explica? | **Pseudo R²** · `prsquared` | McFadden = 1 − ll / ll nula; no se lee como el R² lineal (McFadden considera «excelente» 0.2 a 0.4) | 0.4168 (Cox-Snell 0.408; Nagelkerke 0.570) | ✅ salida sin comentar (McFadden) / ➕ (otros) |
| ¿Qué modelo es mejor? | **AIC / BIC** · `aic`, `bic` | Menor es mejor; BIC penaliza más las variables extra | `reading`: 737.76 / 747.58 · + `writing`: 735.75 / 750.48 · + género y curso: 550.24 / 569.87 | ➕ |
| ¿Una variable extra mejora de verdad? | **Razón de verosimilitud entre modelos** · `2 * (m2.llf - m1.llf)` | Modelos anidados | + `writing`: χ² = 4.006, gl = 1, p = 0.0453 (el Wald de `writing` da 0.047) · + género y curso: χ² = 191.52, gl = 2, p = 2.6e-42 | ➕ |
| ¿Clasificó bien? | **Matriz de confusión** · `confusion_matrix(y, pred)` | Con t = 0.5; filas = real, columnas = predicho | 227 · 96 · 72 · 605 | ✅ |
| ¿Cuánto acierta? | **Exactitud, precisión, sensibilidad** · `accuracy_score`, `precision_score`, `recall_score` | Dependen del umbral y de qué clase es la positiva | 0.832 · 0.863 · 0.894 | ✅ |
| ¿Y la clase negativa? | **Especificidad, valor predictivo negativo, F1** | Con «no aprueba» como positiva: sensibilidad = 0.703 y precisión = 0.759 | Especificidad 0.703 · VPN 0.759 · F1 0.878 | ➕ |
| ¿Mejor que adivinar? | **Línea base** · `y.mean()` | Siempre comparar con predecir la clase más frecuente | 0.677; el modelo gana 15.5 puntos. Con el punto de corte en 50 la línea base sube a 0.865 (salvedad 9) | ✅ |
| ¿Qué umbral usar? | Barrido · `roc_curve` · índice de Youden | Depende del costo de cada error | Mayor exactitud con t = 0.42 (0.833) · Youden t = 0.692 (sensibilidad 0.814, 1 − especificidad 0.176) | ➕ |
| ¿Cuánto separa, sin umbral? | **AUC** · `roc_auc_score` | Probabilidad de que un aprobado reciba más P que un reprobado | 0.8999 (= U / (n1·n0) de Mann-Whitney) | ➕ |
| ¿Las probabilidades son verosímiles? | **Brier**, **log-loss**, **Hosmer-Lemeshow** | HL depende de cómo se agrupa y pierde potencia con pocos datos | Brier 0.1181 · log-loss 0.3669 · HL χ² = 6.89, p = 0.549 | ➕ |
| ¿El logit es lineal en `reading`? | Término cuadrático · razón de verosimilitud | Si el cuadrado no aporta, la forma lineal basta | Coeficiente de `reading²` 0.00076, p = 0.358 | ➕ |
| ¿Alguna fila pesa demasiado? | **Distancia de Cook** · `get_influence().cooks_distance` | Regla práctica: Cook > 4/n merece mirarse | Máximo 0.0302; 59 filas con Cook > 4/n; apalancamiento máximo 0.0037 | ➕ |
| ¿Las predictoras se repiten? | **VIF** · `variance_inflation_factor` | VIF > 5 (o 10) es señal de alerta | `reading`–`writing` 11.27 · `reading`, género y curso 1.07 a 1.14 | ➕ |
| ¿Dos grupos difieren en `reading`? | **Welch** · `ttest_ind(equal_var=False)` · **Mann-Whitney** | Opción segura por defecto | t = 26.48, gl = 637, p = 9.1e-105 · Mann-Whitney p = 3.1e-93 | ➕ |
| ¿Dos categóricas se asocian? | **Chi-cuadrado de independencia** · `chi2_contingency` | Frecuencias esperadas ≥ 5 | Género contra aprobar: χ² = 16.14, p = 5.9e-5 · curso: 16.31, p = 5.4e-5 · almuerzo: 72.70, p = 1.5e-17 | ➕ |
| ¿Cómo entra una categórica? | **Dummy** · `get_dummies(drop_first=True)` | k niveles = k − 1 columnas; la que falta es la referencia | Género 1 columna, etnia 4, educación 5, almuerzo 1, curso 1 (12 con las cinco, 11 sin el curso) | ✅ |
| ¿Cómo evalúo con datos no vistos? | **División** · `train_test_split` · **validación cruzada** · `cross_validate(RepeatedStratifiedKFold)` | La estratificación mantiene el 67.7 % en cada parte | Semilla 42, 80 / 20: 0.835 sin estratificar, 0.820 estratificada · 5 × 20 pliegues: 0.8307 | ➕ |
| ¿Cómo busca el óptimo el software? | **Log-verosimilitud** · búsqueda en grilla | Se maximiza Σ [y·ln p + (1 − y)·ln(1 − p)] | Filas 30 a 39: la grilla da b0 = −15, b1 = 0.22 (ll −3.0920); statsmodels −15.72 y 0.230 (ll −3.0893) | ✅ |
| ¿Cuándo no hay óptimo? | **Separación perfecta** · `PerfectSeparationWarning` | Una variable separa las clases sin solapamiento | Primeras 10 filas: no converge (b0 ≈ −587, b1 ≈ 9.5 al cortar en 100 iteraciones) | ✅ (explicado en el notebook) |

### 3.2 Guía rápida para elegir

| Si quiero… | Herramienta | Verificación |
|---|---|---|
| Predecir un sí / no a partir de numéricas | `sm.Logit` o `LogisticRegression` | Matriz de confusión, AUC y validación cruzada |
| Saber si una variable aporta | Wald + razón de verosimilitud | OR con intervalo; ΔAIC; ¿mejora la validación cruzada? |
| Explicar el efecto de una variable | Razón de momios | Dar el OR por unidad **y** por tramo útil (5 o 10 puntos); la probabilidad cambia según la zona |
| Elegir el umbral | Barrido, ROC, Youden | El costo de cada error (falso positivo contra falso negativo) |
| Saber si el clasificador sirve | Exactitud contra la línea base, AUC, kappa | Mejor que 0.677, y con datos de prueba |
| Predecir un número | Regresión lineal (Semana 7) | R², RMSE |
| Más de dos categorías | Regresión multinomial / *softmax* (la menciona `01` §4; no se practica) | — |
| Dos predictoras muy correlacionadas | VIF; dejar una, o combinarlas | Error estándar del coeficiente y estabilidad en bootstrap |
| Comparar dos grupos sin modelar | Welch / Mann-Whitney, chi-cuadrado | Es la pregunta de la Semana 6 |

### 3.3 Cómo revisar los supuestos del modelo (`reading` → aprobar matemáticas)

La regresión logística **no** exige residuos normales ni varianza constante (eso era de la lineal).

| Supuesto | Cómo revisarlo | Resultado | Si falla |
|---|---|---|---|
| Y binaria | `value_counts()` | 677 y 323 | Otro modelo (multinomial si hay 3 o más categorías) |
| Observaciones independientes | Diseño del estudio | Se tratan como independientes, aunque comparten institución o aula | Modelos de efectos mixtos (fuera del alcance) |
| Logit lineal en X | Término cuadrático, tasa real por tramo | `reading²` p = 0.358; la tasa real sigue a la curva en todos los tramos (sección 6.4) | Transformar, agregar un cuadrado o *splines* |
| Sin colinealidad (solo múltiple) | Correlaciones, VIF | `reading`–`writing`: r = 0.955, VIF = 11.27 | Dejar una o combinarlas (sección 7) |
| Sin separación perfecta | Aviso de statsmodels, coeficientes enormes | Con las 1 000 filas converge; con las primeras 10, no | Más datos, quitar la variable o regularizar |
| Suficientes eventos por variable | Clase menos frecuente ÷ variables (regla: al menos 10) | 323 / 1 = 323; con tres predictoras, 108 | Menos variables |
| Sin puntos influyentes | Cook, apalancamiento | Cook máximo 0.0302; ninguna fila preocupante | Ajustar con y sin ellas |
| Probabilidades calibradas | Hosmer-Lemeshow, tasa real por tramo | p = 0.549; diferencias de 3 puntos en el tramo 60–64 | Recalibrar o cambiar el modelo |

Umbrales que usa el material: α = 0.05 y umbral de decisión 0.5. Reglas prácticas del cuadro: VIF > 5 alerta, Cook > 4/n merece revisión, al menos 10 eventos por variable.

---

## 4. Ejemplo guiado 1: `reading` → aprobar matemáticas (modelo simple, taller `03` Ejercicios 1 a 6)

**Pregunta:** ¿ayuda la nota de lectura a saber si un estudiante aprueba matemáticas, y con qué probabilidad?

### 4.1 De los grupos a la predicción

| Paso | Enfoque | Código | Resultado | Lectura |
|---|---|---|---|---|
| 1 | Descriptiva (✅) | `y.value_counts()`, `groupby("aprueba_mate")["reading score"].describe()` | 677 contra 323 · media de `reading` 75.64 (aprueban) y 55.61 (no) · desviaciones 11.22 y 11.16 | Una diferencia de 20 puntos con dispersiones iguales; hay solapamiento |
| 2 | Gráfico (✅) | `df.boxplot(column="reading score", by="aprueba_mate")` | La caja de quienes aprueban está desplazada hacia arriba | Hay señal, pero no separa perfectamente |
| 3 | Contraste previo (➕) | `ttest_ind(equal_var=False)`, `mannwhitneyu` | t = 26.48, p = 9.1e-105 · AUC = 0.8999 | Descriptiva e inferencia sin modelo; el AUC ya anuncia la calidad del clasificador |
| 4 | Hipótesis (✅) | — | H0: β1 = 0 · H1: β1 ≠ 0 · α = 0.05 | β1 es el coeficiente poblacional del logit |
| 5 | Ajuste (✅) | `sm.Logit(y, sm.add_constant(x)).fit()` | b0 = −10.2254 · b1 = 0.1672 · log-verosimilitud −366.88 | Ecuación: `z = −10.2254 + 0.1672·reading` y `P = 1 / (1 + e^(−z))` |
| 6 | Prueba de Wald (✅) | `modelo.tvalues`, `modelo.pvalues` | Error estándar de b1 0.0109 → z = 15.334, p = 4.5e-53. Para b0: z = −14.565 | Se rechaza H0. La relación positiva no es azar |
| 7 | Intervalo (✅ en la evaluación) | `modelo.conf_int()` | b1 en [0.1458; 0.1886] · b0 en [−11.60; −8.85] | El intervalo excluye 0 |
| 8 | Razón de momios (✅) | `np.exp(b1)` | OR = 1.1820, IC [1.157; 1.208] | Cada punto de lectura multiplica los momios por 1.18 (+18.2 %). No son «18 puntos de probabilidad» |
| 9 | Modelo global (✅ sin comentar) | `modelo.llr`, `modelo.prsquared` | LR χ² = 524.46, p = 4.5e-116 · pseudo R² 0.4168 · AIC 737.76 | El modelo supera claramente al que no usa variables |
| 10 | Intercepto (✅) | `np.exp(-b0)` | b0 = −10.23 es el logit con `reading` = 0 → P = 0.0036 % | Sin sentido práctico: el mínimo observado es 17 |
| 11 | Curva sigmoide (✅) | `plt.plot(x_rango, p_rango)` | Cruza P = 0.5 en `−b0 / b1` = 61.15 | A partir de 62 el modelo dice «aprueba» |
| 12 | Probabilidades (✅) | `1 / (1 + np.exp(-z))` | 40 → 2.8 % · 50 → 13.4 % · 60 → 45.2 % · 70 → 81.4 % · 80 → 95.9 % | `z` crece en línea recta; P, no |
| 13 | Clasificar y evaluar (✅) | `confusion_matrix`, `accuracy_score`... | [[227, 96], [72, 605]] · 0.832 · 0.863 · 0.894 | 168 errores (16.8 %). Mejor que la línea base 0.677 |
| 14 | Predicción (✅) | `sigmoide(b0 + b1 * 65)` | 50 → 13.4 % · 65 → 65.5 % · 80 → 95.9 % (con intervalo ➕: [9.9 %; 18.0 %], [61.3 %; 69.6 %], [94.1 %; 97.2 %]) | La incertidumbre mayor está cerca del punto de corte |

**Conclusión:** con α = 0.05 se rechaza H0. `reading score` se asocia con aprobar matemáticas: cada punto extra multiplica los momios por 1.18 (IC 95 % [1.157; 1.208]) y el modelo clasifica bien al 83.2 % (la línea base es 67.7 %). Con una sola predictora, clasificar con t = 0.5 equivale a la regla «`reading` ≥ 62»: los 168 errores son estudiantes cercanos a ese corte (108 con `reading` entre 55 y 67). Es una asociación entre notas del mismo ámbito, no una prueba de que leer mejor *cause* aprobar matemáticas.

### 4.2 Código listo para pegar

```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, recall_score,
                             roc_auc_score, brier_score_loss, log_loss)

df = pd.read_csv("StudentsPerformance.csv")

# 1) Calidad de datos y exploración por grupo
print(df.shape, df.isnull().sum().sum(), df.duplicated().sum())
df["aprueba_mate"] = (df["math score"] >= 60).astype(int)
x, y = df["reading score"], df["aprueba_mate"]
print(y.value_counts().to_dict())
print(df.groupby("aprueba_mate")["reading score"].describe().round(2))
print(stats.ttest_ind(x[y == 1], x[y == 0], equal_var=False), stats.mannwhitneyu(x[y == 1], x[y == 0]))

# 2) Ajuste por máxima verosimilitud (Taller 03, Ejercicio 2)
modelo = sm.Logit(y, sm.add_constant(x)).fit()
print(modelo.summary())
b0, b1 = modelo.params
print("z de Wald:", modelo.tvalues["reading score"], "| p exacto:", modelo.pvalues["reading score"])
print("IC 95 % de b1:", modelo.conf_int().loc["reading score"].tolist())

# 3) Razón de momios y significancia del modelo completo
print("OR:", np.exp(b1), np.exp(modelo.conf_int().loc["reading score"]).tolist())
print("LR chi2:", modelo.llr, "p:", modelo.llr_pvalue, "| pseudo R2:", modelo.prsquared, "| AIC:", modelo.aic, "BIC:", modelo.bic)

# 4) De z a la probabilidad, momios y punto de corte
sigmoide = lambda z: 1 / (1 + np.exp(-z))
for xv in [40, 50, 60, 70, 80, 90]:
    z = b0 + b1 * xv
    print(xv, round(z, 4), round(sigmoide(z), 4), round(sigmoide(z) / (1 - sigmoide(z)), 4))
print("Punto de corte (P = 0.5):", -b0 / b1)

# 5) Clasificar y evaluar
p = modelo.predict(sm.add_constant(x))
pred = (p >= 0.5).astype(int)
print(confusion_matrix(y, pred))
print(accuracy_score(y, pred), precision_score(y, pred), recall_score(y, pred), "| línea base:", y.mean())
print("AUC:", roc_auc_score(y, p), "Brier:", brier_score_loss(y, p), "log-loss:", log_loss(y, p))

# 6) Probabilidad de estudiantes nuevos, con intervalo de confianza
nuevos = pd.DataFrame({"const": 1.0, "reading score": [50, 65, 80]})
print(modelo.get_prediction(nuevos).summary_frame().round(4))
```

---

## 5. Ejemplo guiado 2: el taller en papel (`02`): z, P, momios y matriz con calculadora

**Pregunta:** ¿se obtienen a mano los mismos números que da el software, y cuánto afecta el redondeo?

### 5.1 Tabla del Paso 2 y 3 (`z`, `e^(−z)`, `P`)

El taller usa `b0 = −10.2254` y `b1 = 0.1672` (4 decimales). El valor exacto de `b1` es 0.16721 (5 decimales): la diferencia, multiplicada por `X`, mueve `z` hasta 0.0007 y eso se nota en la 4.ª cifra de `P`.

| `reading` (X) | `z` a mano (4 dec.) | `e^(−z)` | `P` a mano | `z` con el código | `P` con el código | Momios (código) | ¿Aprueba? |
|---|---|---|---|---|---|---|---|
| 40 | −3.5374 | 34.3774 | 0.0283 | −3.5371 | 0.0283 | 0.0291 | No |
| 50 | −1.8654 | 6.4585 | 0.1341 | −1.8650 | 0.1341 | 0.1549 | No |
| 60 | −0.1934 | 1.2134 | 0.4518 | −0.1929 | 0.4519 | 0.8246 | No (queda justo debajo) |
| 61 | −0.0262 | 1.0265 | 0.4935 | −0.0257 | 0.4936 | 0.9746 | No |
| 70 | 1.4786 | 0.2280 | 0.8144 | 1.4792 | 0.8144 | 4.3894 | Sí |
| 72 (fila 1) | 1.8130 | 0.1632 | 0.8597 | 1.8136 | 0.8598 | 6.1325 | Sí (real: aprobó con 72) |
| 80 | 3.1506 | 0.0428 | 0.9589 | 3.1513 | 0.9590 | 23.3655 | Sí |

### 5.2 Los demás ejercicios

| Ejercicio | Resultado | Lectura |
|---|---|---|
| 3.1 Punto de corte | `X = 10.2254 / 0.1672 = 61.157` a mano · 61.154 con los coeficientes completos | Quien tiene 61 queda en 49.4 % («no aprueba») y quien tiene 62, en 53.5 % |
| 4.1 Estudiante de la fila 1 (`reading` = 72, `math` = 72) | `z = 1.8130`, `P = 0.8597` → «aprueba»; aprobó | El modelo acertó |
| 4.2 Primera fila con `reading` = 50 (índice 182, `math` = 50) | `P = 0.1341` → «no aprueba»; no aprobó | Acertó. Hay 7 estudiantes con `reading` = 50: solo 1 aprobó (`math` = 64) y el modelo acierta 6 de 7; un solo estudiante no mide el 16.8 % de error del modelo |
| 5.1 Razón de momios | `e^0.1672 = 1.1820` | +18.2 % en los momios por punto |
| Efecto en probabilidad | 40 → 41: 2.83 % → 3.33 % (+0.5 puntos) · 60 → 61: 45.19 % → 49.36 % (**+4.2 puntos**; con los coeficientes redondeados, 45.18 % → 49.35 %) | Mismo OR, efectos muy distintos. La clave de `02` y de `03` dice 49.7 % y +4.5 (salvedad 4) |
| 6.1 Matriz de confusión | Exactitud 832 / 1 000 = 0.832 · precisión 605 / 701 = 0.863 · sensibilidad 605 / 677 = 0.894 | Coincide con `confusion_matrix` |
| 6.2 ¿Dónde se equivoca? | 108 de los 168 errores tienen `reading` entre 55 y 67; 89 tienen P entre 0.3 y 0.7 | Se confirma lo que dice la clave: cerca del punto de corte |

### 5.3 Reto final: `writing score` en vez de `reading score`

| | `reading` | `writing` | Lectura |
|---|---|---|---|
| Coeficientes | b0 = −10.2254 · b1 = 0.1672 | b0 = −8.7876 · b1 = 0.1477 | Son los de la clave y los del Excel |
| z de Wald | 15.334 | 15.504 | Las dos son muy significativas |
| Razón de momios por punto | 1.1820 | 1.1591 | Es lo que compara la clave |
| Razón de momios por desviación estándar (14.60 y 15.20 puntos) | 11.49 | 9.43 | Las escalas no son iguales; por desviación la diferencia crece |
| Punto de corte | 61.15 | 59.51 | |
| `P` con `writing` = 65 | — | 0.6927 a mano · 0.6922 con el código (z = 0.8102, no 0.8129) | «Aprueba» en ambos casos |
| Log-verosimilitud / AIC | −366.88 / 737.76 | −382.79 / 769.58 | El AIC difiere en 31.8: no es «ligeramente» |
| Exactitud / AUC | 0.832 / 0.8999 | 0.824 / 0.8881 | Validación cruzada: 0.8307 contra 0.8239 |

**Conclusión:** `reading` tiene la relación más fuerte con aprobar matemáticas, y la diferencia es mayor de lo que sugiere el «ligeramente» de la clave (salvedad 6).

### 5.4 Código listo para pegar

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("StudentsPerformance.csv")
y = (df["math score"] >= 60).astype(int)
m = sm.Logit(y, sm.add_constant(df[["reading score"]])).fit(disp=0)
b0, b1 = m.params
sigmoide = lambda z: 1 / (1 + np.exp(-z))

# 1) Tabla del taller: a mano (coeficientes redondeados) contra el código
filas = []
for x in [40, 50, 60, 61, 70, 72, 80]:
    z4 = -10.2254 + 0.1672 * x
    z = b0 + b1 * x
    filas.append(dict(X=x, z_a_mano=round(z4, 4), e_menos_z=round(np.exp(-z4), 4), P_a_mano=round(sigmoide(z4), 4),
                      z_codigo=round(z, 4), P_codigo=round(sigmoide(z), 4), momios=round(sigmoide(z) / (1 - sigmoide(z)), 4)))
print(pd.DataFrame(filas).to_string(index=False))

# 2) Razón de momios y el efecto, distinto, sobre la probabilidad
print("OR:", np.exp(0.1672), np.exp(b1))
print("40 -> 41:", sigmoide(b0 + b1 * 41) - sigmoide(b0 + b1 * 40), "| 60 -> 61:", sigmoide(b0 + b1 * 61) - sigmoide(b0 + b1 * 60))
print("Punto de corte:", 10.2254 / 0.1672, -b0 / b1)

# 3) La fila 1 y las filas con reading = 50
print(df.loc[0, ["reading score", "math score"]].tolist())
f50 = df[df["reading score"] == 50]
print(len(f50), y[f50.index].sum(), ((m.predict(sm.add_constant(df[["reading score"]]))[f50.index] >= 0.5) == y[f50.index]).sum())

# 4) Reto final: writing score
mw = sm.Logit(y, sm.add_constant(df[["writing score"]])).fit(disp=0)
c0, c1 = mw.params
print(c0, c1, np.exp(c1), -c0 / c1)
print("writing = 65: a mano", sigmoide(-8.7876 + 0.1477 * 65), "| código", sigmoide(c0 + c1 * 65))
sd = df[["reading score", "writing score"]].std()
print("OR por desviación:", np.exp(b1 * sd["reading score"]), np.exp(c1 * sd["writing score"]), "| AIC:", m.aic, mw.aic)
```

---

## 6. Ejemplo guiado 3: evaluar el clasificador (matriz, umbral, línea base y datos no vistos)

**Pregunta:** ¿qué tan bueno es el clasificador, para qué umbral y frente a qué referencia?

### 6.1 Matriz de confusión y métricas (umbral 0.5)

| | Predicho: no aprueba | Predicho: aprueba |
|---|---|---|
| **Real: no aprueba** | 227 (VN) | 96 (FP) |
| **Real: aprueba** | 72 (FN) | 605 (VP) |

| Métrica | Fórmula | Valor | Lectura | Uso |
|---|---|---|---|---|
| Exactitud | (VP + VN) / 1 000 | 0.832 | 83.2 % bien clasificados. Los errores son 96 + 72 = 168 | ✅ |
| Precisión | VP / (VP + FP) = 605 / 701 | 0.863 | De los que el modelo llama «aprueba», el 86.3 % aprueba | ✅ |
| Sensibilidad (*recall*) | VP / (VP + FN) = 605 / 677 | 0.894 | Detecta al 89.4 % de quienes aprueban | ✅ |
| Especificidad | VN / (VN + FP) = 227 / 323 | 0.703 | Detecta al 70.3 % de quienes **no** aprueban: es la métrica más floja | ➕ |
| Valor predictivo negativo | VN / (VN + FN) = 227 / 299 | 0.759 | De los que el modelo llama «no aprueba», el 75.9 % no aprueba | ➕ |
| F1 | 2·P·R / (P + R) | 0.878 | Media armónica de precisión y sensibilidad | ➕ |
| Exactitud balanceada | (sensibilidad + especificidad) / 2 | 0.798 | Corrige el desbalance 677 / 323 | ➕ |
| MCC / kappa | — | 0.609 / 0.608 | Acuerdo por encima del azar: «bueno», no «excelente» | ➕ |
| AUC | `roc_auc_score` | 0.8999 | Probabilidad de que un aprobado reciba más P que un reprobado | ➕ |
| Brier y log-loss | `brier_score_loss`, `log_loss` | 0.1181 y 0.3669 | Contra 0.2187 y 0.6291 de un modelo que predice siempre 67.7 % | ➕ |

### 6.2 Cambiar el umbral

| Umbral t | VN | FP | FN | VP | Exactitud | Precisión | Sensibilidad | Especificidad |
|---|---|---|---|---|---|---|---|---|
| 0.3 | 163 | 160 | 29 | 648 | 0.811 | 0.802 | 0.957 | 0.505 |
| 0.4 | 192 | 131 | 45 | 632 | 0.824 | 0.828 | 0.934 | 0.594 |
| **0.5** | 227 | 96 | 72 | 605 | **0.832** | 0.863 | 0.894 | 0.703 |
| 0.6 | 246 | 77 | 95 | 582 | 0.828 | 0.883 | 0.860 | 0.762 |
| 0.7 | 273 | 50 | 146 | 531 | 0.804 | 0.914 | 0.784 | 0.845 |
| 0.8 | 287 | 36 | 200 | 477 | 0.764 | 0.930 | 0.705 | 0.889 |
| 0.9 | 312 | 11 | 318 | 359 | 0.671 | 0.970 | 0.530 | 0.966 |

Subir el umbral reduce los «aprueba» (701 con 0.5, 513 con 0.8, 370 con 0.9), sube la precisión y baja la sensibilidad: es lo que dice la clave de `Evaluacion/` (Ejercicio 3.2) y aquí se comprueba. Con t = 0.8 el estudiante de `reading` = 70 (P = 0.814) sigue como «aprueba», por 0.014. Con t = 0.9 la exactitud (0.671) cae por debajo de la línea base (0.677). La mejor exactitud en la muestra es la de t = 0.42 (0.833), casi igual a la de 0.5.

### 6.3 Línea base y qué significa «83.2 %»

- Un modelo que siempre dice «aprueba» acierta 677 / 1 000 = 0.677 sin mirar ningún dato (Ejercicio 4.2 del refuerzo). El modelo gana 15.5 puntos.
- Si «en riesgo» (no aprueba) fuera la clase positiva, la sensibilidad sería 227 / 323 = 0.703 y la precisión 227 / 299 = 0.759: el modelo deja pasar como «aprueba» a 96 estudiantes que no aprueban (falsos positivos del modelo, pero los casos más costosos para quien quiere ayudar a los que reprueban; salvedad 5).
- El p-value casi cero **no** quiere decir «explica el 100 %» (Ejercicio 5.2 del refuerzo): el pseudo R² de McFadden es 0.417 y se equivoca en 168 estudiantes.

### 6.4 Dónde se equivoca

| `reading` | Estudiantes | Aprueban (real) | P media del modelo | Errores |
|---|---|---|---|---|
| menos de 50 | 90 | 7.8 % | 5.4 % | 7 |
| 50 a 54 | 70 | 14.3 % | 18.7 % | 10 |
| 55 a 59 | 94 | 34.0 % | 34.0 % | 32 |
| 60 a 64 | 119 | 57.1 % | 54.1 % | 52 |
| 65 a 69 | 114 | 72.8 % | 72.1 % | 31 |
| 70 o más | 513 | 93.0 % | 93.7 % | 36 |

La probabilidad media del modelo sigue a la tasa real en todos los tramos (Hosmer-Lemeshow p = 0.549) y los errores se concentran entre 55 y 69 (115 de 168). Los 36 errores de la última fila son estudiantes con `reading` de 70 o más que no aprueban (falsos positivos): el modelo nunca da 0 ni 1.

### 6.5 Una partición contra validación cruzada

| Evaluación | Exactitud | AUC |
|---|---|---|
| En los mismos 1 000 (lo que hacen los materiales) | 0.832 | 0.8999 |
| 80 / 20, semilla 42, sin estratificar (200 de prueba, 65 % aprueban) | 0.835 | 0.9169 |
| 80 / 20, semilla 42, estratificada (67.5 % aprueban en la prueba) | 0.820 | 0.8753 |
| 2 000 particiones 80 / 20 (media; desviación 0.024; de 0.755 a 0.920) | 0.830 | 0.8993 |
| Validación cruzada 5 × 20 estratificada | 0.8307 | 0.8998 |

Con una sola variable no hay sobreajuste: la exactitud sobre los 1 000 (0.832) es la misma que fuera de muestra (0.8307). Pero una sola partición de 200 estudiantes puede dar entre 0.76 y 0.92: ningún resultado de la Semana 8 debería comunicarse sin esa advertencia (salvedad 10).

### 6.6 Código listo para pegar

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, f1_score, balanced_accuracy_score, matthews_corrcoef,
                             roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split, cross_validate, RepeatedStratifiedKFold

df = pd.read_csv("StudentsPerformance.csv")
y = (df["math score"] >= 60).astype(int)
X = sm.add_constant(df["reading score"])
p = sm.Logit(y, X).fit(disp=0).predict(X)

# 1) Barrido de umbrales
filas = []
for t in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    vn, fp, fn, vp = confusion_matrix(y, (p >= t).astype(int)).ravel()
    filas.append(dict(t=t, VN=vn, FP=fp, FN=fn, VP=vp, exactitud=(vp + vn) / len(y), precision=vp / (vp + fp),
                      sensibilidad=vp / (vp + fn), especificidad=vn / (vn + fp)))
print(pd.DataFrame(filas).round(3).to_string(index=False))

# 2) Métricas que miran los dos errores (umbral 0.5) y umbral de Youden
pred = (p >= 0.5).astype(int)
print(f1_score(y, pred), balanced_accuracy_score(y, pred), matthews_corrcoef(y, pred))
fpr, tpr, umbrales = roc_curve(y, p)
print("Umbral de Youden:", umbrales[np.argmax(tpr - fpr)])

# 3) Calibración: tasa real contra probabilidad media por tramo + Hosmer-Lemeshow
tramo = pd.cut(df["reading score"], [0, 50, 55, 60, 65, 70, 101], right=False)
print(pd.DataFrame({"y": y, "p": p}).groupby(tramo, observed=True).agg(n=("y", "size"), real=("y", "mean"), modelo=("p", "mean")).round(3))
d = pd.DataFrame({"y": y, "p": p})
d["g"] = pd.qcut(d["p"].rank(method="first"), 10, labels=False)
o, e, n = d.groupby("g")["y"].sum(), d.groupby("g")["p"].sum(), d.groupby("g").size()
hl = (((o - e) ** 2) / (e * (1 - e / n))).sum()
print("Hosmer-Lemeshow:", hl, stats.chi2.sf(hl, 8))

# 4) Una sola partición contra validación cruzada
Xs = df[["reading score"]]
Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.2, random_state=42)
m = LogisticRegression(penalty=None, max_iter=1000).fit(Xtr, ytr)
print("Prueba (semilla 42):", m.score(Xte, yte), roc_auc_score(yte, m.predict_proba(Xte)[:, 1]))
cv = cross_validate(LogisticRegression(penalty=None, max_iter=1000), Xs, y, scoring=["accuracy", "roc_auc"],
                    cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42))
print("5 x 20 pliegues:", cv["test_accuracy"].mean(), cv["test_roc_auc"].mean())
```

---

## 7. Ejemplo guiado 4: dos predictoras y colinealidad (Reto final de `03`, `01` §7)

**Pregunta:** ¿qué pasa cuando se agrega `writing score`, que correlaciona 0.955 con `reading score`?

### 7.1 Tres modelos lado a lado

| Modelo | b de `reading` (error estándar) | b de `writing` (error estándar) | Log-verosimilitud | AIC | Exactitud | AUC | Validación cruzada 5 × 20 (exactitud / AUC) |
|---|---|---|---|---|---|---|---|
| Solo `reading` | 0.1672 (0.0109) | — | −366.88 | 737.76 | 0.832 | 0.8999 | 0.8307 / 0.8998 |
| Solo `writing` | — | 0.1477 (0.0095) | −382.79 | 769.58 | 0.824 | 0.8881 | 0.8239 / 0.8883 |
| Las dos | 0.1280 (0.0221) | 0.0395 (0.0199) | −364.88 | 735.75 | 0.834 | 0.9007 | 0.8324 / 0.8999 |

### 7.2 Lectura

| Aspecto | Resultado | Lectura |
|---|---|---|
| Coeficiente de `reading` | Baja de 0.1672 a 0.1280 | Comparte el efecto con `writing` (OR 1.182 → 1.137; el de `writing`, 1.040) |
| Error estándar de `reading` | 0.0109 → 0.0221 (×2.03) | Es la colinealidad: VIF = 11.27 (√VIF = 3.4 es la referencia de la regresión lineal; el factor observado en este modelo es 2.03) |
| Significancia de `writing` | Wald p = 0.047; razón de verosimilitud χ² = 4.006, p = 0.0453 | Al límite de 0.05: depende de la prueba y de la semilla |
| ¿Mejora el modelo? | AIC baja 2.0 (735.75 contra 737.76) pero el BIC sube 2.9 (750.48 contra 747.58). Exactitud 0.832 → 0.834; en validación cruzada 0.8307 → 0.8324 y el AUC es igual | Prácticamente nada: `writing` repite lo que ya dice `reading` |
| Estabilidad (1 000 bootstraps) | Desviación de b de `reading`: 0.0106 (sola) contra 0.0240 (con `writing`). El b de `writing` es negativo en el 3.1 % de las muestras (IC percentil [−0.001; 0.082]). Correlación entre los dos coeficientes: −0.90 | Los coeficientes se «reparten» el efecto y se compensan. Cambia la interpretación, no la predicción |

**Conclusión:** como dice la sección 7 de `01`, la colinealidad vuelve inestables los coeficientes, pero aquí el signo de `reading` no cambia en ningún remuestreo y la capacidad de predicción es la misma (salvedad 12). La pregunta correcta no es «¿qué variable influye más?» sino «¿qué agrega la segunda?»: casi nada.

### 7.3 Código listo para pegar

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import accuracy_score, roc_auc_score

df = pd.read_csv("StudentsPerformance.csv")
y = (df["math score"] >= 60).astype(int)
m1 = sm.Logit(y, sm.add_constant(df[["reading score"]])).fit(disp=0)
mw = sm.Logit(y, sm.add_constant(df[["writing score"]])).fit(disp=0)
m2 = sm.Logit(y, sm.add_constant(df[["reading score", "writing score"]])).fit(disp=0)

# 1) Coeficientes, errores estándar y p
print(m1.params.round(4).to_dict(), m1.bse.round(4).to_dict())
print(m2.params.round(4).to_dict(), m2.bse.round(4).to_dict(), m2.pvalues.round(4).to_dict())

# 2) Correlación y VIF
X2 = sm.add_constant(df[["reading score", "writing score"]])
print(df[["reading score", "writing score"]].corr().iloc[0, 1], [variance_inflation_factor(X2.values, i) for i in (1, 2)])

# 3) ¿Vale la pena la segunda variable? Razón de verosimilitud, AIC y BIC
lr = 2 * (m2.llf - m1.llf)
print(lr, stats.chi2.sf(lr, 1), m1.aic, m2.aic, m1.bic, m2.bic)

# 4) Exactitud y AUC de los tres modelos
for nombre, m, cols in [("reading", m1, ["reading score"]), ("writing", mw, ["writing score"]), ("ambas", m2, ["reading score", "writing score"])]:
    p = m.predict(sm.add_constant(df[cols]))
    print(nombre, accuracy_score(y, p >= 0.5), roc_auc_score(y, p), m.llf, m.aic)

# 5) Estabilidad de los coeficientes con bootstrap
rng = np.random.default_rng(42)
X, yv = X2.to_numpy(float), y.to_numpy()
b = []
for _ in range(1000):
    i = rng.integers(0, len(df), len(df))
    b.append(sm.Logit(yv[i], X[i]).fit(disp=0).params[1:])
b = np.array(b)
print(b.std(axis=0), (b[:, 1] < 0).mean(), np.corrcoef(b.T)[0, 1], np.percentile(b[:, 1], [2.5, 97.5]))
```

---

## 8. Ejemplo guiado 5: variables categóricas en la regresión logística (notebook `Matematicas/regresion_variables_categoricas`)

**Pregunta:** ¿qué cambia cuando se agregan género y curso de preparación como *dummies* al modelo de `reading`?

### 8.1 Efecto crudo de cada categórica (antes de modelar)

| Variable | Grupo | Estudiantes | Aprueban | `reading` medio | Chi-cuadrado (p) | OR crudo |
|---|---|---|---|---|---|---|
| Género | Mujer / hombre | 518 / 482 | 62.0 % / 73.9 % | 72.61 / 65.47 | 16.14 (5.9e-5) | 0.577 (mujer contra hombre) |
| Curso de preparación | Completado / ninguno | 358 / 642 | 75.7 % / 63.2 % | 73.89 / 66.53 | 16.31 (5.4e-5) | 1.811 (completado contra ninguno) |
| Almuerzo | Estándar / reducido | 645 / 355 | 77.1 % / 50.7 % | 71.65 / 64.65 | 72.70 (1.5e-17) | 3.265 (estándar contra reducido) |

### 8.2 Modelo `reading` + género + curso

| Término | Coeficiente (error estándar) | OR | IC 95 % del OR | p |
|---|---|---|---|---|
| Constante | −14.6562 (1.049) | — | — | 2.3e-44 |
| `reading score` | 0.2668 (0.018) | 1.3058 | [1.2595; 1.3537] | 1.1e-47 |
| Mujer (1 = mujer) | −3.4180 (0.312) | 0.0328 | [0.0178; 0.0605] | 7.2e-28 |
| Curso completado | −0.5056 (0.243) | 0.6031 | [0.3745; 0.9713] | 0.038 |

Log-verosimilitud −271.12 (nula −629.11) · LR p = 7.2e-155 · pseudo R² 0.5690 · AIC 550.24 · BIC 569.87 · VIF 1.07 a 1.14. Frente al modelo simple: χ² = 191.52, gl = 2, p = 2.6e-42 y el AIC baja de 737.76 a 550.24. Matriz [[252, 71], [46, 631]]: exactitud 0.883 · precisión 0.899 · sensibilidad 0.932 · AUC 0.9476. En validación cruzada 5 × 20: 0.8820 y AUC 0.9464, es decir, la mejora **no** es sobreajuste.

### 8.3 Lectura (y dos advertencias)

| Término | Qué dice | Advertencia |
|---|---|---|
| `reading` | Cada punto multiplica los momios por 1.31 (con género y curso fijos), más que el 1.18 del modelo simple | El coeficiente cambia al cambiar las demás variables: vive dentro de su modelo |
| Mujer | Con el mismo `reading`, los momios de aprobar de una mujer son 0.033 veces los de un hombre. Con `reading` = 65 (sin curso): 93.6 % contra 32.4 %; con 70: 98.2 % contra 64.6 % | No contradice que las mujeres tengan mejor lectura (72.6 contra 65.5): en crudo aprueban menos (62.0 % contra 73.9 %); controlar por lectura *amplifica* la brecha. En los datos con `reading` entre 68 y 72: 64.2 % (67 mujeres) contra 96.1 % (51 hombres) |
| Curso | En crudo, **más** aprobación (OR 1.81). Con `reading` y género: OR 0.60 | El signo se invierte porque quienes hacen el curso leen mejor (73.9 contra 66.5). Con solo `reading` + curso, el coeficiente es −0.2037 y p = 0.320: solo es «significativo» (p = 0.038) cuando también está el género. No se debe leer como «el curso empeora las chances» |

### 8.4 Código listo para pegar

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score
from sklearn.model_selection import cross_validate, RepeatedStratifiedKFold

df = pd.read_csv("StudentsPerformance.csv")
df["aprueba_mate"] = (df["math score"] >= 60).astype(int)
df["mujer"] = (df["gender"] == "female").astype(int)
df["curso"] = (df["test preparation course"] == "completed").astype(int)
y = df["aprueba_mate"]

# 1) Efecto crudo de cada categórica: porcentaje que aprueba y chi-cuadrado de independencia
for col in ["gender", "test preparation course", "lunch"]:
    tabla = pd.crosstab(df[col], y)
    print(col, stats.chi2_contingency(tabla, correction=False)[:2], (tabla.iloc[:, 1] / tabla.sum(axis=1)).round(3).to_dict())

# 2) Modelo con predictores mixtos
X = sm.add_constant(df[["reading score", "mujer", "curso"]])
m = sm.Logit(y, X).fit(disp=0)
print(m.summary())
print(pd.DataFrame({"OR": np.exp(m.params), "p": m.pvalues}).round(4))
print(np.exp(m.conf_int()).round(4))

# 3) Mejora frente al modelo simple
m1 = sm.Logit(y, sm.add_constant(df[["reading score"]])).fit(disp=0)
lr = 2 * (m.llf - m1.llf)
print(lr, stats.chi2.sf(lr, 2), m1.aic, m.aic)

# 4) Matriz, exactitud, AUC y validación cruzada
p = m.predict(X)
pred = (p >= 0.5).astype(int)
print(confusion_matrix(y, pred), accuracy_score(y, pred), roc_auc_score(y, p))
cv = cross_validate(LogisticRegression(penalty=None, max_iter=5000), df[["reading score", "mujer", "curso"]], y,
                    scoring=["accuracy", "roc_auc"], cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42))
print(cv["test_accuracy"].mean(), cv["test_roc_auc"].mean())

# 5) El curso: ¿cambia el signo al agregar variables?
for cols in (["curso"], ["reading score", "curso"], ["reading score", "mujer", "curso"]):
    mm = sm.Logit(y, sm.add_constant(df[cols])).fit(disp=0)
    print(cols, round(mm.params["curso"], 4), round(mm.pvalues["curso"], 4))

# 6) Mismo reading, distinto género
nuevos = pd.DataFrame({"const": 1.0, "reading score": [65, 65, 70, 70], "mujer": [0, 1, 0, 1], "curso": 0})
print(m.predict(nuevos).round(4).tolist())
```

---

## 9. Ejemplo guiado 6: la máxima verosimilitud por dentro (notebook `Matematicas/regresion_logistica_paso_a_paso`)

**Pregunta:** si no hay fórmula cerrada como en mínimos cuadrados, ¿qué hace el software para hallar `b0` y `b1`?

| Paso | Qué se hace | Resultado | Lectura |
|---|---|---|---|
| 1 | Log-verosimilitud: Σ [y·ln(p) + (1 − y)·ln(1 − p)], con `p = sigmoide(b0 + b1·x)` | Se evalúa en una grilla de 30 × 35 = 1 050 pares con 10 estudiantes (filas 30 a 39) | Es el mismo principio del optimizador, probando combinaciones «a mano» |
| 2 | Mejor par de la grilla | b0 = −15.00, b1 = 0.22, ll = −3.0920 | Verificado (✅) |
| 3 | Óptimo real con `sm.Logit` sobre esas 10 filas | b0 = −15.72, b1 = 0.230, ll = −3.0893 | La grilla se acerca; el optimizador afina |
| 4 | ¿Y con las primeras 10 filas del archivo? | Los que aprueban tienen `reading` de 64 o más y los que no, de 60 o menos: separación perfecta. Con el máximo por defecto (35 iteraciones) solo sale `ConvergenceWarning` (b0 ≈ −536, b1 ≈ 8.6); con `maxiter=100` aparecen también `PerfectSeparationWarning` y los coeficientes siguen creciendo (b0 ≈ −587, b1 ≈ 9.5) | Es la razón por la que el notebook usa las filas 30 a 39 (allí hay solapamiento: aprueban desde 65 y no aprueban hasta 72) |
| 5 | Las 1 000 filas | b0 = −10.2254, b1 = 0.1672, ll = −366.88 (nula −629.11), 7 iteraciones | Converge porque en la zona 55 a 70 las clases se solapan |
| 6 | `LogisticRegression()` por defecto | −10.2241 y 0.16719; con `penalty=None`: −10.2254 y 0.16721 | Como dice el notebook, scikit-learn regulariza un poco por defecto |
| 7 | Las colas | Con `reading` ≤ 40: 27 estudiantes y ninguno aprueba. Con `reading` ≥ 90: 79 y todos aprueban | Casi separación en los extremos; aun así el modelo da entre 0.06 % (con 17) y 99.85 % (con 100), nunca 0 ni 1 |

```python
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("StudentsPerformance.csv")
df["aprueba_mate"] = (df["math score"] >= 60).astype(int)
sigmoide = lambda z: 1 / (1 + np.exp(-z))


def log_verosimilitud(b0, b1, x, y):
    p = np.clip(sigmoide(b0 + b1 * x), 1e-10, 1 - 1e-10)
    return np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))


# 1) Grilla con 10 estudiantes (filas 30 a 39: las clases se solapan)
m10 = df.iloc[30:40]
x10, y10 = m10["reading score"].to_numpy(float), m10["aprueba_mate"].to_numpy(float)
mejor = max((log_verosimilitud(b0, b1, x10, y10), b0, b1) for b0 in np.arange(-25, 5, 1.0) for b1 in np.arange(-0.1, 0.6, 0.02))
print("grilla:", mejor)
opt = sm.Logit(y10, sm.add_constant(x10)).fit(disp=0)
print("statsmodels:", opt.params, opt.llf)

# 2) Las primeras 10 filas separan perfectamente: no hay óptimo finito
h = df.iloc[:10]
with warnings.catch_warnings(record=True) as avisos:
    warnings.simplefilter("always")
    sep = sm.Logit(h["aprueba_mate"], sm.add_constant(h["reading score"].astype(float))).fit(disp=0, maxiter=100)
print(sorted({a.category.__name__ for a in avisos}), sep.params.values, sep.mle_retvals["converged"])

# 3) scikit-learn: la regularización por defecto mueve un poco los coeficientes
X, y = df[["reading score"]].to_numpy(float), df["aprueba_mate"]
for nombre, mod in [("C = 1 (defecto)", LogisticRegression()), ("sin penalización", LogisticRegression(penalty=None, max_iter=1000))]:
    mod.fit(X, y)
    print(nombre, mod.intercept_[0], mod.coef_[0][0])

# 4) Colas casi separadas
r = df["reading score"]
print((r <= 40).sum(), df.loc[r <= 40, "aprueba_mate"].sum(), (r >= 90).sum(), df.loc[r >= 90, "aprueba_mate"].sum())
```

---

## 10. «MA Evaluación 8»: lo que evalúa y las respuestas verificadas

La clave de `Evaluacion/` describe el quiz de Canvas (diapositivas 12 a 16). El caso guía del quiz es «riesgo de deserción» (`x1` = horas de estudio, `x2` = asistencia, `x3` = interacciones); el refuerzo y los notebooks usan en cambio `StudentsPerformance.csv`, así que los números de abajo son los del refuerzo.

| Pregunta | Tipo | Respuesta de la clave | Verificación con código |
|---|---|---|---|
| 1. ¿Qué modela la regresión logística en su forma clásica? | Opción múltiple | `log(p / (1 − p))` como combinación lineal de x | Con el modelo ajustado, `log(p / (1 − p))` coincide con `b0 + b1·x` (diferencia máxima 3.8e-14). El docx muestra la opción deformada («Log log (1/1-p)») por el render; es la misma |
| 2. «p(x) = 1 / (1 + e^−z)» | Verdadero / falso | Verdadero | Es la definición usada en todo el cuadro (sección 4) |
| 3. Odds, complemento, «más probable» | Completar espacios | no ocurra · complemento · más probable | `reading` = 70: P = 0.8144, complemento 0.1856, momios 4.39 > 1 → más probable aprobar |
| 4. Logit, sigmoide, umbral, *odds ratio* | Arrastrar palabras | log-odds · sigmoide · umbral · odds ratio | Banco de palabras: `media`, `colinealidad` y `varianza` son distractores |
| 5. Estadística contra aprendizaje automático | Marcar palabras | Ver abajo | No verificable con código; ver salvedad 2 |

**Pregunta 5.** El texto contrasta el *modelo* (lineal si Y es un número; logística si es 0 / 1; el OR cuantifica el efecto) con la *validación estadística* (inferencia, confianza, significancia y colinealidad). Según la clave, lo que Canvas califica no coincide con ese diseño: acepta «evidencia», «aumentar» y «disminuir», rechaza «regla» y las dos apariciones de «OR», y valida «logística» solo en su primera aparición (auditoría del profesor del 2026-08-21, no repetida aquí). La clave recomienda corregir la configuración y recalificar a todos.

**Refuerzo (`Evaluacion/02_Evaluacion_desarrollo*.md` y `02_Evaluacion_taller*.ipynb`).** Cada paso refuerza una pregunta; todas sus cifras se reprodujeron:

| Paso | Cifra | Verificado |
|---|---|---|
| 1.1 `p(x)` para 40, 60, 70, 90 | 0.028 · 0.452 · 0.814 · 0.992 (`z` = −3.537, −0.193, 1.479, 4.823) | ✅ (la clave escribe −0.192 y 1.480; salvedad 3) |
| 1.2 Mismo `reading`, ¿mismo `p`? | «Verdadero solo en el modelo simple» | ✅ Con tres variables: `reading` = 70 → 98.2 % (hombre) y 64.6 % (mujer) |
| 2.1 Momios 60 y 70 | 0.825 y 4.38 (4.39 sin redondear) | ✅ |
| 2.2 OR y comprobación 60 → 61 | 1.182 · 0.8246 × 1.182 = 0.9746 = momios(61) | ✅ |
| 3.2 Umbral 0.8 | «Sigue como aprueba; sube la precisión y baja el recall» | ✅ Precisión 0.863 → 0.930, sensibilidad 0.894 → 0.705 (sección 6.2); el notebook no lo calcula |
| 4.1 / 4.2 Métricas y línea base | 0.832 · 0.863 · 0.894 · 0.677 | ✅ |
| 5.1 Modelado o validación | Modelado: sigmoide, OR, umbral, `z` · Validación: p-value, IC, colinealidad | ✅ (conceptual) |
| 5.2 «p ≈ 0 significa que explica el 100 %» | «No»: acierta 83.2 % | ✅ Se equivoca en 168 y el pseudo R² es 0.417 |
| Autoevaluación 3 y 4 | `p` = 0.75 → momios 3 · OR = 2 duplica los momios | ✅ |

---

## 11. Un solo script con todo el flujo

No hay `Promt.md` para la Semana 8; este script sigue el flujo de `01` §5 y cubre lo que piden los talleres: explorar, dos pruebas inferenciales (Welch sobre `reading` y Wald sobre el coeficiente, más la razón de verosimilitud del modelo), interpretaciones en español y comentarios en cada bloque.

```python
# --- 1) Cargar y explorar --------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_auc_score

df = pd.read_csv("StudentsPerformance.csv")
print("Filas y columnas:", df.shape, "| Nulos:", df.isnull().sum().sum(), "| Duplicados:", df.duplicated().sum())
df["aprueba_mate"] = (df["math score"] >= 60).astype(int)    # 1 = aprueba matemáticas
x, y = df["reading score"], df["aprueba_mate"]
print("Aprueban:", y.sum(), f"({y.mean():.1%}) | No aprueban:", (1 - y).sum())
print(df.groupby("aprueba_mate")["reading score"].agg(["mean", "median", "std"]).round(2))

# --- 2) Prueba 1: ¿difiere la lectura entre quienes aprueban y quienes no? --
w = stats.ttest_ind(x[y == 1], x[y == 0], equal_var=False)   # Welch: no exige varianzas iguales
print(f"Welch: t = {w.statistic:.2f}, p = {w.pvalue:.2e}")
print("Interpretación:", "la lectura SÍ difiere entre los dos grupos (p < 0.05)." if w.pvalue < 0.05 else "no hay evidencia de diferencia.")

# --- 3) Regresión logística: ajuste y prueba 2 (Wald) ------------------------
modelo = sm.Logit(y, sm.add_constant(x)).fit(disp=0)
b0, b1 = modelo.params
z, p_wald = modelo.tvalues["reading score"], modelo.pvalues["reading score"]
print(f"z = {b0:.4f} + {b1:.4f} * reading | Wald: z = {z:.2f}, p = {p_wald:.2e}")
print("Interpretación:", "el coeficiente es distinto de 0: leer mejor se asocia con aprobar (p < 0.05)." if p_wald < 0.05 else "no se rechaza H0.")

# --- 4) Razón de momios y modelo completo ------------------------------------
or_, (lo, hi) = np.exp(b1), np.exp(modelo.conf_int().loc["reading score"])
print(f"OR = {or_:.3f} (IC 95 %: {lo:.3f} a {hi:.3f}) | LR chi2 = {modelo.llr:.2f}, p = {modelo.llr_pvalue:.1e}, pseudo R2 = {modelo.prsquared:.3f}")
print(f"Interpretación: cada punto de lectura multiplica los momios de aprobar por {or_:.2f} (no son {100*(or_-1):.0f} puntos de probabilidad).")

# --- 5) Curva sigmoide ---------------------------------------------------------
xs = np.linspace(x.min(), x.max(), 300)
plt.scatter(x, y, alpha=0.15)
plt.plot(xs, 1 / (1 + np.exp(-(b0 + b1 * xs))), color="darkred")
plt.axhline(0.5, color="gray", linestyle="--")
plt.xlabel("reading score"); plt.ylabel("P(aprueba matemáticas)"); plt.title("Curva sigmoide del modelo")
plt.show()

# --- 6) Clasificar y evaluar ---------------------------------------------------
p = modelo.predict(sm.add_constant(x))
pred = (p >= 0.5).astype(int)
print(confusion_matrix(y, pred))
print(f"Exactitud {accuracy_score(y, pred):.3f} | precisión {precision_score(y, pred):.3f} | sensibilidad {recall_score(y, pred):.3f} | AUC {roc_auc_score(y, p):.3f} | línea base {y.mean():.3f}")
print(f"Punto de corte: reading = {-b0 / b1:.1f}. Interpretación: el modelo acierta más que predecir siempre 'aprueba' (asociación, no causalidad).")
```

---

## 12. Cuándo usar (y cuándo no) la regresión logística: las evidencias de `01` y `04`

| Criterio | Qué dice el material | Evidencia recalculada | Lectura |
|---|---|---|---|
| ¿Y es binaria? | `01` Ejercicio 1: una recta puede predecir fuera de [0, 1]. `04` Ejercicio 3: «1.15» o «−0.08» | Recta sobre 0 / 1: `aprueba` = −0.7452 + 0.02056·`reading`, R² 0.412. **15** predicciones menores que 0 y **150** mayores que 1 (165 de 1 000; rango −0.396 a 1.311). Con `reading` = 100 predice 1.31 y con 17, −0.40. Breusch-Pagan p = 5.5e-20 | Los valores del Ejercicio 3 de `04` no son inventados: aparecen en los datos |
| ¿Solo importa la decisión? | `04` §4 | Regresión lineal de `math` sobre `reading` (R² 0.668, error estándar residual 8.74) y regla «aprueba si la predicción ≥ 60»: matriz **idéntica** [[227, 96], [72, 605]] (regla `reading` ≥ 62) | Con una sola predictora, el 83.2 % no demuestra una ventaja de la logística: esta aporta probabilidades, OR e inferencia |
| ¿La relación es una S? | `01` §3 | La tasa real sube de 7.8 % (menos de 50) a 93.0 % (70 o más) y el término cuadrático no aporta (p = 0.358) | Una sigmoide con un solo coeficiente describe bien estos datos |
| ¿Y numérica y X numérica? | `04` §1 y §2 | Lineal: `writing` ← `reading`, R² 0.911. Logística: `aprueba` ← `reading`, exactitud 0.832 y pseudo R² 0.417 | R² y exactitud miden cosas distintas (Ejercicio 4 de `04`). Además `04` compara dos Y distintas (`writing` y «aprueba»); con la misma Y ver la fila anterior |
| ¿Dónde se pone el 60? | `01` define «aprueba» como `math` ≥ 60 | Con 50: aprueban 865, línea base 0.865, exactitud 0.893 (+2.8 puntos), AUC 0.920, corte en `reading` 49.1. Con 60: 677, 0.677, 0.832, 0.900, 61.15. Con 70: 409, 0.591, 0.802, 0.885, 73.76. El OR casi no se mueve: 1.179 · 1.182 · 1.174 | El corte de la nota es arbitrario: cambia el balance, la línea base y el punto de corte; no la conclusión sobre el efecto |
| ¿Clases desbalanceadas? | Refuerzo, Ejercicio 4.2 | Línea base 0.677; con el corte en 50 el modelo supera la línea base por solo 2.8 puntos | Reportar siempre la línea base y una métrica que no dependa del desbalance (AUC, kappa) |
| ¿Pocas variables y pocos niveles? | `01` §7, notebook de categóricas | 12 columnas *dummy* con las cinco categóricas (11 sin el curso); con 323 eventos y 3 predictoras hay 108 por variable (regla: 10) | Aquí no hay riesgo de sobreajuste; sí lo habría con muchas más columnas o con pocos estudiantes |
| ¿Colinealidad? | `01` §7: coeficientes «inestables» | `reading`–`writing`: VIF 11.27, error estándar ×2.03, signo estable (sección 7) | Cierto en el error estándar; no cambia la predicción |
| ¿Extrapolar? | — | P(17) = 0.06 %, P(100) = 99.85 %; ningún estudiante con `reading` ≤ 40 aprueba (27) y todos con ≥ 90 aprueban (79) | La sigmoide no llega a 0 ni a 1. Fuera de 17 a 100 no hay datos |
| ¿Causalidad? | `01` §2 («relación real») | Aparece una asociación, con control de lectura; el curso cambia de signo al controlar | «Asociado con», nunca «causa» (salvedad 13) |

---

## 13. Salvedades que conviene conocer

1. **Qué se califica y qué casos se usan.** La actividad es el quiz «MA Evaluación 8» (5 preguntas, clave en `Evaluacion/`); el taller en papel, el de Python y el refuerzo son práctica. El quiz usa el caso de «riesgo de deserción» (horas de estudio, asistencia, interacciones) y los materiales usan `StudentsPerformance.csv`: no se pueden mezclar cifras. No hay `Promt.md` para esta semana, ni un enunciado u rúbrica oficial en el repositorio (la clave menciona 4 criterios de «Revisión» sin detallarlos). En el docx las preguntas 3 y 4 aparecen sin contenido.
2. **Pregunta 5 de Canvas.** Según la auditoría del profesor (2026-08-21), la configuración del quiz califica como correctas «evidencia», «aumentar» y «disminuir» y como incorrectas «regla» y «OR», y evalúa por posición de la palabra y no por concepto. Aquí no se puede reverificar (no hay acceso a Canvas). Si es cierto, hay que corregir la actividad y recalificar a todos, como recomienda la clave.
3. **Redondeo en el taller en papel y en las claves.** (a) La clave de `03` dice que los valores del código «coinciden exactamente» con la tabla del taller en papel; el código da `z` = −3.5371, −1.8650, −0.1929, 1.4792 y 3.1513, y a mano salen −3.5374, −1.8654, −0.1934, 1.4786 y 3.1506 (usar `b1` = 0.1672 en vez de 0.16721). Las probabilidades difieren en la 4.ª cifra para 60 (0.4518 contra 0.4519) y 80 (0.9589 contra 0.9590). (b) En la clave de `02`, `e^(−z)` para `X` = 40 es 34.38, no 34.35; y 1 / (1 + 0.1632) es 0.8597, no 0.8598. (c) `03` Ejercicio 3c comenta `print(-b0 / b1)   # ≈ 61.157`, pero la salida es 61.154 (61.157 es el cálculo a mano). (d) `01` Ejercicio 3 usa `b0` = −10.23 y `b1` = 0.167; con esos números la cuenta literal da 13.2 % para `reading` = 50 (la clave dice 13.4 %), 95.8 % para 80 (95.9 %) y momios de 22.9 (23.4). (e) La clave del refuerzo escribe `z` = −0.192 para 60 y 1.480 para 70; el notebook da −0.1929 y 1.4792 (−0.193 y 1.479). Conviene pedir 5 decimales (`b1` = 0.16721) o aceptar ±0.0001.
4. **Error en la clave: «45.2 % → 49.7 %».** `02` (Paso 5) y `03` (Ejercicio 5c) dicen que entre `reading` 60 y 61 la probabilidad sube de 45.2 % a 49.7 % (4.5 puntos). Con los coeficientes completos pasa a 49.4 % (+4.2 puntos); con los redondeados, a 49.3 %, y el propio Excel (hoja `Paso5_OddsRatio`, celda F10) muestra 4.2 %. El mensaje de la clave sí es correcto: entre 40 y 41 solo sube 0.5 puntos (2.8 % → 3.3 %).
5. **Falsos negativos: la polaridad de la clave de `03` (Ejercicio 6c).** Define bien los 72 falsos negativos (el modelo dice «no aprueba» y aprueba), pero el ejemplo de riesgo mezcla las polaridades: dejar sin ayuda a quien sí va a reprobar es un falso **positivo** del modelo (dice «aprueba» y no aprueba; son 96, más que los 72). La analogía médica sirve si la clase positiva es «enfermo», no «aprueba». Conviene decir qué clase se llama positiva antes de hablar de costos; con «no aprueba» como positiva, la sensibilidad es 0.703 y la precisión 0.759.
6. **Reto final de `writing` (clave de `02` y hoja `Reto_WritingScore`).** (a) Compara los OR por punto (1.182 contra 1.159) y concluye «ligeramente más fuerte»; con escalas distintas (14.60 y 15.20 puntos de desviación) el OR por desviación es 11.49 contra 9.43, y el AIC difiere en 31.8 (737.76 contra 769.58), AUC 0.8999 contra 0.8881: la diferencia es clara. (b) Con `writing` = 65 la clave da `z` = 0.8129 y P = 69.3 %, pero con los coeficientes completos son 0.8102 y 69.2 %. (c) El Excel escribe `b0` y `b1` de `writing` a mano (no se calculan en la hoja).
7. **El notebook de la clave del refuerzo promete una comprobación que no hace.** El Ejercicio 3.2 dice que subir el umbral sube la precisión y baja el recall «como se comprueba numéricamente en el Paso 4», pero el Paso 4 solo calcula el umbral 0.5. La conclusión es cierta (sección 6.2: con t = 0.8, precisión 0.930 y sensibilidad 0.705) pero no está calculada en los materiales.
8. **Diapositivas.** (a) La diapositiva 20 dice que con un OR de 1.04 «la probabilidad de enfermar se multiplica por 1.04 por cada año más»: se multiplican los **momios**, no la probabilidad; es el error que la clave de `02` pide corregir en el Paso 5. (b) La diapositiva 21 (69 %, es decir, `z` = 0.80) y la 22 (36 personas: 11 + 15 = 26 aciertos = 72.2 %; precisión y sensibilidad 75 %) vienen de un video; sus coeficientes no están en la presentación, así que el 69 % no se puede reproducir. (c) La «prueba chi-cuadrado» de la diapositiva 23 es la razón de verosimilitud del `summary()` (`LLR p-value`, 4.5e-116); en los talleres solo la menciona una nota del profesor. (d) Las diapositivas y `01` §5 tienen flujos distintos: la presentación habla de tabla de clasificación y chi-cuadrado; `01` agrega umbral y colinealidad.
9. **«Aprueba» es una etiqueta didáctica.** `math` ≥ 60 es un corte elegido; `math` es numérica y dicotomizarla descarta información (la regresión lineal sobre `math` tiene R² = 0.668). Con 50 aprueban 865 (86.5 %) y el modelo supera la línea base por solo 2.8 puntos (0.893 contra 0.865); con 70 aprueban 409 y el corte de `reading` pasa a 73.76. El OR se mantiene en 1.17 a 1.18.
10. **Todas las métricas de los materiales son de entrenamiento.** La exactitud de 83.2 % y la matriz se calculan con los mismos 1 000 estudiantes; no hay partición. Con una variable no hay sobreajuste (validación cruzada 0.8307), pero una sola partición 80 / 20 puede dar de 0.755 a 0.920 (desviación 0.024) y la semilla 42 da 0.835 sin estratificar y 0.820 estratificada.
11. **«p = 0.000» y las dos pruebas «4.5e-…».** El `summary()` imprime 0.000 para el Wald de `reading` (real: 4.5e-53) y el `LLR p-value` (4.5e-116) es otra prueba: χ² = 524.46 contra z² = 235.13. Coinciden las dos primeras cifras por casualidad; el Wald es una aproximación y la razón de verosimilitud es la prueba preferida para el modelo completo. En el informe, escribir «p < 1e-50» y no «p = 0».
12. **Colinealidad: qué se mueve y qué no.** `01` §7 dice que los coeficientes «pueden cambiar mucho si agregas o quitas un estudiante». Con 1 000 remuestreos, la desviación del coeficiente de `reading` se multiplica por 2.3 (de 0.0106 a 0.0240; el error estándar de Wald, por 2.03) y el de `writing` es negativo en el 3.1 % de las muestras, pero el signo de `reading` nunca cambia y la predicción (AUC 0.900) no empeora. La conclusión de la clave («casi no mejora») es correcta; la advertencia de «signo» es exagerada, igual que en la Semana 7.
13. **Notebook de variables categóricas.** (a) La sección 6 imprime 12 columnas *dummy* «para las 4 categóricas», pero las cuatro nombradas (género, etnia, educación y almuerzo) suman 11; las 12 incluyen el curso, y la solución del Ejercicio 2 dice 11. (b) El curso tiene OR 1.81 en crudo y 0.60 en el modelo, y solo es significativo (p = 0.038) cuando el género está incluido; con `reading` y curso, p = 0.320. La advertencia del notebook es correcta, pero conviene mostrar este cambio de signo. (c) El OR de género (0.033) es tan pequeño porque controla `reading`, que es mayor en las mujeres: en crudo, mujer 62.0 % contra hombre 73.9 %. (d) El 88.3 % es de entrenamiento, aunque la validación cruzada (0.882) confirma que no es sobreajuste. (e) «Todos con p < 0.05»: el del curso (0.038) está al límite.
14. **Excel `Taller_regresion_logistica_calculos.xlsx`.** Los coeficientes están escritos a mano y las fórmulas usan los redondeados (4 decimales); la hoja `Paso4_Estudiantes` toma `math score` = 50 escrito a mano para «la fila con `reading` = 50» (correcto para la primera fila, índice 182; pero de los 7 estudiantes con `reading` = 50, uno aprobó con 64 y el modelo acierta 6). Los porcentajes se muestran con formato de un decimal.
15. **Referencias y archivos que fallan.** (a) `Matematicas/regresion_logistica_paso_a_paso.ipynb` y `regresion_variables_categoricas.ipynb` citan `Semana_7/Matematicas/regresion_lineal_paso_a_paso.ipynb`, que vive en `Semana_8/Matematicas/`. (b) `Matematicas/lr_sklearn.py` abre `/Semana_8/StudentsPerformance.csv` (ruta absoluta): falla con `FileNotFoundError`; además es de regresión lineal y su enlace de Platzi no se verificó. (c) En `Evaluacion/` hay nombres viejos: `03_Evaluacion_explicacion_estudiante.md` (hoy `02_Evaluacion_desarrollo.md`), `02_Evaluacion_8_clave_respuestas.md` (hoy `..._profesor.md`) y `03_Regresion_Lineal_Vs_Regresión Logística.md` (hoy `04_Regresion_Lineal_Vs_Regresion_Logistica.md`); los textos funcionan, los nombres no. (d) El notebook de estudiante `02_Evaluacion_taller.ipynb` termina nombrando las claves `*_profesor` (ignoradas por Git): no se abren en GitHub y delatan dónde están las respuestas. (e) No se revisaron enlaces externos (`numiqo.com`, YouTube) ni el repositorio interactivo. (f) Los materiales dicen «NRC 94103» y la carpeta es `NRC-70446`.
16. **Asociación, no causalidad; sin extrapolar.** El modelo asocia lectura con aprobar matemáticas; no dice que leer mejor haga aprobar. El efecto de género (con la lectura fija) y el cambio de signo del curso muestran que un coeficiente depende de las demás variables del modelo. Fuera de 17 a 100 no hay datos, y en las colas casi no hay variación (27 sin aprobados con `reading` ≤ 40; 79 que aprueban todos con ≥ 90).
