# Estadística básica para el Portafolio de Evidencias (Semana 6)

**Curso:** Fundamentos para Inteligencia Artificial — NRC 94103  

**Para qué sirve este documento:** reunir, en un solo lugar y sin código, toda la estadística que necesitas entender para resolver el taller [**EIARV011_A6 — Portafolio de evidencias: Análisis inferencial de datos**](../../Semana_6/Semana_6_Actividad/EIARV011_A6.md) (y su [anexo con los pasos sugeridos](../../Semana_6/Semana_6_Actividad/EIARV011_A6_Anexo.md))  

**Dataset de ejemplo:** [`StudentsPerformance.csv`](StudentsPerformance.csv) (1000 estudiantes, con notas de matemáticas, lectura y escritura). Todos los ejemplos, ejercicios y analogías de esta guía usan **exclusivamente** este archivo, aunque el anexo del taller también permita `BostonHousing.csv` o `titles.csv`/`credits.csv` (Netflix); los mismos conceptos aplican igual si eliges trabajar con alguno de esos otros *datasets*.

Este documento **no tiene código**: la parte de programación (`pandas`, `scipy`) ya la resolviste o la resolverás en el *notebook*. Aquí lo que necesitas es entender **qué significa cada resultado que el código te va a entregar**, para poder redactarlo correctamente en el portafolio. Por eso cada concepto incluye también su **fórmula matemática**: no para calcularla a mano (`pandas`/`scipy` ya lo hacen), sino para que entiendas de dónde sale cada número y puedas explicarlo con propiedad en el portafolio.

---

## Mapa de la guía: qué sección necesitas para cada paso del taller

El anexo del taller pide 9 pasos. Esta guía cubre el contenido estadístico de los pasos 2 a 8 (los pasos 1, 9 y la entrega final son de organización, redacción y reflexión, no de estadística):

| Paso del anexo | Qué te pide | Sección de esta guía |
|---|---|---|
| Paso 2. Contexto y planteamiento del problema | Redactar una pregunta investigable y las hipótesis H0/H1 | Secciones 6 y 7 |
| Paso 3. Identificación de variables | Clasificar variable dependiente e independiente | Sección 1 |
| Paso 4. Descripción y tamaño de muestra | Reportar n total y n por grupo | Sección 2 |
| Paso 5. Estadística descriptiva y visualización | Medidas descriptivas y gráficos mínimos | Secciones 3, 4 y 5 |
| Paso 6. Validación de supuestos | Normalidad y homogeneidad de varianzas | Sección 8 |
| Paso 7. Selección del análisis inferencial | Elegir y justificar la prueba estadística | Sección 9 |
| Paso 8. Resultados e interpretación | Leer el estadístico, el *p-value* y decidir sobre H0 | Sección 10 |

---

## 1. Tipos de variables (Paso 3 del anexo)

Antes de calcular cualquier cosa hay que saber **qué tipo de dato es cada columna**, porque de eso depende qué operaciones tienen sentido y qué prueba estadística se puede aplicar más adelante.

**Por su naturaleza**, una variable es:

- **Cuantitativa**: se expresa con números y esos números sí se pueden sumar, promediar, etc. Ejemplo: `math score`, `reading score`, `writing score` (todas van de 0 a 100).
- **Cualitativa (o categórica)**: se expresa con categorías, no con cantidades. No tiene sentido "promediarlas". Ejemplo: `gender` (female/male), `lunch` (standard/free-reduced), `test preparation course` (none/completed), `race/ethnicity` (group A a group E).

Dentro de las cualitativas, además, se distingue si las categorías tienen o no un orden natural: `parental level of education` (some high school → some college → bachelor's → master's) es un ejemplo de categórica **ordinal**; `gender` o `lunch`, en cambio, son **nominales** (no hay un orden lógico entre sus categorías).

**Por su papel en la pregunta de investigación**, una variable es:

- **Variable dependiente**: la que se mide, la que queremos explicar o predecir. Suele ser numérica.
- **Variable independiente**: la que podría estar influyendo sobre la dependiente. Puede ser categórica (por ejemplo, comparar grupos) o numérica (por ejemplo, buscar una correlación).

El taller pide elegir mínimo una de cada una: "1 variable dependiente (preferiblemente numérica)" y "1 variable independiente (categórica con 2+ grupos, o numérica si es correlación)".

**Ejemplo aplicado.** Si la pregunta es *"¿el curso de preparación (`test preparation course`) influye en la nota de matemáticas (`math score`)?"*, entonces `math score` es la variable dependiente (cuantitativa continua, la que se mide) y `test preparation course` es la variable independiente (cualitativa nominal, con 2 categorías: `none` y `completed`). Si en cambio la pregunta fuera *"¿la nota de lectura se relaciona con la nota de escritura?"*, ambas son numéricas y no hay una relación de dependencia fija: se plantea como una **correlación** entre dos variables cuantitativas, no como grupo A vs. grupo B.

---

## 2. Población, muestra y tamaño de los grupos (Paso 4 del anexo)

- **Población**: el conjunto completo sobre el que se quiere concluir, aunque no se haya medido a todos. En este ejemplo, sería *todos* los estudiantes que en algún momento presentan un examen como este, en cualquier lugar.
- **Muestra**: el subconjunto que sí se alcanzó a medir y que aparece en el archivo CSV. Aquí, los 1000 estudiantes de `StudentsPerformance.csv` (**n = 1000**).

Cuando se comparan grupos (por ejemplo, según `test preparation course`), también hay que reportar el tamaño de cada grupo, porque un grupo muy pequeño da estimaciones menos confiables que uno grande: un solo dato atípico "pesa" mucho más en un grupo de 60 personas que en uno de 300.

**Ejemplo aplicado.** En `StudentsPerformance.csv`, la columna `test preparation course` divide la muestra en dos grupos: 642 estudiantes que no tomaron el curso (`none`) y 358 que sí lo tomaron (`completed`). Ambos números deben quedar reportados en el portafolio (Paso 4), junto con cualquier criterio de exclusión que se haya aplicado (por ejemplo, si se descartaron filas con datos faltantes).

---

## 3. Estadística descriptiva: el "dato típico" (Paso 5 del anexo)

Para una variable cuantitativa, lo primero que se reporta es qué tan alto o bajo es un valor "normal" dentro de ella.

- **Media**: el promedio de toda la vida (sumar todo y dividir entre el total de datos). Se deja "engañar" fácilmente por valores muy extremos.
- **Mediana**: el valor que queda exactamente en el medio al ordenar todos los datos de menor a mayor. La mitad de los casos está por debajo y la mitad por encima. No le afectan los valores extremos.
- **Moda**: el valor que más se repite. Es la única de las tres que también sirve para variables categóricas (por ejemplo, la categoría más frecuente de `gender`).

Cuando la media y la mediana son casi iguales, es señal de que los datos están repartidos de forma bastante simétrica (sin un grupo extremo "descuadrando" el promedio); cuando son muy distintas, es señal de asimetría.

### Fórmulas

**Media:**

$$
\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}
$$

donde $x_i$ es cada valor individual de la variable y $n$ es el número total de datos (por ejemplo, $n = 1000$ en `StudentsPerformance.csv`).

**Mediana:** no se calcula sumando, sino ordenando los datos de menor a mayor y ubicando el valor central:

$$
\text{Mediana} =
\begin{cases}
x_{\left(\frac{n+1}{2}\right)} & \text{si } n \text{ es impar} \\[6pt]
\dfrac{x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2}+1\right)}}{2} & \text{si } n \text{ es par}
\end{cases}
$$

donde $x_{(i)}$ es el dato que queda en la posición $i$ una vez ordenados todos los valores.

**Moda:** no tiene fórmula; es, simplemente, el valor $x_i$ con mayor frecuencia (número de repeticiones) dentro del conjunto de datos.

**Ejemplo aplicado.** En `math score`: la media es **66.09**, la mediana es **66.0** y la moda es **65**. Como los tres valores son casi idénticos, se puede afirmar que las notas de matemáticas están repartidas de forma bastante simétrica alrededor de 66 puntos, sin un grupo extremo que distorsione el promedio.

---

## 4. Estadística descriptiva: qué tan parejos son los datos (Paso 5 del anexo)

Conocer el "dato típico" no basta: dos grupos pueden tener el mismo promedio y ser completamente distintos (uno muy parejo, otro con notas muy dispersas). Para eso se usan las medidas de dispersión, que también pide el anexo ("desviación, min/max, cuartiles").

- **Rango**: la distancia entre el valor más alto y el más bajo. Da una idea rápida, pero muy sensible a un solo caso extremo.
- **Desviación estándar**: en promedio, qué tan lejos está cada dato de la media. Un número pequeño significa que casi todos los valores son parecidos entre sí; un número grande significa que están muy repartidos.
- **Cuartiles (Q1, Q2, Q3)**: los tres puntos de corte que dividen los datos ordenados en 4 partes iguales, de 25 % cada una. Q2 es la mediana. La distancia entre Q3 y Q1 se llama **rango intercuartílico (IQR)** y se usa para detectar valores atípicos (*outliers*): cualquier dato muy por fuera de ese rango central llama la atención y merece revisarse antes de continuar el análisis.

### Fórmulas

**Rango:**

$$
R = x_{\text{máx}} - x_{\text{mín}}
$$

**Varianza muestral** (el promedio de las distancias, al cuadrado, entre cada dato y la media):

$$
s^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}
$$

**Desviación estándar** (la raíz cuadrada de la varianza, para volver a las unidades originales de la variable):

$$
s = \sqrt{s^2} = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}}
$$

**Posición de cada cuartil** dentro de los datos ordenados (existen varios métodos equivalentes; este es el más usado):

$$
\text{Posición de } Q_k = \frac{k(n+1)}{4}, \qquad k = 1, 2, 3
$$

**IQR y límites para detectar outliers:**

$$
IQR = Q_3 - Q_1
$$

$$
\text{Límite inferior} = Q_1 - 1.5 \times IQR \qquad \text{Límite superior} = Q_3 + 1.5 \times IQR
$$

Cualquier dato por debajo del límite inferior o por encima del límite superior se considera un posible *outlier*.

**Ejemplo aplicado.** En `math score`: el rango es **100** (hay un estudiante con 0 y otro con 100); la desviación estándar es **≈15.16**, lo que indica que la mayoría de los estudiantes se ubica entre 51 y 81 puntos aproximadamente; y los cuartiles son **Q1 = 57**, **Q2 = 66**, **Q3 = 77**, de modo que un estudiante con 80 puntos queda por encima de Q3 y, por lo tanto, dentro del 25 % con mejores notas del curso.

---

## 5. Qué gráfico usar para cada análisis (Paso 5 del anexo)

El anexo pide un mínimo de tres tipos de visualización, cada una asociada a un tipo de pregunta distinto. No hace falta memorizar cómo se programan; sí hay que saber **cuál corresponde a cada situación** para poder justificarlo en el portafolio:

| Situación | Gráfico recomendado | Qué permite ver |
|---|---|---|
| Una sola variable numérica (¿cómo se distribuyen las notas de matemáticas?) | **Histograma** o gráfico de densidad | La forma de la distribución: si es simétrica, si tiene una o varias "jorobas", si hay valores muy extremos |
| Una variable numérica comparada entre grupos (¿la nota de matemáticas cambia según el curso de preparación?) | **Boxplot** (diagrama de caja) o *violin plot*, uno por grupo | La mediana, los cuartiles y los posibles *outliers* de cada grupo, uno al lado del otro, para comparar de un vistazo |
| Dos variables numéricas (¿la nota de lectura se relaciona con la de escritura?) | **Diagrama de dispersión** (*scatter plot*) | Si existe un patrón conjunto entre las dos variables (una nube de puntos que sube, que baja, o que no muestra ningún patrón) |

El boxplot merece un comentario aparte porque conecta directamente con la Sección 4: la "caja" se dibuja exactamente entre Q1 y Q3 (el IQR), la línea dentro de la caja es la mediana, y los puntos que quedan muy alejados de la caja son los candidatos a valores atípicos.

---

## 6. De describir a inferir: por qué no basta con comparar promedios (contexto del Paso 2)

Todo lo anterior es **estadística descriptiva**: resume lo que ya se observó en la muestra. Pero el taller pide un **análisis inferencial**, que es un paso más ambicioso: usar lo que se observó en la muestra (1000 estudiantes) para sacar una conclusión sobre la población completa (todos los estudiantes que presentan un examen así, no solo estos 1000).

El problema es que, si se comparan dos promedios y uno es más alto que el otro, esa diferencia podría deberse a un efecto real, **o simplemente al azar** de qué 1000 estudiantes en particular terminaron en la muestra. La estadística inferencial existe justamente para responder: *"¿es razonable pensar que esta diferencia es real, o es del tamaño que cabría esperar solo por azar?"*. Para responder eso de forma rigurosa (y no a ojo) se necesitan tres ingredientes, que se explican en las siguientes secciones: una **hipótesis** que poner a prueba, una revisión de los **supuestos** de los datos, y la **prueba estadística** adecuada.

**Ejemplo aplicado.** Los estudiantes con curso de preparación completado promedian 69.70 en matemáticas, frente a 64.08 de quienes no lo tomaron. Decir *"en esta muestra de 1000 estudiantes, el promedio de quienes tomaron el curso es 69.70"* es una afirmación **descriptiva** (un cálculo directo). Decir *"el curso de preparación mejora la nota de matemáticas de cualquier estudiante que lo tome, no solo los de esta muestra"* es una afirmación **inferencial**, y para respaldarla con evidencia hace falta exactamente lo que cubren las Secciones 7 a 10.

---

## 7. Formulación de hipótesis: H0 y H1 (Paso 2 del anexo)

Antes de aplicar cualquier prueba inferencial, hay que dejar por escrito qué se está poniendo a prueba, en forma de dos hipótesis que se excluyen mutuamente:

- **H0 (hipótesis nula)**: la opción conservadora, "no pasa nada especial". Según el tipo de pregunta, puede significar: no hay diferencia entre los grupos, no hay relación entre las variables, o el promedio es igual a un valor de referencia.
- **H1 (hipótesis alternativa)**: la opción que sí afirma un efecto: sí hay diferencia entre los grupos, sí hay relación entre las variables, o el promedio es distinto del valor de referencia.

El anexo sugiere tres tipos de preguntas investigables, y a cada una le corresponde una forma distinta de plantear H0/H1:

| Tipo de pregunta | H0 | H1 |
|---|---|---|
| ¿Existe diferencia en la variable X entre los grupos A y B? | El promedio de X es igual en el grupo A y en el grupo B | El promedio de X es diferente entre el grupo A y el grupo B |
| ¿La variable X se relaciona con Y? | No existe correlación entre X y Y (la correlación real es 0) | Sí existe correlación entre X y Y |
| ¿El promedio de X es diferente a un valor objetivo? | El promedio de X es igual al valor objetivo | El promedio de X es diferente del valor objetivo |

### Notación formal

| Tipo de pregunta | H0 | H1 |
|---|---|---|
| Diferencia entre 2 grupos | $H_0: \mu_1 = \mu_2$ | $H_1: \mu_1 \neq \mu_2$ |
| Relación entre X y Y | $H_0: \rho = 0$ | $H_1: \rho \neq 0$ |
| Promedio vs. valor de referencia | $H_0: \mu = \mu_0$ | $H_1: \mu \neq \mu_0$ |

donde $\mu_1$ y $\mu_2$ son los promedios poblacionales de cada grupo, $\rho$ (rho) es el coeficiente de correlación poblacional, y $\mu_0$ es el valor de referencia fijo con el que se compara.

El análisis siempre parte "creyendo" H0, y solo se abandona esa postura si la evidencia de los datos es lo bastante fuerte como para hacerlo (eso es justamente lo que decide el *p-value*, en la Sección 10).

**Ejemplo aplicado.** Para la pregunta *"¿el curso de preparación influye en la nota de matemáticas?"*:

- **H0:** el promedio de `math score` es igual entre los estudiantes que completaron el curso y los que no.
- **H1:** el promedio de `math score` es diferente entre los estudiantes que completaron el curso y los que no.

---

## 8. Validación de supuestos: normalidad y homogeneidad de varianzas (Paso 6 del anexo)

Antes de elegir qué prueba inferencial aplicar, hay que revisar si los datos cumplen ciertas condiciones que algunas pruebas necesitan para ser confiables. El anexo pide validar dos, sobre la variable dependiente:

### Normalidad

Muchas pruebas estadísticas clásicas (llamadas **paramétricas**) asumen que la variable dependiente sigue, aproximadamente, una distribución en forma de campana (**distribución normal**): la mayoría de los valores se concentra alrededor del promedio, y cada vez hay menos casos a medida que uno se aleja hacia los extremos, de forma simétrica.

Esa condición se revisa con una prueba de normalidad (por ejemplo, Shapiro-Wilk), que entrega un *p-value*. La regla de interpretación, como indica el anexo, es:

- Si *p* < 0.05: hay evidencia **en contra** de la normalidad (los datos probablemente no siguen una distribución normal).
- Si *p* ≥ 0.05: **no se rechaza** la normalidad (no hay evidencia suficiente en contra; se puede asumir con cautela).

La normalidad se revisa sobre la variable dependiente, ya sea en la muestra completa o dentro de cada grupo por separado, si se están comparando grupos.

**Fórmula (conceptual) del estadístico de Shapiro-Wilk:**

$$
W = \frac{\left(\sum_{i=1}^{n} a_i\, x_{(i)}\right)^2}{\sum_{i=1}^{n} (x_i - \bar{x})^2}
$$

donde $x_{(i)}$ son los datos ya ordenados y $a_i$ son constantes que dependen del tamaño de muestra (se calculan a partir de lo que se esperaría si los datos vinieran de una distribución normal perfecta). Cuanto más cercano a 1 es $W$, más se parece la distribución observada a una normal. No se calcula a mano: `scipy.stats.shapiro()` entrega directamente $W$ y su *p-value*.

### Homogeneidad de varianzas

Cuando se comparan dos o más grupos, además de la normalidad importa que la **dispersión** (varianza) de la variable dependiente sea parecida entre esos grupos: no que unos estén muy "revueltos" y otros muy "parejos". Esto se revisa con una prueba de homogeneidad de varianzas (por ejemplo, la prueba de Levene), que también se interpreta con la misma regla del *p-value* frente a 0.05.

**Fórmula del estadístico de Levene:**

$$
W = \frac{N-k}{k-1} \cdot \frac{\sum_{i=1}^{k} n_i (\bar{Z}_{i\cdot} - \bar{Z}_{\cdot\cdot})^2}{\sum_{i=1}^{k} \sum_{j=1}^{n_i} (Z_{ij} - \bar{Z}_{i\cdot})^2}
$$

donde $Z_{ij} = |x_{ij} - \tilde{x}_i|$ es la distancia absoluta de cada dato a la mediana ($\tilde{x}_i$) de su propio grupo, $k$ es el número de grupos, $N$ el total de datos y $n_i$ el tamaño de cada grupo. En esencia, Levene convierte la pregunta "¿varían igual los grupos?" en "¿tienen estas distancias a la mediana el mismo promedio en todos los grupos?", y le aplica a esas distancias la misma lógica de un ANOVA (Sección 9).

**Ejemplo aplicado.** Al evaluar la normalidad de `math score` con la prueba de Shapiro-Wilk se obtiene *p* ≈ 0.00015 (menor a 0.05): en sentido estricto hay evidencia en contra de una normalidad perfecta, algo frecuente cuando la muestra es grande (con 1000 datos, la prueba detecta hasta desviaciones muy pequeñas de la campana ideal); en la práctica, la distribución sigue siendo razonablemente simétrica (Sección 3). Al comparar la varianza de `math score` entre el grupo con curso de preparación y el grupo sin curso mediante la prueba de Levene se obtiene *p* ≈ 0.47 (mayor a 0.05): no se rechaza la homogeneidad de varianzas, es decir, ambos grupos tienen una dispersión interna comparable.

---

## 9. Selección de la prueba estadística inferencial (Paso 7 del anexo)

Con el tipo de variables (Sección 1), el número de grupos a comparar y el resultado de los supuestos (Sección 8) ya se puede elegir la prueba adecuada. La lógica general es: **si se cumplen los supuestos, se usa una prueba paramétrica; si no se cumplen, se usa su versión no paramétrica**, que responde la misma pregunta sin necesitar la forma de campana.

| Qué se quiere comparar | Se cumplen los supuestos (normalidad y homogeneidad) | No se cumplen los supuestos |
|---|---|---|
| El promedio de X entre **2 grupos** independientes | **Prueba t de Student** para muestras independientes | **U de Mann-Whitney** |
| El promedio de X entre **3 o más grupos** | **ANOVA** de un factor | **Kruskal-Wallis** |
| El promedio de X frente a un **valor de referencia fijo** | **Prueba t de una muestra** | Prueba de rangos con signo de Wilcoxon |
| La relación entre **dos variables numéricas** | **Correlación de Pearson** | **Correlación de Spearman** |

Todas estas pruebas comparten la misma lógica de fondo (calculan qué tan compatible es lo observado con H0), solo cambian según el tipo de dato y si se cumplen o no los supuestos; por eso no hace falta memorizar sus fórmulas de memoria para resolver el taller, pero sí ayuda saber de dónde salen para poder explicarlas en el portafolio.

### Fórmulas de las pruebas más usadas en este taller

**Prueba t de Student** (2 grupos independientes, varianzas homogéneas):

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{\dfrac{1}{n_1} + \dfrac{1}{n_2}}}, \qquad
s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}
$$

donde $\bar{x}_1, \bar{x}_2$ son las medias de cada grupo, $s_1^2, s_2^2$ sus varianzas, $n_1, n_2$ sus tamaños, y $s_p$ es la desviación estándar combinada ("*pooled*") de ambos grupos.

**Prueba t de una muestra** (compara el promedio contra un valor de referencia $\mu_0$):

$$
t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
$$

**ANOVA de un factor** (compara $k$ grupos a la vez):

$$
F = \frac{\text{MSB}}{\text{MSW}}, \qquad
\text{MSB} = \frac{\sum_{i=1}^{k} n_i(\bar{x}_i - \bar{x})^2}{k-1}, \qquad
\text{MSW} = \frac{\sum_{i=1}^{k} \sum_{j=1}^{n_i} (x_{ij} - \bar{x}_i)^2}{N-k}
$$

MSB ("*mean square between*") mide qué tan distintos son los promedios de los grupos entre sí; MSW ("*mean square within*") mide qué tan dispersos son los datos dentro de cada grupo. Un $F$ grande indica que las diferencias entre grupos son grandes en comparación con la variación normal dentro de cada grupo.

**Correlación de Pearson:**

$$
r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}
$$

$r$ va de −1 a 1: cerca de 1 indica relación lineal positiva fuerte (cuando sube X, sube Y), cerca de −1 indica relación lineal negativa fuerte, y cerca de 0 indica poca o ninguna relación lineal.

**Versiones no paramétricas** (cuando no se cumplen los supuestos, trabajan sobre los *rangos* de los datos en lugar de sus valores exactos, por lo que no necesitan normalidad):

Correlación de Spearman:

$$
r_s = 1 - \frac{6\sum_{i=1}^{n} d_i^2}{n(n^2-1)}
$$

donde $d_i$ es la diferencia entre el rango de $x_i$ y el rango de $y_i$ para cada observación.

Kruskal-Wallis (equivalente no paramétrico de ANOVA), donde $R_i$ es la suma de rangos del grupo $i$, $n_i$ su tamaño y $N$ el total de datos:

$$
H = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N+1)
$$

La U de Mann-Whitney sigue la misma idea para 2 grupos: aplica, sobre los rangos, una lógica equivalente a la de la prueba t.

**Ejemplo aplicado.** Para comparar `math score` entre los 2 grupos de `test preparation course`, y habiendo verificado que la varianza es homogénea entre ambos (Sección 8), la prueba adecuada es la **prueba t de Student para muestras independientes** (aunque la normalidad estricta no se cumpla del todo, con un tamaño de muestra grande como n = 1000 esta prueba sigue siendo razonablemente confiable). Si en cambio se quisiera comparar `math score` entre los 5 grupos de `race/ethnicity`, al ser más de 2 grupos correspondería usar **ANOVA** (o **Kruskal-Wallis** si los supuestos no se cumplieran).

---

## 10. Resultados e interpretación: el estadístico de prueba y el *p-value* (Paso 8 del anexo)

Toda prueba inferencial entrega, como mínimo, dos números:

- **El estadístico de prueba** (por ejemplo, el valor *t* en una prueba t, el valor *F* en ANOVA, o el coeficiente *r* en una correlación): resume, en un solo número, qué tan grande es la diferencia o la relación observada en la muestra.
- **El *p-value***: la probabilidad de observar una diferencia (o una relación) al menos tan grande como la que se vio en la muestra, **si H0 fuera cierta** (si en realidad no hubiera ningún efecto).

En notación formal, para una prueba de dos colas (la más común en este taller):

$$
p = P\big(|T| \geq |t_{\text{obs}}| \;\big|\; H_0 \text{ verdadera}\big)
$$

donde $T$ es la variable aleatoria del estadístico de prueba bajo H0 (por ejemplo, la distribución t) y $t_{\text{obs}}$ es el valor observado en la muestra (Sección 9). Cuanto más extremo (alejado de 0) es el estadístico observado, menor es el *p-value*.

La regla de decisión es la misma que en la Sección 8:

- Si *p* < 0.05 → se **rechaza H0**: la evidencia es lo bastante fuerte como para preferir H1 (sí hay diferencia, sí hay relación).
- Si *p* ≥ 0.05 → **no se rechaza H0**: no hay evidencia suficiente para afirmar un efecto real; podría tratarse simplemente de azar.

Es importante remarcar dos cosas al redactar la interpretación en el portafolio: (1) "no rechazar H0" no significa "demostrar que H0 es cierta", solo que no hubo evidencia suficiente en su contra; y (2) un resultado inferencial (por ejemplo, una correlación o una diferencia de promedios) nunca demuestra por sí solo una relación de causa y efecto, solo que existe una asociación estadística.

**Ejemplo aplicado.** Al aplicar la prueba t de Student sobre `math score` entre los grupos de `test preparation course`, se obtiene un estadístico *t* ≈ −5.70 y un *p-value* ≈ 1.5 × 10⁻⁸ (un número muchísimo menor a 0.05). Como *p* < 0.05, se **rechaza H0**: hay evidencia estadística suficientemente fuerte de que el promedio de `math score` sí difiere entre quienes completaron el curso de preparación y quienes no. La interpretación correcta para el portafolio sería: *"con un nivel de significancia del 5 %, se rechaza la hipótesis nula; la muestra aporta evidencia de que el curso de preparación está asociado con una nota de matemáticas más alta, aunque esta asociación no prueba, por sí sola, una relación de causalidad."*

---

## Glosario rápido

| Palabra | En una frase |
|---|---|
| Población | El conjunto completo del que se quiere concluir |
| Muestra | El subconjunto que sí se midió (aquí, los 1000 estudiantes) |
| Variable dependiente | La que se mide o se quiere explicar |
| Variable independiente | La que podría estar influyendo |
| Media | El promedio de toda la vida |
| Mediana | El valor que queda justo en la mitad al ordenar los datos |
| Moda | El valor que más se repite |
| Desviación estándar | Qué tan lejos están, en promedio, los datos de la media |
| Cuartil / IQR | Puntos de corte que dividen los datos ordenados en 4 partes; el IQR ayuda a detectar *outliers* |
| Correlación | Qué tanto se mueven juntas dos variables numéricas (de −1 a 1) |
| Hipótesis nula (H0) | La opción conservadora: no hay diferencia ni relación |
| Hipótesis alternativa (H1) | La opción que afirma que sí hay diferencia o relación |
| Normalidad | Si una variable se distribuye aproximadamente en forma de campana |
| Homogeneidad de varianzas | Si dos o más grupos tienen una dispersión interna parecida |
| Prueba paramétrica | Prueba que asume normalidad (y a veces homogeneidad); ej. prueba t, ANOVA |
| Prueba no paramétrica | Alternativa que no exige normalidad; ej. Mann-Whitney, Kruskal-Wallis |
| *p-value* | Qué tan raro sería el resultado observado si H0 fuera cierta |

## Notación matemática usada en esta guía

| Símbolo | Significado |
|---|---|
| $x_i$ | Cada valor individual de la variable |
| $n$ | Número de datos en la muestra (o en un grupo) |
| $N$ | Número total de datos, sumando todos los grupos |
| $k$ | Número de grupos que se comparan |
| $\sum$ | Sumatoria: "sumar todos los valores que siguen" |
| $\bar{x}$ | Media muestral |
| $\tilde{x}$ | Mediana |
| $\mu$ | Media poblacional (el valor "real" que la muestra intenta estimar) |
| $\mu_0$ | Valor de referencia fijo contra el que se compara un promedio |
| $s^2$ | Varianza muestral |
| $s$ | Desviación estándar muestral |
| $Q_1, Q_2, Q_3$ | Primer, segundo (mediana) y tercer cuartil |
| $IQR$ | Rango intercuartílico ($Q_3 - Q_1$) |
| $\rho$ (rho) | Coeficiente de correlación poblacional |
| $r$ | Coeficiente de correlación de Pearson (muestral) |
| $r_s$ | Coeficiente de correlación de Spearman |
| $H_0$ / $H_1$ | Hipótesis nula / hipótesis alternativa |
| $t$, $F$, $W$ | Estadísticos de prueba (t de Student, ANOVA, Shapiro-Wilk/Levene) |
| $p$ | *p-value*: probabilidad del resultado observado si H0 fuera cierta |

Estos símbolos son los mismos que aparecen en las fórmulas de las Secciones 3, 4, 7, 8 y 9; si en algún momento una fórmula se ve confusa, conviene volver a esta tabla para identificar qué representa cada letra.

## Resumen — ¿qué uso según la pregunta?

| Pregunta del portafolio | Herramienta estadística |
|---|---|
| ¿Es X numérica o categórica? ¿Cuál es la dependiente y cuál la independiente? | Clasificación de variables (Sección 1) |
| ¿Cuántos datos tengo en total y por grupo? | Tamaño de muestra, n por grupo (Sección 2) |
| ¿Cuál es el valor "típico" de mi variable numérica? | Media, mediana, moda (Sección 3) |
| ¿Qué tan parejos o dispersos están los datos? | Rango, desviación estándar, cuartiles/IQR (Sección 4) |
| ¿Cómo visualizo la distribución, la comparación por grupo, o la relación entre dos variables? | Histograma, boxplot, diagrama de dispersión (Sección 5) |
| ¿Cómo planteo formalmente lo que quiero comprobar? | H0 y H1 (Sección 7) |
| ¿Puedo confiar en una prueba paramétrica o debo usar una no paramétrica? | Prueba de normalidad y de homogeneidad de varianzas (Sección 8) |
| ¿Qué prueba inferencial le corresponde a mi pregunta? | Tabla de selección de la prueba (Sección 9) |
| ¿Qué significa el resultado que arrojó la prueba? | Estadístico de prueba, *p-value* y decisión sobre H0 (Sección 10) |
