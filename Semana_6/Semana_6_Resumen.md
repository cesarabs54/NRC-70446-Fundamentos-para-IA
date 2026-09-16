# Estadística inferencial

**Dataset:** `StudentsPerformance.csv` — 1000 estudiantes, con su género, el nivel educativo de sus papás, y
sus notas en matemáticas, lectura y escritura.

---

## Paso 1 — ¿Qué es la estadística inferencial?

Imagina que tu mamá está cocinando una olla enorme de sopa y quiere saber si le falta sal. Ella **no se toma
toda la olla** para averiguarlo — prueba solo **una cucharada**. Si esa cucharada sabe bien, asume que toda
la olla sabe bien.

Eso es exactamente lo que hace la **estadística inferencial**: usa una "cucharada" de datos (una parte
pequeña) para adivinar cómo es el "plato completo" (todos los datos que existen), sin tener que medirlo
todo.

En nuestro caso: tenemos las notas de 1000 estudiantes. No son *todos* los estudiantes del mundo que
presentan este examen — son nuestra "cucharada". La estadística inferencial nos deja usar esos 1000 para
adivinar, con reglas serias (no a lo loco), qué pasa con *todos* los demás estudiantes que nunca vamos a
poder medir.

---

## Paso 2 — Concepto clave 1: muestras y poblaciones

- **Población** = TODOS los estudiantes del planeta que alguna vez presentan este examen. Imposible
  medirlos a todos.
- **Muestra** = los 1000 estudiantes que sí tenemos en `StudentsPerformance.csv`. Nuestra "cucharada".

**Ejemplo con el dataset:** la columna `parental level of education` (nivel educativo de los padres) tiene
6 grupos. El grupo más chico, `master's degree`, tiene solo 59 estudiantes; el más grande, `some college`,
tiene 226. Si calculas el promedio de matemáticas en el grupo de 59, ese número es **menos confiable** que
el promedio del grupo de 226 — con pocos datos, un solo estudiante con una nota muy rara puede mover mucho
el promedio. Con más datos, esos casos raros se "diluyen" y el promedio se acerca más a la verdad.

Es como adivinar el sabor de la sopa con media cucharada (poco confiable) vs. con un plato completo (mucho
más confiable), aunque ninguno de los dos sea la olla entera.

---

## Paso 3 — Concepto clave 2: hipótesis y pruebas estadísticas

Cuando queremos comprobar algo, hacemos como una **apuesta entre dos amigos**:

- **H0 (hipótesis nula):** "no pasa nada raro, todo es igual". Ejemplo: "el nivel educativo de los padres NO
  cambia la nota de matemáticas de sus hijos".
- **H1 (hipótesis alternativa):** "sí pasa algo". Ejemplo: "el nivel educativo de los padres SÍ se relaciona
  con la nota de matemáticas".

Para decidir quién gana la apuesta, usamos los datos y calculamos un número llamado **p-value** — piénsalo
como un "termómetro de sorpresa":

- Si el termómetro marca **muy bajo** (algo así como "esto casi no podría pasar por pura casualidad"), le
  creemos a H1: sí pasa algo raro.
- Si el termómetro marca **normal** (esto podría pasar fácil por azar), nos quedamos con H0: no hay
  evidencia de que pase algo especial.

La regla que casi todo el mundo usa: si el termómetro marca menos de **5%** (0.05), le creemos a H1.

---

## Paso 4 — Ejercicio guiado: ¿las notas de matemáticas son diferentes entre hombres y mujeres?

**Paso a paso, con los datos reales del CSV:**

1. **Miramos los promedios.** Separamos el dataset por género y calculamos el promedio de `math score`:
   - Hombres: 482 estudiantes, promedio = **68.73**
   - Mujeres: 518 estudiantes, promedio = **63.63**
   - Hay una diferencia de casi 5.1 puntos. Pero... ¿es una diferencia *real*, o pudo salir así solo por
     casualidad de quién quedó en la muestra?

2. **Planteamos la apuesta.**
   - H0: el promedio de matemáticas es igual entre hombres y mujeres (la diferencia de 5.1 puntos es pura
     casualidad).
   - H1: el promedio SÍ es diferente de verdad.

3. **Usamos la "máquina" que calcula el termómetro de sorpresa** (una prueba estadística llamada *prueba
   t*). Con estos 1000 estudiantes, esa máquina da un p-value de **0.00000009** (casi cero).

4. **Comparamos con la regla del 5%.** 0.00000009 es MUCHÍSIMO menor que 0.05 — el termómetro está
   marcando "esto es rarísimo si en realidad no hubiera ninguna diferencia".

5. **Conclusión:** se rechaza H0. Sí hay una diferencia real (no solo casualidad) entre el promedio de
   matemáticas de hombres y mujeres en esta muestra.

**Importante:** esto NO significa que un género sea "más inteligente" que el otro. Solo significa que, en
este conjunto de datos, hay una diferencia que no se explica por azar — podría deberse a muchos factores
(sociales, educativos, etc.) que el dataset no registra. Una prueba estadística encuentra *patrones*, no
explica *por qué* existen.

---

## Paso 5 — Resumen visual

| Concepto | En una frase | En nuestro ejemplo |
|---|---|---|
| Población | TODOS los casos que existen, imposibles de medir por completo | Todos los estudiantes del mundo que presentan este examen |
| Muestra | La parte que sí medimos | Los 1000 estudiantes de `StudentsPerformance.csv` |
| H0 (hipótesis nula) | "No pasa nada especial" | El promedio de matemáticas es igual entre géneros |
| H1 (hipótesis alternativa) | "Sí pasa algo" | El promedio de matemáticas es diferente entre géneros |
| p-value | El "termómetro de sorpresa": qué tan raro sería el resultado si H0 fuera cierta | 0.00000009 — rarísimo |
| Regla del 5% | Si el termómetro marca menos de 5%, le creemos a H1 | 0.00000009 < 0.05 → se rechaza H0 |
| Conclusión | Traducir el número a una frase que tenga sentido | Sí hay una diferencia real entre hombres y mujeres en matemáticas, en esta muestra |

---

*Generado a partir del archivo `StudentsPerformance.csv` — ver también los documentos
de la Semana 6 (`01_Estadistica_inferencial_conceptos.md`, `02_Pruebas_Hipotesis_conceptos.md`) para
profundizar con más ejercicios.*
