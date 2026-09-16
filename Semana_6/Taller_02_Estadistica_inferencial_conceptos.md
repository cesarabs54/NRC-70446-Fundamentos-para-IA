# Taller en clase: Estadística Inferencial y Test de Hipótesis (con Python)

**Fundamentos para IA · NRC 94103 · Semana 6**

**Dataset de trabajo:** `StudentsPerformance.csv` (1000 registros de estudiantes).

Este taller desarrolla **en código Python** los 8 ejercicios conceptuales de
[`01_Estadistica_inferencial_conceptos.md`](01_Estadistica_inferencial_conceptos.md). Ahí resolviste cada uno
con papel y lápiz; aquí vas a comprobarlo con `pandas` y `scipy.stats`, paso a paso. Trabajen en parejas o
grupos pequeños, en un *notebook* (Colab, Jupyter o Anaconda).

**Configuración inicial** (ejecuta esto una sola vez, al comienzo):

```python
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("StudentsPerformance.csv")
df.head()
```

---

## Ejercicio 1 — Estadística descriptiva vs. inferencial

*(Corresponde al Ejercicio 1 de `01_...md`.)* Vas a calcular el promedio de `math score` por grupo de
`test preparation course`, y a distinguir qué parte de tu trabajo es descriptiva y cuál sería inferencial.

```python
none = df.loc[df["test preparation course"] == "none", "math score"]
completado = df.loc[df["test preparation course"] == "completed", "math score"]

print(f"n sin curso = {len(none)}, media = {none.mean():.2f}")
print(f"n con curso = {len(completado)}, media = {completado.mean():.2f}")
```

**Preguntas:**

a) Los dos números que acabas de calcular (`len()` y `.mean()`) ¿son estadística descriptiva o inferencial?
b) Si a partir de esos dos promedios concluyes *"el curso mejora el puntaje de TODOS los estudiantes que
presentan este examen"*, ¿esa conclusión es descriptiva o inferencial? ¿Por qué haría falta algo más que
estos dos números para sostenerla con rigor?

---

## Ejercicio 2 — Población y muestra

*(Corresponde al Ejercicio 2 de `01_...md`.)* Vas a contar cuántos estudiantes hay en cada nivel educativo de
los padres.

```python
conteo = df["parental level of education"].value_counts()
print(conteo)
```

**Preguntas:**

a) ¿Cuál es el grupo más pequeño y cuál el más grande? Anota sus tamaños.
b) En este estudio, ¿cuál es la población y cuál la muestra?
c) ¿Por qué el promedio de `math score` del grupo más pequeño podría ser menos confiable que el del grupo
más grande? (Pista: calcula también `df.groupby("parental level of education")["math score"].mean()` y
piensa qué tan fácil sería que un solo estudiante atípico mueva ese promedio en cada grupo.

---

## Ejercicio 3 — Variables dependiente e independiente

*(Corresponde al Ejercicio 3 de `01_...md`.)* Vas a inspeccionar los tipos de dato y una correlación.

```python
print(df[["lunch", "writing score", "reading score", "gender", "math score"]].dtypes)

correlacion = df["reading score"].corr(df["writing score"])
print(f"Correlación reading vs. writing: {correlacion:.3f}")
```

**Preguntas:** para cada pregunta de investigación, identifica la variable dependiente y la independiente:

a) ¿`lunch` se relaciona con `writing score`?
b) ¿`reading score` se relaciona con `writing score`?
c) ¿`gender` se relaciona con `math score`?

---

## Ejercicio 4 — Plantear H0 y H1 con datos reales

*(Corresponde al Ejercicio 4 de `01_...md`.)* Antes de aplicar cualquier prueba, calcula las medias que vas a
comparar.

```python
standard = df.loc[df["lunch"] == "standard", "writing score"]
reducido = df.loc[df["lunch"] == "free/reduced", "writing score"]

print(f"n standard = {len(standard)}, media = ____")
print(f"n free/reduced = {len(reducido)}, media = ____")
```

**Pregunta:** con esos dos promedios ya calculados, escribe en una celda de texto (Markdown) H0 y H1 para la
pregunta *"¿el tipo de almuerzo se relaciona con el puntaje de escritura?"*, usando la notación μ₁ = μ₂ /
μ₁ ≠ μ₂.

---

## Ejercicio 5 — Calcular e interpretar un p-value

*(Corresponde al Ejercicio 5 de `01_...md`.)* Vas a poner a prueba, con datos reales, si el curso de
preparación se relaciona con el puntaje de matemáticas.

```python
resultado = stats.mannwhitneyu(none, completado, alternative="two-sided")
print(f"Mann-Whitney U -> estadístico={resultado.statistic}, p-value=____")
```

**Preguntas:**

a) ¿Ese p-value es "chiquito" o "grande" según la regla de α = 0.05?
b) ¿Se rechaza o no se rechaza H0?
c) Redacta la conclusión en una frase conectada con la pregunta original.

---

## Ejercicio 6 — Errores tipo I y tipo II: el efecto del tamaño de muestra

*(Corresponde al Ejercicio 6 de `01_...md`.)* Vas a comprobar, con una simulación, por qué una muestra chica
aumenta el riesgo de error tipo II. Toma una submuestra aleatoria de solo 50 estudiantes y repite la prueba
del Ejercicio 5.

```python
muestra_chica = df.sample(n=50, random_state=42)   # una "muestra" de solo 50 estudiantes

n_chico = muestra_chica.loc[muestra_chica["test preparation course"] == "none", "math score"]
c_chico = muestra_chica.loc[muestra_chica["test preparation course"] == "completed", "math score"]

print(f"n sin curso = {len(n_chico)}, n con curso = {len(c_chico)}")
resultado_chico = stats.mannwhitneyu(n_chico, c_chico, alternative="two-sided")
print(f"p-value con n=50 -> ____")
```

**Preguntas:**

a) Compara el p-value que obtuviste aquí con el del Ejercicio 5 (n = 1000). ¿Sigue siendo menor a 0.05?
b) Si en esta muestra de 50 concluyes "no hay evidencia de que el curso influya", pero en el fondo el curso
sí tiene un efecto real (como sugiere la muestra completa) — ¿qué tipo de error acabas de cometer, I o II?
c) ¿Qué relación ves entre el tamaño de muestra y el riesgo de este error?

---

## Ejercicio 7 — Validar los supuestos (normalidad y homogeneidad)

*(Corresponde al Ejercicio 7 de `01_...md`.)* Antes de confiar en la prueba del Ejercicio 5, valida sus
supuestos.

```python
shapiro_none = stats.shapiro(none)
shapiro_completado = stats.shapiro(completado)
levene = stats.levene(none, completado)

print(f"Shapiro-Wilk 'none'      -> p-value=____")
print(f"Shapiro-Wilk 'completed' -> p-value=____")
print(f"Levene -> p-value=____")
```

**Preguntas:**

a) ¿Se cumple la normalidad en los dos grupos?
b) ¿Se cumple la homogeneidad de varianzas?
c) Con estos resultados, ¿fue buena idea usar Mann-Whitney U como prueba principal en el Ejercicio 5?

---

## Ejercicio 8 — Elegir la prueba con más de 2 grupos

*(Corresponde al Ejercicio 8 de `01_...md`.)* La columna `race/ethnicity` tiene 5 grupos. Vas a comparar
`math score` entre los 5 con las dos herramientas para más de 2 grupos.

```python
grupos = [g["math score"].values for _, g in df.groupby("race/ethnicity")]

anova = stats.f_oneway(*grupos)
kruskal = stats.kruskal(*grupos)

print(f"ANOVA -> p-value=____")
print(f"Kruskal-Wallis -> p-value=____")
```

**Preguntas:**

a) ¿Se está comparando 2 grupos o más de 2? ¿Cuál es la herramienta paramétrica y cuál la no paramétrica?
b) ¿Qué decides sobre H0 con estos resultados?
c) Para saber *cuáles* grupos específicos difieren entre sí (no solo que "alguno" difiere), ¿qué tendrías que
hacer después? (No hace falta ejecutarlo — solo nombra la idea.)

---
