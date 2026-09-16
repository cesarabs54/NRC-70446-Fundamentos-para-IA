# Taller en clase: Visualización de Datos con Matplotlib (Python)

**Fundamentos para IA · NRC 94103 · Semana 5**

**Nivel:** Taller básico

**Dataset de trabajo:** [`StudentsPerformance.csv`](StudentsPerformance.csv) (1000 estudiantes: notas de matemáticas, lectura y escritura, más género, tipo de almuerzo, curso de preparación, nivel educativo de los padres y grupo étnico).

## Antes de empezar

Este taller es 100 % práctico: vas a construir, uno por uno, los tipos de gráfico más comunes con la librería `matplotlib`, usando siempre el mismo *dataset* para que puedas comparar resultados entre ejercicios. Si necesitas repasar qué es la media, la mediana o los cuartiles antes de graficarlos, consulta [`01_Estadistica_basica.md`](../01_%20Estadistica_basica/01_Estadistica_Basica.md), en la carpeta vecina.

**Cómo trabajar el taller:**

1. Abre un *notebook* nuevo (Google Colab, Jupyter o Anaconda) en esta misma carpeta, donde está `StudentsPerformance.csv`.
2. Copia el código de cada ejercicio en una celda y ejecútalo (`Shift + Enter`).
3. Donde veas `____`, complétalo tú antes de correr la celda (puede ser un número, un nombre de columna o una palabra).
4. Responde las preguntas de cada ejercicio en una celda de texto (Markdown), justo debajo del gráfico.
5. Trabaja en parejas o en grupos pequeños; discutan las respuestas antes de escribirlas.

**Configuración inicial** (ejecútala una sola vez, al comienzo del *notebook*):

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("StudentsPerformance.csv")
df.head()
```

---

## ¿Por qué visualizar los datos?

Un número suelto (como "la media es 66.09") es difícil de imaginar. Un gráfico, en cambio, se entiende de un vistazo. Por eso, antes de elegir un tipo de gráfico siempre conviene hacerse una pregunta: **¿qué tipo de variable quiero mostrar, y qué quiero que la persona que lo vea entienda?** Esa pregunta guía todo este taller y se resume en esta tabla, a la que volverás varias veces:

| Lo que tengo | Lo que quiero mostrar | Gráfico recomendado |
|---|---|---|
| 1 variable de categorías (palabras) | Cuántos casos hay de cada categoría | Gráfico de barras |
| 1 variable numérica | Cómo se distribuyen los valores (forma, dónde se concentran) | Histograma |
| 1 variable numérica, comparada entre grupos | Diferencias de mediana, dispersión y valores atípicos entre grupos | Diagrama de caja (*boxplot*) |
| 2 variables numéricas | Si existe una relación o patrón conjunto entre ambas | Diagrama de dispersión (*scatter*) |
| 1 variable de categorías, como parte de un total | Qué proporción (%) representa cada categoría del total | Gráfico de pastel (*pie*) — con cuidado, ver Ejercicio 5 |

---

## Ejercicio 1 — Gráfico de barras: contar categorías

Cuando una columna tiene **palabras** (categorías), como `test preparation course`, lo primero que solemos hacer es contar cuántas veces aparece cada una. Esa tabla de conteos se grafica de forma natural con un **gráfico de barras**: una barra por categoría, con una altura igual a su conteo.

```python
conteo = df["test preparation course"].value_counts()
print(conteo)

plt.figure(figsize=(6, 4))
plt.bar(conteo.index, conteo.values, color="#5a7d9a")
plt.title("Estudiantes según curso de preparación")
plt.xlabel("Test preparation course")
plt.ylabel("Número de estudiantes")
plt.show()
```

**Preguntas:**

a) Según el gráfico, ¿hay más estudiantes que tomaron el curso de preparación o que no lo tomaron? Anota los dos conteos exactos.
b) Cambia `"test preparation course"` por `"lunch"` en la primera línea y vuelve a correr todo el bloque. ¿Qué categoría es más frecuente?
c) ¿Por qué no tendría sentido hacer este mismo gráfico con la columna `math score`? (Pista: piensa en cuántas barras distintas tendrías que dibujar.)

---

## Ejercicio 2 — Histograma: la forma de una variable numérica

Un histograma agrupa los valores numéricos en "cajones" (*bins*) de rangos iguales y cuenta cuántos datos caen en cada uno. Sirve para ver de un vistazo si los datos se concentran en el centro, si hay valores muy altos o muy bajos, y qué tan simétrica es la distribución.

```python
math = df["math score"]
media = math.mean()
mediana = math.median()

plt.figure(figsize=(7, 5))
plt.hist(math, bins=20, color="#5a7d9a", edgecolor="white")
plt.axvline(media, color="#c0392b", linestyle="--", label=f"Media ({media:.1f})")
plt.axvline(mediana, color="#27ae60", linestyle=":", label=f"Mediana ({mediana:.1f})")
plt.title("Distribución de math score")
plt.xlabel("Nota de matemáticas")
plt.ylabel("Número de estudiantes")
plt.legend()
plt.show()

print(f"Media = ____, Mediana = ____")
```

**Preguntas:**

a) ¿La media y la mediana quedan muy cerca o muy lejos una de otra en el gráfico? ¿Qué te dice eso sobre la simetría de los datos? (Puedes repasar este concepto en la Sección 3 de `01_Estadistica_basica.md`.)
b) Cambia `bins=20` por `bins=5` y luego por `bins=50`. ¿Qué le pasa a la forma del histograma? ¿Se pierde o se gana información al cambiar el número de *bins*?
c) Repite el ejercicio con `reading score` en vez de `math score`. ¿La forma se parece a la de matemáticas?

---

## Ejercicio 3 — Diagrama de caja (*boxplot*): comparar grupos

El *boxplot* dibuja, para cada grupo, una caja entre el primer cuartil (Q1) y el tercer cuartil (Q3), una línea en la mediana, y puntos sueltos para los valores atípicos (*outliers*). Es la mejor forma de comparar varios grupos numéricos al mismo tiempo.

```python
sin_curso = df.loc[df["test preparation course"] == "none", "math score"]
con_curso = df.loc[df["test preparation course"] == "completed", "math score"]

plt.figure(figsize=(6, 5))
plt.boxplot([sin_curso, con_curso], tick_labels=["none", "completed"])
plt.title("math score según curso de preparación")
plt.xlabel("Test preparation course")
plt.ylabel("Nota de matemáticas")
plt.show()
```

**Preguntas:**

a) ¿Qué grupo tiene la caja más "arriba" (mediana más alta)?
b) ¿Ves puntos sueltos por debajo de las cajas? ¿Qué representan?
c) A partir del gráfico, ¿dirías que el curso de preparación está relacionado con una nota más alta? ¿Qué necesitarías, además del gráfico, para afirmarlo con más seguridad? (No hace falta calcularlo — solo nombra la idea; se retoma en el taller de la Semana 6.)

---

## Ejercicio 4 — Diagrama de dispersión: relación entre dos variables numéricas

Cuando se tienen dos variables numéricas para el mismo estudiante (por ejemplo, su nota de lectura y su nota de escritura), un **diagrama de dispersión** ubica cada estudiante como un punto: su posición horizontal es una variable, y su posición vertical es la otra. Si los puntos forman una nube que sube en diagonal, hay una relación entre las dos variables.

```python
plt.figure(figsize=(6, 6))
plt.scatter(df["reading score"], df["writing score"], alpha=0.4, color="#5a7d9a")
plt.title("Relación entre nota de lectura y de escritura")
plt.xlabel("Reading score")
plt.ylabel("Writing score")
plt.show()

correlacion = df["reading score"].corr(df["writing score"])
print(f"Correlación reading-writing: ____")
```

**Preguntas:**

a) Describe con tus palabras la forma de la nube de puntos: ¿sube, baja, o no muestra ningún patrón?
b) El número de correlación que imprimiste va de -1 a 1. Según ese número, ¿la relación es fuerte o débil? ¿Positiva o negativa?
c) Cambia `"writing score"` por `"math score"` en el `scatter` (deja `reading score` en el eje X). ¿La nube de puntos se ve igual de "apretada" o más dispersa que la anterior?

---

## Ejercicio 5 — Gráfico de pastel: proporciones de un total

El gráfico de pastel (*pie chart*) muestra qué porcentaje del total representa cada categoría, como si fuera una torta repartida en pedazos. Funciona bien con **pocas categorías** (2 a 5); con muchas categorías se vuelve difícil de leer.

```python
conteo_almuerzo = df["lunch"].value_counts()

plt.figure(figsize=(5, 5))
plt.pie(conteo_almuerzo.values, labels=conteo_almuerzo.index, autopct="%1.1f%%",
        colors=["#5a7d9a", "#adad3b"])
plt.title("Proporción de estudiantes según tipo de almuerzo")
plt.show()
```

**Preguntas:**

a) ¿Qué porcentaje de estudiantes tiene almuerzo `standard`?
b) Ahora intenta lo mismo, pero con `"parental level of education"` en vez de `"lunch"` (esa columna tiene 6 categorías). ¿El gráfico se sigue leyendo con facilidad, o se vuelve confuso?
c) Con lo que observaste en b), ¿en qué casos usarías un gráfico de barras en vez de un gráfico de pastel?

---

## Ejercicio 6 — Barras para comparar el promedio de varios grupos

También se puede usar un gráfico de barras para comparar un **promedio** (no solo un conteo) entre varias categorías. Aquí se compara la nota media de matemáticas entre los 5 grupos de `race/ethnicity`.

```python
promedio_por_grupo = df.groupby("race/ethnicity")["math score"].mean().sort_index()
print(promedio_por_grupo)

plt.figure(figsize=(7, 5))
plt.bar(promedio_por_grupo.index, promedio_por_grupo.values, color="#5a7d9a")
plt.title("Promedio de math score por grupo étnico")
plt.xlabel("race/ethnicity")
plt.ylabel("Promedio de math score")
plt.show()
```

**Preguntas:**

a) ¿Cuál grupo tiene el promedio más alto y cuál el más bajo?
b) El eje Y de este gráfico **no empieza en 0**, a menos que tú lo fuerces. Agrega la línea `plt.ylim(0, 100)` justo antes de `plt.show()` y vuelve a correr el bloque. ¿Cambia tu impresión de qué tan grandes son las diferencias entre grupos?
c) En tus palabras: ¿por qué el rango del eje Y puede hacer que una diferencia se vea "más dramática" o "más chiquita" de lo que realmente es?

---

## Reto final — Elige tu propio gráfico

Ya viste barras, histograma, *boxplot*, dispersión y pastel. Ahora te toca a ti decidir.

1. Elige **una** de estas preguntas (o propón una propia con el visto bueno de tu profesor):
   - ¿La nota de escritura (`writing score`) se distribuye de forma parecida entre hombres y mujeres (`gender`)?
   - ¿El nivel educativo de los padres (`parental level of education`) se relaciona con la nota de lectura (`reading score`)?
   - ¿Existe relación entre la nota de matemáticas (`math score`) y la de escritura (`writing score`)?
2. Usando la tabla de la sección **"¿Por qué visualizar los datos?"**, decide qué tipo de gráfico es el más adecuado para tu pregunta.
3. Constrúyelo en una celda de código, reutilizando y adaptando el código de los ejercicios anteriores. No olvides `plt.title()`, `plt.xlabel()` y `plt.ylabel()`.
4. En una celda de texto, responde: **¿por qué elegiste ese tipo de gráfico y no otro?** y **¿qué conclusión sacas de lo que observas?**

---

## Glosario rápido

| Palabra | En una frase |
|---|---|
| `plt.bar()` | Dibuja un gráfico de barras (categorías o promedios por grupo) |
| `plt.hist()` | Dibuja un histograma (distribución de una variable numérica) |
| `plt.boxplot()` | Dibuja un diagrama de caja (compara grupos con mediana, cuartiles y *outliers*) |
| `plt.scatter()` | Dibuja un diagrama de dispersión (relación entre dos variables numéricas) |
| `plt.pie()` | Dibuja un gráfico de pastel (proporciones de un total, con pocas categorías) |
| `plt.title()` / `plt.xlabel()` / `plt.ylabel()` | Ponen título y etiquetas a los ejes — nunca deben faltar |
| `plt.legend()` | Muestra qué representa cada color o línea del gráfico |

---

## Material relacionado

Guía conceptual de estadística básica (sin código): [`01_Estadistica_basica.md`](../01_%20Estadistica_basica/01_Estadistica_Basica.md).
Clave de respuestas de este taller (uso docente): [`Taller_01_Visualizacion_de_datos_profesor.md`](Taller_01_Visualizacion_de_datos_profesor.md).
