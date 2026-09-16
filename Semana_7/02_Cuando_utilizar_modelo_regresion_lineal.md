# Cuándo utilizar un modelo de regresión lineal

Ya viste, en [`01_Regresion_lineal_conceptos_basicos.md`](01_Regresion_lineal_conceptos_basicos.md), **qué es**
la regresión lineal y **cómo** se ajusta. Esta hoja responde una pregunta distinta y, en la práctica, anterior
a esa: antes de ajustar cualquier modelo, ¿cómo sé si la regresión lineal es siquiera la herramienta correcta
para el problema que tengo enfrente? Seguimos usando `StudentsPerformance.csv` (1000 estudiantes, con
`math score`, `reading score`, `writing score`, y variables categóricas como `gender`, `race/ethnicity` y
`parental level of education`) para hacerlo concreto.

---

## 1. Las grandes preguntas

Antes de escribir una sola línea de código, respóndete estas tres preguntas. Si las tres respuestas apuntan
en la misma dirección, la regresión lineal es un excelente punto de partida.

### 1.1 ¿Tengo que predecir sobre una variable numérica?

La regresión lineal predice **números continuos** (un puntaje, un precio, una temperatura), no categorías.
Si lo que quieres predecir es una etiqueta ("aprobó" / "no aprobó", "grupo A" / "grupo B" / "grupo C"), no
estás frente a un problema de regresión sino de **clasificación**, y necesitas otra familia de modelos
(regresión logística, árboles de clasificación, etc.).

- `writing score` a partir de `reading score` → **sí**, es numérica continua (10 a 100 en los datos reales):
  problema de regresión, candidato natural para regresión lineal.
- "¿Aprobó `writing score` (≥ 60) o no?" → **no**, es una categoría binaria: problema de clasificación, no de
  regresión lineal clásica (esto ya se vio en el Ejercicio 6 de `01_...md`).

### 1.2 ¿Las variables independientes con las que cuento son primordialmente numéricas?

La regresión lineal trabaja de forma nativa con números. Las variables **categóricas** (`gender`,
`race/ethnicity`, `parental level of education`, `lunch`, `test preparation course`) no entran directamente a
la ecuación: hay que convertirlas primero, típicamente con **variables dummy** (0/1), como ya hiciste con
`gender` en el Ejercicio 7 de `01_...md`. Cuantas más variables categóricas tengas, y cuantos más niveles
tenga cada una, más se infla el modelo:

$$\text{writing score} = b_0 + b_1 \times \text{gender}_{\text{(1=mujer)}}$$

Esa transformación funciona bien para una variable con **pocos niveles** (género: 2). El problema aparece
cuando la mayoría de tus predictoras son categóricas y con muchos niveles — lo que nos lleva directo a la
siguiente pregunta.

### 1.3 ¿No cuento con una gran cantidad de variables y/o variables categóricas con muchos niveles?

Cada variable categórica con *k* niveles se convierte, típicamente, en *k − 1* columnas dummy nuevas. En
`StudentsPerformance.csv`:

| Variable | Niveles | Columnas dummy que agregaría |
|---|---|---|
| `gender` | 2 | 1 |
| `race/ethnicity` | 5 (`group A`…`group E`) | 4 |
| `parental level of education` | 6 | 5 |

Si metes las tres al modelo, ya pasaste de 3 columnas originales a 10. Con pocos datos y muchas columnas, el
modelo puede **sobreajustarse** (memorizar la muestra en vez de aprender el patrón general) y sus
coeficientes se vuelven inestables y difíciles de interpretar. Esta es la razón práctica detrás de la
recomendación "reduce las variables lo más que puedas" que viene en la sección 2.

**Ejercicio 1.** Para cada situación, decide si las "tres grandes preguntas" apuntan a favor de usar
regresión lineal, y por qué:

a) Predecir `math score` a partir de `reading score` y `writing score`.
b) Predecir `test preparation course` (completado / no completado) a partir de las tres notas.
c) Predecir `writing score` a partir de `gender`, `race/ethnicity`, `parental level of education` y
`lunch` (las cuatro categóricas, sin ninguna variable numérica).

<details>
<summary>Ver solución explicada</summary>

a) **Sí, a favor.** `math score` es numérica continua (pregunta 1 ✔), las predictoras (`reading score`,
`writing score`) son numéricas (pregunta 2 ✔), y son solo dos variables, sin categóricas de muchos niveles
(pregunta 3 ✔). Es un caso ideal para regresión lineal.

b) **No.** Falla la primera pregunta: `test preparation course` es una categoría binaria, no un número. Se
necesita un modelo de clasificación (por ejemplo, regresión logística), no regresión lineal clásica.

c) **A favor, pero con cuidado.** La variable a predecir es numérica (pregunta 1 ✔), pero *todas* las
predictoras son categóricas (pregunta 2 en contra) y entre las cuatro suman muchos niveles combinados
(`race/ethnicity` con 5, `parental level of education` con 6 — pregunta 3 en contra). Técnicamente se puede
hacer con variables dummy, pero es el escenario donde conviene reducir variables (por ejemplo, quedarte solo
con la categórica que más se relacione con `writing score`) antes de ajustar el modelo.

</details>

---

## 2. Recomendaciones prácticas

### 2.1 Si tienes que predecir variables numéricas, empieza con regresión lineal; si no funciona, salta a otros modelos

La regresión lineal es barata de ajustar, rápida de interpretar y, como viste en `01_...md`, es la base
conceptual de modelos más complejos (regresión logística, redes neuronales). Por eso es el **modelo base**
("*baseline*") natural: si un modelo simple ya explica bien tus datos (R² alto, residuos razonables), no
necesitas empezar directamente con algo más costoso y difícil de interpretar. Solo si la relación entre tus
variables es claramente no lineal, o el R² es bajo incluso agregando variables razonables, tiene sentido
saltar a modelos más sofisticados.

### 2.2 Reduce las variables lo más que puedas

Agregar una variable más *nunca* baja el R² sobre los datos de entrenamiento, así que siempre es tentador
seguir sumando predictoras. El problema es que cada variable de más:

- añade ruido y aumenta el riesgo de sobreajuste (ver Sección 5 del `01_...md`, sobre revisar supuestos),
- hace más difícil interpretar qué está pasando realmente,
- y, como viste en el Ejercicio 4 de `Taller_02_Regresion_lineal_conceptos_basicos.md`, agregar `math score`
  a un modelo que ya tenía `reading score` mejoró el R² de 0.9113 a apenas 0.913 — una mejora casi nula para
  el costo de una variable adicional.

La pregunta correcta no es "¿esta variable ayuda?" sino "¿esta variable ayuda **lo suficiente** como para
justificar el modelo más complicado?". Esa es exactamente la idea de **comparación entre modelos** que ya
viste en la tabla de la Sección 2 de `01_...md`.

### 2.3 ¡Cuidado con la multicolinealidad!

La **multicolinealidad** ocurre cuando dos o más variables predictoras están muy correlacionadas *entre
sí*. En ese caso, el modelo no puede distinguir bien cuál de las dos está realmente causando el efecto sobre
`Y`, y sus coeficientes individuales se vuelven inestables (pueden cambiar mucho, o incluso de signo, con
pequeños cambios en los datos), aunque el modelo en conjunto siga prediciendo razonablemente bien.

Con los datos reales de `StudentsPerformance.csv`, la correlación entre las tres notas es:

| | `math score` | `reading score` | `writing score` |
|---|---|---|---|
| **`math score`** | 1.00 | 0.82 | 0.80 |
| **`reading score`** | 0.82 | 1.00 | **0.95** |
| **`writing score`** | 0.80 | 0.95 | 1.00 |

`reading score` y `writing score` están correlacionadas en **0.95** — muy alto. Si quisieras predecir, por
ejemplo, `math score` usando *ambas* como predictoras a la vez, el modelo tendría problemas para "repartir"
el efecto entre las dos: son, en buena medida, la misma información contada dos veces. Una señal práctica de
alerta es calcular la correlación entre cada par de predictoras antes de meterlas juntas al modelo; si es muy
alta (como aquí), suele bastar con dejar una sola de las dos.

### 2.4 No predigas fuera del dominio de la variable independiente

Un modelo de regresión lineal solo "aprendió" la relación **dentro del rango de datos que vio**. En
`StudentsPerformance.csv`, `reading score` va de 17 a 100. La ecuación `writing score = -0.6676 + 0.9935 ×
reading score` (de `01_...md`) se ajustó con datos en ese rango — no hay ninguna garantía de que la misma
relación se sostenga fuera de él.

- Predecir para `reading score = 80` → **válido**: está dentro del rango observado (17–100).
- Predecir para `reading score = 0` → **inválido en la práctica** (esto ya se discutió en el Ejercicio 3 de
  `01_...md`: `b0` es un artefacto matemático, no una predicción confiable, precisamente porque 0 está fuera
  — o en el borde extremo — de lo que el modelo observó).
- Predecir para `reading score = 150` → **inválido**: no solo está fuera del rango 0–100 de la prueba, sino
  que además el modelo nunca vio ejemplos ahí; extrapolar así puede dar resultados absurdos (en este caso,
  una predicción de escritura por encima de 100, un puntaje que no existe).

Esta idea se llama **extrapolación**, y es una de las formas más comunes de usar mal un modelo de regresión
ya perfectamente válido dentro de su dominio.

**Ejercicio 2.** Con las cuatro recomendaciones de esta sección:

a) Tienes un modelo `writing score = b0 + b1 × reading score + b2 × math score`. ¿Qué recomendación de esta
sección deberías revisar primero, sabiendo que `reading score` y `math score` correlacionan en 0.82? ¿Qué
harías con esa información?

b) Un compañero quiere predecir el `writing score` de un estudiante que reportó `reading score = -5` (un
error de captura). ¿Qué recomendación aplica aquí, y qué le dirías?

c) Tienes 1000 estudiantes y quieres agregar `gender`, `race/ethnicity`, `parental level of education` y
`lunch` al modelo, todas a la vez. ¿Qué recomendación te haría dudar antes de hacerlo directamente?

<details>
<summary>Ver solución explicada</summary>

a) La de **multicolinealidad** (2.3). Una correlación de 0.82 entre `reading score` y `math score` es alta:
antes de interpretar `b1` y `b2` por separado como "el efecto puro de cada variable", conviene verificar si
el modelo con ambas realmente mejora mucho el R² frente al modelo con solo `reading score` (que ya tenía
R² ≈ 0.91). Si la mejora es marginal — como de hecho ocurre en los datos reales —, es más simple y más
estable quedarse con una sola de las dos.

b) La de **no extrapolar / dominio de la variable** (2.4). `reading score = -5` no solo es un error de
captura evidente (el rango real es 0–100), sino que además está completamente fuera de lo que el modelo
observó al entrenarse. Le diría que corrija el dato de entrada antes de predecir nada — cualquier predicción
con ese valor no tiene respaldo del modelo.

c) La de **reducir variables / cuidado con muchas categóricas** (2.2 y la pregunta 1.3). Esas cuatro
categóricas combinadas agregan muchas columnas dummy nuevas (fácilmente más de 10) frente a solo 1000
estudiantes, lo que aumenta el riesgo de sobreajuste y hace el modelo más difícil de interpretar. Antes de
meterlas todas, valdría la pena revisar cuál (o cuáles) realmente se relaciona con `writing score`, y dejar
solo esas.

</details>

---

## 3. Checklist rápido

Antes de ajustar un modelo de regresión lineal, revisa:

| # | Pregunta | Si la respuesta es "no" / "sí" (según corresponda) |
|---|---|---|
| 1 | ¿Lo que quiero predecir es numérico continuo? | Si es una categoría, usa un modelo de clasificación en su lugar. |
| 2 | ¿Mis predictoras son mayormente numéricas? | Si son categóricas, conviértelas a variables dummy antes de ajustar. |
| 3 | ¿Tengo pocas variables, y las categóricas tienen pocos niveles? | Si tienes muchas, prioriza y reduce antes de ajustar. |
| 4 | ¿Ya probé el modelo simple antes de saltar a algo más complejo? | Empieza simple; solo escala si el modelo simple no alcanza. |
| 5 | ¿Revisé la correlación entre mis predictoras? | Si es muy alta entre dos de ellas, considera dejar solo una. |
| 6 | ¿Voy a predecir dentro del rango de datos que vio el modelo? | Si no, esa predicción es una extrapolación no confiable. |

## Resumen

1. **Las tres grandes preguntas**: ¿es numérica la variable a predecir?, ¿son numéricas las predictoras?, y
   ¿son pocas y con pocos niveles las categóricas? — si las tres apuntan a favor, la regresión lineal es un
   buen punto de partida.
2. **Empieza simple**: la regresión lineal es el modelo base natural; solo salta a algo más complejo si el
   modelo simple no explica bien los datos.
3. **Menos es más**: agregar variables casi siempre mejora el R² un poco, pero no siempre justifica la
   complejidad extra — compara modelos, no solo acumules predictoras.
4. **Multicolinealidad**: predictoras muy correlacionadas entre sí (como `reading score` y `writing score`,
   en 0.95) hacen inestables los coeficientes individuales del modelo.
5. **No extrapoles**: un modelo solo es confiable prediciendo dentro del rango de datos con el que se ajustó
   — fuera de ahí, sus predicciones no tienen respaldo.
