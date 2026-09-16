## Aclaración importante primero

Estos tres números (Shapiro A = 0.002, Shapiro B = 0.41, Levene = 0.03) son del **Ejercicio 4** de `02_Pruebas_Hipotesis_conceptos.md` — un caso **hipotético** ("con fines de práctica"), no calculado sobre `StudentsPerformance.csv`. No hay datos reales detrás de "grupo A" y "grupo B" para reproducir el cálculo exacto, pero sí puedo explicarte **cómo se obtienen este tipo de números**, y verificarlo con un caso real del *dataset* que tiene prácticamente el mismo patrón.

## Qué mide Shapiro-Wilk

**H0 de Shapiro-Wilk:** "estos datos vienen de una distribución normal (forma de campana)". Un p-value bajo dice: "esta forma es demasiado rara para venir de una campana perfecta".

## La idea (sin necesitar la tabla completa)

Shapiro-Wilk compara tus datos, **ordenados de menor a mayor**, contra la forma que *deberían* tener si vinieran de una campana perfecta. Es casi lo mismo que hace un **gráfico Q-Q**: si tus puntos ordenados caen casi en línea recta contra los valores esperados de una normal, el estadístico $W$ sale cercano a 1 (parece normal). Si se desvían (colas muy largas, asimetría, valores atípicos), $W$ baja.

La fórmula es:

$$W = \frac{\left(\sum_{i=1}^{n} a_i \, x_{(i)}\right)^2}{\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

- $x_{(i)}$ = tus datos **ordenados** (del más chico al más grande).
- $a_i$ = unos pesos fijos que **no calculas tú**: vienen de tablas estadísticas precalculadas, basadas en cómo se comportarían, en promedio, los datos ordenados de una muestra normal de ese mismo tamaño $n$. (A diferencia de Levene o la prueba t, aquí no hay una fórmula corta para sacarlos "a mano" — por eso Shapiro-Wilk siempre se calcula con software.)
- El **denominador** es la variabilidad total de tus datos (lo mismo que viste en el R²: $SS_{tot}$).

Si el numerador (la versión "ponderada como si fuera normal") es casi igual al denominador (la variabilidad real) → $W \approx 1$ → p-value alto. Si son muy distintos → $W$ baja → p-value bajo.

## Interpretando los números del ejercicio

| | p-value | ¿Se cumple normalidad (con α=0.05)? |
|---|---|---|
| Grupo A | 0.002 | **No** (0.002 < 0.05 → se rechaza H0: la forma es demasiado rara para ser una campana) |
| Grupo B | 0.41 | **Sí** (0.41 ≥ 0.05 → no hay evidencia de que no sea normal) |

## Verificación con un caso real casi idéntico

Busqué en `StudentsPerformance.csv` un par de grupos con este mismo patrón (uno falla normalidad, el otro no) — `math score` según `test preparation course`:

```
Shapiro 'none'      (n=642): statistic=0.9921, p-value=0.001754
Shapiro 'completed' (n=358): statistic=0.9937, p-value=0.139349
```

¡Casi calcado al ejercicio hipotético! `none` (p≈0.0018) se comporta como el "grupo A" (rechaza normalidad); `completed` (p≈0.139) se comporta como el "grupo B" (no la rechaza).

## Y el Levene = 0.03 del ejercicio

Esa es la misma fórmula que ya dedujimos paso a paso para el ejercicio de género/`writing score` (comparar qué tan "esparcido" está cada grupo alrededor de su mediana). Aquí, p = 0.03 < 0.05 → **se rechaza la homogeneidad de varianzas**: los dos grupos no tienen la misma dispersión.

## Por qué esto lleva a Mann-Whitney U

Con **normalidad fallando** (grupo A) **y** **varianzas distintas** (Levene), ninguno de los dos supuestos de la prueba t clásica se cumple — por eso el ejercicio concluye que conviene **Mann-Whitney U** (no exige ninguno de los dos) o, como alternativa paramétrica, la **prueba t de Welch** (no exige varianzas iguales, aunque sí sería más sensible a la falla de normalidad).

¿Quieres que te muestre también, con un ejemplo pequeño (n=8, para que se vea manejable), cómo se ordenan los datos y se aplican los pesos $a_i$ de la tabla, aunque sea de forma aproximada?