# La estadística explicada

Esta hoja te explica, con ejemplos sencillos, las ideas que necesitas para resolver la actividad de la Semana 6 (el portafolio con el archivo `StudentsPerformance.csv`, que tiene las notas de 1000 estudiantes).

---

## 1. Estadística descriptiva vs. estadística inferencial

Imagina que cuentas cuántos dulces tiene cada compañero de tu salón, y sacas el promedio. Eso es solo **contar y resumir lo que ya viste**: eso es la **estadística descriptiva**.

Ahora imagina que, con esos datos de tu salón, quieres adivinar cuántos dulces tienen en promedio **todos los niños del país**, aunque no los hayas contado a todos. Eso es **adivinar con evidencia**, y así funciona la **estadística inferencial**: usar un grupo pequeño (lo que sí mediste) para sacar una conclusión sobre un grupo mucho más grande (lo que no mediste).

En nuestra actividad: contamos las notas de 1000 estudiantes (descriptiva) para tratar de entender qué pasa con **todos** los estudiantes que presentan ese examen (inferencial).

**La fórmula, por si la quieres ver:**

> x̄ = (x₁ + x₂ + ... + xₙ) / n
>
> - x̄ ("x barra") = el promedio
> - x₁, x₂, ..., xₙ = cada uno de los valores de la muestra
> - n = cuántos valores hay
>
> En palabras: sumas todos los valores y divides entre cuántos son. Es justo lo que hace
> `df["math score"].mean()` en Python — ahora ya sabes qué calcula por dentro.

**Ejercicio 1.** En `StudentsPerformance.csv`, 642 estudiantes no tomaron el curso de preparación (promedio de matemáticas = 64.08) y 358 sí lo tomaron (promedio = 69.70).

a) La frase *"el promedio de matemáticas del grupo que sí tomó el curso es 69.70"* ¿es descriptiva o inferencial?
b) La frase *"el curso de preparación mejora el promedio de matemáticas de todos los estudiantes que presentan este examen, no solo los de esta muestra"* ¿es descriptiva o inferencial?
c) En tus palabras: ¿por qué hay que dar el salto de a) a b) con cuidado, y no basta con ver que 69.70 > 64.08?

<details>
<summary>Ver solución explicada</summary>

a) **Descriptiva**: es solo un cálculo directo sobre los datos que ya tenemos, un resumen de lo observado.

b) **Inferencial**: generaliza la conclusión más allá de los 1000 estudiantes de la muestra, hacia toda la
población de estudiantes que presentan el examen.

c) Porque la diferencia que vemos en la muestra (69.70 vs. 64.08) podría deberse simplemente al azar de qué
1000 estudiantes en particular terminaron en nuestros datos, y no a un efecto real del curso. Para dar el
salto de manera responsable hace falta una prueba de hipótesis que calcule qué tan probable es ver esa
diferencia si el curso, en realidad, no tuviera ningún efecto.

</details>

## 2. Población y muestra

- **Población** = TODOS los estudiantes que existen y presentan este examen en el mundo. Es imposible preguntarles a todos.
- **Muestra** = el grupito que sí alcanzamos a medir: los 1000 estudiantes del archivo.

Es como si quisieras saber qué película le gusta más a todo tu colegio, pero solo puedes preguntarle a un salón. Ese salón es tu muestra; el colegio completo es tu población.

**Ejercicio 2.** Piensa en la pregunta: *"¿el nivel educativo de los padres influye en el puntaje de
matemáticas de los estudiantes que presentan este examen, en cualquier parte del mundo?"* En el *dataset*,
la columna `parental level of education` tiene 6 grupos; el más pequeño (`master's degree`) tiene solo 59
estudiantes, mientras que el más grande (`some college`) tiene 226.

a) ¿Cuál es la población en este caso?
b) ¿Cuál es la muestra?
c) ¿Por qué ese grupo de solo 59 estudiantes podría darnos una idea menos confiable de su verdadero promedio
que el grupo de 226?

<details>
<summary>Ver solución explicada</summary>

a) **Población**: todos los estudiantes del mundo que presentan este examen, sin importar si están o no en
el archivo.

b) **Muestra**: los 1000 estudiantes de `StudentsPerformance.csv`.

c) Con una muestra pequeña dentro de un grupo, cada estudiante individual "pesa" mucho más en el promedio: un
solo estudiante con una nota muy alta o muy baja puede mover bastante el resultado. Con 226 estudiantes, un
caso atípico se diluye mucho más y el promedio calculado tiende a estar más cerca del verdadero promedio de
la población.

</details>

**La fórmula detrás del inciso c):**

> SE = s / √n
>
> - SE (*error estándar*) = qué tan lejos esperamos, en promedio, que esté el promedio de nuestra muestra
>   del promedio real de la población
> - s = desviación estándar de la muestra (qué tan "revueltos" están los datos)
> - n = tamaño de la muestra
>
> Fíjate que n está dividiendo dentro de una raíz: mientras más grande el grupo, más chico se vuelve SE — es
> decir, más confiable es el promedio. Por eso el grupo de 226 estudiantes (`some college`) da un promedio
> más confiable que el de solo 59 (`master's degree`).

## 3. Variables: la que "causa" y la que "se mide"

En nuestros datos hay cosas que se miden (los puntajes) y cosas que podrían explicar por qué el puntaje sube o baja (por ejemplo, si el estudiante tomó o no un curso de preparación).

- **Variable dependiente**: la nota de matemáticas (`math score`). Es la que queremos explicar.
- **Variable independiente**: si tomó el curso de preparación (`test preparation course`). Es la que podría estar influyendo.

Piénsalo como plantas: si riegas una planta y no riegas otra, "regar o no regar" es la variable independiente, y "qué tan alto creció" es la variable dependiente.

**La fórmula para el caso b) (dos variables numéricas, sin dependiente/independiente fija):**

> r = Σ(xᵢ - x̄)(yᵢ - ȳ) / √[Σ(xᵢ - x̄)² · Σ(yᵢ - ȳ)²]
>
> - r = coeficiente de correlación (siempre entre -1 y 1)
> - x̄, ȳ = el promedio de cada una de las dos variables
>
> No necesitas calcularla a mano: `df["reading score"].corr(df["writing score"])` la hace por ti. La idea es
> simple: r cerca de 1 (o de -1) significa que las dos variables se mueven muy juntas; r cerca de 0 significa
> que casi no hay relación entre ellas.

**Ejercicio 3.** Para cada pregunta de investigación con el *dataset*, identifica la variable dependiente y
la independiente:

a) ¿El tipo de almuerzo (`lunch`) se relaciona con el puntaje de escritura (`writing score`)?
b) ¿El puntaje de lectura (`reading score`) se relaciona con el puntaje de escritura (`writing score`)?
c) ¿El género (`gender`) se relaciona con el puntaje de matemáticas (`math score`)?

<details>
<summary>Ver solución explicada</summary>

a) Dependiente: `writing score` (lo que se mide). Independiente: `lunch` (lo que podría influir).

b) Aquí las dos son numéricas y se busca una **correlación**, no un efecto de una sobre otra: no hay una
dependiente/independiente fija — cualquiera de las dos podría plantearse como "la que se mide".

c) Dependiente: `math score`. Independiente: `gender`.

</details>

## 4. Hipótesis: H0 y H1 (como una apuesta)

Una **hipótesis** es simplemente una idea que queremos comprobar con datos, antes de saber si es cierta o no. Cuando queremos comprobar algo, hacemos como una apuesta con dos opciones:

- **H0 (hipótesis nula)**: "no pasa nada especial, todo es igual". Ejemplo: "el curso de preparación NO cambia la nota de matemáticas".
- **H1 (hipótesis alternativa)**: "sí pasa algo, sí hay diferencia". Ejemplo: "el curso de preparación SÍ cambia la nota de matemáticas".

Con los datos, buscamos evidencia para decidir cuál de las dos apuestas gana.

**En notación formal**, para cuando compares dos promedios (como en el Ejercicio 4):

> H0: μ₁ = μ₂
> H1: μ₁ ≠ μ₂
>
> μ ("mu") representa el promedio de **toda la población** (no el de la muestra, que se escribe x̄) de cada
> grupo. H0 dice que esos dos promedios poblacionales son iguales; H1 dice que son distintos.

**Ejercicio 4.** Plantea H0 y H1 (en palabras, como una apuesta) para esta pregunta: *"¿el tipo de almuerzo
(`lunch`: `standard` vs. `free/reduced`) se relaciona con el puntaje de escritura (`writing score`)?"*

<details>
<summary>Ver solución explicada</summary>

**H0:** "no pasa nada especial: el tipo de almuerzo no cambia el puntaje de escritura; en el fondo, los dos
grupos tienen el mismo promedio."

**H1:** "sí pasa algo: el puntaje de escritura sí difiere según el tipo de almuerzo."

(Dato real para verificar más adelante: el promedio de `writing score` es 70.82 en el grupo `standard` y
63.02 en el grupo `free/reduced` — una diferencia real que se puede poner a prueba justo con estas
hipótesis.)

</details>

## 5. El p-value: "¿qué tan sorprendido deberías estar?"

El **p-value** es un número que te dice qué tan raro (o normal) sería el resultado que viste, **si en realidad H0 fuera cierta** (si de verdad no pasara nada especial).

- Si el p-value es **muy chiquito** (menos de 0.05), es como si dijeras: "¡qué casualidad tan rara! Esto casi no podría pasar por azar" → entonces **rechazamos H0** (creemos que sí hay diferencia real).
- Si el p-value es **grande** (0.05 o más), es como decir: "esto podría pasar fácilmente por azar, no es tan raro" → entonces **no rechazamos H0** (no hay evidencia suficiente de diferencia).

El número 0.05 es como la regla del juego que usamos siempre: "si la probabilidad de que sea pura casualidad es menor al 5%, le creemos a H1".

**En notación formal:**

> p = P(dato tan extremo o más extremo que el observado | H0 es verdadera)
>
> Se lee: "la probabilidad de los datos, suponiendo que H0 es cierta". Es una probabilidad *condicional*: no
> es la probabilidad de que H0 sea verdadera, sino la probabilidad de los datos *si* H0 lo fuera — dos cosas
> muy distintas.

**Ejercicio 5.** Al comparar el puntaje de matemáticas entre estudiantes con curso de preparación y sin él,
se obtiene un p-value de 0.00000008 (casi cero).

a) ¿Ese resultado es "chiquito" o "grande" según la regla de 0.05?
b) ¿Le creemos a H0 o a H1?
c) En tus palabras: si el curso en realidad no tuviera ningún efecto, ¿qué tan sorprendido deberías estar de
ver una diferencia tan grande entre los dos grupos?

<details>
<summary>Ver solución explicada</summary>

a) **Chiquito** — muchísimo menor a 0.05.

b) Le creemos a **H1**: se rechaza H0.

c) Deberíamos estar **muy sorprendidos**: sería casi imposible ver una diferencia de casi 5.6 puntos entre
642 y 358 estudiantes solo por pura casualidad, si el curso realmente no tuviera ningún efecto sobre la nota.

</details>

## 6. Dos formas de equivocarse (errores tipo I y tipo II)

Imagina la alarma contra incendios de tu casa:

- **Error tipo I** (falsa alarma): la alarma suena, pero no hay ningún incendio. Aquí sería: decir "sí hay diferencia" cuando en realidad NO la hay.
- **Error tipo II** (no darte cuenta): hay un incendio de verdad, pero la alarma NO suena. Aquí sería: decir "no hay diferencia" cuando en realidad SÍ la hay.

Nadie puede evitar los dos errores al 100% al mismo tiempo, pero mientras más datos tengamos (como nuestros 1000 estudiantes), menos probable es que nos equivoquemos sin darnos cuenta (error tipo II).

**Las probabilidades detrás de cada error:**

> α = P(rechazar H0 | H0 es verdadera) → probabilidad de error tipo I (por convención, α = 0.05)
> β = P(no rechazar H0 | H0 es falsa) → probabilidad de error tipo II
> Poder estadístico = 1 − β → probabilidad de detectar un efecto real cuando sí existe
>
> Cuantos más datos tengas, más chico se vuelve β (y más grande el poder estadístico) — por eso, con 1000
> estudiantes, es más difícil que un efecto real se nos escape sin darnos cuenta.

**Ejercicio 6.** Imagina que, por pura casualidad en la muestra, concluimos que *"el curso de preparación SÍ
mejora la nota"* cuando en realidad, en toda la población de estudiantes del mundo, el curso no tiene ningún
efecto real.

a) ¿Qué tipo de error es este: I o II?
b) Ahora al revés: concluimos que *"el curso NO tiene efecto"* cuando en realidad sí lo tiene. ¿Qué tipo de
error es este?
c) ¿Por qué tener 1000 estudiantes en la muestra (en vez de, digamos, 20) ayuda a cometer menos el error del
inciso b)?

<details>
<summary>Ver solución explicada</summary>

a) **Error tipo I** (falsa alarma: decimos que sí hay diferencia cuando en realidad no la hay).

b) **Error tipo II** (no darse cuenta: hay un efecto real, pero no lo detectamos).

c) Con más datos, las pruebas estadísticas tienen más capacidad ("poder estadístico") para detectar un efecto
real, incluso si es pequeño. Con una muestra muy chica, un efecto real puede pasar desapercibido simplemente
porque no hay suficiente evidencia acumulada para distinguirlo del azar.

</details>

## 7. ¿Los datos se comportan "normal"? (los supuestos)

Antes de usar ciertas herramientas estadísticas, hay que revisar si los datos se comportan de una manera esperada, como si midieras la estatura de tus compañeros: la mayoría está en la mitad (ni muy bajitos ni muy altos), y pocos están en los extremos. Eso forma una especie de "campana". A esto le llamamos **normalidad**.

También revisamos si los grupos que comparamos tienen una variedad parecida (que unos no estén súper "revueltos" y otros súper "parejos"). A esto le llamamos **homogeneidad de varianzas**.

Estas revisiones son como probar el agua con el dedo antes de meterte a la piscina: te dicen qué herramienta (prueba estadística) es segura usar después.

**La fórmula de la variabilidad (la misma s de la Sección 2):**

> s² = Σ(xᵢ - x̄)² / (n - 1)      s = √s²
>
> s² es la **varianza** (qué tan "revueltos" están los datos); su raíz cuadrada, s, es la **desviación
> estándar** — la misma que aparece en la fórmula del error estándar (Sección 2). Cuando decimos que dos
> grupos tienen "una variabilidad parecida" (homogeneidad de varianzas), estamos comparando este número
> entre los grupos.

**Ejercicio 7.** Si separas las notas de matemáticas en dos grupos (con curso de preparación y sin curso) y
calculas cuánto varían las notas dentro de cada uno, obtienes una variabilidad parecida en los dos grupos
(ambos con una desviación estándar de aproximadamente 14 a 15 puntos).

a) ¿Esto describe la **normalidad** o la **homogeneidad de varianzas**?
b) ¿Por qué es importante revisar esto *antes* de comparar los promedios de los dos grupos, y no después?

<details>
<summary>Ver solución explicada</summary>

a) **Homogeneidad de varianzas**: describe qué tan parecida es la "variedad" (dispersión) de las notas
dentro de cada grupo, comparando un grupo con el otro.

b) Porque algunas herramientas estadísticas (las "paramétricas", como la prueba t clásica) asumen que esa
variedad es parecida entre los grupos para funcionar correctamente. Revisarlo antes evita usar una
herramienta cuyos supuestos los propios datos no cumplen, lo que podría llevar a una conclusión equivocada.

</details>

## 8. ¿Qué herramienta uso? (elegir la prueba)

Según lo que encontremos al "probar el agua":

- Si los datos se comportan "normal" → usamos herramientas **paramétricas** (como la prueba t o ANOVA).
- Si los datos NO se comportan "normal" → usamos herramientas **no paramétricas** (como Mann-Whitney U o Kruskal-Wallis), que funcionan igual de bien sin necesitar esa forma de campana.

No te preocupes por memorizar estos nombres: lo importante es la idea — hay una herramienta para cuando los datos se comportan "normal" y otra para cuando no, y las dos te ayudan a responder la misma pregunta.

**Las fórmulas de las dos herramientas paramétricas:**

> Prueba t (2 grupos):  t = (x̄₁ - x̄₂) / SE
>
> ANOVA (3+ grupos):  F = MSB / MSW
>
> En los dos casos la idea es la misma: arriba va "qué tan separados están los grupos", abajo va "cuánta
> variabilidad esperaríamos de todos modos, solo por azar". Un t o una F grandes (comparados con lo que el
> azar produciría) llevan a un p-value chiquito.

**Ejercicio 8.** La columna `race/ethnicity` del *dataset* tiene 5 grupos (A a E), con tamaños entre 89 y
319 estudiantes, y promedios de matemáticas que van de 61.63 (grupo A) hasta 73.82 (grupo E).

a) ¿Aquí estamos comparando 2 grupos o más de 2?
b) Si los datos de cada grupo se comportan "normal", ¿qué herramienta paramétrica usarías? (No es la prueba
t: esa solo compara 2 grupos a la vez.)
c) Si no se comportan "normal", ¿cuál sería la alternativa no paramétrica?

<details>
<summary>Ver solución explicada</summary>

a) **Más de 2** — son 5 grupos.

b) **ANOVA**, diseñada para comparar las medias de 3 o más grupos al mismo tiempo.

c) **Kruskal-Wallis**, la versión no paramétrica de ANOVA.

(Dato real: al aplicar estas dos pruebas sobre los 5 grupos étnicos se obtiene ANOVA con *p* = 1.37×10⁻¹¹ y
Kruskal-Wallis con *p* = 1.19×10⁻¹¹ — ambas coinciden en que sí hay diferencias en el puntaje de matemáticas
entre, al menos, algunos de los grupos.)

</details>

---

## Resumen para tu portafolio (en una frase cada uno)

1. **Descriptiva**: resumo lo que veo. **Inferencial**: adivino con evidencia sobre todos, a partir de una parte.
2. **Población**: todos. **Muestra**: el grupo que sí medí.
3. **Variable dependiente**: lo que se mide. **Independiente**: lo que podría influir.
4. **H0**: no pasa nada. **H1**: sí pasa algo.
5. **p-value**: qué tan raro sería el resultado si H0 fuera cierta. Si es menor a 0.05, le creo a H1.
6. **Error tipo I**: falsa alarma. **Error tipo II**: no darme cuenta de algo real.
7. **Supuestos**: reviso cómo se comportan los datos antes de elegir la herramienta.
8. **Prueba**: paramétrica si los datos son "normales"; no paramétrica si no lo son.

## Fórmulas de referencia rápida

| Concepto | Fórmula | Sección |
|---|---|---|
| Promedio (media) | x̄ = Σxᵢ / n | 1 |
| Error estándar | SE = s / √n | 2 |
| Varianza / desviación estándar | s² = Σ(xᵢ - x̄)² / (n - 1) ; s = √s² | 7 |
| Correlación | r = Σ(xᵢ-x̄)(yᵢ-ȳ) / √[Σ(xᵢ-x̄)² · Σ(yᵢ-ȳ)²] | 3 |
| Hipótesis (2 grupos) | H0: μ₁ = μ₂ ; H1: μ₁ ≠ μ₂ | 4 |
| p-value | p = P(datos \| H0 verdadera) | 5 |
| Errores tipo I / II | α = P(rechazar H0 \| H0 verdadera) ; β = P(no rechazar H0 \| H0 falsa) | 6 |
| Prueba t (2 grupos) | t = (x̄₁ - x̄₂) / SE | 8 |
| ANOVA (3+ grupos) | F = MSB / MSW | 8 |

No necesitas memorizar estas fórmulas para hacer la actividad — `pandas` y `scipy.stats` las calculan por
ti (lo verás en `Taller_03_Prueba_Hipotesis_conceptos.md`). Están aquí para que, cuando el código te dé un
número, sepas de dónde sale.
