# Taller: regresión logística paso a paso — modelo matemático

**Fundamentos para IA · NRC 94103 · Semana 8**

**Datos:** `StudentsPerformance.csv` (1000 estudiantes, mismo archivo de las Semanas 6 y 7 —
[`Semana_7/StudentsPerformance.csv`](../Semana_7/StudentsPerformance.csv), también disponible en esta
carpeta como `Semana_8/StudentsPerformance.csv`).

**Objetivo:** en Semana 7 ajustaste rectas (regresión lineal) a mano. En este taller vas a construir, con
lápiz y calculadora, un modelo de **regresión logística** completo: desde la ecuación hasta la clasificación
final, usando **una sola variable predictora** (`reading score`) para predecir si un estudiante **aprueba
matemáticas** (`math score >= 60`).

No necesitas programar nada para resolver los ejercicios. Cuando termines, vas a comprobar estos mismos
resultados con código en [`03_Taller_regresion_logistica.md`](03_Taller_regresion_logistica.md) /
`03_Taller_regresion_logistica.ipynb` (o con la calculadora en línea
[numiqo.com/statistics-calculator/regression](https://numiqo.com/statistics-calculator/regression)).

---

## Paso 0. Definir el problema

| | |
|---|---|
| Variable dependiente (`Y`) | `aprueba_mate` = 1 si `math score >= 60`, 0 si no |
| Variable independiente (`X`) | `reading score` |
| Tamaño de la muestra | 1000 estudiantes: 677 aprueban (`Y=1`), 323 no aprueban (`Y=0`) |

**Ejercicio 0.1.** Antes de calcular nada: ¿por qué no podemos ajustar aquí una recta `Y = b0 + b1·X` como en
la Semana 7 y quedarnos con ese resultado?

> Tu respuesta:
>
>
>

---

## Paso 1. El modelo matemático

La regresión logística se construye en **dos fórmulas**, una detrás de la otra.

**Fórmula 1 — el predictor lineal `z`** (idéntica a la regresión lineal de la Semana 7):

```
z = b0 + b1 · X
```

**Fórmula 2 — la función logística**, que convierte `z` en una probabilidad entre 0 y 1:

```
P(Y = 1) = 1 / (1 + e^(-z))
```

Uniendo las dos, la ecuación completa del modelo es:

```
P(aprueba mate) = 1 / (1 + e^(-(b0 + b1 · reading score)))
```

Al ajustar este modelo con los 1000 estudiantes (usando el método de **máxima verosimilitud**, no mínimos
cuadrados — el software hace este cálculo por nosotros), se obtienen estos coeficientes:

```
b0 = -10.2254
b1 =   0.1672
```

**Ejercicio 1.1.** Escribe la ecuación completa del modelo reemplazando `b0` y `b1` por sus valores
numéricos (deja `X` como variable).

> Tu respuesta:
>
>

---

## Paso 2. Calcular `z` a mano

Con la fórmula `z = -10.2254 + 0.1672 · X`, completa la tabla para distintos valores de `reading score`.
Trabaja con 4 decimales.

| reading score (X) | Operación | z |
|---|---|---|
| 40 | -10.2254 + 0.1672 × 40 | **____** |
| 50 | -10.2254 + 0.1672 × 50 | **____** |
| 60 | -10.2254 + 0.1672 × 60 | **____** |
| 70 | -10.2254 + 0.1672 × 70 | **____** |
| 80 | -10.2254 + 0.1672 × 80 | **____** |

¿Qué patrón observas: `z` crece o decrece a medida que `reading score` aumenta? ¿Por qué?

> Tu respuesta:
>
>

---

## Paso 3. Convertir `z` en probabilidad

Ahora aplica la función logística `P = 1 / (1 + e^(-z))` a cada valor de `z` que calculaste en el Paso 2.
Recuerda: `e ≈ 2.71828`.

| reading score (X) | z | e^(-z) | P = 1/(1+e^(-z)) | ¿Aprueba? (umbral 0.5) |
|---|---|---|---|---|
| 40 | -3.5374 | **____** | **____** | **____** |
| 50 | -1.8654 | **____** | **____** | **____** |
| 60 | -0.1934 | **____** | **____** | **____** |
| 70 |  1.4786 | **____** | **____** | **____** |
| 80 |  3.1506 | **____** | **____** | **____** |

**Ejercicio 3.1.** Con `reading score = 60`, la probabilidad debería quedar muy cerca del 50%. ¿A qué valor
exacto de `reading score` corresponde `P = 0.5`? (Pista: `P = 0.5` ocurre cuando `z = 0`; despeja `X` de
`0 = -10.2254 + 0.1672·X`).

> Tu respuesta:
>
>

---

## Paso 4. Comprobar con un estudiante real del dataset

La primera fila de `StudentsPerformance.csv` es una estudiante mujer con `reading score = 72` y
`math score = 72` (por lo tanto `aprueba_mate = 1`, porque 72 ≥ 60).

**Ejercicio 4.1.** Calcula `z` y `P` a mano para esta estudiante y compara la predicción del modelo con lo
que realmente ocurrió.

> Tu respuesta:
>
>
>

**Ejercicio 4.2 (reto).** Busca en el archivo `StudentsPerformance.csv` una fila con `reading score = 50`.
Calcula `P` a mano, compara con `math score` de esa fila y di si el modelo acertó o falló para esa persona.

> Tu respuesta:
>
>
>

---

## Paso 5. Interpretar el coeficiente: la razón de momios (*odds ratio*)

El coeficiente `b1 = 0.1672` es difícil de interpretar directamente porque está en la escala del *log-odds*
(el *logit*), no en la escala de probabilidad. Para interpretarlo mejor, se calcula la **razón de momios**:

```
odds ratio = e^b1
```

**Ejercicio 5.1.** Calcula el *odds ratio* de `reading score` con `b1 = 0.1672` y explica, en tus palabras,
qué significa ese número para la probabilidad de aprobar matemáticas.

> Tu respuesta:
>
>
>

---

## Paso 6. Evaluar el modelo completo: matriz de confusión

Al aplicar el modelo (umbral 0.5) a los 1000 estudiantes del dataset, se obtiene esta matriz de confusión:

| | Predicho: no aprueba | Predicho: aprueba |
|---|---|---|
| **Real: no aprueba** | 227 | 96 |
| **Real: aprueba** | 72 | 605 |

**Ejercicio 6.1.** Con estos cuatro números, calcula a mano:

a) La **exactitud** (*accuracy*): proporción de estudiantes clasificados correctamente.
b) La **precisión**: de los que el modelo predijo "aprueba", ¿qué porcentaje aprobó de verdad?
c) La **sensibilidad** (*recall*): de los que realmente aprobaron, ¿qué porcentaje detectó el modelo?

> Tus respuestas:
>
>
>

**Ejercicio 6.2.** De los 96 + 72 = 168 estudiantes mal clasificados, ¿cuáles crees que son más "difíciles"
para el modelo: los que tienen `reading score` muy alto o muy bajo, o los que están cerca del punto de corte
que hallaste en el Ejercicio 3.1? Justifica tu respuesta con lo que ya sabes de la curva sigmoide.

> Tu respuesta:
>
>
>

---

## Reto final

Repite el Paso 1 a paso 3 de este taller, pero usando `writing score` en vez de `reading score` como variable
independiente:

1. Verifica en `03_Taller_regresion_logistica.md` / `03_Taller_regresion_logistica.ipynb` (o en
   [numiqo.com/statistics-calculator/regression](https://numiqo.com/statistics-calculator/regression)
   pegando los datos) cuáles son los coeficientes `b0` y `b1` para `writing score`.
2. Calcula a mano `z` y `P` para un estudiante con `writing score = 65`.
3. Compara el *odds ratio* de `writing score` con el de `reading score` (Paso 5): ¿cuál de las dos variables
   parece tener una relación más fuerte con aprobar matemáticas?

---

## Hoja de fórmulas (resumen)

| Fórmula | Para qué sirve |
|---|---|
| `z = b0 + b1·X` | Combina la(s) variable(s) independiente(s) en un solo número (el *logit*) |
| `P(Y=1) = 1 / (1 + e^(-z))` | Convierte `z` en una probabilidad entre 0 y 1 (función logística) |
| Clasificación: `P ≥ 0.5 → Y=1`, si no `Y=0` | Convierte la probabilidad en una decisión |
| `odds = P / (1 - P)` | Momios: qué tan más probable es que ocurra el evento frente a que no ocurra |
| `odds ratio = e^b1` | Cuánto se multiplican los momios por cada unidad adicional de `X` |
