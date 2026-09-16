# Regresión lineal: conceptos básicos

Esta hoja te explica, con ejemplos sencillos, las ideas que necesitas para la Semana 7. Vamos a usar el
archivo `StudentsPerformance.csv` (el mismo de la Semana 6), con las notas de 1000 estudiantes en tres
exámenes: matemáticas (`math score`), lectura (`reading score`) y escritura (`writing score`).

> 💡 Puedes explorar el [**recurso interactivo de la Semana 7**](../Aplicacion_interactiva_profesor/Semana_7/index.html) (cuatro módulos: correlación y mínimos cuadrados, ajuste y residuos, prueba de hipótesis sobre la pendiente, y cuándo usar el modelo / predicción) mientras lees esta guía, para ver en vivo cómo cambian los coeficientes con los mismos datos de `StudentsPerformance.csv`.

---

## 1. La relación de la estadística con la inteligencia artificial

Cuando hablamos de "inteligencia artificial", muchas veces imaginamos algo mágico. Pero en el fondo, gran
parte de la IA (sobre todo el *machine learning*) es **estadística aplicada a gran escala**: son fórmulas que
buscan patrones en los datos, los resumen en números (parámetros) y usan esos números para predecir cosas
nuevas.

Piénsalo como un profesor con mucha experiencia: después de ver cientos de estudiantes, "intuye" que quien
lee bien también suele escribir bien. Un modelo de IA hace lo mismo, pero de forma matemática: mira los datos
de muchos estudiantes y convierte esa intuición en un número que puede usar para predecir.

- La **estadística descriptiva** nos ayuda a entender los datos con los que vamos a "entrenar" ese
  modelo (¿qué tan dispersas están las notas?, ¿hay estudiantes con puntajes muy atípicos?).
- La **estadística inferencial** nos ayuda a decidir si lo que "aprendió" el modelo es un patrón real o
  pura casualidad de los 1000 estudiantes que tenemos en el archivo.
- Un modelo de IA, en el fondo, es una función matemática con parámetros que se ajustan con datos. La
  **regresión lineal** es el ejemplo más simple y más importante de esa idea: es, literalmente, el primer
  "modelo" que casi todos los científicos de datos aprenden antes de pasar a modelos más complejos.

**Ejercicio 1.** Piensa en un sistema que, con el puntaje de lectura de un estudiante, intenta predecir su
puntaje de escritura.

a) ¿Qué papel juega la estadística descriptiva antes de construir ese modelo?
b) ¿Qué papel juega la estadística inferencial al momento de decidir si el modelo realmente aprendió algo útil?

<details>
<summary>Ver solución explicada</summary>

a) La estadística descriptiva permite explorar los datos de los 1000 estudiantes: ver el promedio y la
dispersión de `reading score` y `writing score`, detectar estudiantes atípicos, y hacerse una primera idea de
si las dos notas parecen moverse juntas (por ejemplo, con un diagrama de dispersión) antes de ajustar
cualquier modelo.

b) La estadística inferencial permite responder si la relación que "aprendió" el modelo (por ejemplo, "a
mayor puntaje de lectura, mayor puntaje de escritura") es un patrón que se sostiene más allá de estos 1000
estudiantes, o si podría deberse al azar de esa muestra en particular.

</details>

## 2. ¿Cómo sabemos si un modelo es mejor? Pruebas de hipótesis

No basta con que un modelo "se vea bien". Para decir con seriedad que un modelo funciona, o que una variable
sí ayuda a predecir algo, necesitamos apoyarnos en **pruebas de hipótesis** (como viste en la Semana 6). Es
como cuando un profesor dice "estoy seguro de que estudiar más mejora la nota": no basta con la impresión,
hay que comprobarlo con evidencia.

- **H0 (hipótesis nula)**: la variable NO tiene relación real con lo que queremos predecir (su efecto es
  cero). Ejemplo: "el puntaje de lectura no tiene ninguna relación real con el de escritura".
- **H1 (hipótesis alternativa)**: la variable SÍ tiene una relación real. Ejemplo: "el puntaje de lectura sí
  tiene una relación real con el de escritura".

En regresión lineal, cada variable tiene asociado un **p-value**: nos dice qué tan probable sería observar
la relación que vemos en los datos si, en realidad, esa variable no influyera en nada. Si el p-value es menor
a 0.05, rechazamos H0 y decimos que la variable sí aporta información útil al modelo.

Ese p-value sale de un **estadístico *t*** para el coeficiente, que compara qué tan grande es `b1` frente a
su propio margen de error (el **error estándar**, $SE(b_1)$):

$$t = \frac{b_1 - 0}{SE(b_1)}$$

Es la misma lógica de la prueba *t* que ya conoces de la Semana 6: mientras más grande sea $|t|$ (es decir,
mientras más "lejos de cero", en unidades de error estándar, esté el coeficiente), más pequeño es el p-value
y más confiados podemos estar de que `b1` no es cero por puro azar.

También comparamos modelos completos entre sí: por ejemplo, un modelo que predice `writing score` solo con
`reading score`, contra uno que además incluye `math score`, para ver si agregar esa segunda variable mejora
la predicción de forma significativa, y no solo por azar.

| Concepto | Descripción breve | Importancia |
|---|---|---|
| **Comparación entre modelos** | Contrastar dos o más versiones de un modelo (por ejemplo, uno que predice `writing score` solo con `reading score`, contra otro que además usa `math score`) para ver cuál explica o predice mejor. | Evita quedarnos con un modelo más complicado si no aporta una mejora real; ayuda a elegir la versión más simple que funcione igual de bien. |
| **Pruebas de hipótesis** | Plantear H0 ("la variable no tiene efecto sobre la nota") y H1 ("sí tiene efecto"), y usar el p-value para decidir cuál apoyan los datos. | Da un criterio objetivo, basado en probabilidad, para decidir si un coeficiente o una diferencia entre modelos es real o solo azar de la muestra de 1000 estudiantes. |
| **Validación estadística** | Revisar los supuestos del modelo (normalidad de residuos con Shapiro-Wilk, homogeneidad de varianzas con Levene, etc.) y métricas de ajuste (R², error de predicción). | Confirma que las conclusiones del modelo (por ejemplo, "leer bien predice escribir bien") son confiables y no vienen de aplicar mal la herramienta a los datos. |

**Ejercicio 2.** Al ajustar una regresión lineal simple con `reading score` para predecir `writing score`, se
obtiene un coeficiente positivo con un valor *t* de aproximadamente 101 (y un p-value prácticamente cero).

a) Plantea H0 y H1 para esta variable.
b) ¿Rechazamos o no H0?
c) En tus palabras, ¿qué significa ese resultado sobre la relación entre el puntaje de lectura y el de
escritura?

<details>
<summary>Ver solución explicada</summary>

a) **H0:** el puntaje de lectura (`reading score`) no tiene ninguna relación real con el de escritura
(`writing score`); su efecto verdadero es cero. **H1:** el puntaje de lectura sí tiene una relación real con
el de escritura.

b) **Rechazamos H0**: el p-value es muchísimo menor a 0.05, así que la evidencia en contra de "no hay
relación" es abrumadora.

c) Significa que es prácticamente imposible que la relación que vemos entre `reading score` y `writing score`
en los datos se deba solo a la casualidad de estos 1000 estudiantes; hay una relación real y muy fuerte entre
leer bien y escribir bien.

</details>

## 3. ¿Qué es la regresión lineal y para qué sirve?

La **regresión lineal** es una herramienta que busca la línea recta que mejor describe la relación entre una
variable que queremos predecir (variable dependiente, `Y`) y una o más variables que usamos para predecirla
(variables independientes, `X`). Es como trazar, en una hoja cuadriculada, la línea que mejor "atraviesa" una
nube de puntos: cada punto es un estudiante, con su nota de lectura en un eje y su nota de escritura en el
otro.

La idea es una ecuación como esta:

$$Y = b_0 + b_1 X$$

- `b0` (intercepto): el valor de `Y` cuando `X` vale cero.
- `b1` (pendiente): cuánto sube o baja `Y` por cada unidad que sube `X`.

### ¿De dónde salen `b0` y `b1`? Mínimos cuadrados

La recta "buena" no se adivina: es la que minimiza la suma de los errores al cuadrado entre lo que predice
el modelo ($\hat{y}_i$) y el valor real ($y_i$) de cada estudiante:

$$SS_{res} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

La pendiente y el intercepto que logran ese mínimo tienen una fórmula directa (por eso se llama **regresión
por mínimos cuadrados**, *least squares*):

$$b_1 = \frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sum_{i=1}^{n}(x_i-\bar{x})^2} = \frac{S_{xy}}{S_{xx}}
\qquad\qquad
b_0 = \bar{y} - b_1 \bar{x}$$

Con `reading score` como `x` y `writing score` como `y`, esas fórmulas dan justamente `b1 = 0.9935` y
`b0 = -0.6676` (los valores redondeados que usamos en el Ejercicio 3). El numerador de `b1` mide cuánto se
mueven juntas las dos variables; el denominador mide cuánto varía por sí sola `reading score`.

Sirve para dos cosas principales:

1. **Explicar**: entender qué tanto y en qué dirección una variable influye sobre otra (¿leer mejor se
   relaciona con escribir mejor?).
2. **Predecir**: una vez tenemos la ecuación, podemos calcular un valor de `Y` para un `X` nuevo que no
   habíamos visto antes (un estudiante del que solo conocemos su nota de lectura).

**Ejercicio 3.** Con `StudentsPerformance.csv`, al ajustar `writing score = b0 + b1 * reading score` se
obtiene aproximadamente `b0 = -0.67` y `b1 = 0.99`.

a) Según esta ecuación, ¿cuánto sube el puntaje de escritura esperado por cada punto adicional en el puntaje
de lectura?
b) Calcula el puntaje de escritura esperado para un estudiante con `reading score = 80`.
c) ¿Tiene sentido interpretar literalmente `b0` (la nota de escritura cuando la de lectura es 0) en este
caso? ¿Por qué?

<details>
<summary>Ver solución explicada</summary>

a) Sube aproximadamente **0.99 puntos** por cada punto adicional en lectura (eso es `b1`, casi 1 a 1).

b) `writing score = -0.67 + 0.99 * 80 = -0.67 + 79.2 = 78.53` → aproximadamente **78.8 puntos** (el cálculo
exacto con los coeficientes completos da 78.81).

c) Casi no tiene sentido práctico: un puntaje de lectura de 0 es un caso extremo que casi nunca ocurre en
este examen, así que `b0` aquí es sobre todo un punto matemático necesario para definir la recta, no algo
que debamos interpretar literalmente como "la nota de escritura de alguien que sacó cero en lectura".

</details>

## 4. Regresión lineal y la IA

La regresión lineal no es solo un tema "de estadística clásica": es la base conceptual de muchos modelos de
IA:

- Es, en sí misma, uno de los algoritmos de *machine learning* más usados para tareas de predicción de
  valores numéricos (lo que se llama un problema de **regresión**, en contraste con **clasificación**, donde
  se predicen categorías, como si un estudiante aprobó o no aprobó).
- Los modelos más complejos (regresión logística, redes neuronales, modelos de *deep learning*) parten de la
  misma idea: combinar variables de entrada con pesos (coeficientes) para producir una salida, y luego
  ajustar esos pesos con los datos. Un sistema que combinara `reading score`, `math score` y otras variables
  con pesos ajustados, para predecir `writing score`, sigue exactamente esa lógica.
- Entender bien la regresión lineal (qué son los coeficientes, cómo se interpretan, cómo se evalúa si el
  modelo es bueno) da las bases para entender modelos de IA mucho más sofisticados más adelante.

**Ejercicio 4.** Imagina un modelo que predice `writing score` usando tanto `reading score` como
`math score`, cada uno con su propio peso (coeficiente). Explica, en tus palabras, por qué eso sigue siendo,
en el fondo, la misma idea que una regresión lineal simple con una sola variable.

<details>
<summary>Ver solución explicada</summary>

Porque la ecuación solo se extiende de `Y = b0 + b1*X` a `Y = b0 + b1*X1 + b2*X2`: sigue siendo una
combinación lineal (sumas y multiplicaciones simples) de las variables de entrada, cada una con su propio
peso. No hay ninguna función "rara" en el medio que tuerza la relación; simplemente ahora hay dos pendientes
en vez de una. Muchos modelos de IA más complejos agregan funciones no lineales entre las combinaciones de
variables, pero la idea de "pesos que se multiplican por variables y se suman" nace exactamente aquí.

</details>

## 5. Flujo para llevar a cabo una regresión lineal

Un flujo típico para construir y validar un modelo de regresión lineal, usando `reading score` y
`writing score` como ejemplo:

1. **Explorar los datos**: revisar valores faltantes, atípicos, y graficar `reading score` contra
   `writing score` (¿se ve una tendencia lineal, como una línea de puntos subiendo?).
2. **Plantear el modelo**: elegir la variable dependiente (`writing score`) y la(s) independiente(s)
   (`reading score`).
3. **Ajustar el modelo**: calcular los coeficientes (`b0`, `b1`) que minimizan el error entre lo predicho y
   lo real (método de mínimos cuadrados).
4. **Evaluar los coeficientes**: revisar el p-value de `reading score` (paso 2 de esta hoja) para saber si
   su efecto es estadísticamente significativo.
5. **Evaluar el ajuste global**: revisar métricas como el **R²** (qué tanto de la variación de `writing
   score` explica el modelo, de 0 a 1; en este caso, alrededor de 0.91) y el error de predicción.

   El **R²** compara el error que comete el modelo ($SS_{res}$, la misma suma de errores al cuadrado de
   arriba) contra el error que se cometería si simplemente predijéramos siempre el promedio de `Y`
   ($SS_{tot}$):

   $$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}{\sum_{i=1}^{n}(y_i-\bar{y})^2}$$

   Un $R^2 = 0.91$ significa que el modelo explica el 91 % de la variación de `writing score`; el 9 %
   restante es error que el modelo no captura. Ese mismo error se resume, en la escala original de las
   notas, con el **error estándar de los residuos** (qué tan lejos, en promedio, cae la predicción de la
   nota real):

   $$RMSE = \sqrt{\frac{SS_{res}}{n}} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$$
6. **Revisar supuestos**: verificar que los residuos (diferencias entre la nota real y la predicha) se
   comporten de manera razonable (sin patrones raros, más o menos distribuidos "normal").
7. **Predecir / interpretar**: usar el modelo para predecir la nota de escritura de un estudiante nuevo, o
   para explicar qué tanto se relacionan leer bien y escribir bien.

### Ejemplo aplicado: revisar la homogeneidad de varianzas con Levene

El paso 6 (revisar supuestos) suena abstracto hasta que se aplica a datos reales. Un supuesto muy común de
comprobar es la **homogeneidad de varianzas**: que la dispersión de `Y` sea parecida entre distintos grupos
de `X`, sobre todo cuando `X` es una variable categórica (por ejemplo, `gender`).

*Situación real:* `writing score` entre hombres (n=482, media=63.31) y mujeres (n=518, media=72.47).

- **H0 (Levene):** las dos varianzas son iguales — hombres y mujeres tienen una dispersión de notas
  igualmente "pareja".
- **H1 (Levene):** las varianzas son distintas.
- **Resultado real:** Levene, p = 0.934.

Como `0.934 > 0.05`, **no se rechaza H0**: la variabilidad de `writing score` es prácticamente igual en
ambos grupos, aunque sus promedios sean muy distintos (72.47 vs. 63.31). Esto valida usar una prueba t
clásica (o, de forma equivalente, una regresión lineal con `gender` como variable 0/1) para comparar esos
promedios: al hacerlo, se obtiene `t ≈ -9.98`, `p ≈ 2×10⁻²²` — una diferencia real y muy significativa a
favor de las mujeres.

**Dato para conectar con el resto de la hoja:** comparar dos grupos con una prueba t es, matemáticamente, un
caso particular de regresión lineal donde `X` es una variable "dummy" (0 = hombre, 1 = mujer):

$$\text{writing score} = b_0 + b_1 \times \text{gender}_{\text{(1 = mujer)}}$$

El coeficiente `b1` de esa regresión es, justamente, la diferencia de promedios entre grupos:

$$b_1 = \bar{y}_{\text{mujeres}} - \bar{y}_{\text{hombres}} = 72.47 - 63.31 \approx 9.16 \text{ puntos}$$

Y el estadístico de la prueba t que compara ambos promedios se calcula así (versión con varianzas iguales,
válida aquí porque Levene no rechazó H0):

$$t = \frac{\bar{y}_{\text{mujeres}} - \bar{y}_{\text{hombres}}}{SE(\bar{y}_{\text{mujeres}} - \bar{y}_{\text{hombres}})} \approx -9.98$$

Es exactamente el mismo número (con el signo cambiado según qué grupo se reste primero) que arrojaría el
p-value del coeficiente `b1` en la regresión con la variable dummy: dos formas distintas de hacer la misma
pregunta.

**Ejercicio 5.** Ordena estos pasos como deberían ocurrir en un flujo de regresión lineal (ya están
mezclados): "revisar el R² del modelo", "graficar `reading score` contra `writing score` para ver si la
relación se ve lineal", "calcular los coeficientes b0 y b1", "predecir el puntaje de escritura de un
estudiante nuevo a partir de su puntaje de lectura".

<details>
<summary>Ver solución explicada</summary>

1. Graficar `reading score` contra `writing score` para ver si la relación se ve lineal (exploración).
2. Calcular los coeficientes b0 y b1 (ajustar el modelo).
3. Revisar el R² del modelo (evaluar el ajuste).
4. Predecir el puntaje de escritura de un estudiante nuevo a partir de su puntaje de lectura (predicción).

</details>

## 6. Usos de la regresión lineal

La regresión lineal se usa en muchísimos contextos, por ejemplo:

- **Educación**: como en este mismo ejemplo, predecir un puntaje (escritura) a partir de otro (lectura), o
  a partir de horas de estudio, para identificar estudiantes que podrían necesitar apoyo.
- **Economía y finanzas**: predecir precios, ventas, o el efecto de una tasa de interés.
- **Salud**: relacionar hábitos (horas de sueño, ejercicio) con indicadores de salud (presión arterial,
  peso).
- **Negocios**: predecir cuántas unidades se venderán según la inversión en publicidad.
- **Ciencia de datos e IA**: como línea base ("baseline") antes de probar modelos más complejos, y como
  pieza fundamental dentro de modelos más grandes.

**Ejercicio 6.** Para cada situación, indica si tendría sentido usar una regresión lineal para responderla, y
por qué:

a) Predecir el puntaje de escritura (`writing score`) de un estudiante a partir de su puntaje de matemáticas
(`math score`).
b) Predecir si un estudiante aprobó o no aprobó el examen (sí/no) a partir de sus puntajes.

<details>
<summary>Ver solución explicada</summary>

a) **Sí tiene sentido**: `writing score` es una variable numérica continua, y buscamos ver cómo cambia en
función de otra variable numérica (`math score`); es exactamente el tipo de problema para el que se diseñó
la regresión lineal. (Dato real: en este caso, `b0 ≈ 14.9`, `b1 ≈ 0.80`, y el modelo explica cerca del 64%
de la variación en `writing score`, un poco menos que con `reading score`.)

b) **No es el caso ideal**: la variable a predecir ("aprobó" o "no aprobó") es una categoría, no un número
continuo. Para este tipo de problema se usa un modelo de **clasificación** (por ejemplo, regresión
logística), no una regresión lineal clásica.

</details>

---

## Resumen

1. **Estadística e IA**: la IA, en el fondo, usa herramientas estadísticas para encontrar y validar patrones
   en los datos, como la relación entre leer bien y escribir bien.
2. **Pruebas de hipótesis en regresión**: el p-value de cada variable nos dice si su efecto es real o podría
   ser puro azar.
3. **Regresión lineal**: busca la recta `Y = b0 + b1*X` que mejor describe la relación entre variables, para
   explicar y predecir.
4. **Regresión lineal y la IA**: es la base conceptual de modelos de IA más complejos que combinan variables
   con pesos ajustables.
5. **Flujo**: explorar → plantear → ajustar → evaluar coeficientes → evaluar ajuste global → revisar
   supuestos → predecir.
6. **Usos**: predicción de puntajes, precios, ventas, indicadores de salud, y como base de modelos de IA más
   avanzados.
