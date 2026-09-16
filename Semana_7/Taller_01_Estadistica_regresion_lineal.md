# Taller: Fundamentos de Estadística para Regresión Lineal

**Fundamentos para IA · NRC 94103 · Semana 7**

Este taller **no usa Python**: es un taller de lápiz y papel (o calculadora) para que domines, paso a paso,
las fórmulas que hay *detrás* de la regresión lineal — las mismas que `scipy`/`statsmodels` calculan por ti
en el taller con código. Entender estas cuentas a mano te da la base para:

- Resolver con soltura los ejercicios con Python de esta misma Semana 7
  ([`Taller_02_Regresion_lineal_conceptos_basicos.md`](Taller_02_Regresion_lineal_conceptos_basicos.md)).
- Entender la Semana 8 (regresión logística), que reutiliza exactamente los mismos conceptos de mínimos
  cuadrados, coeficientes y pruebas de hipótesis, aplicados a un problema distinto.

Resuelve cada ejercicio **antes** de mirar la solución oculta en "Ver solución explicada". Usa lápiz y papel:
verás que las cuentas, aunque largas, son solo sumas, restas, multiplicaciones y raíces cuadradas.

---

## Caso de estudio para todo el taller

Un profesor quiere saber si las **horas de estudio** de sus estudiantes (X) se relacionan con la
**nota del examen** (Y, sobre 100). Reunió estos 6 datos:

| Estudiante | Horas de estudio (X) | Nota del examen (Y) |
|---|---|---|
| A | 2 | 48 |
| B | 3 | 58 |
| C | 5 | 63 |
| D | 6 | 72 |
| E | 8 | 78 |
| F | 9 | 88 |

Vas a usar estos mismos 6 datos en todos los ejercicios del taller, construyendo la regresión paso a paso.

---

## Ejercicio 1 — Media y desviaciones (el punto de partida de toda fórmula)

Antes de calcular cualquier coeficiente de regresión, necesitas la **media** de cada variable y qué tanto se
aleja cada dato de su media (su **desviación**). Estas desviaciones son el ingrediente de casi todas las
fórmulas que vienen después.

$$\bar{x} = \frac{\sum x_i}{n} \qquad \bar{y} = \frac{\sum y_i}{n}$$

**Tarea:** completa la tabla, calculando la desviación de cada dato respecto a su media
(`dx = x - x̄`, `dy = y - ȳ`).

| X | Y | dx = X − x̄ | dy = Y − ȳ |
|---|---|---|---|
| 2 | 48 | ____ | ____ |
| 3 | 58 | ____ | ____ |
| 5 | 63 | ____ | ____ |
| 6 | 72 | ____ | ____ |
| 8 | 78 | ____ | ____ |
| 9 | 88 | ____ | ____ |

**Preguntas:**

a) ¿Cuánto valen `x̄` y `ȳ`?
b) Si sumas toda la columna `dx` (con su signo), ¿cuánto debería dar? ¿Por qué crees que ese resultado no es
casualidad?
c) ¿Qué estudiante se aleja más de la media en horas de estudio, y qué estudiante se aleja más en nota?

<details>
<summary>Ver solución explicada</summary>

`x̄ = (2+3+5+6+8+9)/6 = 33/6 = 5.5` horas. `ȳ = (48+58+63+72+78+88)/6 = 407/6 ≈ 67.83` puntos.

| X | Y | dx = X − x̄ | dy = Y − ȳ |
|---|---|---|---|
| 2 | 48 | −3.50 | −19.83 |
| 3 | 58 | −2.50 | −9.83 |
| 5 | 63 | −0.50 | −4.83 |
| 6 | 72 | +0.50 | +4.17 |
| 8 | 78 | +2.50 | +10.17 |
| 9 | 88 | +3.50 | +20.17 |

**a)** `x̄ = 5.5`, `ȳ ≈ 67.83`.

**b)** La suma de `dx` da **0** (igual pasaría con `dy`). No es casualidad: por definición, la media es el
punto donde las desviaciones positivas y negativas se cancelan exactamente; es la propiedad matemática que
hace que la media sea el "centro de equilibrio" de los datos.

**c)** En horas de estudio, los estudiantes A y F se alejan más de la media (±3.50). En nota, también A y F
se alejan más (−19.83 y +20.17). Esto ya sugiere que los estudiantes más extremos en X también lo son en Y —
una primera pista visual de que las dos variables se mueven juntas.

</details>

---

## Ejercicio 2 — Covarianza y coeficiente de correlación (r)

La **covarianza** resume si dos variables se mueven juntas (cuando una sube, ¿la otra también sube?), y el
**coeficiente de correlación (r)** la convierte en un número entre −1 y 1, fácil de interpretar.

$$S_{xy} = \sum (x_i-\bar{x})(y_i-\bar{y}) \qquad S_{xx} = \sum (x_i-\bar{x})^2 \qquad S_{yy} = \sum (y_i-\bar{y})^2$$

$$r = \frac{S_{xy}}{\sqrt{S_{xx} \cdot S_{yy}}}$$

**Tarea:** usando las columnas `dx` y `dy` del Ejercicio 1, completa esta tabla y súmala.

| dx | dy | dx · dy | dx² | dy² |
|---|---|---|---|---|
| −3.50 | −19.83 | ____ | ____ | ____ |
| −2.50 | −9.83 | ____ | ____ | ____ |
| −0.50 | −4.83 | ____ | ____ | ____ |
| +0.50 | +4.17 | ____ | ____ | ____ |
| +2.50 | +10.17 | ____ | ____ | ____ |
| +3.50 | +20.17 | ____ | ____ | ____ |
| **Suma** | | **Sxy = ____** | **Sxx = ____** | **Syy = ____** |

**Preguntas:**

a) Con las tres sumas, calcula `r`.
b) ¿`r` es positivo o negativo? ¿Qué significa ese signo en el contexto de horas de estudio y nota?
c) ¿El valor de `r` indica una relación fuerte, moderada o débil entre las dos variables?

<details>
<summary>Ver solución explicada</summary>

| dx | dy | dx · dy | dx² | dy² |
|---|---|---|---|---|
| −3.50 | −19.83 | +69.42 | 12.25 | 393.36 |
| −2.50 | −9.83 | +24.58 | 6.25 | 96.69 |
| −0.50 | −4.83 | +2.42 | 0.25 | 23.36 |
| +0.50 | +4.17 | +2.08 | 0.25 | 17.36 |
| +2.50 | +10.17 | +25.42 | 6.25 | 103.36 |
| +3.50 | +20.17 | +70.58 | 12.25 | 406.69 |
| **Suma** | | **Sxy = 194.5** | **Sxx = 37.5** | **Syy = 1040.83** |

**a)** `r = 194.5 / √(37.5 × 1040.83) = 194.5 / √39031.25 = 194.5 / 197.56 ≈ 0.98`.

**b)** `r` es **positivo**: significa que, en general, a más horas de estudio, mayor es la nota — las dos
variables suben juntas.

**c)** `r ≈ 0.98` está muy cerca de 1, así que indica una relación **lineal muy fuerte** entre horas de
estudio y nota del examen (con estos 6 datos).

</details>

---

## Ejercicio 3 — La recta de mínimos cuadrados (b0 y b1)

Ya tienes todo lo necesario para encontrar la recta `Y = b0 + b1·X` que mejor resume la relación entre las
dos variables — la misma idea que viste en
[`01_Regresion_lineal_conceptos_basicos.md`](01_Regresion_lineal_conceptos_basicos.md), sección 3.

$$b_1 = \frac{S_{xy}}{S_{xx}} \qquad b_0 = \bar{y} - b_1 \cdot \bar{x}$$

**Tarea:** usando `Sxy` y `Sxx` del Ejercicio 2, calcula `b1` y `b0`.

`b1 = Sxy / Sxx = ____ / ____ = ____`

`b0 = ȳ − b1 · x̄ = ____ − ____ · ____ = ____`

**Preguntas:**

a) Escribe la ecuación completa de la recta con los valores que calculaste.
b) Interpreta `b1` en una frase: ¿cuánto sube la nota esperada por cada hora adicional de estudio?
c) ¿Tiene sentido interpretar literalmente `b0` (la nota esperada con 0 horas de estudio) en este caso?

<details>
<summary>Ver solución explicada</summary>

`b1 = Sxy / Sxx = 194.5 / 37.5 ≈ 5.19`

`b0 = ȳ − b1 · x̄ = 67.83 − 5.19 × 5.5 ≈ 67.83 − 28.52 ≈ 39.31`

**a)** `Nota = 39.31 + 5.19 · (Horas de estudio)`.

**b)** Por cada hora adicional de estudio, la nota esperada sube aproximadamente **5.19 puntos**, según este
modelo.

**c)** Parcialmente: `b0 ≈ 39.31` sería la nota esperada de un estudiante que no estudia nada. A diferencia
de un caso extremo como "cero habitaciones" en una casa, aquí sí es un valor posible en la realidad (un
estudiante podría no estudiar), aunque está fuera del rango de horas observado en los datos (2 a 9), así que
hay que interpretarlo con cautela — es una extrapolación.

</details>

---

## Ejercicio 4 — R²: ¿qué tan bien ajusta la recta?

El coeficiente de determinación **R²** te dice qué porcentaje de la variación de Y queda explicado por el
modelo. Con regresión simple (una sola X), es tan sencillo como elevar `r` al cuadrado.

$$R^2 = r^2$$

**Tarea:** con el `r` que calculaste en el Ejercicio 2, calcula `R²` y exprésalo como porcentaje.

`R² = r² = ____² = ____ = ____%`

**Preguntas:**

a) ¿Qué porcentaje de la variación en la nota del examen queda explicado por las horas de estudio, según
este modelo?
b) ¿Qué porcentaje de la variación **no** queda explicado por el modelo? ¿A qué se podría deber ese
porcentaje restante?
c) Si `R²` hubiera sido 0.20 en lugar del valor que obtuviste, ¿confiarías igual en el modelo para predecir
la nota de un estudiante nuevo? ¿Por qué?

<details>
<summary>Ver solución explicada</summary>

`R² = r² = 0.98² ≈ 0.9692`, es decir, aproximadamente **96.9%**.

**a)** Cerca del **97%** de la variación en la nota del examen queda explicada por las horas de estudio en
este modelo — un ajuste muy alto para un ejemplo con solo 6 datos.

**b)** El **3%** restante no queda explicado por `X`; podría deberse a otros factores no incluidos en el
modelo (por ejemplo, la calidad del estudio, el estado de ánimo el día del examen, conocimientos previos,
etc.), o simplemente a variación aleatoria.

**c)** No: un `R² = 0.20` significaría que el modelo solo explica el 20% de la variación de la nota, y el
80% restante quedaría sin explicar. Sería arriesgado confiar en una predicción basada en un modelo que deja
la mayor parte de la variación sin explicar; convendría buscar otras variables o revisar si la relación es
realmente lineal.

</details>

---

## Ejercicio 5 — Predicción y análisis de residuos

Con la ecuación del Ejercicio 3, ya puedes predecir la nota de cualquier estudiante a partir de sus horas de
estudio — y comparar esa predicción con la nota real de los estudiantes que sí conoces (el **residuo**:
`residuo = Y real − Y predicho`).

**Tarea 1 — predicción para un estudiante nuevo:** usa la ecuación para predecir la nota de un estudiante
que estudió 7 horas, y de otro que estudió 10 horas.

`Predicción(X=7) = 39.31 + 5.19 × 7 = ____`

`Predicción(X=10) = 39.31 + 5.19 × 10 = ____`

**Tarea 2 — residuos de los datos originales:** completa la tabla, calculando la predicción y el residuo
para cada uno de los 6 estudiantes.

| X | Y real | Y predicho | Residuo (Y real − Y predicho) |
|---|---|---|---|
| 2 | 48 | ____ | ____ |
| 3 | 58 | ____ | ____ |
| 5 | 63 | ____ | ____ |
| 6 | 72 | ____ | ____ |
| 8 | 78 | ____ | ____ |
| 9 | 88 | ____ | ____ |

**Preguntas:**

a) De las dos predicciones de la Tarea 1 (X=7 y X=10), ¿cuál te genera más confianza? (Pista: revisa el
rango de horas de estudio de los datos originales, de 2 a 9.)
b) ¿Qué estudiante tiene el residuo más grande (en valor absoluto)? ¿Qué significa ese residuo sobre su
nota real comparada con lo que predice el modelo?
c) Si sumas todos los residuos de la tabla (con su signo), ¿qué resultado esperarías obtener, y por qué?

<details>
<summary>Ver solución explicada</summary>

**Tarea 1:**

`Predicción(X=7) = 39.31 + 5.19 × 7 = 39.31 + 36.33 ≈ 75.61` puntos.

`Predicción(X=10) = 39.31 + 5.19 × 10 = 39.31 + 51.87 ≈ 91.17` puntos.

**Tarea 2:**

| X | Y real | Y predicho | Residuo |
|---|---|---|---|
| 2 | 48 | 49.68 | −1.68 |
| 3 | 58 | 54.87 | +3.13 |
| 5 | 63 | 65.24 | −2.24 |
| 6 | 72 | 70.43 | +1.57 |
| 8 | 78 | 80.80 | −2.80 |
| 9 | 88 | 85.99 | +2.01 |

**a)** La de X=7 genera más confianza: está **dentro** del rango de horas observado en los datos (2 a 9). La
de X=10 es una **extrapolación** (fuera del rango observado): el modelo asume que la relación sigue siendo
igual de lineal más allá de 9 horas, algo que no se puede confirmar con estos datos.

**b)** El estudiante E (X=8, Y=78) tiene el residuo más grande en valor absoluto (−2.80): su nota real
quedó 2.80 puntos **por debajo** de lo que predice el modelo para alguien que estudió 8 horas.

**c)** Se espera que la suma dé (prácticamente) **0**: por construcción, la recta de mínimos cuadrados es
la que hace que los residuos positivos y negativos se compensen exactamente (la pequeña diferencia de
redondeo aquí es solo por trabajar con decimales aproximados).

</details>

---

## Ejercicio 6 — Prueba de hipótesis sobre la pendiente

Como viste en la sección 2 de [`01_Regresion_lineal_conceptos_basicos.md`](01_Regresion_lineal_conceptos_basicos.md),
no basta con calcular `b1`: hay que comprobar si es **estadísticamente significativo**, o si podría ser
resultado del azar con solo 6 datos.

- **H0:** el verdadero valor de la pendiente es 0 (no hay relación real entre horas de estudio y nota).
- **H1:** el verdadero valor de la pendiente es distinto de 0 (sí hay relación real).

$$SSE = \sum \text{residuo}_i^2 \qquad MSE = \frac{SSE}{n-2} \qquad SE(b_1) = \sqrt{\frac{MSE}{S_{xx}}} \qquad t = \frac{b_1}{SE(b_1)}$$

**Tarea:** usando los residuos del Ejercicio 5, completa los cálculos.

`SSE = (−1.68)² + (3.13)² + (−2.24)² + (1.57)² + (−2.80)² + (2.01)² = ____`

`MSE = SSE / (n − 2) = ____ / 4 = ____`

`SE(b1) = √(MSE / Sxx) = √(____ / 37.5) = ____`

`t = b1 / SE(b1) = 5.19 / ____ = ____`

El valor crítico de *t*, con 4 grados de libertad (`n − 2 = 6 − 2 = 4`) y α = 0.05 (dos colas), es
**t crítico ≈ 2.776** (valor de tabla).

**Preguntas:**

a) ¿El valor de *t* que calculaste es mayor o menor que el valor crítico (2.776)?
b) Con ese resultado, ¿rechazas o no rechazas H0?
c) Redacta la conclusión en una frase, conectada con la pregunta original sobre horas de estudio y nota.

<details>
<summary>Ver solución explicada</summary>

`SSE = 2.82 + 9.80 + 5.02 + 2.46 + 7.84 + 4.04 ≈ 32.03`

`MSE = 32.03 / 4 ≈ 8.01`

`SE(b1) = √(8.01 / 37.5) = √0.2135 ≈ 0.46`

`t = 5.19 / 0.46 ≈ 11.23`

**a)** `t ≈ 11.23` es **mucho mayor** que el valor crítico de 2.776.

**b)** Se **rechaza H0**: con esta evidencia, la pendiente calculada no se explica por puro azar.

**c)** "Existe evidencia estadística suficiente (con estos 6 datos, α = 0.05) para afirmar que las horas de
estudio se relacionan de forma real con la nota del examen; sería muy poco probable observar una pendiente
tan alejada de 0 si, en el fondo, no existiera ninguna relación."

*(Nota: con una muestra tan pequeña (n=6) este resultado es solo ilustrativo del procedimiento — en la
práctica, con datasets grandes como `StudentsPerformance.csv`, este mismo cálculo lo hace `scipy.stats.linregress`
automáticamente, como viste en el Ejercicio 2 del taller con código.)*

</details>

---

## Ejercicio 7 — De comparar grupos a regresión: la variable *dummy* y Levene

Hasta ahora `X` fue siempre un número (horas de estudio). Pero `X` también puede ser una variable
**categórica de dos grupos**, convertida en 0 y 1 (una variable **dummy**) — como `gender` en
`StudentsPerformance.csv`. Este ejercicio usa datos reales (no el caso de las 6 horas de estudio) para
mostrar que comparar dos grupos es, en el fondo, una regresión lineal con una sola variable dummy.

*Datos reales:* `writing score` entre hombres (n=482, media=63.31) y mujeres (n=518, media=72.47).
Antes de comparar esas medias con una prueba t, se comprobó el supuesto de homogeneidad de varianzas con
Levene: **p = 0.934**.

**Tarea:**

a) Con la regla de siempre (α = 0.05), decide si el supuesto de homogeneidad de varianzas se cumple o no,
a partir de ese p-value de Levene.
b) Define `X = 0` para hombres y `X = 1` para mujeres. En una regresión `Y = b0 + b1·X` con una variable
dummy de dos grupos, `b0` es la media del grupo de referencia (`X=0`) y `b1` es la diferencia de medias
entre los dos grupos. Con esa regla, calcula `b0` y `b1` usando las medias dadas arriba (sin necesidad de
sumas ni desviaciones).

`b0 = ____`

`b1 = ____ − ____ = ____`

c) Escribe la ecuación completa de la recta y verifica: ¿qué predice para `X=0` y para `X=1`? ¿Coincide con
las medias reales de cada grupo?

<details>
<summary>Ver solución explicada</summary>

**a)** `p = 0.934 > 0.05` → **no se rechaza H0 de Levene**: las varianzas de `writing score` son homogéneas
entre hombres y mujeres. Esto valida usar la prueba t clásica (o esta misma regresión con variable dummy)
para comparar sus promedios.

**b)** `b0 = media de hombres (X=0) = 63.31`. `b1 = media de mujeres − media de hombres = 72.47 − 63.31 = 9.16`.

**c)** `writing score = 63.31 + 9.16 · X`. Para `X=0` (hombre): `63.31 + 9.16 × 0 = 63.31` — coincide
exactamente con la media real de los hombres. Para `X=1` (mujer): `63.31 + 9.16 × 1 = 72.47` — coincide
exactamente con la media real de las mujeres. Esto confirma que comparar dos grupos con sus medias es
matemáticamente idéntico a ajustar una regresión lineal simple con una variable dummy: el intercepto es la
media del grupo de referencia, y la pendiente es la diferencia de medias entre grupos.

*(Nota: a diferencia de los Ejercicios 1 a 6, aquí no se pide calcular Levene a mano — con n=482 y n=518
sería un cálculo enorme para hacer con lápiz y papel. Lo importante de este ejercicio es la conexión
conceptual: el mismo marco de la regresión lineal (b0, b1, supuestos como homogeneidad de varianzas) sirve
tanto para predecir con una variable numérica (horas de estudio) como para comparar dos grupos con una
variable categórica.)*

</details>

---

## Resumen: de estas fórmulas a la Semana 8

Estos 7 ejercicios cubren, a mano, el mismo camino que recorrerás con código en el resto de la Semana 7:
medias y desviaciones → covarianza y correlación → coeficientes de la recta → R² → predicción y residuos →
prueba de hipótesis sobre la pendiente → comparación de grupos con variable dummy y Levene. En la Semana 8
(regresión logística) volverás a usar exactamente estas mismas ideas — coeficientes, H0/H1, p-values, ajuste
del modelo — pero aplicadas a predecir una **categoría** (sí/no) en lugar de un número continuo.
