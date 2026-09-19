# Taller de refuerzo — Regresión logística paso a paso

**Fundamentos para IA · NRC 94103 · Semana 8**

Este taller está pensado para que afiances, en orden, los conceptos que evalúa "MA Evaluación 8". No son las
mismas preguntas del examen: son ejercicios previos, con cálculos completos, para que llegues a la
evaluación entendiendo el *por qué* de cada respuesta y no solo memorizando cuál opción marcar.

Usamos el mismo caso guía y los mismos datos reales del curso: `../StudentsPerformance.csv` (1000
estudiantes), donde `Y = 1` si el estudiante **aprueba matemáticas** (`math score >= 60`) y `Y = 0` si no
aprueba, y `X = reading score` como variable predictora. Al ajustar el modelo sobre los 1000 estudiantes se
obtiene:

```
b0 = -10.2254        b1 = 0.16721
```

Vas a usar estos dos números durante todo el taller — vale la pena que los tengas a la vista.

---

## Paso 1. Del predictor lineal `z` a la probabilidad (sigmoide)

Todo modelo de regresión logística se calcula en **dos pasos**, nunca en uno solo:

```
Paso A — predictor lineal:   z = b0 + b1 * X
Paso B — función sigmoide:   p(x) = 1 / (1 + e^(-z))
```

`z` puede ser cualquier número (negativo, positivo, grande o pequeño). La sigmoide es la que se encarga de
"aplastarlo" para que siempre quede entre 0 y 1, como debe ser una probabilidad.

**Ejercicio 1.1.** Completa la tabla calculando `z` y luego `p(x)` para distintos valores de `reading
score`, usando `b0 = -10.2254` y `b1 = 0.16721`.

| reading score | z = b0 + b1·X | p(x) = 1/(1+e^-z) |
|---|---|---|
| 40 | | |
| 60 | | |
| 70 | | |
| 90 | | |

**Ejercicio 1.2 (verdadero/falso, como en la evaluación).** "Si dos estudiantes A y B tienen el mismo
`reading score`, siempre van a tener exactamente el mismo `p(x)`, sin importar ninguna otra información
sobre ellos." ¿Verdadero o falso? Justifica.

---

## Paso 2. Odds y odds ratio

Los **odds** (momios) no son lo mismo que la probabilidad. Se definen así:

```
odds = p / (1 - p)
```

- `p` es la probabilidad de que ocurra el evento (aprobar).
- `1 - p` es el **complemento**: la probabilidad de que **no** ocurra (no aprobar).
- Si `odds > 1`, el evento es **más probable** que su contrario. Si `odds < 1`, es **menos probable**.

**Ejercicio 2.1.** Con los valores de `p(x)` que calculaste en el ejercicio 1.1, calcula los *odds* de
aprobar para `reading score = 60` y `reading score = 70`.

Ahora el concepto más importante para interpretar coeficientes: el **odds ratio (OR)**. En un modelo con una
sola variable, `OR = e^b1`.

**Ejercicio 2.2.** Calcula el *odds ratio* de `reading score` (`b1 = 0.16721`) y explica, en una frase, qué
significa.

---

## Paso 3. El umbral de decisión y sus consecuencias

El modelo entrega una **probabilidad**, no una decisión. Para convertirla en "aprueba / no aprueba" hace
falta un **umbral** `t` (normalmente 0.5): si `p(x) >= t`, se predice "aprueba".

**Ejercicio 3.1.** Usando los `p(x)` calculados en el ejercicio 1.1 y un umbral `t = 0.5`, clasifica a cada
estudiante.

**Ejercicio 3.2.** Si en vez de `t = 0.5` usaras un umbral más exigente, `t = 0.8` (solo clasificas "aprueba"
cuando el modelo está muy seguro), ¿qué le pasaría al estudiante con `reading score = 70` (`p = 0.814`)? ¿Y
qué pasaría, en general, con la cantidad de estudiantes clasificados como "aprueba" si subes el umbral?

---

## Paso 4. Evaluando el modelo: matriz de confusión

Aplicando el modelo completo (umbral 0.5) a los 1000 estudiantes del archivo, se obtiene esta matriz de
confusión real:

| | Predicho: no aprueba | Predicho: aprueba |
|---|---|---|
| **Real: no aprueba** | 227 (VN) | 96 (FP) |
| **Real: aprueba** | 72 (FN) | 605 (VP) |

**Ejercicio 4.1.** Con estos cuatro números, calcula:

a) **Exactitud (accuracy)** = (VP + VN) / total
b) **Precisión** = VP / (VP + FP)
c) **Recall (sensibilidad)** = VP / (VP + FN)

**Ejercicio 4.2.** De los 1000 estudiantes, 677 aprueban y solo 323 no aprueban (clases desbalanceadas).
Imagina un modelo "tonto" que siempre predice "aprueba", sin mirar ningún dato. ¿Qué *accuracy* tendría ese
modelo? ¿Por qué este ejemplo ilustra la advertencia de que "*accuracy* puede engañar cuando hay desbalance
entre clases"?

---

## Paso 5. Estadística inferencial: ¿el efecto es real o es azar?

Haber calculado `b1 = 0.16721` con estos 1000 estudiantes no basta para decir que `reading score` "de
verdad" influye en aprobar matemáticas — podría ser una casualidad de esta muestra. Para eso está la
**inferencia estadística**:

- **H0 (hipótesis nula):** el verdadero coeficiente de `reading score` es cero (no influye).
- **H1 (hipótesis alternativa):** el verdadero coeficiente es distinto de cero (sí influye).
- La **prueba de Wald** da un estadístico *z* (en este modelo, *z* ≈ 15.3) y un **p-value** casi cero.
- Como el p-value es mucho menor a 0.05, **rechazamos H0** con alta **significancia** y **confianza**.

**Ejercicio 5.1.** Clasifica cada uno de estos términos como parte del **modelado** (construir y usar el
modelo para predecir) o de la **validación estadística** (decidir si lo que el modelo aprendió es confiable):
`sigmoide`, `p-value`, `odds ratio`, `intervalo de confianza`, `umbral`, `colinealidad`, `z (predictor
lineal)`.

**Ejercicio 5.2.** Un estudiante afirma: "Como el p-value de `reading score` es prácticamente cero, eso
significa que `reading score` explica el 100% de si un estudiante aprueba matemáticas o no." ¿Estás de
acuerdo? Justifica usando lo visto en el Paso 4.

---

## Autoevaluación final (mímica de la evaluación real)

Antes de presentar "MA Evaluación 8", resuelve estas 5 preguntas con tus propias palabras:

1. En una frase, explica por qué la regresión logística se dice "lineal en el logit" y no "lineal en la
   probabilidad".
2. Escribe la fórmula de la sigmoide de memoria y explica qué representa cada símbolo (`z`, `e`, `p(x)`).
3. Define *odds* con tus propias palabras y calcula los *odds* de un evento con `p = 0.75`.
4. Explica, sin mirar el material, para qué sirve el odds ratio y qué significa un `OR = 2`.
5. Da un ejemplo (distinto al de este taller) de un concepto de **modelado** y uno de **validación
   estadística** en regresión logística.
