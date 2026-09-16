
## ¿Por qué existe la prueba t de Welch?

La prueba t "clásica" (la que usaste con `writing score` por género) tiene un requisito escondido: **combina (agrupa/"pooled") las dos varianzas en una sola**, como si ambos grupos tuvieran exactamente la misma dispersión. Eso solo es justo si Levene confirma que sí la tienen (como en tu caso, p = 0.934).

**¿Qué pasa si Levene falla** (las varianzas SÍ son distintas)? Combinarlas sería como promediar el ruido de un salón silencioso con el de un salón ruidoso y tratarlos como si fueran igual de ruidosos — distorsiona el resultado. La **prueba t de Welch** resuelve esto: **nunca combina las varianzas**, cada grupo aporta su propia dispersión al cálculo. Por eso funciona bien tanto si las varianzas son iguales como si no — es la opción "segura por defecto" cuando tienes dudas.

## Un ejemplo real donde SÍ hace falta Welch

Busqué en el mismo *dataset* un caso donde Levene **sí falla**: `writing score` según `test preparation course`.

```
n sin curso = 642, media = 64.50, desv.est = 15.00
n con curso = 358, media = 74.42, desv.est = 13.38

Levene -> p = 0.0147   (< 0.05: las varianzas NO son homogéneas)
```

## La diferencia en la fórmula

**Prueba t clásica (pooled)** — combina las dos varianzas en una sola $s_p^2$ y usa:

$$SE_{pooled} = \sqrt{s_p^2\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}, \qquad df = n_1+n_2-2$$

**Prueba t de Welch** — nunca combina; cada grupo aporta *su propia* varianza dividida por su propio tamaño:

$$SE_{Welch} = \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}, \qquad t = \frac{\bar{x}_1-\bar{x}_2}{SE_{Welch}}$$

Con tus números: $SE_{Welch} = \sqrt{\frac{15.00^2}{642} + \frac{13.38^2}{358}} = 0.922$, y $t = \frac{64.50-74.42}{0.922} = -10.75$.

## La parte más curiosa: los grados de libertad ya no son un número "redondo"

En la prueba clásica, $df = n_1+n_2-2 = 998$ (siempre entero). Welch usa la **fórmula de Welch-Satterthwaite**, que "penaliza" con menos grados de libertad cuando las varianzas y tamaños de grupo son muy distintos entre sí:

$$df_{Welch} = \frac{\left(\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1-1}+\frac{(s_2^2/n_2)^2}{n_2-1}}$$

Con tus números da **df = 811.13** — un número **no entero**, y notablemente menor que 998. Ese es literalmente el "precio" que paga Welch por no asumir que las varianzas son iguales: es más conservador, así que exige un poquito más de evidencia (menos grados de libertad = distribución t un poco más "ancha").

## Comparación lado a lado (verificado con el CSV real)

| | Prueba t clásica | Prueba t de Welch |
|---|---|---|
| t | -10.4092 | -10.7525 |
| df | 998 (entero) | 811.13 (no entero) |
| p-value | 3.69×10⁻²⁴ | 2.66×10⁻²⁵ |

```
t clasica (pooled): t=-10.4092, p=3.685e-24, df=998.0
t Welch:            t=-10.7525, p=2.663e-25, df=811.13
```

En este caso, como la diferencia es tan grande, **las dos pruebas llegan a la misma conclusión** (se rechaza H0 con muchísima confianza en ambas) — pero los números sí cambian, y en casos más límite (p cerca de 0.05) elegir la prueba correcta según Levene puede cambiar la decisión final. Por eso la regla práctica es: **Levene falla → usa Welch** (`equal_var=False` en `scipy.stats.ttest_ind`); **Levene se cumple → usa la clásica** (`equal_var=True`), como en tu ejercicio de `writing score` por género.