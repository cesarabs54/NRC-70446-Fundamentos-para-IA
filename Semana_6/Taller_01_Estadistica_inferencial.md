# Taller: Estadística Inferencial

**Fundamentos para IA · NRC 94103**

**Dataset de referencia:** `StudentsPerformance.csv`. Todos los ejercicios son **solo estadística — sin
código Python**: se resuelven razonando sobre resultados ya dados. El objetivo es afianzar los conceptos de
estadística inferencial que vas a necesitar en las Semanas 7 y 8, cuando trabajes **regresión lineal**: probar
hipótesis sobre una correlación, interpretar una pendiente y un intercepto, leer el coeficiente de
determinación (R²), y reconocer los riesgos de extrapolar.

**Antes de empezar, recuerda:**

- **H0 / H1:** la apuesta de "no pasa nada" vs. "sí pasa algo".
- **p-value:** qué tan raro sería el resultado si H0 fuera cierta. Si p < α (0.05), se rechaza H0.
- **Correlación (r):** un número entre -1 y 1 que mide qué tan fuerte y en qué dirección se mueven juntas dos
  variables numéricas. Cerca de 0 = poca relación; cerca de ±1 = relación fuerte.
- **Regresión lineal:** además de decir *qué tan* relacionadas están dos variables (eso lo hace la
  correlación), ajusta una recta que permite **predecir** una variable a partir de la otra:
  `y = pendiente × x + intercepto`.

---

## Ejercicio 1 — Repaso: comparar dos grupos

*Situación:* se compara el puntaje de escritura (`writing score`) entre hombres y mujeres. Resultados:
hombres (n = 482, media = 63.31), mujeres (n = 518, media = 72.47). Prueba de Levene: p = 0.934. Prueba t:
t = -9.98, p = 2.02×10⁻²².

**Fórmula (repaso de la prueba t, Semana 6):**

> t = (x̄₁ − x̄₂) / √(sp²(1/n₁ + 1/n₂))     con     sp² = [(n₁−1)s₁² + (n₂−1)s₂²] / (n₁+n₂−2)
>
> Arriba va la diferencia de medias; abajo, el error estándar combinado de los dos grupos. (La fórmula
> completa de Levene está en `02_Pruebas_Hipotesis_conceptos.md`.)

**Preguntas:**

    a) Escribe H0 y H1 para esta comparación.
    b) Con Levene p = 0.934, ¿se cumple la homogeneidad de varianzas? ¿Por qué eso hace que la prueba t sea una
    buena elección aquí?
    c) Con el p-value de la prueba t, ¿qué decides sobre H0? Redacta la conclusión en una frase.

---

## Ejercicio 2 — Probar si una correlación es significativa (puente a regresión)

*Situación:* se calcula la correlación entre `math score` y `reading score`: r = 0.818, con p ≈ 0
(prácticamente cero, mucho menor que 0.001).

En una prueba de hipótesis sobre una correlación, las hipótesis se escriben así:

    - H0: ρ = 0 (no existe correlación real entre las dos variables en la población)
    - H1: ρ ≠ 0 (sí existe correlación real)

**La fórmula para poner a prueba una correlación:**

> t = r × √(n − 2) / √(1 − r²)     con     df = n − 2
>
> Este estadístico t se compara igual que el de la prueba t clásica: entre más grande (en valor absoluto),
> más chico el p-value. Con r = 0.818 y n = 1000: t = 0.818 × √998 / √(1 − 0.818²) ≈ **44.9** — un valor
> enorme, coherente con un p-value prácticamente cero.

**Preguntas:**

    a) Con ese p-value, ¿se rechaza o no se rechaza H0?
    b) El valor r = 0.818, ¿indica una correlación débil, moderada o fuerte? ¿Positiva o negativa?
    c) ¿Por qué necesitamos una prueba de hipótesis para la correlación, y no basta con mirar que r = 0.818 es
    "un número alto"? (Pista: piensa en qué pasaría si solo tuvieras 5 estudiantes en tu muestra en vez de
    1000.)

---

## Ejercicio 3 — Qué SÍ y qué NO te dice el coeficiente de correlación

*Situación:* la correlación entre `reading score` y `writing score` es r = 0.955 (calculada sobre los 1000
estudiantes).

**Preguntas:**

a) Clasifica esta correlación: ¿débil, moderada o fuerte? ¿Positiva o negativa?
b) ¿Un valor de r tan alto significa que leer bien *causa* escribir bien? Explica.
c) Si te dijeran "r = 0.955, entonces por cada punto que sube reading score, writing score sube 0.955
puntos", ¿esa afirmación es correcta? (Pista: eso no es lo que mide r — es lo que mide otra cosa, que verás
en el Ejercicio 4.)

---

## Ejercicio 4 — Interpretar una recta de regresión lineal simple

*Situación:* con esos mismos datos (`reading score` como variable predictora, `writing score` como variable
a predecir), se ajusta una recta de regresión:

**writing score = -0.6676 + 0.9935 × reading score**

**Cómo se calculan la pendiente y el intercepto:**

> pendiente (b₁) = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²
> intercepto (b₀) = ȳ − b₁ × x̄
>
> La pendiente es, en el fondo, la misma covarianza que usa la correlación (r), pero reescalada según la
> variabilidad de cada variable — por eso pendiente y r casi siempre tienen el mismo signo, aunque no sean el
> mismo número (ver Ejercicio 3c). Con los 1000 estudiantes, usando `reading score` como x y `writing score`
> como y, esta fórmula da exactamente b₁ = 0.9935 y b₀ = -0.6676 — los mismos números de la ecuación de
> arriba.

**Preguntas:**

a) ¿Qué representa el número **0.9935** (la pendiente)? Redacta su interpretación en una frase, en términos
de "por cada punto que sube/baja reading score...".
b) ¿Qué representaría, en teoría, el número **-0.6676** (el intercepto)? ¿Tiene sentido práctico un
`reading score` de 0 en este *dataset*?
c) Usa la fórmula para predecir el `writing score` de un estudiante con `reading score` = 80.

---

## Ejercicio 5 — Leer el coeficiente de determinación (R²)

*Situación:* para el mismo modelo del Ejercicio 4, R² = 0.911 (91.1%).

**La fórmula de R²:**

> R² = 1 − (SSres / SStot)
>
> - SSres = Σ(yᵢ − ŷᵢ)² → qué tan lejos quedan los datos reales de lo que predice la recta
> - SStot = Σ(yᵢ − ȳ)² → qué tan lejos quedan los datos reales de su propio promedio (sin usar el modelo)
>
> **Caso especial:** en una regresión lineal simple (una sola variable predictora, como aquí), R² es
> exactamente el cuadrado del coeficiente de correlación: **R² = r²**. Compruébalo: en el Ejercicio 3,
> r = 0.955 entre `reading score` y `writing score` → r² = 0.955² ≈ 0.911 — el mismo R² de este ejercicio.

**Preguntas:**

a) En tus palabras: ¿qué porcentaje de la variación en `writing score` "explica" el modelo a partir de
`reading score`?
b) ¿Qué podría explicar el otro 8.9% que el modelo no captura?
c) Si en otro modelo obtuvieras R² = 0.15 en vez de 0.911, ¿qué tan confiable sería usar ese segundo modelo
para predecir? Explica.

---

## Ejercicio 6 — El riesgo de extrapolar

*Situación:* en `StudentsPerformance.csv`, el `reading score` va de 17 a 100 (nunca hay un valor fuera de
ese rango). Usando la recta del Ejercicio 4, alguien calcula la predicción para un estudiante hipotético con
`reading score` = 150:

**writing score = -0.6676 + 0.9935 × 150 = 148.36**

**Preguntas:**

a) El `writing score` real en este *dataset* solo puede ir de 0 a 100. ¿Qué problema notas en el resultado de
148.36?
b) ¿Por qué es riesgoso usar un modelo de regresión para predecir con valores de x muy por fuera del rango
de datos con los que se construyó (aquí, 17 a 100)? A esto se le llama **extrapolar**.
c) ¿Cuál sería un rango razonable de `reading score` dentro del cual sí confiarías en las predicciones de
este modelo?

---

## Material relacionado

Conceptos base (Semana 6): [`01_Estadistica_inferencial_conceptos.md`](01_Estadistica_inferencial_conceptos.md)
y [`02_Pruebas_Hipotesis_conceptos.md`](02_Pruebas_Hipotesis_conceptos.md). Clave de respuestas de este
taller: [`Taller_01_Estadistica_inferencial_profesor.md`](Taller_01_Estadistica_inferencial_profesor.md).
Para la Semana 7 (regresión lineal), estos 6 ejercicios cubren exactamente el vocabulario que necesitarás:
correlación, pendiente, intercepto, R² y extrapolación.
