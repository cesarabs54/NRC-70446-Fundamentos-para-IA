# Semana 2 — Cuadro técnico consolidado

**Tema:** Python para ciencia de datos con pandas: carga de datos, exploración (EDA), diagnóstico de calidad, limpieza básica, agregación y primeras visualizaciones.
**Actividad calificada:** estudio de caso colaborativo «Consulta en un *Dataset*» (`EIARV011_A2`, 5.0 puntos: presentación 0.5 + análisis del dataset 1.5 + calidad de datos 1.5 + Python 1.5). Se entrega un PDF y el enlace público al notebook (Colab o Jupyter). La guía de la sesión pide además un notebook individual con `StudentsPerformance.csv` u otro dataset propio de al menos 5 columnas y 30 filas (ejecuta sin error, decisiones de limpieza documentadas, código legible); en el repositorio no hay rúbrica numérica para ese entregable.
**Datasets de la semana:**

| Archivo | Dónde se usa | Tamaño |
|---|---|---|
| `StudentsPerformance.csv` | Actividad A2 y Taller 01 | 1 000 × 8: tres notas de 0 a 100 y cinco categóricas. Sin nulos ni duplicados |
| `credits.csv` | Taller 02 | 77 801 × 5 (5 489 títulos, 54 589 personas). Es el mismo archivo de la Semana 4 (idéntico byte a byte) |
| Ventas simuladas y DataFrame de 8 estudiantes | Taller 04 y Ejemplos | 500 filas y 8 filas, generados en la propia celda |

> Todas las cifras de este documento se recalcularon ejecutando el código (Python 3.11.9, pandas 2.3.3 y, para comprobar compatibilidad, pandas 3.0.6; NumPy 2.4.6, Matplotlib 3.11.2, seaborn 0.13.2). Las marcadas con ✅ son las que ya aparecen en los notebooks y claves del profesor (`EIARV011_A2_analisis_profesor.ipynb`, `EIARV011_A2_informe_estudio_de_caso.md`, `Taller_01_EDA_solucion.ipynb` y `Taller_02_EDA_profesor.ipynb`); las marcadas con ➕ son alternativas que se pueden aplicar y que **no** están en esos materiales. El Taller 04 solo tiene guía del estudiante (sin clave): sus cifras son recalculadas y no llevan marca.
>
> Esta semana no hay estadística inferencial (SciPy llega en las Semanas 4 y 5), así que la sección 3 reemplaza el «cuadro de pruebas» por un cuadro de funciones de pandas y NumPy.

---

## 1. Procedimientos de la actividad (de punta a punta)

| Etapa | Librería | Procedimiento / funciones | Para qué sirve | Ejemplo en la actividad |
|---|---|---|---|---|
| Carga | Pandas | `read_csv`, `head()` | Leer el archivo y ver las primeras filas | `StudentsPerformance.csv` → 1 000 filas × 8 columnas. El archivo del repositorio trae **todos** los campos entre comillas (también las notas); pandas igual las lee como `int64` |
| Tamaño y nombres | Pandas | `shape`, `columns` | Saber cuántos datos y qué variables hay | (1000, 8): `gender`, `race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`, `math score`, `reading score`, `writing score` |
| Tipos de datos | Pandas | `dtypes`, `info()` | Separar numéricas de categóricas y ver los no nulos | 3 `int64` + 5 de texto (`object` en pandas 2.x, `str` en 3.x); 1 000 no nulos en las 8 |
| Resumen general | Pandas | `describe()` | Media, desviación, cuartiles, mínimo y máximo | `math` 66.09 / 15.16 · `reading` 69.17 / 14.60 · `writing` 68.05 / 15.20 (media / desviación) |
| Diccionario de datos | Pandas + criterio | `nunique()`, `unique()`, tabla manual | Naturaleza, formato y propósito de cada columna | `gender` 2 categorías, `race/ethnicity` 5, `parental level of education` 6 (ordinal), `lunch` 2, `test preparation course` 2; tres notas enteras de 0 a 100 |
| Nulos | Pandas | `isnull().sum()` | Detectar datos faltantes | 0 en las 8 columnas |
| Duplicados | Pandas | `duplicated().sum()` | Detectar filas repetidas | 0. Sin un identificador de estudiante, «duplicado» solo puede significar fila completa idéntica |
| Inconsistencias lógicas | Pandas | `min()`, `max()`, `str.strip()`, `nunique()` | Valores fuera de escala o categorías mal escritas | Las 3 notas están dentro de [0, 100]; 0 espacios sobrantes; sin variantes de mayúsculas (✅ en el informe, ➕ como código) |
| Atípicos | Pandas | `quantile`, regla 1.5 × IQR | Marcar casos a revisar | `math`: Q1 57, Q3 77, IQR 20, límites [27; 107] → 8 atípicos (0, 8, 18, 19, 22, 23, 24, 26). Los 8 son mujeres, 7 con almuerzo `free/reduced` y 7 sin curso |
| Boxplot | Seaborn | `sns.boxplot(x=...)` | Confirmar visualmente los atípicos | Solo se grafica `math score` |
| Frecuencias | Pandas | `value_counts()`, `normalize=True` | Frecuencia y porcentaje de cada categoría | `gender` 518 / 482 (51.8 % / 48.2 %); `test preparation course` 642 / 358 (64.2 % / 35.8 %) |
| Estadísticos numéricos | Pandas | `describe()` | Resumir las notas | Ver fila «Resumen general» (el notebook solo imprime `math` y `reading`) |
| Distribución | Matplotlib | `df[cols].hist(bins=15)` | Ver la forma de cada nota | Las tres son aproximadamente simétricas (sesgo −0.28, −0.26, −0.29) |
| Relaciones | Pandas | `corr()`, `groupby().mean()` | Asociación entre notas y entre categoría y nota | Lectura–escritura 0.955 · mate–lectura 0.818 · mate–escritura 0.803. Curso → `math`: 64.08 (`none`) vs. 69.70 (`completed`) |
| Variable derivada | Pandas | `mean(axis=1)` | Un indicador compuesto por estudiante | `average score`: media 67.77, mínimo 9, máximo 100. Por nivel educativo de los padres: de 63.10 (`high school`) a 73.60 (`master's degree`) |
| Informe | Redacción | 6 preguntas del anexo | Convertir los hallazgos en texto | Ver sección 4 |
| Entrega | — | PDF + enlace Colab con permiso de visualización | Condición de admisibilidad del checklist | Nombre: `primerapellido_primernombre_nombredelaactividad` |

---

## 2. Qué gráfico usar

| Pregunta | Gráfico (función) | Ejemplo con el dataset | Cuidado al leerlo | Uso |
|---|---|---|---|---|
| ¿Cuántos casos hay de cada categoría? | Barras · `value_counts().plot(kind="bar")` | `gender` 518 / 482; curso 642 / 358 | `value_counts()` ordena por frecuencia: en una ordinal (`parental level of education`) se pierde el orden natural; usar `.loc[orden]` | ✅ |
| ¿Cómo se distribuye una numérica? | Histograma · `df[cols].hist(bins=15)` | `math`: los dos bins más altos (184 y 173 estudiantes) cubren 60 a 73 | Con 3 columnas dibuja una grilla 2 × 2 con un cuadro vacío. El número de *bins* cambia la historia: con 5 el pico es 484; con 15, 184; con 20, 144 | ✅ |
| ¿Hay atípicos? | Boxplot · `sns.boxplot(x=...)` | `math`: 8 puntos bajo el bigote inferior; `reading`: 6; `writing`: 5 | Graficar solo `math` deja la impresión de que es la única con atípicos (salvedad 1) | ✅ (math) / ➕ |
| ¿Cómo se compara una numérica entre grupos? | Boxplot por grupo · `sns.boxplot(data=df, x="lunch", y="math score")` | `standard`: Q1 61, mediana 69, Q3 80. `free/reduced`: Q1 49, mediana 60, Q3 69 | Muestra la diferencia, no prueba que sea real (eso es Semana 5) | ➕ |
| ¿Hay relación entre dos numéricas? | Dispersión · `sns.scatterplot` | Lectura vs. escritura: nube diagonal estrecha (r = 0.955) | Las notas son enteras: muchos puntos se superponen; usar `alpha` | ➕ |
| ¿Qué tan fuertes son todas las correlaciones juntas? | Mapa de calor · `sns.heatmap(df[notas].corr(), annot=True)` | Matriz 3 × 3 con valores de 0.803 a 0.955 | Con 3 variables una tabla alcanza | ➕ |
| ¿Cómo se compara un promedio entre grupos? | Barras de `groupby().mean()` | Curso → `math`: 64.08 vs. 69.70. Almuerzo → `math`: 58.92 vs. 70.03 | El notebook imprime la tabla pero no la grafica | ➕ |

---

## 3. Funciones de pandas y NumPy que se pueden aplicar

### 3.1 Cuadro de funciones (StudentsPerformance)

| Pregunta | Función | Cuándo usarla / supuestos | Ejemplo con el dataset | Uso |
|---|---|---|---|---|
| ¿Cuántos datos y de qué tipo? | `shape`, `dtypes`, `info()` | Siempre lo primero | 1 000 × 8: 3 `int64` + 5 texto | ✅ |
| ¿Qué valores distintos hay? | `unique()`, `nunique()` | Detecta errores de captura («Ing. Software» vs. «ing software») | `gender` 2, `race/ethnicity` 5, `parental level of education` 6, `lunch` 2, `test preparation course` 2 | ✅ |
| ¿Faltan datos? | `isnull().sum()` | Antes de promediar o modelar | 0 nulos | ✅ |
| ¿Hay filas repetidas? | `duplicated().sum()` | Fila completa; con un ID se puede afinar | 0 | ✅ |
| ¿Los valores están en el rango del dominio? | `min()`, `max()`, `between(0, 100)` | Reglas de negocio | 1 000 de 1 000 notas en [0, 100]. Un solo 0 (fila 59: 0 / 17 / 10). Con 100: 7 en `math`, 17 en `reading`, 14 en `writing` | ➕ |
| ¿El texto es consistente? | `str.strip()`, `str.lower()` + `nunique()` | Comparar el número de categorías antes y después | 0 espacios sobrantes; el conteo no cambia | ➕ |
| ¿Cuáles son atípicos? | **IQR 1.5×** · `quantile` | Robusto; recomendado por el anexo («al menos 1 variable») | `math` 8 (0, 8, 18, 19, 22, 23, 24, 26) · `reading` 6 (17, 23, 24, 24, 26, 28) · `writing` 5 (10, 15, 19, 22, 23). 12 estudiantes distintos; 2 lo son en las tres notas (filas 59 y 980) | ✅ (math) / ➕ |
| ¿Atípicos según z-score o MAD? | `(x - x.mean()) / x.std()` > 3 · MAD modificado > 3.5 | z-score asume forma simétrica; MAD es robusto | z > 3: 4 / 4 / 4. MAD > 3.5: 2 / 1 / 1 (math / reading / writing). El IQR marca más porque las tres notas tienen cola izquierda | ➕ |
| ¿Cuántos hay de cada categoría? | `value_counts()`, `normalize=True` | Categóricas | `race/ethnicity`: C 31.9 %, D 26.2 %, B 19.0 %, E 14.0 %, A 8.9 %. `lunch`: 64.5 % `standard`. `parental level of education`: `some college` 22.6 %, `associate's` 22.2 %, `high school` 19.6 %, `some high school` 17.9 %, `bachelor's` 11.8 %, `master's` 5.9 % | ✅ (gender, curso) / ➕ |
| ¿Dato típico y dispersión? | `describe()`, `mode()`, `std()` | Numéricas | Moda: 65 / 72 / 74. Coeficiente de variación: 0.229 / 0.211 / 0.223 (math / reading / writing) | ✅ / ➕ |
| ¿Qué forma tiene? | `skew()`, `kurt()` | Media ≈ mediana no basta | Sesgo: −0.28, −0.26, −0.29. Curtosis (exceso): 0.27, −0.07, −0.03 → leve cola hacia notas bajas | ➕ |
| ¿Hay relación lineal? | `corr()` (Pearson) | Dos numéricas, sin atípicos extremos | 0.955 (lectura–escritura), 0.818 (mate–lectura), 0.803 (mate–escritura). Sin la fila 59: 0.815 y 0.799 (mate con lectura y con escritura) | ✅ |
| ¿Hay relación monótona? | `rank().corr()` (o `corr(method="spearman")`) | Sesgo, atípicos u ordinales. La opción `method="spearman"` **requiere SciPy** (salvedad 17) | 0.949, 0.804, 0.778 en los mismos tres pares | ➕ |
| ¿Cuánto cambia una nota según el grupo? | `groupby().mean()`; `agg(["mean", "median", "std", "count"])` | Categórica vs. numérica | Curso: `math` +5.6, `reading` +7.4, `writing` +9.9 a favor de `completed`. Almuerzo: +11.1 / +7.0 / +7.8 a favor de `standard` | ✅ (mean) / ➕ |
| ¿Es grande esa diferencia? | d de Cohen · `(m1 - m2) / s_pooled` | Diferencia de medias en unidades de desviación | Curso: 0.38 / 0.52 / 0.69. Almuerzo: 0.78 / 0.49 / 0.53. Género (mujeres − hombres): −0.34 / 0.50 / 0.63 (math / reading / writing) | ➕ |
| ¿Cuánta variación explica una categórica? | η² · `SS_entre / SS_total` | Compara variables entre sí | Sobre `average score`: `lunch` 8.4 %, curso 6.6 %, nivel educativo 5.1 %, etnia 3.5 %, género 1.7 %. Sobre `math`: `lunch` 12.3 %, etnia 5.5 %, nivel 3.2 %, curso 3.2 %, género 2.8 % | ➕ |
| ¿Dos categóricas se asocian? | `pd.crosstab` | Tabla de frecuencias | Género × curso: 184 / 334 mujeres y 174 / 308 hombres (`completed` / `none`) → 35.5 % vs. 36.1 % completaron. Almuerzo × curso: 36.9 % (`free/reduced`) vs. 35.2 % (`standard`) | ➕ |
| ¿Cómo creo una variable nueva? | `mean(axis=1)`, `pd.cut`, `apply` | Derivadas de las existentes | `average score` ✅. `pd.cut` de `math` en tramos de 10: 150 (≤ 50), 189, 270, 215, 126, 50 (90–100). Aprobar con ≥ 60 en `math`: 67.7 % (75.7 % con curso vs. 63.2 % sin curso) | ✅ / ➕ |
| ¿Cómo respeto el orden de una ordinal? | `pd.Categorical(..., ordered=True)`, `.loc[orden]` | Niveles con orden natural | `some high school` 65.11 → `high school` 63.10 → `some college` 68.48 → `associate's` 69.57 → `bachelor's` 71.92 → `master's` 73.60. Spearman con el nivel codificado de 0 a 5: 0.187 | ➕ |

### 3.2 Funciones de los Talleres 02 a 04

| Pregunta | Función | Cuándo usarla / supuestos | Ejemplo | Uso |
|---|---|---|---|---|
| ¿Cómo construyo una numérica a partir de filas? | `groupby().size()` | Cuando el dataset solo trae identificadores (`credits.csv`) | `cast_size`: actores por título | ✅ |
| ¿Cómo filtro y verifico? | `df[df[col] == v]`, `.unique()` | Después de filtrar, comprobar que quedó solo lo esperado | Ejemplos de clase: `df[df["ciudad"] != "Bogotá"]` también devuelve a Iván, cuya ciudad es `NaN` | — |
| ¿Cómo resumo por categoría? | `groupby().mean()` / `sum()` / `agg()` + `reset_index()` | Elegir la agregación según el tipo de dato | Ejemplos B1 a B5: `groupby("programa")["nota_final"]` → Industrial 3.40, Sistemas 4.55, Software 3.30 (n = 3: el `NaN` se omite). Ventas: ticket promedio por región | — |
| ¿Cómo imputo? | `fillna(valor)`, `transform("median")` | Mediana si hay sesgo; por grupo si la variable depende de otra; moda o «Sin dato» en texto | Ejemplos de clase: `nota_final` con la media (3.686), `ciudad` con un valor fijo, `semestre` con la mediana (5.0) | — |
| ¿Cómo combino tablas? | `merge(on=..., how="left")` + `assert len(...)` | Verificar que no duplicó ni perdió filas | Ventas × clientes: 500 filas antes y después | — |
| ¿Cómo mido tiempos? | `time.perf_counter()` | `time.time()` tiene resolución de 15.6 ms en Windows (salvedad 15) | Lazo 9.83 ms vs. vectorizado 0.089 ms | — |

### 3.3 Guía rápida para elegir

| Si quiero… | Variable numérica | Variable categórica |
|---|---|---|
| Resumirla | `describe()`, media, mediana, desviación | `value_counts(normalize=True)` |
| Ver su forma | Histograma + `skew()` | Barras (respetando el orden si es ordinal) |
| Detectar rarezas | IQR / z-score / MAD + boxplot | Categorías con menos del 1 % o variantes de escritura |
| Relacionarla con otra | `corr()` o `rank().corr()` + dispersión | `crosstab` |
| Comparar grupos | `groupby().agg(...)`, boxplot por grupo, d de Cohen | `crosstab(normalize="index")` |
| Tratar faltantes | Mediana (si hay sesgo), mediana por grupo, o indicador de «faltaba» | Moda o «Sin dato» |

Regla práctica: antes de imputar, preguntarse si los faltantes son aleatorios. En `credits.csv`, 4 550 de los 9 772 nulos de `character` son directores, que no tienen personaje: son faltantes estructurales, no un olvido. Rellenarlos con «Sin dato» mezclaría «no aplica» con «no se registró» (los otros 5 222 son actores).

---

## 4. Las preguntas del anexo y su evidencia

| Pregunta del anexo | Qué responde el informe de referencia | Evidencia en código | Qué se podría añadir (➕) |
|---|---|---|---|
| 1. ¿Qué fenómeno representa? | Rendimiento de 1 000 estudiantes en 3 pruebas y su relación con factores demográficos y socioeducativos | `shape`, `dtypes`, `head()` ✅ | Aclarar que son 1 000 filas sin identificador: no se puede seguir a un estudiante ni descartar duplicados lógicos |
| 2. ¿Cuáles son las 5 variables más importantes? | Las 3 notas + `test preparation course` + `parental level of education` | `groupby().mean()` ✅ | η² y d de Cohen (sección 3.1): `lunch` pesa más que el curso y que el nivel educativo (salvedad 3) |
| 3. ¿Qué hallazgos hay en la distribución? | Género equilibrado (51.8 / 48.2), curso desbalanceado (64.2 % sin curso), etnia C 31.9 % vs. A 8.9 %; notas simétricas con medias 66–69 y desviación ≈ 15 | `value_counts`, `describe`, `hist` ✅ | `skew()` y `kurt()`; IQR en las tres notas |
| 4. ¿Qué relaciones hay? (mínimo 2) | Correlaciones 0.955 / 0.818 / 0.803; curso +5.6 / +7.4 / +9.9; almuerzo 70.8 vs. 62.2 en el promedio | `corr()`, `groupby().mean()` ✅ | Spearman, d de Cohen, `crosstab` género × curso (las mujeres puntúan +7 en `reading` y +9 en `writing`, pero −5 en `math`) |
| 5. ¿Qué problemas de calidad hay y cómo se abordan? | 0 nulos, 0 duplicados, 8 atípicos en `math` (un 0), nombres con espacios y `/` | `isnull`, `duplicated`, IQR ✅ | Atípicos en `reading` y `writing`; ver que los 12 casos son mujeres en su mayoría (8 de 12), con almuerzo reducido (10 de 12) y sin curso (11 de 12), lo que sugiere desempeño real y no error de captura |
| 6. ¿Qué problema de IA podría plantearse? | Regresión de `math score`; clasificación aprobado/no aprobado; *clustering* de perfiles | — | Con `math` ≥ 60 como umbral el 67.7 % aprueba (clases moderadamente desbalanceadas) |

---

## 5. Taller 01 — EDA con `StudentsPerformance.csv`

| Ejercicio | Solución del profesor | Resultado recalculado | Observación |
|---|---|---|---|
| 1.1 `gender` | `value_counts()` + `normalize=True` | `female` 518 (51.8 %), `male` 482 (48.2 %) ✅ | Equilibrado |
| 1.2 `test preparation course` | Igual | `none` 642 (64.2 %), `completed` 358 (35.8 %) ✅ | Relación 1.8 : 1; el grupo `completed` es suficientemente grande (358) |
| 1.3 Barras lado a lado | `plt.subplots(1, 2)` + `plot(kind="bar", ax=axes[i])` | Dos paneles ✅ | Error común: olvidar `ax=` (genera dos figuras) |
| 2.1 `describe()` de `math` | Media ≈ mediana ≈ 66 | media 66.09, mediana 66, std 15.16, mín 0, Q1 57, Q3 77, máx 100 ✅ | Sesgo −0.28: simétrica con cola izquierda leve |
| 2.2 Histogramas, 15 bins | Forma de campana con pico entre 60 y 75 | `math`: 184 y 173 en los dos bins centrales ✅ | Correcto; el ancho del bin es 6.67 puntos |
| 2.3 `describe()` de las tres | «`math` tiene mayor `std` y rango» | std: `math` 15.163, `reading` 14.600, `writing` **15.196**. Rango: `math` 100, `writing` 90, `reading` 83 | Mayor rango: `math`; mayor dispersión: **`writing`** (salvedad 8) |
| Reto (`groupby`) | `lunch` o `parental level of education` | `lunch`: 70.03 vs. 58.92 (+11.11). Nivel educativo → `math`: `master's` 69.75, `bachelor's` 69.39, `associate's` 67.88, `some college` 67.13, `some high school` 63.50, `high school` 62.14 ✅ | Correlación no es causalidad |

---

## 6. Taller 02 — EDA con `credits.csv`

| Ejercicio | Clave del profesor | Resultado recalculado | Observación |
|---|---|---|---|
| 1.1 `role` | ACTOR 73 251 (≈ 94.2 %) · DIRECTOR 4 550 (≈ 5.8 %) | Igual: 94.15 % / 5.85 % ✅ | Desbalance estructural, no de muestreo |
| 1.2 `name` top 10 | — | Kareena Kapoor Khan 25, Boman Irani 25, Shah Rukh Khan 23, Takahiro Sakurai 21, Amitabh Bachchan 20, Raúl Campos 20, Priyanka Chopra Jonas 20, Paresh Rawal 20, Anupam Kher 19, Yuki Kaji 19. El 77.8 % de los nombres (42 252 de 54 314) aparece una sola vez ✅ | `name` no identifica personas (salvedad 10) |
| 2.1 `cast_size` | count ≈ 5 340, media ≈ 13.7, std ≈ 14.9, mediana 10, máx 207 | count 5 340, media 13.72, std 14.87, mín 1, Q1 5, mediana 10, Q3 17, máx 207 ✅. Sesgo 3.30, curtosis 19.38, P95 42, P99 73 | Sesgo a la derecha (media > mediana) |
| 2.2 Histograma, 30 bins | Cola larga a la derecha | El primer bin concentra 2 117 de 5 340 títulos (39.7 %); 79.5 % tiene menos de 20 actores; 380 atípicos por IQR (> 35) ✅ | Con `np.log1p` el sesgo baja de 3.30 a −0.10 ➕ |
| 2.3 `director_size` | count ≈ 4 041, media ≈ 1.13, std ≈ 0.45, máx 11 | count 4 041, media 1.126, std 0.454, máx 11 ✅ | El 89.8 % de los títulos con director tiene uno solo |
| Reto: top 10 de reparto | 207, 173, 160, 137, 137, 135, 128, 126, 117, 115 | Igual ✅ (`tm32982`, `tm244149`, `tm39888`, …) | Todos son `tm` (películas) |
| Calidad (no está en la clave) | — | `character`: 9 772 nulos = 4 550 directores + **5 222 actores**. 0 duplicados exactos; 88 combinaciones (persona, título, rol) repetidas con personajes distintos | Ver salvedades 9 a 12 |

---

## 7. Taller 04 (ventas simuladas) y ejemplos de clase

### 7.1 Ventas simuladas (semilla 7)

| Actividad | Resultado recalculado | Lectura |
|---|---|---|
| 1. Producto más vendido por región | Centro: Laptop 62 940 000 · Norte: Mouse 69 040 000 · Oriente: Laptop 70 570 000 · Sur: Audifonos 49 255 000 | Es ruido: cada producto aparece con los 5 precios (salvedad 14) |
| 1. Preguntas propias | Cliente con mayor gasto: 1 (20 320 000), luego 98 y 30. Ticket promedio por región: Oriente 2 141 016 · Norte 1 927 177 · Centro 1 863 661 · Sur 1 701 653 | Ejemplos de `groupby` + `agg` |
| 2. `merge` | 500 filas antes y después; 0 nulos tras el `merge`. Corporativo: 237 ventas, suma 467 145 000, media 1 971 075.9. Retail: 263 ventas, suma 488 460 000, media 1 857 262.4. Total 955 605 000 | El `assert` pasa |
| 4. Lazo vs. vectorizado | Mediana de 20 corridas: lazo 9.83 ms, vectorizado 0.089 ms → 111× (entre 85× y 131×) | Con `time.time()` en Windows falla (salvedad 15) |

### 7.2 Ejemplos de clase (DataFrame de 8 estudiantes)

| Ejemplo | Resultado verificado | Observación |
|---|---|---|
| 0 y 1 | (8, 5). Nulos: `semestre` 1, `nota_final` 1, `ciudad` 1. `describe()` solo muestra `semestre` y `nota_final` (count 7) | Responde la pregunta de clase sobre `programa` |
| 3 filtros | Aprobaron: Ana, Luis, Iván, Pedro (3.0), Elena. Software y aprobaron: Ana. «No son de Bogotá»: Ana, Marta, **Iván** (ciudad `NaN`), Pedro, Elena | `NaN != "Bogotá"` es `True` |
| 4 | `ciudad.value_counts()`: Cúcuta 3, Bogotá 3, Medellín 1 (7 de 8: ignora el `NaN`) | |
| 5 | `dropna()` deja 5 de 8 filas. Media de `nota_final` 3.686; mediana de `semestre` 5.0 | Tres estrategias para tres columnas |
| 6 `apply` | Sin imputar, `NaN >= 3.0` es `False` y Sofía queda «Reprobado»; imputando la media (3.69) queda «Aprobado» | Ambas son información inventada (salvedad 16) |
| A1 y A2 (NumPy) | Media 21.17; 3 mayores de 21; en meses `[228 264 240 300 216 276]`; posiciones pares `[19 20 18]`; mayores de 20 `[22 25 23]` | |
| A4 | Semestre ≥ 5 y reprobados: **vacío** (David, nota 2.5, tiene semestre `NaN`). No Bogotá y nota > 4.0: Ana, Iván, Elena | |
| A5 | 5 categorías; tras `lower()` + `strip()` quedan 4 (`cúcuta`, `cucuta`, `bogotá`, `bogota`); con acentos normalizados quedan 2 (`cucuta` 3, `bogota` 2) | Respuesta a la «pregunta de cierre» |
| B1 a B5 | `groupby("programa")`: Industrial 3.40 (máx 3.8, mín 3.0) · Sistemas 4.55 (5.0 / 4.1) · Software 3.30 (4.5 / 2.5; n = 3 porque el `NaN` se omite). `merge` con `ciudades_info`: Iván («Sin dato») queda sin región. Top 3 de `nota_final`: Iván 5.0, Ana 4.5, Elena 4.1 | |

---

## 8. Código listo para pegar

Los bloques suponen los CSV junto al notebook, como en las guías. Todos se ejecutaron sin error con pandas 2.3.3 y 3.0.6.

### 8.1 Actividad A2: EDA ampliado sobre `StudentsPerformance.csv`

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("StudentsPerformance.csv")
notas = ["math score", "reading score", "writing score"]
categoricas = [c for c in df.columns if c not in notas]

# 1) Comprensión y calidad
print(df.shape, df.isnull().sum().sum(), df.duplicated().sum())
print(df[notas].agg(["min", "max"]).T)                      # rango válido 0-100
for c in categoricas:                                        # variantes de texto
    print(c, df[c].nunique(), df[c].str.strip().str.lower().nunique())

# 2) Atípicos por IQR en las TRES notas (la solución solo mira math score)
def atipicos_iqr(s):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return s[(s < lo) | (s > hi)].sort_values(), (lo, hi)

for c in notas:
    atip, lims = atipicos_iqr(df[c])
    print(c, lims, len(atip), atip.tolist())

z = (df[notas] - df[notas].mean()) / df[notas].std()
mad = (df[notas] - df[notas].median()).abs().median()
mz = 0.6745 * (df[notas] - df[notas].median()) / mad
print((z.abs() > 3).sum().tolist(), (mz.abs() > 3.5).sum().tolist())

# 3) Forma, relación y tamaño del efecto
df["average score"] = df[notas].mean(axis=1)
print(df[notas].skew().round(2).tolist(), df[notas].kurt().round(2).tolist())
print(df[notas].corr().round(3))
print(df[notas].rank().corr().round(3))                     # Spearman sin SciPy

def cohen_d(a, b):
    sp = np.sqrt(((len(a) - 1) * a.var() + (len(b) - 1) * b.var()) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp

def eta2(col, y):
    g = df.groupby(col)[y]
    return (g.count() * (g.mean() - df[y].mean()) ** 2).sum() / ((df[y] - df[y].mean()) ** 2).sum()

for var, g1, g0 in [("test preparation course", "completed", "none"),
                    ("lunch", "standard", "free/reduced"),
                    ("gender", "female", "male")]:
    print(var, {c: round(cohen_d(df.loc[df[var] == g1, c], df.loc[df[var] == g0, c]), 2)
                for c in notas + ["average score"]})
print(pd.DataFrame({c: {y: round(eta2(c, y), 3) for y in notas + ["average score"]}
                    for c in categoricas}).T)
print(pd.crosstab(df["gender"], df["test preparation course"]))

# 4) Ordinal en su orden natural
orden = ["some high school", "high school", "some college",
         "associate's degree", "bachelor's degree", "master's degree"]
print(df.groupby("parental level of education")["average score"].mean().loc[orden].round(2))

# 5) Gráficos
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
sns.boxplot(data=df, x="lunch", y="math score", ax=ax[0])
sns.heatmap(df[notas].corr(), annot=True, vmin=0.5, vmax=1, ax=ax[1])
df["parental level of education"].value_counts().loc[orden].plot(kind="bar", ax=ax[2])
plt.tight_layout()
plt.show()
```

### 8.2 Taller 02: películas vs. series en `credits.csv`

```python
import pandas as pd

df = pd.read_csv("credits.csv")
df["tipo"] = df["id"].str[:2].map({"tm": "Película", "ts": "Serie"})   # tm = MOVIE, ts = SHOW

# cast_size por tipo (la clave del profesor los mezcla)
cast = (df[df["role"] == "ACTOR"].groupby(["tipo", "id"]).size()
        .rename("cast_size").reset_index())
print(cast.groupby("tipo")["cast_size"].describe().round(2))

# títulos que la clave descarta sin avisar
con_actores = df.loc[df["role"] == "ACTOR", "id"].nunique()
print("títulos sin actores:", df["id"].nunique() - con_actores)

# calidad
print(df["character"].isnull().groupby(df["role"]).sum())
print("nombres con más de un person_id:", (df.groupby("name")["person_id"].nunique() > 1).sum())
print("persona-título-rol repetidos:", df.duplicated(["person_id", "id", "role"]).sum())
```

Resultado: `Película` 3 541 títulos, media 16.72, mediana 12, máx 207; `Serie` 1 799 títulos, media 7.80, mediana 7, máx 48. 149 títulos sin actores. Nulos de `character`: 5 222 en ACTOR y 4 550 en DIRECTOR. 264 nombres con más de un `person_id`. 88 combinaciones repetidas.

### 8.3 Taller 04: ventas con precios coherentes y tiempos con `perf_counter`

```python
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
precios = {"Laptop": 1_200_000, "Mouse": 45_000, "Teclado": 90_000,
           "Monitor": 650_000, "Audifonos": 60_000}
n = 500
ventas = pd.DataFrame({
    "id_venta": range(1, n + 1),
    "producto": rng.choice(list(precios), n),
    "region": rng.choice(["Norte", "Sur", "Centro", "Oriente"], n),
    "unidades": rng.integers(1, 10, n),
    "id_cliente": rng.integers(1, 120, n),
})
ventas["precio_unitario"] = ventas["producto"].map(precios)      # un precio por producto
ventas["total"] = ventas["unidades"] * ventas["precio_unitario"]

resumen = ventas.groupby(["region", "producto"], as_index=False)["total"].sum()
print(resumen.sort_values("total", ascending=False).groupby("region").head(1))

t0 = time.perf_counter()
totales_loop = []
for i in range(len(ventas)):
    fila = ventas.iloc[i]
    totales_loop.append(fila["unidades"] * fila["precio_unitario"])
t_loop = time.perf_counter() - t0

t0 = time.perf_counter()
totales_vec = (ventas["unidades"] * ventas["precio_unitario"]).to_numpy()
t_vec = time.perf_counter() - t0
print(np.array_equal(totales_loop, totales_vec), f"~{t_loop / t_vec:.0f}x más rápido")
```

Con NumPy 2.4.6, Laptop lidera las cuatro regiones (Sur 146 400 000, Centro 140 400 000, Norte 139 200 000, Oriente 133 200 000). La razón de tiempos varía de una corrida a otra.

---

## 9. Salvedades que conviene conocer

**Actividad calificada (informe de referencia, rúbrica y archivos)**

1. **«`math score` es la única variable con valores atípicos».** El informe de referencia lo dice en la pregunta 2 (fila de `math score`), pero con la misma regla IQR salen 8 atípicos en `math score`, 6 en `reading score` (17, 23, 24, 24, 26, 28) y 5 en `writing score` (10, 15, 19, 22, 23). En total son 12 estudiantes distintos y 2 (filas 59 y 980) son atípicos en las tres notas. El notebook solo revisa `math score`, que es lo que pide el anexo («al menos 1 variable»); la frase del informe afirma más de lo que el código comprueba.
2. **«Relación consistente y gradual» de `parental level of education`.** En el orden natural, `some high school` (65.11) queda por encima de `high school` (63.10), así que la secuencia no es monótona (el resto sí sube: 68.48, 69.57, 71.92, 73.60). La asociación global es débil: Spearman 0.187 y η² = 5.1 % del promedio.
3. **Elección de las 5 variables.** El informe prioriza `test preparation course` sobre `lunch` por ser accionable (defendible) y llama «indirecta» a la medición de `lunch`. Por tamaño de efecto, `lunch` pesa más: η² del promedio 8.4 % frente a 6.6 %, y d de Cohen 0.63 frente a 0.55 (en `math`, 0.78 frente a 0.38). Conviene que la justificación diga «por accionable», no «por efecto».
4. **Cifras de `writing score` sin respaldo en el notebook de la actividad.** El informe cita media 68.05, desviación 15.20 y mínimo 10, pero `EIARV011_A2_analisis_profesor.ipynb` solo hace `describe()` de `math` y `reading`. Los valores sí salen en `Taller_01_EDA_solucion.ipynb`.
5. **Criterios de formato que el enunciado no fija.** La rúbrica puntúa el «número de páginas» según «el criterio solicitado» y el checklist exige Arial 11 e interlineado 1.5, pero ni `EIARV011_A2.md` ni el anexo indican páginas, tipo de letra ni interlineado.
6. **Encabezado del informe.** Dice «NRC 94103», deja vacío «Elaborado por» y fecha «Julio de 2026»; este repositorio es el NRC 70446. Conviene revisarlo si se reparte.
7. **Copias del dataset.** Las copias de `StudentsPerformance.csv` de la actividad, la solución, el Taller 01 y la Semana 6 son idénticas byte a byte. El `.xlsx`, el `.bak_semicolon` y la copia de una entrega usan el mismo contenido (verificado fila a fila), pero estas dos últimas separan con `;`: `read_csv` sin `sep=";"` devuelve **una sola columna** (1000, 1).

**Taller 01**

8. **Reflexión 4.** La clave dice que `math score` tiene la mayor desviación estándar, pero la salida del propio notebook muestra `writing` 15.196 > `math` 15.163 > `reading` 14.600 (diferencia de 0.03: prácticamente empate). Lo que sí es cierto es que `math` tiene el rango más amplio (0 a 100, frente a 90 y 83).

**Taller 02**

9. **«Por película» mezcla películas y series.** El notebook habla de «películas», pero los identificadores `tm` (película) y `ts` (serie) están mezclados: 3 541 películas y 1 799 series con actores. Las películas promedian 16.72 actores (mediana 12) y las series 7.80 (mediana 7). La correspondencia `tm` = MOVIE y `ts` = SHOW se verificó contra `titles.csv` de la Semana 4 (3 744 y 2 106 títulos). Además, 149 títulos tienen solo director y 1 448 no tienen director: `groupby` sobre un rol los descarta en silencio.
10. **`name` no identifica personas.** Hay 264 nombres con más de un `person_id` (homónimos, como «Akshay Kumar») y 15 nombres con espacios sobrantes. Para contar personas hay que usar `person_id` (el top 10 coincide por casualidad). Las 88 combinaciones (persona, título, rol) repetidas tienen personajes distintos: no son duplicados.
11. **`character` nulo.** Los 9 772 nulos son 4 550 directores y 5 222 actores; no son «los directores» (así lo afirma el cuadro de la Semana 4).
12. **No comparar con la Semana 4 sin mirar la definición.** El Taller 02 define `cast_size` solo con actores (5 340 títulos, media 13.72); la Semana 4 define `tamano_reparto` como `nunique(person_id)` por título con cualquier rol (5 489 títulos, media 14.10). Es el mismo CSV con otra variable.

**Guía de la sesión, Taller 04 y entorno**

13. **`fillna(method="ffill")` (guía, §6.3).** Da `FutureWarning` en pandas 2.3.3 y `TypeError` en 3.0.6: usar `.ffill()`. La guía (§9) también dice que `groupby` y `merge` se retoman «en la Semana 3», pero la Semana 3 trata de frameworks; reaparecen desde la Semana 4.
14. **Actividades 1 y 2: datos simulados incoherentes.** `producto` y `precio_unitario` se sortean por separado: cada producto aparece con los 5 precios («Mouse» a 1 200 000), así que «el producto más vendido por región» es ruido. Además, `clientes` se genera sin semilla propia: re-ejecutar solo esa celda cambia `ciudad` y `segmento`. Con una semilla única (`default_rng(7)`) y un precio por producto, Laptop lidera las cuatro regiones.
15. **Actividad 4: `time.time()` en Windows.** Con Python 3.11.9 su resolución es de 15.6 ms; en 49 de 50 mediciones vectorizadas dio exactamente 0.0, y `t_loop / t_vec` lanza `ZeroDivisionError` (en la prueba, 2 de 3 corridas). `time.perf_counter()` da 9.83 ms contra 0.089 ms (111×, entre 85× y 131×).
16. **Ejemplos de clase con `NaN`.** Imputar la media (3.69) a Sofía la deja «Aprobado» y no imputar la deja «Reprobado»: ninguna es un dato real. En `semestre`, un `NaN` cae en el `else` («Avanzado») de una función con `if/elif/else`. El filtro «semestre ≥ 5 y reprobó» devuelve vacío porque David tiene semestre `NaN`. Y `lower()` + `strip()` no unifican «Cúcuta» y «cucuta» (hace falta `str.normalize("NFKD")` o `unicodedata`).
17. **Spearman desde pandas.** `df.corr(method="spearman")` importa SciPy; sin SciPy da `ModuleNotFoundError` (en la imagen Docker llega con `scikit-learn`). `df.rank().corr()` da el mismo resultado sin esa dependencia.
