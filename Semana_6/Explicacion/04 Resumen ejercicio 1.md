
## Por qué "¿Cuánta?", es una pregunta aparte

Fíjate que el resumen divide la conclusión en **3 preguntas distintas**, y eso no es casualidad — son tres cosas *diferentes* que la estadística responde por separado:

1. **¿Puedo usar la prueba t?** → esto lo responde **Levene** (supuestos).
2. **¿Hay diferencia real?** → esto lo responde el **p-value** (0 o 1: ¿es estadísticamente significativo o no?).
3. **¿Cuánta?** → esto **no** lo responde el p-value. Lo responde algo mucho más simple: **la resta de los dos promedios**.

Este es exactamente el mismo punto que vimos en el Ejercicio 5/7 del otro taller ("p pequeño ≠ efecto grande"): el p-value te dice *si* confiar en que la diferencia es real, pero es ciego al **tamaño** de esa diferencia. Para el tamaño, necesitas otra cuenta — mucho más sencilla.

## El cálculo de "¿cuánta?"

No hace falta nada del mundo de las pruebas de hipótesis — es una simple resta de las medias que ya tenías:

$$\text{Diferencia} = \bar{x}_{mujeres} - \bar{x}_{hombres} = 72.47 - 63.31 = 9.16 \approx 9.2 \text{ puntos}$$

Es decir: en promedio, una mujer de la muestra sacó **9.2 puntos más** que un hombre en `writing score`. Esto se llama el **tamaño del efecto** (en sus unidades originales, puntos de examen) — es la respuesta a "¿me importa esto en la vida real?", distinta de "¿es estadísticamente significativo?".

## Por qué separar estas dos preguntas importa

Imagina dos escenarios hipotéticos:

- **Escenario A:** p = 2.02×10⁻²² (rechazas H0) y la diferencia es de **9.2 puntos** → hay evidencia fuerte de una diferencia **grande y relevante**.
- **Escenario B (como en el ejercicio de los "Estudios A y B" que ya viste):** p < 0.05 (rechazas H0) pero la diferencia es de solo **0.3 puntos** → hay evidencia fuerte de una diferencia **real pero casi irrelevante en la práctica**.

Con solo el p-value, los dos escenarios se ven "igual de significativos". Preguntar **"¿cuánta?"** es lo que te permite distinguir un hallazgo importante de uno estadísticamente real pero trivial.

## Verificación con el CSV real

```python
mujeres.mean() - hombres.mean()
# 72.4672 - 63.3112 = 9.1560
```

$$9.156 \approx 9.2 \text{ puntos} ✓$$

Coincide con lo que dice el resumen. Si quisieras ir un paso más allá (para tus talleres de regresión en la Semana 7), este mismo tamaño de efecto también se puede **estandarizar** dividiéndolo entre la dispersión combinada de los datos — eso se llama *Cohen's d*, y responde "¿cuántas desviaciones estándar de distancia hay entre los dos grupos?" en vez de "¿cuántos puntos?". ¿Te gustaría que te lo explique también?