# Estudio de caso: Consulta en un *Dataset*

**Curso:** Fundamentos para Inteligencia Artificial (NRC 94103)
**Institución:** Universidad Minuto de Dios (UNIMINUTO)
**Docente:** Ing. César Alfonso Bolado Silva
**Elaborado por:** 
**Actividad:** Semana 2 – Estudio de caso colaborativo
**Fecha:** Julio de 2026

---

## 1. Objeto de estudio

El presente estudio de caso analiza el uso del lenguaje Python para la lectura, exploración y análisis de un archivo CSV correspondiente al *dataset* **Students Performance in Exams** (Kaggle, 2019), el cual contiene los resultados de 1000 estudiantes en tres pruebas estandarizadas: matemáticas, lectura y escritura, junto con variables demográficas y socioeducativas.

El problema a analizar consiste en comprender cómo se relacionan las variables categóricas (género, grupo étnico, nivel educativo de los padres, tipo de almuerzo y realización de un curso de preparación) con las variables numéricas (los tres puntajes) y en determinar la calidad e integridad de los datos antes de extraer conclusiones. Este ejercicio permite evidenciar, de forma práctica, el ciclo típico de un proyecto de ciencia de datos: carga de datos, exploración inicial, diagnóstico de calidad y análisis exploratorio.

## 2. Actores y contextos

**Actores involucrados:**

- **Estudiantes del curso (equipo colaborativo):** responsables de descargar el *dataset*, construir el *notebook* de análisis y redactar el informe.
- **Docente del curso:** orienta el uso de Python, aclara dudas y evalúa la actividad según la rúbrica.
- **Fuente de datos (Kaggle / autor del *dataset*):** provee el archivo `StudentsPerformance.csv` utilizado como insumo del análisis.

**Contexto tecnológico:**

El análisis se desarrolló en un *notebook* de Jupyter (compatible con Google Colab) usando Python 3 y las siguientes librerías:

- **pandas:** carga del CSV y manipulación tabular de los datos (`read_csv`, `describe`, `groupby`, `value_counts`).
- **numpy:** soporte numérico para los cálculos estadísticos.
- **matplotlib** y **seaborn:** visualización (histogramas, diagramas de caja, mapas de calor de correlación).

El entorno de trabajo corresponde a un equipo local con Python 3.11, en el cual se instalaron las dependencias (`pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`) mediante `pip`.

## 3. Objetivos

- Aplicar Python (librería *pandas*) para cargar y procesar un archivo CSV de datos educativos.
- Explorar y caracterizar cada una de las ocho columnas del *dataset*, identificando su tipo, formato y propósito.
- Diagnosticar la calidad de los datos (valores nulos, duplicados y atípicos) antes de realizar cualquier análisis.
- Analizar la distribución de las variables categóricas y numéricas más relevantes.
- Interpretar los resultados obtenidos para identificar tendencias y relaciones entre las variables, y plantear un posible problema predictivo a futuro.

## 4. Informe final

### 4.1 Comprensión de las variables (diccionario de datos)

El *dataset* tiene **1000 filas y 8 columnas**, sin valores nulos ni registros duplicados.

| Variable | Naturaleza | Formato | Propósito |
|---|---|---|---|
| `gender` | Categórica nominal | Texto: `female` / `male` | Sexo del estudiante |
| `race/ethnicity` | Categórica nominal | Texto: `group A`–`group E` | Grupo demográfico anonimizado |
| `parental level of education` | Categórica ordinal | Texto (6 niveles, de *some high school* a *master's degree*) | Máximo nivel educativo alcanzado por los padres/tutores |
| `lunch` | Categórica nominal | Texto: `standard` / `free/reduced` | Tipo de almuerzo recibido; se usa como aproximación (*proxy*) del nivel socioeconómico |
| `test preparation course` | Categórica nominal | Texto: `none` / `completed` | Indica si el estudiante completó un curso de preparación previo al examen |
| `math score` | Numérica discreta | Entero (0–100) | Puntaje obtenido en la prueba de matemáticas |
| `reading score` | Numérica discreta | Entero (0–100) | Puntaje obtenido en la prueba de lectura |
| `writing score` | Numérica discreta | Entero (0–100) | Puntaje obtenido en la prueba de escritura |

### 4.2 Diagnóstico de calidad de los datos

- **Valores nulos:** `df.isnull().sum()` reporta **0 nulos** en las 8 columnas; el *dataset* está completo.
- **Duplicados:** `df.duplicated().sum()` reporta **0 filas duplicadas**.
- **Valores atípicos:** aplicando el método de rango intercuartílico (IQR) sobre `math score` (Q1 = 57, Q3 = 77, IQR = 20), el límite inferior es 27. Se identificaron **8 registros** con puntajes de matemáticas por debajo de ese límite, incluyendo **un caso extremo con puntaje 0**, el único valor nulo/cero entre las tres pruebas. Este dato amerita verificación adicional (¿inasistencia, error de digitación o desempeño real?) antes de decidir si se conserva, se corrige o se excluye del análisis.
- **Inconsistencias lógicas:** todos los puntajes se encuentran dentro del rango válido (0–100), por lo que no se detectaron valores fuera de escala. Como observación menor, los nombres de columnas contienen espacios y el carácter `/` (p. ej. `race/ethnicity`), lo cual dificulta su uso directo en código; se recomienda normalizarlos (por ejemplo, a *snake_case*) antes de un análisis más avanzado.

### 4.3 Análisis por variable

**Variables categóricas**

| Variable | Categoría | Frecuencia | Porcentaje |
|---|---|---|---|
| `gender` | female | 518 | 51.8 % |
| `gender` | male | 482 | 48.2 % |
| `test preparation course` | none | 642 | 64.2 % |
| `test preparation course` | completed | 358 | 35.8 % |

La muestra está prácticamente equilibrada por género. En contraste, casi dos tercios de los estudiantes (64.2 %) **no** completaron el curso de preparación, lo que limita la representatividad de ese subgrupo en comparaciones posteriores.

**Variables numéricas**

| Estadístico | `math score` | `reading score` | `writing score` |
|---|---|---|---|
| Media | 66.09 | 69.17 | 68.05 |
| Mediana | 66.00 | 70.00 | 69.00 |
| Desviación estándar | 15.16 | 14.60 | 15.20 |
| Mínimo | 0 | 17 | 10 |
| Máximo | 100 | 100 | 100 |

Las tres variables presentan distribuciones aproximadamente simétricas, con medias entre 66 y 69 puntos y desviaciones estándar cercanas a 15, lo que indica una dispersión moderada. `math score` es la única variable con un mínimo de 0, coherente con el valor atípico detectado en el diagnóstico de calidad.

## 5. Preguntas para el informe final

**1. ¿Qué fenómeno, proceso o contexto representa el *dataset*?**
Representa el rendimiento académico de 1000 estudiantes en tres pruebas estandarizadas (matemáticas, lectura y escritura) y su posible relación con factores demográficos y socioeducativos: género, grupo étnico, nivel educativo de los padres, tipo de almuerzo (proxy socioeconómico) y realización de un curso de preparación previo al examen.

**2. ¿Cuáles son las 5 variables más importantes para describir el caso y por qué?**

| # | Variable | Tipo | Por qué es importante |
|---|---|---|---|
| 1 | `math score` | Numérica | Es una de las tres variables *resultado* que el estudio busca explicar; junto con `reading score` y `writing score` cuantifica el rendimiento académico, el fenómeno central del *dataset*. Es además la única con valores atípicos y un mínimo de 0, lo que la hace clave también para el diagnóstico de calidad. |
| 2 | `reading score` | Numérica | Completa el conjunto de variables resultado. Presenta una correlación muy fuerte con `writing score` (r = 0.955) y fuerte con `math score` (r = 0.818), por lo que ayuda a validar la consistencia interna del desempeño de cada estudiante. |
| 3 | `writing score` | Numérica | Tercera variable resultado; junto con las dos anteriores permite construir el indicador compuesto `average score`, usado para comparar subgrupos (por ejemplo, por nivel educativo de los padres). |
| 4 | `test preparation course` | Categórica | Es el único factor directamente modificable por el estudiante (a diferencia de género, etnia o contexto familiar). Se asocia con puntajes más altos en las tres pruebas (+5.6 en matemáticas, +7.4 en lectura, +9.9 en escritura), lo que la convierte en la variable con mayor relevancia práctica para posibles intervenciones educativas. |
| 5 | `parental level of education` | Categórica ordinal | Funciona como indicador del entorno socioeducativo del estudiante. Al ser ordinal (seis niveles, de *some high school* a *master's degree*), permite observar una relación consistente y gradual con el promedio de desempeño, lo que la hace más informativa que otras variables demográficas como `race/ethnicity`. |

Estas cinco se priorizan sobre `gender`, `race/ethnicity` y `lunch` porque las tres primeras son el objetivo mismo del análisis (sin ellas no habría "rendimiento" que estudiar), y las dos últimas son las variables explicativas que mostraron el efecto más marcado y accionable sobre ese resultado en el análisis exploratorio (sección 4.3 y pregunta 4). `lunch`, aunque también relevante como proxy socioeconómico, se consideró secundaria frente a `parental level of education` por representar una aproximación indirecta y no una medición directa del contexto familiar.

**3. ¿Qué hallazgos se observan en la distribución de variables (categóricas y numéricas)?**
En las categóricas, la muestra está equilibrada en género (51.8 % / 48.2 %), pero desbalanceada en preparación previa (64.2 % no la completó) y en grupo étnico (el grupo C concentra el 31.9 % de los casos frente a solo 8.9 % del grupo A). En las numéricas, los tres puntajes tienen distribuciones simétricas con medias entre 66 y 69 y desviaciones estándar cercanas a 15; `math score` es la única variable con un valor mínimo de 0, mientras que `reading score` y `writing score` tienen mínimos de 17 y 10 respectivamente.

**4. ¿Qué relación relevante encontraron entre las variables? (mínimo 2)**
- Existe una correlación muy fuerte entre `reading score` y `writing score` (r = 0.955), y correlaciones fuertes de `math score` con ambas (r = 0.818 y r = 0.803 respectivamente): un estudiante que obtiene un buen puntaje en una prueba tiende a obtenerlo también en las otras dos.
- Haber completado el curso de preparación (`test preparation course`) se asocia con puntajes más altos en las tres pruebas: +5.6 puntos en matemáticas, +7.4 en lectura y +9.9 en escritura, en promedio, respecto a quienes no lo completaron.
- El tipo de almuerzo (`lunch`), usado como proxy socioeconómico, también muestra una diferencia notable: el promedio general de quienes reciben almuerzo estándar es 70.8, frente a 62.2 de quienes reciben almuerzo gratuito o reducido.

**5. ¿Qué problemas de calidad de datos detectaron y cómo los abordan?**
No se encontraron valores nulos ni registros duplicados, por lo que el *dataset* está completo en ese sentido. Sí se detectaron 8 valores atípicos en `math score` mediante el método IQR, incluyendo un caso extremo con puntaje 0; este se aborda documentándolo explícitamente y recomendando su verificación antes de un análisis predictivo (en lugar de eliminarlo automáticamente, dado que podría reflejar un caso real y no un error). Adicionalmente, se recomienda normalizar los nombres de columnas (espacios y el carácter `/`) para facilitar su manipulación programática en etapas posteriores del proyecto.

**6. Con base en lo observado, ¿qué pregunta de IA o problema predictivo podría plantearse a futuro con este *dataset*?**
Se podría plantear un problema de **regresión** para predecir el puntaje de matemáticas (`math score`) a partir de las variables demográficas y de preparación (género, nivel educativo de los padres, tipo de almuerzo y curso de preparación). De forma alternativa, un problema de **clasificación** binaria (aprobado/no aprobado, usando un umbral de puntaje) permitiría identificar tempranamente a estudiantes en riesgo académico, y un análisis de ***clustering*** podría usarse para segmentar perfiles de estudiantes con necesidades de apoyo similares.

## Bibliografía

Boschetti, A. y Massaron, L. (2018). *Python Data Science Essentials: A Practitioner's Guide Covering Essential Data Science Principles, Tools, and Techniques* (pp. 10-35). Packt Publishing, Limited.

So, A., Joseph, T. V., John, R. T., Worsley, A. y Asare, S. (2020). *The data science workshop: A new, interactive approach to learning data science* (pp. 16-36). Packt Publishing, Limited.

Mert, U., y Cuhadaroglu, M. (2018). *Mastering numerical computing with NumPy: Master scientific computing and perform complex operations with ease* (pp. 55-87). Packt Publishing, Limited.

Jakki Seshapanpu. (2019). *Students Performance in Exams*. Kaggle. https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
