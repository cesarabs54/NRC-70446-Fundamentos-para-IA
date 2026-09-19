# Regresión logística: conceptos básicos

Esta hoja te explica, con ejemplos sencillos, las ideas que necesitas para la Semana 8. Seguimos usando el
archivo `StudentsPerformance.csv` (el mismo de las Semanas 6 y 7), con las notas de 1000 estudiantes en tres
exámenes: matemáticas (`math score`), lectura (`reading score`) y escritura (`writing score`). La diferencia
con la Semana 7 es que ahora no vamos a predecir una nota (un número continuo), sino algo binario: si un
estudiante **aprueba o no** matemáticas, usando como umbral `math score >= 60`.

---

## 1. De predecir números a predecir categorías

En la Semana 7 aprendiste a predecir un número (`writing score`) a partir de otro número (`reading score`)
con una regresión lineal. Pero muchas preguntas importantes no se responden con un número, sino con un
"sí o no": ¿este estudiante aprueba o no aprueba?, ¿este correo es spam o no es spam?, ¿este paciente tiene
o no una enfermedad?

Esto es un problema de **clasificación**, y la **regresión logística** es la herramienta más básica e
importante para resolverlo cuando el resultado tiene dos categorías (clasificación **binaria**). En vez de
predecir directamente "aprueba" o "no aprueba", predice **la probabilidad** de que ocurra el evento que nos
interesa (por ejemplo, "probabilidad de aprobar"), y luego esa probabilidad se convierte en una decisión
(sí/no) usando un umbral, típicamente 0.5.

- La **estadística descriptiva** nos ayuda a entender los datos antes de clasificar (¿qué proporción de
  estudiantes aprueba?, ¿cómo se distribuye `reading score` entre los que aprueban y los que no?).
- La **estadística inferencial** nos ayuda a decidir si una variable (como `reading score`) realmente aporta
  información para predecir si alguien aprueba, o si esa aparente relación es azar de la muestra.
- La regresión logística es, junto con la regresión lineal, uno de los dos "modelos base" que casi todo
  científico de datos aprende primero: la lineal para predecir números, la logística para predecir
  categorías.

**Ejercicio 1.** De los 1000 estudiantes del archivo, 677 aprueban matemáticas (`math score >= 60`) y 323 no
aprueban.

a) ¿Por qué no tendría sentido usar una regresión lineal clásica para predecir directamente "aprobó" (1) o
"no aprobó" (0) a partir de `reading score`?
b) ¿Qué papel juega la estadística descriptiva antes de construir el modelo de clasificación?

<details>
<summary>Ver solución explicada</summary>

a) Porque la variable a predecir solo puede valer 0 o 1, mientras que una recta de regresión lineal
(`Y = b0 + b1*X`) puede dar cualquier valor, incluyendo números negativos o mayores a 1, que no tienen sentido
como "probabilidad de aprobar". Además, la relación entre `reading score` y la probabilidad de aprobar no es
una línea recta, sino una curva en forma de "S" (como se ve en la sección 3).

b) Permite explorar los datos antes de modelar: ver qué proporción aprueba y no aprueba (677 vs. 323), y
comparar cómo se distribuye `reading score` entre ambos grupos (por ejemplo, con un histograma o un
boxplot), para tener una primera idea de si el puntaje de lectura parece diferenciar a quienes aprueban de
quienes no.

</details>

## 2. ¿Cómo sabemos si la variable realmente ayuda a clasificar? Pruebas de hipótesis

Igual que en regresión lineal, no basta con que el modelo "se vea bien": necesitamos **pruebas de
hipótesis** para decir con seriedad que una variable ayuda a predecir la categoría.

- **H0 (hipótesis nula)**: la variable NO tiene relación real con la probabilidad del evento (su coeficiente
  verdadero es cero). Ejemplo: "el puntaje de lectura no tiene ninguna relación real con la probabilidad de
  aprobar matemáticas".
- **H1 (hipótesis alternativa)**: la variable SÍ tiene una relación real con esa probabilidad. Ejemplo: "el
  puntaje de lectura sí tiene una relación real con la probabilidad de aprobar matemáticas".

En regresión logística, cada variable tiene un coeficiente y un **p-value** asociado (viene de una prueba
llamada **prueba de Wald**, basada en un estadístico *z*): nos dice qué tan probable sería observar el
coeficiente que vemos si, en realidad, esa variable no influyera en nada. Si el p-value es menor a 0.05,
rechazamos H0 y decimos que la variable sí aporta información útil para clasificar.

Antes de ver la tabla, vale la pena separar dos ideas que se confunden fácil: **probabilidad** y **momios
(*odds*)**.

- La **probabilidad** de aprobar es simplemente `p`, un número entre 0 y 1.
- Los **momios (*odds*)** comparan la probabilidad de que el evento ocurra con la probabilidad de que **no**
  ocurra (su **complemento**, `1 - p`):

```
odds = p / (1 - p)
```

**Analogía:** es la misma idea de las apuestas deportivas. Si un equipo tiene "momios de 3 a 1" para ganar,
se considera 3 veces más probable que gane a que pierda (`odds = 3`). Si `odds > 1`, el evento es **más
probable** que su contrario; si `odds < 1`, es **menos probable**.

**Ejemplo con los datos:** para un estudiante con `reading score = 70`, el modelo estima `p ≈ 0.814` (lo
vas a calcular tú mismo en el Ejercicio 3). Sus momios de aprobar son
`0.814 / (1 - 0.814) = 0.814/0.186 ≈ 4.38`: casi 4.4 veces más probable que apruebe a que no apruebe.

Con esto se entiende mejor la última fila de la siguiente tabla, la **razón de momios (odds ratio)**: no
compara `p` contra `1-p` para un solo estudiante, sino cómo cambian esos momios cuando `X` sube en una
unidad.

| Concepto | Descripción breve | Importancia |
|---|---|---|
| **Coeficiente (b1)** | Mide cómo cambia el *log-odds* (la versión "en escala logarítmica" de la probabilidad) del evento por cada unidad que sube la variable independiente. | Su signo indica si la variable aumenta o disminuye la probabilidad del evento; su tamaño, junto con el p-value, indica qué tan fuerte y confiable es esa relación. |
| **Prueba de Wald (z, p-value)** | Plantea H0 ("el coeficiente verdadero es cero") y H1 ("es distinto de cero"), y usa el estadístico *z* y su p-value para decidir. | Da un criterio objetivo para saber si una variable realmente ayuda a clasificar o si su aparente efecto es solo azar de la muestra de 1000 estudiantes. |
| **Razón de momios (odds ratio)** | Es `e^b1`: cuánto se multiplican los momios (odds) del evento por cada unidad adicional en la variable. | Traduce el coeficiente (difícil de interpretar directamente) a un número más intuitivo: "por cada punto extra de lectura, los momios de aprobar se multiplican por tanto". |

**Ejercicio 2.** Al ajustar una regresión logística con `reading score` para predecir si un estudiante
aprueba matemáticas (`math score >= 60`), se obtiene un coeficiente `b1 ≈ 0.167`, con un estadístico *z*
de aproximadamente 15.3 y un p-value prácticamente cero.

a) Plantea H0 y H1 para esta variable.
b) ¿Rechazamos o no H0?
c) En tus palabras, ¿qué significa ese resultado sobre la relación entre el puntaje de lectura y la
probabilidad de aprobar matemáticas?

<details>
<summary>Ver solución explicada</summary>

a) **H0:** el puntaje de lectura (`reading score`) no tiene ninguna relación real con la probabilidad de
aprobar matemáticas; su coeficiente verdadero es cero. **H1:** el puntaje de lectura sí tiene una relación
real con esa probabilidad.

b) **Rechazamos H0**: el p-value es muchísimo menor a 0.05, así que la evidencia en contra de "no hay
relación" es abrumadora.

c) Significa que es prácticamente imposible que la relación que vemos entre `reading score` y la probabilidad
de aprobar matemáticas se deba solo a la casualidad de estos 1000 estudiantes: leer mejor está asociado de
forma real (y positiva) con una mayor probabilidad de aprobar matemáticas.

</details>

## 3. ¿Qué es la regresión logística y para qué sirve?

La **regresión logística** busca la curva (no la recta) que mejor describe la relación entre una o más
variables independientes (`X`) y la **probabilidad** de que ocurra un evento binario (`Y = 1` si aprueba,
`Y = 0` si no aprueba). En vez de una línea recta, usa una curva en forma de "S" llamada **función
sigmoide**, que siempre da valores entre 0 y 1 (como debe ser una probabilidad).

Hay dos formas equivalentes de escribir el mismo modelo, y conviene reconocer ambas:

**Forma clásica — el modelo es lineal en el *logit* (log-odds), no en la probabilidad:**

```
log( p(x) / (1 - p(x)) ) = b0 + b1 * X
```

**Analogía:** piensa en la probabilidad como una manguera doblada en forma de "S" — es difícil medirla con
una regla recta porque se curva. El *logit* (`log(p/(1-p))`, el logaritmo de los momios que viste arriba) es
como "desdoblar" esa manguera: convierte la curva en una línea recta, para poder seguir usando la misma idea
de "combinación lineal de variables" que ya conocías de la regresión lineal (Semana 7). Por eso se dice que
la regresión logística es **lineal en el logit**, y esta es, de hecho, la forma en la que suele presentarse
el modelo en un examen o en un libro de texto.

**Forma práctica — el mismo modelo, pero calculado en dos pasos, útil para hacer las cuentas a mano:**

```
z = b0 + b1 * X                (combinación lineal, igual que en regresión lineal)
P(Y = 1) = 1 / (1 + e^(-z))    (función sigmoide: convierte z en una probabilidad entre 0 y 1)
```

- `b0` e `b1` se interpretan sobre `z` (el *log-odds*), no directamente sobre la probabilidad: por eso se
  suele reportar también el **odds ratio** (`e^b1`) para facilitar la interpretación.
- Cuando `z` es muy negativo, `P(Y=1)` se acerca a 0; cuando `z` es muy positivo, `P(Y=1)` se acerca a 1;
  cuando `z = 0`, `P(Y=1) = 0.5`.
- Para tomar una decisión (aprueba / no aprueba), se compara `P(Y=1)` contra un **umbral** (normalmente 0.5):
  si `P(Y=1) >= 0.5`, se predice "aprueba"; si no, "no aprueba".

Sirve para dos cosas principales:

1. **Explicar**: entender qué tanto y en qué dirección una variable influye sobre la probabilidad de un
   evento (¿leer mejor se relaciona con mayor probabilidad de aprobar matemáticas?).
2. **Predecir / clasificar**: una vez tenemos la ecuación, podemos calcular la probabilidad de aprobar para
   un estudiante nuevo del que solo conocemos su puntaje de lectura, y decidir si lo clasificamos como
   "aprueba" o "no aprueba".

**Ejercicio 3.** Con `StudentsPerformance.csv`, al ajustar
`P(aprueba matemáticas) = sigmoide(b0 + b1 * reading score)` se obtiene aproximadamente `b0 = -10.23` y
`b1 = 0.167`.

a) Calcula `z` y luego `P(Y=1)` para un estudiante con `reading score = 50`. ¿Lo clasificarías como que
aprueba o no aprueba matemáticas (umbral 0.5)?
b) Calcula `P(Y=1)` para un estudiante con `reading score = 80`. ¿Qué decisión tomarías?
c) El odds ratio de `reading score` es `e^0.167 ≈ 1.18`. En tus palabras, ¿qué significa ese número?
d) Calcula los **momios (*odds*)** de aprobar para el estudiante de la parte b) (`reading score = 80`).
¿Son mayores o menores a 1? ¿Qué significa eso?

<details>
<summary>Ver solución explicada</summary>

a) `z = -10.23 + 0.167*50 = -10.23 + 8.35 = -1.88`. `P(Y=1) = 1/(1+e^1.88) ≈ 0.134`, es decir, **13.4%** de
probabilidad de aprobar. Como es menor a 0.5, se **clasifica como "no aprueba"**.

b) `z = -10.23 + 0.167*80 = -10.23 + 13.36 = 3.13`. `P(Y=1) = 1/(1+e^-3.13) ≈ 0.959`, es decir, **95.9%** de
probabilidad de aprobar. Como es mayor a 0.5, se **clasifica como "aprueba"**.

c) Significa que, por cada punto adicional en `reading score`, los **momios (odds)** de aprobar matemáticas
se multiplican por aproximadamente 1.18 (un aumento del 18%). No es un aumento directo de "18 puntos de
probabilidad"; es un efecto sobre los momios, que se traduce en un aumento de probabilidad más fuerte quienes
están cerca del punto medio (donde `P ≈ 0.5`) que en los extremos (donde la probabilidad ya está muy cerca de
0 o de 1).

d) `odds = P/(1-P) = 0.959/(1-0.959) = 0.959/0.041 ≈ 23.4`. Como es mucho mayor a 1, para este estudiante es
**muchísimo más probable aprobar que no aprobar** (aproximadamente 23 a 1 a favor de aprobar) — coherente
con que su `P(Y=1)` ya está muy cerca de 1.

</details>

## 4. Regresión logística y la IA

La regresión logística no es solo un tema "de estadística clásica": es una pieza conceptual central de la
IA moderna:

- Es, en sí misma, uno de los algoritmos de *machine learning* más usados para tareas de **clasificación
  binaria**: detección de spam, diagnóstico médico (enfermo / sano), riesgo de crédito (paga / no paga),
  abandono de clientes (se va / se queda), etc.
- La función sigmoide que convierte `z` en una probabilidad es exactamente la misma idea que usa **una
  neurona** de una red neuronal con activación sigmoide: una combinación lineal de entradas con pesos,
  pasada por una función que "aplasta" el resultado entre 0 y 1. La regresión logística es, literalmente,
  la red neuronal más pequeña posible (una sola neurona).
- Cuando hay más de dos categorías (por ejemplo, clasificar una imagen en "gato", "perro" o "ave"), se usa
  una generalización de esta misma idea llamada **regresión softmax**, que es la capa de salida típica de
  muchas redes neuronales de clasificación.
- Entender bien la regresión logística (qué es `z`, qué hace la sigmoide, cómo se interpreta un coeficiente
  y un odds ratio, cómo se evalúa un clasificador) da las bases para entender clasificadores de IA mucho más
  sofisticados más adelante.

**Ejercicio 4.** Imagina un modelo que predice si un estudiante aprueba matemáticas usando tanto
`reading score` como `writing score`, cada uno con su propio peso (coeficiente). Explica, en tus palabras,
por qué eso sigue siendo, en el fondo, la misma idea que una regresión logística simple con una sola
variable.

<details>
<summary>Ver solución explicada</summary>

Porque `z` solo se extiende de `z = b0 + b1*X` a `z = b0 + b1*X1 + b2*X2`: sigue siendo una combinación
lineal (pesos multiplicados por variables y sumados) de las variables de entrada. Lo único que cambia es que
ahora `z` combina dos variables en vez de una; después, ese `z` se sigue pasando por la misma función
sigmoide para obtener una probabilidad entre 0 y 1. Esa es exactamente la estructura de "combinación lineal +
función que aplasta el resultado" que reaparece, multiplicada muchas veces, dentro de una red neuronal.

</details>

## 5. Flujo para llevar a cabo una regresión logística

Un flujo típico para construir y validar un modelo de regresión logística, usando `reading score` para
predecir si un estudiante aprueba matemáticas:

1. **Explorar los datos**: revisar cuántos estudiantes aprueban y cuántos no (677 vs. 323, en este caso), y
   comparar cómo se distribuye `reading score` entre ambos grupos.
2. **Plantear el modelo**: elegir la variable dependiente binaria (`aprueba matemáticas`: 1/0) y la(s)
   independiente(s) (`reading score`).
3. **Ajustar el modelo**: calcular los coeficientes (`b0`, `b1`) que hacen más probable observar los datos
   reales (método de **máxima verosimilitud**, distinto de los mínimos cuadrados de la regresión lineal).
4. **Evaluar los coeficientes**: revisar el p-value de `reading score` (sección 2) para saber si su efecto
   es estadísticamente significativo.
5. **Elegir un umbral y clasificar**: convertir la probabilidad predicha en una decisión (aprueba / no
   aprueba), típicamente con el umbral 0.5.
6. **Evaluar el desempeño del clasificador**: construir una **matriz de confusión** y calcular métricas como
   **exactitud (accuracy)**, **precisión** y **sensibilidad (recall)**.
7. **Predecir / interpretar**: usar el modelo para estimar la probabilidad de aprobar de un estudiante nuevo,
   o para explicar qué tanto se relaciona leer bien con la probabilidad de aprobar matemáticas.

Con el modelo del ejercicio 3 (umbral 0.5) sobre los 1000 estudiantes se obtiene esta matriz de confusión:

| | Predicho: no aprueba | Predicho: aprueba |
|---|---|---|
| **Real: no aprueba** | 227 (verdaderos negativos) | 96 (falsos positivos) |
| **Real: aprueba** | 72 (falsos negativos) | 605 (verdaderos positivos) |

De ahí se obtiene una **exactitud** de `(227+605)/1000 ≈ 83.2%`, una **precisión** de
`605/(605+96) ≈ 86.3%` (de los que el modelo dice que aprueban, qué porcentaje aprueba de verdad) y una
**sensibilidad** de `605/(605+72) ≈ 89.4%` (de los que sí aprueban, qué porcentaje detecta el modelo).

**Ejercicio 5.** Ordena estos pasos como deberían ocurrir en un flujo de regresión logística (ya están
mezclados): "calcular la exactitud y la matriz de confusión", "ajustar el modelo con máxima verosimilitud
para obtener b0 y b1", "comparar la proporción de aprobados y no aprobados en los datos", "clasificar a un
estudiante nuevo como aprueba/no aprueba según su probabilidad predicha".

<details>
<summary>Ver solución explicada</summary>

1. Comparar la proporción de aprobados y no aprobados en los datos (exploración).
2. Ajustar el modelo con máxima verosimilitud para obtener b0 y b1 (ajuste del modelo).
3. Calcular la exactitud y la matriz de confusión (evaluación del desempeño).
4. Clasificar a un estudiante nuevo como aprueba/no aprueba según su probabilidad predicha (predicción).

</details>

## 6. Usos de la regresión logística

La regresión logística se usa en muchísimos contextos, siempre que la pregunta sea de tipo "sí o no":

- **Educación**: como en este ejemplo, predecir si un estudiante aprueba o reprueba, o si abandona el
  curso, a partir de sus notas u otras variables.
- **Salud**: predecir si un paciente tiene o no una enfermedad a partir de síntomas o resultados de
  exámenes (diagnóstico).
- **Finanzas**: predecir si un cliente pagará o no un préstamo (riesgo de crédito), o si una transacción es
  fraudulenta.
- **Marketing**: predecir si un cliente comprará un producto, o si cancelará un servicio (*churn*).
- **Ciencia de datos e IA**: como línea base ("baseline") para cualquier problema de clasificación binaria
  antes de probar modelos más complejos (árboles de decisión, redes neuronales, etc.).

**Ejercicio 6.** Para cada situación, indica si tendría más sentido usar una regresión lineal o una
regresión logística, y por qué:

a) Predecir el puntaje exacto de matemáticas (`math score`) de un estudiante a partir de su puntaje de
lectura.
b) Predecir si un estudiante aprueba o no matemáticas (`math score >= 60`) a partir de su puntaje de
lectura.

<details>
<summary>Ver solución explicada</summary>

a) **Regresión lineal**: `math score` es una variable numérica continua (puede tomar muchos valores, no solo
dos), así que buscamos predecir directamente ese número; es el tipo de problema para el que se diseñó la
regresión lineal (como se vio en la Semana 7).

b) **Regresión logística**: la variable a predecir ("aprueba" o "no aprueba") es binaria, no un número
continuo. La regresión logística está diseñada justamente para modelar la probabilidad de un evento con dos
categorías y convertirla en una clasificación.

</details>

## 7. Una trampa común: modelar vs. validar, y el problema de la colinealidad

Hasta aquí viste **cómo se construye y se usa** el modelo (`z`, la sigmoide, el umbral, el odds ratio). Pero
hay una segunda capa, distinta, que se encarga de **auditar si ese modelo es confiable**: la validación
estadística (p-value, intervalo de confianza, y una advertencia importante llamada **colinealidad**).

**Colinealidad** ocurre cuando dos (o más) variables independientes están tan correlacionadas entre sí que
el modelo no puede distinguir bien el aporte de cada una por separado.

**Ejemplo con los datos:** en `StudentsPerformance.csv`, la correlación entre `reading score` y
`writing score` es de **0.95** (prácticamente perfecta). Si construyeras un modelo que use *ambas* variables
al mismo tiempo para predecir si un estudiante aprueba matemáticas, el modelo tendría dificultades para
"repartir" el efecto entre las dos: como casi siempre suben y bajan juntas, no hay suficiente información en
los datos para saber cuánto le corresponde a cada una por separado, y los coeficientes se vuelven inestables
(pueden cambiar mucho si agregas o quitas un estudiante de la muestra).

**Analogía:** es como preguntarle a dos testigos que vieron exactamente lo mismo, desde el mismo lugar, y
que además son mejores amigos: sus versiones van a coincidir casi siempre, así que es difícil saber cuál de
los dos "aporta" la información real y cuál solo está repitiendo al otro.

Con esto, ya puedes separar con claridad **qué pertenece a cada capa**:

| Modelado (construir y usar el modelo) | Validación estadística (auditar si es confiable) |
|---|---|
| predictor lineal `z`, logit | p-value (prueba de Wald) |
| función sigmoide | intervalo de confianza |
| umbral de decisión | colinealidad |
| odds ratio | significancia (¿es real o azar?) |

**Ejercicio 7.** Clasifica cada uno de estos términos como parte del **modelado** o de la **validación
estadística**: `sigmoide`, `p-value`, `odds ratio`, `intervalo de confianza`, `umbral`, `colinealidad`,
`z (predictor lineal)`.

<details>
<summary>Ver solución explicada</summary>

| Modelado | Validación estadística |
|---|---|
| sigmoide | p-value |
| odds ratio | intervalo de confianza |
| umbral | colinealidad |
| z (predictor lineal) | |

**Por qué:** sigmoide, odds ratio, umbral y `z` son piezas de **cómo el modelo calcula y comunica una
predicción**. p-value, intervalo de confianza y colinealidad son herramientas para **auditar si ese modelo
es confiable**: si el efecto de una variable es real (p-value, confianza) o si hay un problema que dificulta
confiar en los coeficientes (colinealidad, cuando dos variables predictoras están muy correlacionadas entre
sí, como `reading score` y `writing score` en este *dataset*).

</details>

---

## Resumen

1. **De números a categorías**: la regresión logística predice la probabilidad de un evento binario
   (aprueba / no aprueba), no un número continuo como la regresión lineal.
2. **Pruebas de hipótesis en regresión logística**: el p-value de cada coeficiente (prueba de Wald) nos dice
   si su efecto sobre la probabilidad del evento es real o podría ser puro azar.
3. **Regresión logística**: combina las variables en `z = b0 + b1*X` (equivalente a `log(p/(1-p)) = z`, el
   *logit*) y pasa ese resultado por una función sigmoide para obtener siempre una probabilidad entre 0 y 1.
4. **Regresión logística y la IA**: es, en esencia, la neurona más simple posible, y la base conceptual de
   los clasificadores usados en redes neuronales.
5. **Flujo**: explorar → plantear → ajustar (máxima verosimilitud) → evaluar coeficientes → elegir umbral y
   clasificar → evaluar desempeño (matriz de confusión, exactitud) → predecir.
6. **Usos**: diagnóstico médico, riesgo de crédito, detección de fraude, predicción de abandono, y como base
   de clasificadores de IA más avanzados.
7. **Modelar vs. validar**: sigmoide, umbral y odds ratio sirven para construir y usar el modelo; p-value,
   confianza y colinealidad sirven para auditar si ese modelo es confiable.
