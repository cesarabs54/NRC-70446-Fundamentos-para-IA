# Taller en clase: Prueba de Hipótesis (con Python)

**Fundamentos para IA · NRC 94103 · Semana 6**

**Dataset de trabajo:** `StudentsPerformance.csv` (1000 registros de estudiantes).

Este taller desarrolla **en código Python** los 8 ejercicios conceptuales de
[`02_Pruebas_Hipotesis_conceptos.md`](02_Pruebas_Hipotesis_conceptos.md). Ahí resolviste cada uno con papel y
lápiz; aquí vas a comprobarlo con `pandas` y `scipy.stats`, paso a paso. Trabajen en parejas o grupos
pequeños, en un *notebook* (Colab, Jupyter o Anaconda).

**Configuración inicial** (ejecuta esto una sola vez, al comienzo):

```python
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("StudentsPerformance.csv")

alpha = 0.05  # nivel de significancia que usaremos en todo el taller
```

---

## Ejercicio 1 — ¿Es candidata para una prueba de hipótesis?

*(Corresponde al Ejercicio 1 de `02_...md`.)* Antes de decidir si cada situación necesita una prueba de
hipótesis, calcula lo que hay detrás de cada una.

```python
# Situación B: solo conteo (descriptiva) — ¿cuántos estudiantes hay en cada grupo de lunch?
print(df["lunch"].value_counts())

# Situación A: comparación entre grupos — promedio de math score por gender
print(df.groupby("gender")["math score"].mean().round(2))

# Situación C: relación entre dos variables numéricas — correlación reading vs. writing
correlacion = df["reading score"].corr(df["writing score"])
print(f"Correlación reading vs. writing: ____")   # completa con :.3f
```

**Pregunta:** de las tres situaciones (A, B, C), ¿cuáles son candidatas naturales para una prueba de
hipótesis y cuáles no? Justifica usando lo que acabas de calcular.

---

## Ejercicio 2 — H0 y H1 con más de dos grupos

*(Corresponde al Ejercicio 2 de `02_...md`.)* Vas a comparar `math score` entre los 6 niveles de
`parental level of education`, y a poner a prueba tus hipótesis con ANOVA.

```python
# ANOVA compara las medias de varios grupos (aquí, 6) en un solo test —
# a diferencia de la prueba t, que solo compara 2 grupos a la vez.

# Paso 1: separar "math score" en una lista, un grupo por cada nivel educativo.
niveles = df.groupby("parental level of education")
grupos = [subgrupo["math score"].values for _, subgrupo in niveles]

# Paso 2: aplicar ANOVA a los 6 grupos a la vez.
anova = stats.f_oneway(*grupos)
print(f"ANOVA -> statistic={anova.statistic:.2f}, p-value=____")
```

**Preguntas:**

a) Escribe H0 y H1 para esta comparación (con notación μ₁, μ₂, ... μ₆).
b) Con el p-value que obtuviste, ¿se rechaza o no se rechaza H0?
c) ¿Por qué H0 no puede escribirse simplemente como "las medias son diferentes"?

---

## Ejercicio 3 — Programar la regla de decisión

*(Corresponde al Ejercicio 3 de `02_...md`.)* En vez de decidir "a mano", escribe una función que aplique la
regla de decisión automáticamente.

```python
def decidir(p_value, alpha=0.05):
    if p_value < alpha:
        return "se rechaza H0"
    else:
        return "no se rechaza H0"

p_ejemplo = 0.023
print(f"Con p-value = {p_ejemplo}: ____")   # completa: llama a decidir(p_ejemplo)
```

**Preguntas:**

a) ¿Qué imprime tu función con `p_ejemplo = 0.023`?
b) Redacta la conclusión en una frase, sin usar la palabra "p-value".
c) ¿Qué error cometerías si dijeras "hay un 2.3% de probabilidad de que H0 sea verdadera"?

---

## Ejercicio 4 — Elegir la prueba a partir de los supuestos

*(Corresponde al Ejercicio 4 de `02_...md`.)* Primero resuelve el caso hipotético del documento con código;
luego aplica la misma lógica a datos reales del *dataset*.

```python
# --- Parte 1: caso hipotético del documento (con fines de práctica) ---
p_shapiro_A = 0.002
p_shapiro_B = 0.41
p_levene = 0.03

print("Normalidad grupo A:", "se cumple" if p_shapiro_A >= alpha else "NO se cumple")
print("Normalidad grupo B:", "se cumple" if p_shapiro_B >= alpha else "NO se cumple")
print("Homogeneidad de varianzas:", "se cumple" if p_levene >= alpha else "NO se cumple")

# --- Parte 2: la misma lógica, pero con datos reales (math score por gender) ---
hombres = df.loc[df["gender"] == "male", "math score"]
mujeres = df.loc[df["gender"] == "female", "math score"]

# shapiro(): ¿esta muestra numérica se parece a una distribución normal?
# H0 de Shapiro es "sí es normal" -> si p < alpha, se rechaza (es decir, NO es normal).
sh_hombres = stats.shapiro(hombres)
sh_mujeres = stats.shapiro(mujeres)
# levene(): ¿estos dos grupos tienen una variabilidad (varianza) parecida?
lev = stats.levene(hombres, mujeres)

print(f"Shapiro hombres p=____, Shapiro mujeres p=____, Levene p=____")
```

**Preguntas:**

a) En el caso hipotético (Parte 1), ¿qué prueba usarías para comparar las medias?
b) En los datos reales (Parte 2), ¿se cumple la normalidad en los dos grupos? ¿Y la homogeneidad de
varianzas?
c) ¿La conclusión de la Parte 2 coincide con la del caso hipotético? ¿Por qué sí o por qué no?

---

## Ejercicio 5 — Aplicar los pasos 6 y 7 con datos reales

*(Corresponde al Ejercicio 5 de `02_...md`.)* Vas a repetir, con código, el ejemplo aplicado de la sección 5
del documento — pero ahora con `writing score` según `lunch`.

```python
standard = df.loc[df["lunch"] == "standard", "writing score"]
reducido = df.loc[df["lunch"] == "free/reduced", "writing score"]

print(f"n standard = {len(standard)}, media = ____")
print(f"n free/reduced = {len(reducido)}, media = ____")

levene_lunch = stats.levene(standard, reducido)                              # supuesto: varianzas parecidas
t_lunch = stats.ttest_ind(standard, reducido)                                # prueba t (paramétrica)
u_lunch = stats.mannwhitneyu(standard, reducido, alternative="two-sided")    # Mann-Whitney U (no paramétrica)

print(f"Levene -> p-value=____")
print(f"t de Student -> t=____, p-value=____")
print(f"Mann-Whitney U -> p-value=____")

print(f"Decisión: {decidir(t_lunch.pvalue)}")   # reutiliza la función del Ejercicio 3
```

**Pregunta:** con estos resultados, redacta la interpretación (paso 7) en una frase conectada con la
pregunta "¿el tipo de almuerzo se relaciona con el puntaje de escritura?".

---

## Ejercicio 6 — Detectar el error en una interpretación (con datos reales)

*(Corresponde al Ejercicio 6 de `02_...md`.)* Usa el resultado real del curso de preparación para comparar
una interpretación incorrecta con una correcta.

```python
none = df.loc[df["test preparation course"] == "none", "math score"]
completado = df.loc[df["test preparation course"] == "completed", "math score"]
# Mann-Whitney U otra vez: no exige normalidad, buena opción cuando no estamos
# seguros de que se cumplan los supuestos (como en el Ejercicio 4).
p_curso = stats.mannwhitneyu(none, completado, alternative="two-sided").pvalue

interpretacion_incorrecta = (
    f"Obtuve un p-value de {p_curso:.2g}, así que estoy "
    f"{(1 - p_curso) * 100:.1f}% seguro de que el curso causa la mejora en la nota."
)
interpretacion_correcta = (
    f"Obtuve un p-value de {p_curso:.2g} (menor que α = {alpha}), lo que es evidencia "
    "estadísticamente significativa de que el curso está asociado con una mejor nota — "
    "aunque, al ser datos observacionales, no puedo afirmar que el curso sea la causa."
)

print(interpretacion_incorrecta)
print(interpretacion_correcta)
```

**Pregunta:** el código de arriba *calcula* `(1 - p_curso) * 100` para armar la frase incorrecta a propósito.
¿Por qué esa operación no tiene ningún sentido estadístico, aunque Python la calcule sin quejarse?

---

## Ejercicio 7 — Significancia vs. tamaño del efecto (con datos reales)

*(Corresponde al Ejercicio 7 de `02_...md`.)* Vas a comparar los mismos dos grupos de `race/ethnicity`
(`group A` y `group E`) en `math score`, dos veces: primero con una muestra pequeña (10 estudiantes por
grupo) y luego con el grupo completo, para ver cómo el tamaño de muestra afecta el p-value aunque la
diferencia real entre los grupos casi no cambie.

```python
grupo_a = df.loc[df["race/ethnicity"] == "group A", "math score"]
grupo_e = df.loc[df["race/ethnicity"] == "group E", "math score"]

# Muestra pequeña: solo los primeros 10 estudiantes de cada grupo
a_chica = grupo_a.head(10)
e_chica = grupo_e.head(10)
t_chica = stats.ttest_ind(a_chica, e_chica)

# Grupo completo (todos los estudiantes de cada grupo)
t_completo = stats.ttest_ind(grupo_a, grupo_e)

print(f"Muestra chica -> n={len(a_chica)}/{len(e_chica)}, diferencia={e_chica.mean() - a_chica.mean():.2f}, "
      f"t=____, p=____")
print(f"Grupo completo -> n={len(grupo_a)}/{len(grupo_e)}, diferencia={grupo_e.mean() - grupo_a.mean():.2f}, "
      f"t=____, p=____")

print(f"Decisión (muestra chica): {decidir(t_chica.pvalue)}")
print(f"Decisión (grupo completo): {decidir(t_completo.pvalue)}")
```

**Preguntas:**

a) ¿En cuál de los dos casos se rechaza H0 (con α = 0.05)?
b) La diferencia observada es parecida en ambos casos (revisa los dos valores de `diferencia` que imprimiste).
¿Qué cambió entre un caso y otro para que la decisión sobre H0 sea distinta? (Pista: es la misma idea que
trabajaste en el Ejercicio 6 de `Taller_02_Estadistica_inferencial_conceptos.md`, con una submuestra de 50
estudiantes.)
c) Si solo tuvieras la muestra chica, ¿sería correcto concluir "no hay diferencia entre los grupos"? ¿Por qué?

---

## Ejercicio 8 — Errores tipo I y II en un caso médico

*(Corresponde al Ejercicio 8 de `02_...md`.)* Este ejercicio es de razonamiento (no requiere cálculo sobre el
*dataset*) y usa, a propósito, un caso médico en vez de `StudentsPerformance.csv`: los errores tipo I/II se
entienden mejor con un ejemplo de alto riesgo (decidir sobre un tratamiento) que con notas de examen. Aun así,
vas a representarlo en código para practicar cómo se modela una decisión con incertidumbre.

```python
situacion_real = "el tratamiento SÍ reduce la presión"       # lo que en verdad pasa (desconocido en la vida real)
decision_estudio = "el tratamiento SÍ reduce la presión"     # lo que concluye el estudio

if decision_estudio == situacion_real:
    print("Decisión correcta")
elif decision_estudio == "el tratamiento SÍ reduce la presión" and situacion_real == "no hay diferencia":
    print("Error tipo I: se adopta un tratamiento que no funciona")
else:
    print("Error tipo II: se descarta un tratamiento que sí funciona")
```

**Pregunta:** cambia manualmente los valores de `situacion_real` y `decision_estudio` para representar un
error tipo I, y luego un error tipo II. ¿Cuál de los dos te parece más grave en este caso médico? Justifica.

---
