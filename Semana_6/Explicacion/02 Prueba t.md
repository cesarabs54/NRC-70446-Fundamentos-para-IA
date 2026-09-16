## Qué mide el estadístico t

El **t** responde una pregunta muy concreta: *"la diferencia que veo entre los dos promedios (63.31 vs. 72.47), ¿es grande comparada con el 'ruido' natural de los datos, o es chiquita comparada con ese ruido?"*

$$t = \frac{\text{diferencia entre promedios}}{\text{error estándar (el "ruido" esperado de esa diferencia, por azar)}}$$

Si la diferencia es mucho más grande que el ruido esperado → t grande (en valor absoluto) → sospechoso, "esto no parece azar". Si es parecida al ruido → t chico → "esto sí podría ser azar".

## La fórmula paso a paso (con tus números reales)

Como Levene dijo que las varianzas son homogéneas (p = 0.934), se usa la **prueba t con varianza combinada (pooled)**:

**Paso 1 — Los datos de cada grupo:**

| Grupo | n | media | desv. estándar |
|---|---|---|---|
| Hombres | 482 | 63.3112 | 14.1138 |
| Mujeres | 518 | 72.4672 | 14.8448 |

**Paso 2 — Combinar las dos varianzas en una sola** (ponderando por tamaño de grupo):

$$s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} = \frac{481 \times 14.11^2 + 517 \times 14.84^2}{998} = 210.17$$

**Paso 3 — El "error estándar" de la diferencia entre las dos medias** (el ruido esperado):

$$SE = \sqrt{s_p^2 \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} = \sqrt{210.17 \left(\frac{1}{482} + \frac{1}{518}\right)} = 0.9175$$

**Paso 4 — El estadístico t: diferencia de medias ÷ error estándar:**

$$t = \frac{63.3112 - 72.4672}{0.9175} = \frac{-9.156}{0.9175} = -9.98$$

**¿Por qué negativo?** Porque restamos *hombres − mujeres*, y los hombres promedian menos: la resta da un número negativo. El signo solo indica la dirección (quién es mayor); lo que importa para la fuerza de la evidencia es el tamaño, 9.98 — un valor enorme.

**Paso 5 — Grados de libertad:** $df = n_1+n_2-2 = 998$.

**Paso 6 — Convertir t en p-value**, usando la distribución t con 998 grados de libertad (que a ese tamaño ya es casi idéntica a una campana normal):

$$p = 2 \times P(T_{998} \geq |{-9.98}|) = 2.02\times10^{-22}$$

## La analogía: qué tan "fuera de lo normal" es t = -9.98

Con 998 grados de libertad, la distribución t se parece muchísimo a una campana de Gauss normal. En una campana normal, un valor a **más de 5 desviaciones estándar** del centro ya es prácticamente imposible (probabilidad astronómicamente chica). Aquí **t = -9.98** está casi **10 desviaciones estándar** lejos del centro (del "aquí no pasa nada especial").

Es como decir: la altura promedio de un salón es 1.70 m con una variación típica de 10 cm, y de repente mides a alguien de **2.70 m** (10 "unidades de variación" por encima del promedio). No dirías "qué casualidad" — dirías "algo raro está pasando aquí, esto no es una persona común". Eso es exactamente lo que dice p = 2.02×10⁻²²: es tan extremo que, si de verdad no hubiera diferencia entre hombres y mujeres, verías un resultado así **una vez en 500 mil billones de intentos**. Prácticamente imposible por azar → se rechaza H0 sin ninguna duda.

## Verificación con el cálculo real

```
t manual  = -9.979557910004507
p manual  = 2.0198777068679151e-22

scipy:      TtestResult(statistic=-9.979557910004507, pvalue=2.0198777068679151e-22, df=998.0)
```

Coincide exactamente — así se construye el `t=-9.98, p=2.02×10⁻²²` por dentro, paso a paso.