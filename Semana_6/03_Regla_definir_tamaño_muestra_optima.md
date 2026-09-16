## Pregunta: ¿Hay alguna regla para definir el tamaño de la muestra óptima?

## Sí — se llama "análisis de potencia" (power analysis)

No existe un número mágico universal ("usa siempre n=30" es un mito muy repetido). El tamaño de muestra "óptimo" se **calcula** a partir de 4 ingredientes que tú decides de antemano, antes de recolectar los datos:

| Ingrediente | ¿Qué es? | Ejemplo típico |
|---|---|---|
| **α (significancia)** | El riesgo de error tipo I que aceptas | 0.05 |
| **Potencia (1-β)** | La probabilidad de detectar el efecto *si de verdad existe* (lo contrario de error tipo II) | 0.80 u 0.90 (80% o 90%) |
| **Tamaño del efecto (d)** | Qué tan grande es la diferencia que te interesa detectar, en unidades estandarizadas | Depende del caso (ver abajo) |
| **Variabilidad de los datos (σ)** | Ya está incluida dentro de *d* (Cohen's d divide la diferencia entre la desviación estándar) | — |

La lógica: **mientras más chico es el efecto que quieres detectar, más muestra necesitas** para no perderlo entre el ruido — es exactamente lo que vimos con la simulación de n=50 (el efecto real del curso "desapareció" con poca muestra).

## La fórmula (para comparar 2 grupos, como en tus ejercicios)

$$n_{\text{por grupo}} = \frac{2(z_{\alpha/2} + z_{\beta})^2}{d^2}$$

donde $d$ es el **tamaño del efecto de Cohen** (la diferencia de medias dividida entre la desviación estándar combinada — el mismo concepto que te ofrecí explicar hace un par de mensajes):

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_p}$$

## Ejemplo con tus propios datos: `math score` por `gender`

$$d = \frac{68.73 - 63.63}{14.94} = 0.341 \quad (\text{un efecto "pequeño-mediano"})$$

Con $\alpha=0.05$ (dos colas, $z_{\alpha/2}=1.96$) y potencia del 80% ($z_\beta=0.84$):

$$n_{\text{por grupo}} = \frac{2(1.96+0.84)^2}{0.341^2} = 135.2 \approx \textbf{136 estudiantes por grupo}$$

Verificado con `statsmodels` (que usa la distribución t exacta en vez de la aproximación normal): **136 por grupo** para 80% de potencia, **182 por grupo** para 90% de potencia.

**Lo interesante:** tu muestra real tiene **482 y 518** por grupo — casi 4 veces más de lo que hacía falta para 80% de potencia. Por eso el p-value salió tan extremo (9.12×10⁻⁸): con ese tamaño de muestra, tienes muchísima más capacidad de detección de la mínima necesaria.

## Reglas de dedo (cuando no puedes calcular *d* de antemano)

- **Comparar 2 grupos, efecto mediano (d≈0.5):** ~64 por grupo para 80% de potencia.
- **Comparar 2 grupos, efecto pequeño (d≈0.2):** ~393 por grupo — los efectos pequeños son "caros" de detectar.
- **Correlación:** para detectar r≈0.3 con 80% de potencia, hacen falta ~84 observaciones; para r≈0.1 (efecto débil), ~782.
- **ANOVA con 3+ grupos:** generalmente necesitas *más* muestra por grupo que en una comparación de 2, porque "repartes" la potencia entre más comparaciones.

## El trade-off, en una frase

No hay un "n óptimo" abstracto — hay un **n óptimo para el efecto que te importa detectar**. Pedir "más muestra siempre" no es gratis (cuesta tiempo/dinero) y pedir "menos muestra" arriesga cometer error tipo II (como en tu simulación de n=50). El análisis de potencia es la forma de decidir *antes* de recolectar datos: "necesito al menos X observaciones para tener una probabilidad razonable de detectar el efecto que me interesa, si es que existe".

```
Cohen's d (math score, gender) = 0.3407
n necesario por grupo (80% potencia) = 135.2  (statsmodels: 136.2)
n necesario por grupo (90% potencia) = 181.1  (statsmodels: 182.0)
```

¿Quieres que te muestre cómo calcular esto en Python con `statsmodels.stats.power`, o prefieres que lo agreguemos como un ejercicio nuevo en alguno de los talleres?