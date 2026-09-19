# Taller en clase: Regresión Logística (con Python)

**Fundamentos para IA · NRC 94103 · Semana 8**

**Dataset de trabajo:** `StudentsPerformance.csv` (1000 registros de estudiantes).

Este taller desarrolla **en código Python** los conceptos de
[`01_Regresion_logistica_conceptos_basicos.md`](01_Regresion_logistica_conceptos_basicos.md) y del
[taller en papel](02_Taller_regresion_logistica.md) que ya resolviste a mano. Ahí calculaste `z`, la sigmoide y
la matriz de confusión con calculadora; aquí vas a comprobar esos mismos resultados con `pandas`,
`statsmodels` y `scikit-learn`, y a graficar el modelo. Trabaja en un *notebook* (Colab, Jupyter o Anaconda).

**Configuración inicial** (ejecuta esto una sola vez, al comienzo):

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, ConfusionMatrixDisplay

df = pd.read_csv("StudentsPerformance.csv")
df.columns = [c.strip() for c in df.columns]
df["aprueba_mate"] = (df["math score"] >= 60).astype(int)
df[["reading score", "math score", "aprueba_mate"]].head()
```

---

## Ejercicio 1 — Exploración: ¿se ve una relación?

Antes de ajustar cualquier modelo, hay que explorar los datos: ¿cuántos estudiantes aprueban y cuántos no?,
¿cómo se distribuye `reading score` en cada grupo?

```python
print(df["aprueba_mate"].value_counts())

df.boxplot(column="reading score", by="aprueba_mate")
plt.xlabel("aprueba_mate (0 = no, 1 = sí)")
plt.ylabel("reading score")
plt.title("Reading score según si aprueba matemáticas")
plt.suptitle("")
plt.show()
```

**Preguntas:**

a) Según el conteo, ¿cuántos estudiantes aprueban y cuántos no aprueban matemáticas?
b) En el *boxplot*, ¿el grupo que aprueba tiene, en general, un `reading score` más alto que el que no
aprueba? ¿Qué tan clara se ve la diferencia?
c) ¿Esto es estadística **descriptiva** o **inferencial**? ¿Qué te falta para poder afirmar que la relación
es real y no producto del azar de la muestra?

---

## Ejercicio 2 — Ajustar el modelo con `statsmodels`

Vas a ajustar la regresión logística `aprueba_mate ~ reading score` usando **máxima verosimilitud** (el
método que `statsmodels` calcula por ti, a diferencia de los mínimos cuadrados de la regresión lineal).

```python
X = sm.add_constant(df["reading score"])
y = df["aprueba_mate"]

modelo = sm.Logit(y, X).fit()
print(modelo.summary())
```

**Preguntas:**

a) Localiza en la tabla los coeficientes `b0` (`const`) y `b1` (`reading score`). ¿Coinciden con los que
usaste en el taller en papel (`b0 = -10.2254`, `b1 = 0.1672`)?
b) ¿Cuál es el `P>|z|` (valor p) de `reading score`? Con `α = 0.05`, ¿es significativo el coeficiente?
c) Plantea `H0` y `H1` para el coeficiente de `reading score`, y redacta la conclusión de la prueba de Wald
en una frase.

---

## Ejercicio 3 — De `z` a la probabilidad, con código

Ahora vas a reproducir el Paso 2 y el Paso 3 del taller en papel, pero calculando con `numpy` en vez de
calculadora.

```python
b0 = modelo.params["const"]
b1 = modelo.params["reading score"]

valores_x = np.array([40, 50, 60, 70, 80])
z = ____
p = 1 / (1 + np.exp(-z))

for x, zi, pi in zip(valores_x, z, p):
    print(f"reading score = {x}:  z = {zi:.4f}   P = {pi:.4f}  ({pi*100:.1f}%)")
```

**Preguntas:**

a) Completa el código (reemplaza `____`) con la fórmula de `z = b0 + b1·X`.
b) Compara los valores de `P` con la tabla que llenaste a mano en el Paso 3 del taller en papel. ¿Coinciden?
c) ¿Para qué valor de `reading score`, aproximadamente, `P` cruza el 50%? Verifícalo con
`-b0/b1` y compara con tu respuesta del Ejercicio 3.1 del taller en papel.

---

## Ejercicio 4 — Graficar la curva sigmoide

```python
x_rango = np.linspace(df["reading score"].min(), df["reading score"].max(), 300)
z_rango = b0 + b1 * x_rango
p_rango = 1 / (1 + np.exp(-z_rango))

plt.figure(figsize=(8, 5))
plt.scatter(df["reading score"], df["aprueba_mate"], alpha=0.15, label="Datos reales (0/1)")
plt.plot(x_rango, p_rango, color="darkred", linewidth=2.5, label="P(aprueba) estimada")
plt.axhline(0.5, color="gray", linestyle="--", linewidth=1)
plt.xlabel("reading score")
plt.ylabel("P(aprueba matemáticas)")
plt.title("Curva sigmoide del modelo")
plt.legend()
plt.show()
```

**Preguntas:**

a) ¿La curva tiene la forma de "S" que esperabas?
b) ¿Dónde cruza la curva la línea punteada de `P = 0.5`? ¿Coincide con el valor que calculaste en el
Ejercicio 3c?
c) ¿Por qué la nube de puntos (los datos reales) solo tiene valores en `Y = 0` o `Y = 1`, mientras que la
curva roja toma cualquier valor entre 0 y 1?

---

## Ejercicio 5 — Interpretar el coeficiente: *odds ratio*

```python
odds_ratio = ____
print(f"odds ratio (reading score) = {odds_ratio:.4f}")
```

**Preguntas:**

a) Completa el código para calcular el *odds ratio* de `reading score` (pista: `np.exp(...)`).
b) En tus palabras, ¿qué significa este número para la probabilidad de aprobar matemáticas?
c) ¿Es lo mismo decir "los momios se multiplican por 1.18" que decir "la probabilidad sube 18 puntos
porcentuales"? Explica por qué sí o por qué no.

---

## Ejercicio 6 — Clasificar y evaluar el modelo

```python
df["p_hat"] = modelo.predict(X)
df["prediccion"] = (df["p_hat"] >= 0.5).astype(int)

matriz = confusion_matrix(df["aprueba_mate"], df["prediccion"])
print(matriz)

ConfusionMatrixDisplay(matriz, display_labels=["No aprueba", "Aprueba"]).plot()
plt.show()

exactitud = accuracy_score(df["aprueba_mate"], df["prediccion"])
precision = precision_score(df["aprueba_mate"], df["prediccion"])
sensibilidad = recall_score(df["aprueba_mate"], df["prediccion"])
print(f"Exactitud: {exactitud:.3f}   Precisión: {precision:.3f}   Sensibilidad: {sensibilidad:.3f}")
```

**Preguntas:**

a) ¿La matriz de confusión coincide con la que usaste en el Paso 6 del taller en papel (227 / 96 / 72 / 605)?
b) ¿Coinciden la exactitud, la precisión y la sensibilidad con las que calculaste a mano?
c) De los cuatro números de la matriz, ¿cuáles son los **falsos negativos**? En el contexto de "predecir si
un estudiante aprueba", ¿qué consecuencia práctica tendría un falso negativo?

---

## Reto final — Agregar una segunda variable

Repite el Ejercicio 2, pero ahora con **dos** variables independientes: `reading score` y `writing score`.

```python
X2 = sm.add_constant(df[["reading score", "writing score"]])
modelo2 = sm.Logit(y, X2).fit()
print(modelo2.summary())
```

1. ¿Cambió mucho el coeficiente de `reading score` al agregar `writing score`? ¿A qué se debe esto? (Pista:
   revisa la correlación entre las dos variables con `df[["reading score","writing score"]].corr()`, y
   relaciónalo con lo que ya viste sobre **colinealidad** en `01_Regresion_logistica_conceptos_basicos.md`,
   sección 7).
2. Calcula la nueva exactitud del modelo con dos variables. ¿Mejoró mucho respecto al modelo con una sola
   variable?
3. Verifica alguno de tus resultados con la calculadora en línea
   [numiqo.com/statistics-calculator/regression](https://numiqo.com/statistics-calculator/regression),
   pegando los datos directamente.
