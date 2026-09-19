# Regresión lineal vs. regresión logística

Ya conoces las dos por separado (Semana 7 y Semana 8). Esta hoja las pone **una al lado de la otra**, usando
siempre el mismo archivo, `StudentsPerformance.csv` (1000 estudiantes), y la misma variable predictora,
`reading score`, para que la única diferencia real que veas sea **qué tipo de pregunta responde cada una**.

---

## 1. La pregunta que cada una responde

**Analogía:** imagina que tienes dos instrumentos sobre un escritorio: un **termómetro** y un **semáforo**.

- El **termómetro** te da un número exacto, que puede ser casi cualquier valor (36.4°C, 37.1°C, 38.9°C...).
  Así es la **regresión lineal**: predice un **número continuo**.
- El **semáforo** solo tiene dos estados útiles para decidir: **para** o **sigue** (rojo o verde). No te
  interesa "qué tan rojo" está, solo la decisión final. Así es la **regresión logística**: predice la
  **probabilidad de una categoría** (y de ahí, una decisión de dos opciones).

Con el mismo `reading score` como termómetro de entrada, puedes hacer dos preguntas muy distintas sobre un
estudiante:

| Pregunta | Tipo de respuesta | Herramienta |
|---|---|---|
| "¿Cuánto va a sacar en escritura (`writing score`)?" | Un número entre 0 y 100 | **Regresión lineal** |
| "¿Va a aprobar matemáticas (`math score >= 60`)?" | Sí / No | **Regresión logística** |

**Ejercicio 1.** Para cada pregunta, di si el "termómetro" (regresión lineal) o el "semáforo" (regresión
logística) es el instrumento correcto, y por qué:

a) "¿Cuántos puntos exactos sacará un estudiante en matemáticas?"
b) "¿Este estudiante pertenece al grupo de riesgo de reprobar (sí/no)?"

<details>
<summary>Ver solución explicada</summary>

a) **Termómetro (regresión lineal)**: la respuesta es un número continuo (`math score`, de 0 a 100), no una
categoría.

b) **Semáforo (regresión logística)**: la respuesta es binaria ("pertenece al grupo de riesgo" o "no"), así
que necesitamos una probabilidad convertida en decisión, no un número.

</details>

---

## 2. Comparación en una tabla

| | Regresión lineal | Regresión logística |
|---|---|---|
| **¿Qué predice?** | Un número continuo (`Y`) | La probabilidad de un evento binario (`Y=1` o `Y=0`) |
| **Ejemplo con nuestros datos** | `writing score` (0 a 100) | ¿Aprueba matemáticas? (sí/no) |
| **Forma de la relación** | Una **línea recta** | Una **curva en forma de "S"** (sigmoide) |
| **Ecuación** | `Y = b0 + b1·X` | `log(p/(1-p)) = b0 + b1·X`, luego `p = 1/(1+e^-z)` |
| **Rango de la predicción** | Cualquier número (`-∞` a `+∞`) | Siempre entre 0 y 1 |
| **Cómo se ajustan los coeficientes** | Mínimos cuadrados (minimizar el error al cuadrado) | Máxima verosimilitud (maximizar qué tan "creíbles" son los datos observados) |
| **Cómo se interpreta `b1`** | Directo: "por cada punto de X, Y sube/baja b1 unidades" | Indirecto: mejor usar el **odds ratio** (`e^b1`): "por cada punto de X, los momios de Y=1 se multiplican por tanto" |
| **Cómo se evalúa el modelo** | **R²** (qué % de la variación explica el modelo), error de predicción | **Matriz de confusión**: exactitud, precisión, recall |
| **Decisión final** | El número calculado, tal cual | Se compara la probabilidad contra un **umbral** (normalmente 0.5) |

---

## 3. La misma variable, dos preguntas: ejemplo lado a lado

Con `reading score` como única variable predictora, se ajustaron ambos modelos sobre los 1000 estudiantes
de `StudentsPerformance.csv`.

**Regresión lineal** — predice `writing score`:

```
writing score = -0.6676 + 0.9935 * reading score        (R² ≈ 0.911)
```

**Regresión logística** — predice si aprueba matemáticas (`math score >= 60`):

```
z = -10.2254 + 0.16721 * reading score
p(aprueba) = 1 / (1 + e^(-z))                            (con umbral 0.5 para decidir)
```

**Ejercicio 2.** Para un estudiante con `reading score = 60`, calcula:

a) Su `writing score` esperado, usando la regresión lineal.
b) Su probabilidad de aprobar matemáticas, usando la regresión logística. ¿Lo clasificarías como que aprueba
o no aprueba (umbral 0.5)?
c) ¿Por qué la respuesta de (a) es "un número más" mientras que la de (b) necesitó un paso extra (comparar
contra 0.5) para llegar a una conclusión?

<details>
<summary>Ver solución explicada</summary>

a) `writing score = -0.6676 + 0.9935*60 = -0.6676 + 59.61 = 58.94` → aproximadamente **58.9 puntos**. Ya es
la respuesta final: no hace falta ningún paso adicional.

b) `z = -10.2254 + 0.16721*60 = -10.2254 + 10.0326 = -0.1928`. `p = 1/(1+e^0.1928) ≈ 0.452` (**45.2%**).
Como `0.452 < 0.5`, se **clasifica como "no aprueba"**.

c) Porque la regresión lineal ya entrega directamente la magnitud que nos interesa (una nota). La regresión
logística entrega una **probabilidad**, que es una magnitud intermedia; para llegar a una decisión "aprueba
/ no aprueba" hace falta un paso más: compararla contra un umbral. Es la diferencia entre leer el
termómetro (ya terminaste) y mirar el semáforo (todavía tienes que decidir si te detienes o sigues).

</details>

---

## 4. Por qué no se pueden intercambiar

**Analogía:** usar regresión lineal para predecir "aprueba / no aprueba" es como intentar leer un semáforo
con un termómetro: podrías obtener un número como "1.3" o "-0.2", pero ese número no es ni una probabilidad
válida (debería estar entre 0 y 1) ni tiene una interpretación clara como "sí" o "no".

**Ejercicio 3.** Si ajustaras una regresión lineal clásica usando `reading score` para predecir directamente
"aprueba matemáticas" (codificado como 1 = aprueba, 0 = no aprueba), el modelo podría devolver, para algunos
estudiantes, un valor de `Y` predicho igual a `1.15` o `-0.08`. Explica qué problema revela cada uno de esos
dos números.

<details>
<summary>Ver solución explicada</summary>

- `Y predicho = 1.15`: no tiene sentido como probabilidad, porque una probabilidad nunca puede superar 1
  (100%). La recta de la regresión lineal no tiene ningún mecanismo que la obligue a quedarse entre 0 y 1.
- `Y predicho = -0.08`: tampoco tiene sentido, porque una probabilidad nunca puede ser negativa.

Ambos casos muestran por qué la regresión lineal **no está diseñada** para variables binarias: la recta
puede salir libremente del rango [0,1], mientras que la regresión logística usa la función sigmoide
precisamente para evitar este problema, "encerrando" siempre el resultado entre 0 y 1.

</details>

---

## 5. Cómo se evalúa cada una (no se comparan con la misma vara)

**Analogía:** no calificarías un tiro al arco (¿entró o no entró? — binario) con la misma métrica que usarías
para medir qué tan lejos llegó un lanzamiento de jabalina (una distancia en metros — continua). Cada tipo de
resultado necesita su propia métrica.

| Regresión lineal | Regresión logística |
|---|---|
| **R²**: en el ejemplo, `R² ≈ 0.911`, es decir, el modelo explica el 91.1% de la variación de `writing score`. | **Exactitud (accuracy)**: en el ejemplo, `≈ 83.2%` de los estudiantes quedan bien clasificados. |
| Error de predicción: qué tan lejos, en puntos, quedó la predicción del valor real. | **Precisión** y **recall**: de los que el modelo dice que aprueban, ¿cuántos aprueban de verdad?; de los que sí aprueban, ¿a cuántos detecta el modelo? |

**Ejercicio 4.** Un estudiante dice: "Si el R² de mi regresión lineal es 0.91, entonces la exactitud de mi
regresión logística también debería rondar 0.91, porque ambos modelos son 'buenos' de la misma forma."
¿Estás de acuerdo?

<details>
<summary>Ver solución explicada</summary>

**No.** R² y *accuracy* miden cosas distintas, en escalas distintas, para tipos de modelo distintos. R²
mide qué proporción de la **variación de un número continuo** explica el modelo; *accuracy* mide qué
proporción de **clasificaciones correctas** (aciertos binarios) logra el modelo. Que uno sea alto no implica
nada directo sobre el otro — de hecho, en este mismo curso, la regresión lineal de `writing score` tiene
`R² ≈ 0.91` y la regresión logística de "aprueba matemáticas" tiene `accuracy ≈ 0.83`; son buenos ajustes,
pero cada uno según el criterio que le corresponde a su propio tipo de problema.

</details>

---

## 6. Resumen

1. **Misma familia, distinta pregunta**: ambas combinan variables con coeficientes (`b0 + b1·X`), pero la
   lineal predice un número y la logística predice la probabilidad de una categoría.
2. **Recta vs. curva**: la lineal traza una recta sin restricciones; la logística traza una curva en forma
   de "S" que siempre queda entre 0 y 1.
3. **Ajuste**: mínimos cuadrados para la lineal, máxima verosimilitud para la logística.
4. **Interpretación del coeficiente**: directa en unidades de `Y` en la lineal; a través del odds ratio
   (`e^b1`) en la logística.
5. **Evaluación**: R² y error de predicción para la lineal; matriz de confusión, exactitud, precisión y
   recall para la logística.
6. **No son intercambiables**: usar regresión lineal sobre una variable binaria puede dar predicciones sin
   sentido (menores a 0 o mayores a 1); la regresión logística existe justamente para evitar ese problema.
