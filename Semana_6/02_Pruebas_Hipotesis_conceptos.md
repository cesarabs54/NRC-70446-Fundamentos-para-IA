# Semana 6 — Estadística Inferencial I: Prueba de Hipótesis

Este documento retoma las ideas de [`01_Estadistica_inferencial_conceptos.md`](01_Estadistica_inferencial_conceptos.md)
(población, muestra, variables, H0/H1, p-value, errores, supuestos) y se enfoca en la mecánica completa de
**aplicar y leer una prueba de hipótesis**: cómo se plantea, qué resultados produce y cómo se interpretan.
Aquí solo se explica la parte estadística — sin código de programación. Todos los ejemplos y ejercicios usan
`StudentsPerformance.csv` (1000 estudiantes), el mismo *dataset* del portafolio; si quieres ver cómo se
calcula todo esto con Python, esa versión está en el *notebook* del portafolio y en
[`Taller_02_Prueba_Hipotesis.md`](Taller_03_Prueba_Hipotesis_conceptos.md).

Si nunca has visto estos conceptos, empieza por el documento `01`; si ya los conoces y quieres ver cómo se
aplican paso a paso, sigue leyendo aquí.

---

## 1. ¿Qué es una prueba de hipótesis y para qué sirve?

Todos los días tomamos decisiones con información incompleta: un entrenador decide si un nuevo método de
entrenamiento realmente mejora el rendimiento del equipo, o si el buen resultado del último mes fue
casualidad; una tienda decide si una promoción realmente aumentó las ventas, o si coincidió con un fin de
semana con más gente en la calle.

Una **prueba de hipótesis** es el procedimiento formal para responder ese tipo de preguntas: usa una
**muestra** de datos para decidir si un patrón que observamos (una diferencia entre grupos, una relación entre
variables) es real, o si es lo bastante pequeño como para explicarse solo por el azar del muestreo.

En nuestro caso: algunos estudiantes tomaron un curso de preparación antes del examen y otros no. ¿El curso
realmente está asociado con mejores notas, o la diferencia que se ve en los datos podría deberse simplemente
a qué estudiantes quedaron en la muestra?

**Ejercicio 1.** Para cada situación con `StudentsPerformance.csv`, decide si es (o no) una candidata natural
para una prueba de hipótesis, y explica por qué:

a) Comparar el promedio de `math score` entre hombres y mujeres, para saber si la diferencia observada en la
muestra también se sostendría en toda la población de estudiantes que presentan el examen.
b) Simplemente reportar cuántos estudiantes hay en cada grupo de `lunch` (`standard` vs. `free/reduced`).
c) Decidir si la relación que se ve entre `reading score` y `writing score` en la muestra también se
cumpliría para todos los estudiantes que presentan este examen, o si podría deberse al azar de quién quedó
en los datos.

<details>
<summary>Ver solución explicada</summary>

a) **Sí es candidata.** Hay una comparación entre grupos y una pregunta de generalización: ¿la diferencia
observada refleja algo real de la población, o es azar de la muestra?

b) **No es candidata.** Es pura descripción/conteo (estadística descriptiva): no hay ninguna comparación con
incertidumbre por resolver, solo se está resumiendo lo que ya se observó.

c) **Sí es candidata.** Aunque aquí la pregunta es sobre una relación entre dos variables numéricas (una
correlación) y no sobre una diferencia entre grupos, sigue siendo el mismo tipo de salto: de "lo que vi en
la muestra" a "lo que sería cierto en la población".

</details>

---

## 2. H0 y H1, en notación formal

Recordando el documento `01`: toda prueba de hipótesis arranca con dos afirmaciones que compiten entre sí.

- **H0 (hipótesis nula):** no hay diferencia / no hay efecto / no hay relación. Se escribe, por ejemplo, como
  μ₁ = μ₂ (las medias de los dos grupos son iguales).
- **H1 (hipótesis alternativa):** sí hay diferencia. Se escribe μ₁ ≠ μ₂ (prueba de dos colas) o μ₁ > μ₂ /
  μ₁ < μ₂ si la pregunta tiene una dirección específica (prueba de una cola).

En este documento trabajaremos siempre con pruebas de **dos colas** (no asumimos de antemano en qué dirección
iría la diferencia), que es el caso más común y más conservador.

Para comparar más de dos grupos a la vez se usa una prueba distinta a la t de Student, llamada **ANOVA**
(*Análisis de Varianza*): en vez de comparar los grupos de dos en dos, los compara todos juntos en un solo
test. La aplicarás con código en `Taller_03_Prueba_Hipotesis_conceptos.md`; aquí trabajemos primero las
hipótesis.

**Ejercicio 2.** Quieres investigar si el nivel educativo de los padres (`parental level of education`, que
en el *dataset* tiene 6 categorías: *some high school, high school, some college, associate's degree,
bachelor's degree, master's degree*) se relaciona con el puntaje de matemáticas.

a) Escribe H0 y H1 para esta pregunta.
b) ¿Por qué H0 no se puede escribir simplemente como "las medias son diferentes"?

<details>
<summary>Ver solución explicada</summary>

a) **H0:** μ₁ = μ₂ = μ₃ = μ₄ = μ₅ = μ₆ (las medias de `math score` son iguales en los 6 grupos). **H1:** al
menos una de las medias es diferente de las demás.

b) Porque "las medias son diferentes" sugiere que *todas* difieren entre sí, y eso no es lo que se pone a
prueba. H1 solo afirma que existe *al menos una* diferencia en algún par de grupos — podría ser que 5 de los
6 grupos tengan medias casi idénticas y uno solo se separe del resto, y aun así H1 sería la conclusión
correcta. (Dato real: al comparar estos 6 grupos se obtiene *p* = 5.59×10⁻⁶ → se rechaza H0; para saber
*cuáles* grupos específicos difieren haría falta una prueba adicional, llamada comparación *post-hoc*, que
queda fuera del alcance de este documento.)

</details>

**La fórmula de ANOVA (la aplicarás con código en el taller):**

> F = MSB / MSW = [SSB / (k−1)] / [SSW / (N−k)]
>
> - SSB (*suma de cuadrados entre grupos*) = Σ nᵢ(x̄ᵢ − x̄)² → qué tan separadas están las medias de los
>   grupos entre sí
> - SSW (*suma de cuadrados dentro de los grupos*) = ΣΣ(xᵢⱼ − x̄ᵢ)² → qué tan dispersos son los datos
>   dentro de cada grupo
> - k = número de grupos; N = tamaño total de la muestra
>
> Con los 6 niveles educativos: SSB ≈ 7295.6, SSW ≈ 222393.5, dfB = k−1 = 5, dfW = N−k = 994 → **F = 6.52**
> (el mismo *p* = 5.59×10⁻⁶ del Ejercicio 2). Un F grande significa que la variabilidad *entre* grupos supera
> bastante a la variabilidad *dentro* de cada grupo — señal de que sí hay diferencias reales.

---

## 3. Nivel de significancia (α) y valor p

- **α (nivel de significancia):** el umbral de riesgo que aceptamos de antemano para rechazar H0 por error.
  Por convención (Fisher, principios del siglo XX), se usa **α = 0.05**.
- **p-value:** la probabilidad de observar un resultado tan extremo como el tuyo (o más), **asumiendo que H0
  es cierta**. No es la probabilidad de que H0 sea verdadera — es una probabilidad *condicional* sobre los
  datos, dado H0.

**Regla de decisión:**

| Comparación | Decisión | Interpretación |
|---|---|---|
| p-value < α | Se rechaza H0 | Evidencia estadísticamente significativa a favor de H1 |
| p-value ≥ α | No se rechaza H0 | No hay evidencia suficiente para descartar H0 |

**La idea detrás de cualquier estadístico de prueba:**

> estadístico = (diferencia observada − diferencia esperada bajo H0) / error estándar de la diferencia
>
> Todas las pruebas que verás en este documento (t, F, U) siguen esta misma lógica; solo cambia cómo se
> calcula el "error estándar de la diferencia" en cada caso. Entre más grande el estadístico (en valor
> absoluto), más raro sería el resultado si H0 fuera cierta — y más chico el p-value.

**Ejercicio 3.** Aplicaste una prueba y obtuviste *p*-value = 0.023, con α = 0.05.

a) ¿Rechazas o no rechazas H0?
b) Redacta la conclusión en una frase, sin usar la palabra "p-value".
c) ¿Qué error cometerías si dijeras: "hay un 2.3% de probabilidad de que H0 sea verdadera"?

<details>
<summary>Ver solución explicada</summary>

a) Como 0.023 < 0.05, **se rechaza H0**.

b) "Hay evidencia estadísticamente significativa de que existe una diferencia entre los grupos."

c) Confundirías dos probabilidades distintas: el *p*-value es la probabilidad de los datos observados
**asumiendo que H0 es cierta** — P(datos | H0) —, no la probabilidad de que H0 sea cierta dados los datos —
P(H0 | datos). Son cantidades diferentes y no se pueden intercambiar (es el mismo error lógico que confundir
"la probabilidad de toser si tienes gripa" con "la probabilidad de tener gripa si toses").

</details>

---

## 4. Proceso paso a paso

1. **Plantear la pregunta y las hipótesis** (H0 y H1), antes de mirar los resultados.
2. **Elegir las variables**: identificar la variable dependiente (lo que se mide) y la independiente (lo que
   se compara).
3. **Describir la muestra**: tamaño de cada grupo, medias, desviaciones estándar.
4. **Validar los supuestos**: normalidad (con la prueba de Shapiro-Wilk) y homogeneidad de varianzas (con la
   prueba de Levene), para decidir entre una prueba paramétrica o no paramétrica.
5. **Aplicar la prueba** y obtener el estadístico y el p-value.
6. **Comparar el p-value con α** y tomar la decisión sobre H0.
7. **Traducir el resultado a lenguaje natural**, conectado con la pregunta original — un número solo no le
   sirve a nadie.

**La fórmula de Levene (paso 4, homogeneidad de varianzas):**

> Zᵢⱼ = |xᵢⱼ − medianaᵢ|
>
> W = [(N−k)/(k−1)] × [Σ nᵢ(Z̄ᵢ − Z̄)²] / [ΣΣ(Zᵢⱼ − Z̄ᵢ)²]
>
> La idea: primero mides qué tan lejos está cada dato de la mediana de su propio grupo (Zᵢⱼ); si esas
> distancias son parecidas entre grupos, las varianzas son homogéneas. (La prueba de Shapiro-Wilk, para
> normalidad, tiene una fórmula más compleja que no se calcula a mano — siempre se deja a
> `scipy.stats.shapiro()`.)

**Ejercicio 4.** (Caso hipotético, con fines de práctica.) Estás en el paso 4: comparas dos grupos
independientes en una variable numérica y obtienes estos resultados: Shapiro-Wilk grupo A → *p* = 0.002;
Shapiro-Wilk grupo B → *p* = 0.41; Levene (varianzas) → *p* = 0.03.

    a) ¿Se cumple la normalidad en los dos grupos?
    b) ¿Se cumple la homogeneidad de varianzas?
    c) ¿Qué prueba usarías en el paso 5 para comparar las medias, y por qué?

<details>
<summary>Ver solución explicada</summary>

a) No de forma conjunta: el grupo A tiene *p* = 0.002 (< 0.05, se rechaza la normalidad); el grupo B sí
parece normal (*p* = 0.41).

b) No: Levene da *p* = 0.03 (< 0.05), por lo que se rechaza la homogeneidad de varianzas — los dos grupos
tienen variabilidad distinta.

c) Con normalidad y homogeneidad fallando, lo más apropiado es la prueba de **Mann-Whitney U** (no
paramétrica, no exige ninguno de los dos supuestos). Si por alguna razón se prefiere una prueba paramétrica,
existe una variante de la prueba t diseñada justamente para cuando las varianzas no son homogéneas: la
**prueba t de Welch**, que no asume varianzas iguales entre grupos.

</details>

---

## 5. Ejemplo aplicado completo: `math score` según `gender`

**Paso 1 — Planteamiento.**

*Pregunta:* ¿existe una diferencia significativa en el puntaje de matemáticas entre estudiantes hombres y
mujeres?

- H0: μ(hombres) = μ(mujeres)
- H1: μ(hombres) ≠ μ(mujeres)

**Paso 2 — Variables.** Dependiente: `math score` (numérica). Independiente: `gender` (categórica, 2 grupos).

**Paso 3 — Describir la muestra.** Al separar el *dataset* por `gender`, se obtiene:

| Grupo | n | Media | Desv. estándar |
|---|---|---|---|
| Hombres | 482 | 68.73 | 14.36 |
| Mujeres | 518 | 63.63 | 15.49 |

**Paso 4 — Validar supuestos.** Shapiro-Wilk: hombres → *p* = 0.038; mujeres → *p* = 0.0035. Levene
(varianzas) → *p* = 0.556.

Ambos grupos obtienen *p-value* < 0.05 en Shapiro-Wilk (formalmente, se rechaza la normalidad), pero Levene
indica varianzas homogéneas (*p* = 0.556). Con muestras grandes (n > 480 por grupo), Shapiro-Wilk es muy
sensible a desviaciones pequeñas de la normalidad que no invalidan la prueba t gracias al **Teorema del
Límite Central** — por eso, en la práctica, se reporta la prueba t como principal y Mann-Whitney U como
verificación, en vez de descartar la prueba t por completo.

**Paso 5 — Aplicar la prueba t** de Student: t = 5.3832, df = 998, *p*-value = 9.12×10⁻⁸. Como verificación,
Mann-Whitney U: *p*-value = 4.28×10⁻⁷ (misma conclusión).

**¿De dónde sale ese t = 5.38?** La fórmula, para 2 grupos independientes, es:

> sp² = [(n₁−1)s₁² + (n₂−1)s₂²] / (n₁+n₂−2)      (varianza combinada de los dos grupos)
> SE = √(sp² × (1/n₁ + 1/n₂))
> t = (x̄₁ − x̄₂) / SE

Con los números de la tabla del Paso 3 (n₁=482, x̄₁=68.73, s₁=14.36; n₂=518, x̄₂=63.63, s₂=15.49): sp² ≈
223.68, SE ≈ 0.947, t ≈ (68.73−63.63)/0.947 ≈ 5.39 — muy cerca del 5.3832 que da `scipy.stats.ttest_ind`
con los datos exactos (la pequeña diferencia es solo por el redondeo de la tabla).

**Paso 6 — Decisión.** p-value ≪ α (0.05) en ambas pruebas → **se rechaza H0**.

**Paso 7 — Interpretación.** Hay evidencia estadísticamente muy fuerte de que el puntaje promedio de
matemáticas difiere entre hombres y mujeres en esta muestra: los hombres promedian cerca de 5 puntos más. Al
tratarse de datos observacionales (no un experimento aleatorizado), esto es una **asociación**, no una prueba
de causalidad — podría reflejar factores sociales o educativos de fondo no registrados en el *dataset*.

**Ejercicio 5.** Repite el razonamiento de los pasos 6 y 7 (decisión e interpretación) con estos resultados,
ya calculados, para `writing score` según `lunch`:

| Grupo | n | Media |
|---|---|---|
| `standard` | 645 | 70.82 |
| `free/reduced` | 355 | 63.02 |

    - Levene (varianzas): p = 0.105.
    - Prueba t: t = 8.01, p = 3.19×10⁻¹⁵. 
    - Mann-Whitney U: p = 5.08×10⁻¹⁴.

    a) ¿Se rechaza o no se rechaza H0?
    b) Redacta la interpretación en una frase, conectada con la pregunta de si el tipo de almuerzo se relaciona
    con el puntaje de escritura.

<details>
<summary>Ver solución explicada</summary>

a) Ambas pruebas dan *p*-value muchísimo menor que α = 0.05 → **se rechaza H0**.

b) "Hay evidencia estadísticamente muy fuerte de que el puntaje de escritura difiere según el tipo de
almuerzo: los estudiantes con almuerzo `standard` promedian cerca de 7.8 puntos más que los de
`free/reduced`. Al ser datos observacionales, esto es una asociación — podría reflejar diferencias
socioeconómicas de fondo — y no prueba que el tipo de almuerzo *cause* directamente el puntaje."

</details>

---

## 6. Errores comunes al interpretar resultados

- **"No significativo" ≠ "no hay diferencia".** Un p-value alto solo indica que no hay evidencia suficiente
  con estos datos; no demuestra que H0 sea verdadera.
- **p pequeño ≠ efecto grande.** El p-value mide qué tan improbable es el resultado bajo H0, no qué tan
  grande es la diferencia. Con muestras grandes (como n=1000), hasta diferencias pequeñas producen p-values
  diminutos — para el tamaño del efecto se usan otras medidas (p. ej., la diferencia de medias en unidades
  reales, o *Cohen's d*).
- **Asociación ≠ causalidad.** Rechazar H0 en datos observacionales no prueba que una variable *cause* la
  otra; podría haber variables de confusión de por medio.
- **"Pescar" resultados (*p-hacking*).** Probar muchas combinaciones de variables hasta encontrar una con
  *p* < 0.05, y reportar solo esa, es engañoso: con suficientes intentos, algo "dará significativo" por puro
  azar.

**La fórmula de Cohen's d (tamaño del efecto):**

> d = (x̄₁ − x̄₂) / sp
>
> Usa la misma varianza combinada (sp, de la fórmula de la prueba t) para expresar la diferencia en
> "unidades de desviación estándar". A diferencia del p-value, d no depende del tamaño de la muestra. Por
> convención: d ≈ 0.2 es un efecto chico, 0.5 mediano, 0.8 grande.
>
> Para `math score` según `gender`: d ≈ 0.34 (efecto chico-a-mediano) — a pesar de que el p-value fue
> astronómicamente chiquito (9.12×10⁻⁸). Ahí está, en números, el punto de "p pequeño ≠ efecto grande": la
> significancia estadística y el tamaño real del efecto son dos preguntas distintas.

**Ejercicio 6.** Un compañero concluye: *"Obtuve un p-value de 0.001, así que estoy 99.9% seguro de que el
curso de preparación causa la mejora en la nota."*

Identifica **dos** errores distintos en esta afirmación y corrígelos.

<details>
<summary>Ver solución explicada</summary>

**Error 1 — Mal uso del p-value como "certeza".** Un p-value de 0.001 no significa "99.9% de seguridad de que
H1 es cierta". El p-value no mide la probabilidad de una hipótesis; mide qué tan compatibles son los datos
con H0. Nunca se resta de 1 para obtener una "probabilidad de H1".

**Error 2 — Afirmar causalidad a partir de datos observacionales.** Rechazar H0 solo indica una diferencia
estadísticamente significativa entre grupos; no prueba que una variable *cause* la otra. Para hablar de
causa se necesitaría, por ejemplo, un experimento aleatorizado (asignar al azar quién toma el curso y quién
no), algo que este *dataset* no tiene.

**Corrección:** "Obtuve un p-value de 0.001 (menor que α = 0.05), lo que es evidencia estadísticamente
significativa de que el curso de preparación está asociado con una mejor nota — aunque, al ser datos
observacionales, no puedo afirmar que el curso sea la causa."

</details>

**Ejercicio 7.** Vas a comparar `math score` entre los grupos `group A` y `group E` de `race/ethnicity`, dos
veces: primero con una muestra pequeña (los primeros 10 estudiantes de cada grupo), y luego con el grupo
completo.

- **Muestra pequeña** (n = 10 por grupo): `group A` media = 57.50, `group E` media = 66.70 (diferencia =
  9.20 puntos). Prueba t → *p* = 0.2585.
- **Grupo completo** (`group A`: n = 89; `group E`: n = 140): `group A` media = 61.63, `group E` media =
  73.82 (diferencia = 12.19 puntos). Prueba t → *p* = 1.08×10⁻⁸.

a) ¿En cuál de los dos casos se rechaza H0 (con α = 0.05)?
b) La diferencia observada es parecida en ambos casos (9.20 y 12.19 puntos), pero la decisión sobre H0
cambia. ¿Qué cambió entre un caso y otro para explicar esto?
c) Si solo tuvieras la muestra pequeña, ¿sería correcto concluir "no hay diferencia entre los grupos"?

<details>
<summary>Ver solución explicada</summary>

a) Con la muestra pequeña **no se rechaza H0** (0.2585 ≥ 0.05); con el grupo completo **sí se rechaza H0**
(1.08×10⁻⁸ < 0.05).

b) Lo único que cambió fue el tamaño de la muestra (n = 10 por grupo vs. n = 89 y 140); la diferencia real
entre los grupos es parecida en los dos casos, pero con pocos datos hay demasiada incertidumbre para
detectarla con confianza — al estudio pequeño le falta "poder estadístico". Es el error "p pequeño ≠ efecto
grande" visto al revés: aquí un efecto real puede quedar sin detectar solo por falta de muestra, no porque
no exista. (Misma idea que el Ejercicio 6 de `Taller_02_Estadistica_inferencial_conceptos.md`, con una
submuestra de 50 estudiantes.)

c) No. "No se rechaza H0" no equivale a "H0 es verdadera": solo significa que, con esos 10 estudiantes por
grupo, no hubo evidencia suficiente. El resultado con el grupo completo muestra que la diferencia sí existe;
la muestra pequeña simplemente no alcanzaba para detectarla con confianza — este es justamente el riesgo de
un **error tipo II** (ver Ejercicio 8).

</details>

**Ejercicio 8.** *(Ejemplo fuera de `StudentsPerformance.csv`, a propósito: los errores tipo I/II se
entienden mejor con un caso de alto riesgo, como uno médico, que con notas de examen.)* Un hospital evalúa un
tratamiento nuevo para la presión arterial. H0: el tratamiento nuevo
no reduce la presión más que el estándar. H1: sí la reduce más.

a) Describe qué significaría, en este contexto, cometer un **error tipo I**.
b) Describe qué significaría cometer un **error tipo II**.
c) ¿Cuál de los dos te parece más grave en este caso? Justifica (no hay una única respuesta correcta).

<details>
<summary>Ver solución explicada</summary>

a) **Error tipo I:** rechazar H0 cuando en realidad es verdadera — es decir, concluir que el tratamiento
nuevo funciona mejor cuando en realidad no hace ninguna diferencia. Consecuencia: se adopta un tratamiento
que no aporta beneficio real, con sus costos y posibles efectos secundarios innecesarios.

b) **Error tipo II:** no rechazar H0 cuando en realidad es falsa — es decir, concluir que no hay diferencia
cuando el tratamiento nuevo sí es mejor. Consecuencia: se descarta un tratamiento realmente efectivo,
privando a futuros pacientes de un beneficio real.

c) Respuesta abierta: en un contexto médico, muchas veces se argumenta que el error tipo II es más grave
(negar un tratamiento que sí funciona), pero depende de los riesgos y costos del tratamiento — si tiene
efectos secundarios severos, el error tipo I podría ser el más grave. Lo importante es justificar la
respuesta con el contexto, no memorizar cuál error es "siempre peor".

</details>

---

## Resumen (referencia rápida)

| Concepto | En una frase |
|---|---|
| Prueba de hipótesis | Usar una muestra para decidir si un patrón observado es real o azar |
| H0 / H1 | "No pasa nada" vs. "sí pasa algo" |
| α = 0.05 | El umbral de riesgo aceptado por convención |
| p-value | Qué tan raro sería el resultado si H0 fuera cierta |
| Decisión | p < α → se rechaza H0; p ≥ α → no se rechaza H0 |
| Supuestos | Normalidad (Shapiro-Wilk) y homogeneidad de varianzas (Levene) antes de elegir la prueba |
| t de Student / Mann-Whitney U | Comparar 2 grupos (paramétrica / no paramétrica) |
| Interpretación | Traducir el resultado a la pregunta original, distinguiendo asociación de causalidad |

## Fórmulas de referencia rápida

| Concepto | Fórmula |
|---|---|
| ANOVA | F = MSB/MSW = [SSB/(k−1)] / [SSW/(N−k)] |
| Estadístico de prueba (general) | (diferencia observada − diferencia esperada bajo H0) / error estándar |
| Levene (homogeneidad de varianzas) | W = [(N−k)/(k−1)] × Σnᵢ(Z̄ᵢ−Z̄)² / ΣΣ(Zᵢⱼ−Z̄ᵢ)², con Zᵢⱼ = \|xᵢⱼ−medianaᵢ\| |
| Prueba t de Student (2 grupos) | t = (x̄₁−x̄₂) / √(sp²(1/n₁+1/n₂)) |
| Cohen's d (tamaño del efecto) | d = (x̄₁−x̄₂) / sp |

Estas son las mismas fórmulas que `scipy.stats` calcula por ti en
[`Taller_03_Prueba_Hipotesis_conceptos.md`](Taller_03_Prueba_Hipotesis_conceptos.md) (y que ves
implementadas paso a paso en el *notebook* del profesor).

**Material relacionado en esta carpeta:** presentación [`02_Prueba_Hipotesis.pptx`](02_Prueba_Hipotesis_conceptos_profesor.pptx),
taller [`Taller_02_Prueba_Hipotesis.md`](Taller_03_Prueba_Hipotesis_conceptos.md) (con código en Python y su clave de
respuestas), y el documento conceptual previo
[`01_Estadistica_inferencial_conceptos.md`](01_Estadistica_inferencial_conceptos.md).
