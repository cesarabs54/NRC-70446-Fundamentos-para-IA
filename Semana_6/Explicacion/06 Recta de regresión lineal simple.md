
## Qué es esta ecuación

Es la fórmula de una **recta** — la misma que aprendiste en el colegio, $y = mx + b$, pero con nombres de estadística:

$$\text{writing score} = \underbrace{-0.6676}_{\text{intercepto } (b)} + \underbrace{0.9935}_{\text{pendiente } (m)} \times \text{reading score}$$

De los 1000 puntos (uno por estudiante, con su `reading score` y su `writing score`), esta recta es la que **mejor los atraviesa** — específicamente, la que minimiza $SS_{res}$ (la suma de errores al cuadrado que calculamos para el R²). Por eso se llama "mínimos cuadrados" (*least squares*).

## Paso 1 — La pendiente: cuánta "coreografía" hay entre las dos variables

$$m = \frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sum_{i=1}^{n}(x_i-\bar{x})^2} = \frac{S_{xy}}{S_{xx}}$$

Con $x$ = `reading score`, $y$ = `writing score`. El **numerador** ($S_{xy}$ = 211,574.87) es prácticamente lo mismo que usaste para calcular r: mide cuánto se mueven juntas las dos variables. El **denominador** ($S_{xx}$ = 212,952.44) mide cuánto varía *solo* `reading score`. Al dividir, obtienes: *"por cada unidad que varía reading, cuánto varía writing en promedio"*.

$$m = \frac{211{,}574.87}{212{,}952.44} = 0.9935$$

**Atajo equivalente** (usando la correlación r que ya calculaste y las desviaciones estándar de cada variable):

$$m = r \times \frac{s_y}{s_x} = 0.9546 \times \frac{15.20}{15.24} = 0.9935$$

## Paso 2 — El intercepto: "anclar" la recta para que pase por el centro de los datos

Una vez tienes la pendiente, el intercepto se obtiene exigiendo que la recta pase exactamente por el punto (promedio de x, promedio de y):

$$b = \bar{y} - m\bar{x} = 68.054 - (0.9935 \times 69.169) = -0.6676$$

Aquí $\bar{x}$ = 69.169 (promedio de `reading score`) y $\bar{y}$ = 68.054 (promedio de `writing score`).

## Verificación con un estudiante real

Tomé el primer estudiante del archivo: `reading score` = 72, `writing score` real = 74.

$$\hat{y} = -0.6676 + 0.9935 \times 72 = 70.87$$

El modelo predijo **70.87**, y su nota real fue **74** — un error de 3.13 puntos para ese estudiante en particular (ese tipo de errores, sumados y elevados al cuadrado para los 1000 estudiantes, es justamente el $SS_{res}$ = 20,470.86 del R² que ya explicamos).

## Verificación completa con el CSV real

```
pendiente manual (Sxy/Sxx)     = 0.9935311142409596
intercepto manual (ybar - m*xbar) = -0.6675536409329368
pendiente vía r*(sy/sx)        = 0.9935311142409595

scipy.stats.linregress: slope=0.9935311142409595, intercept=-0.6675536409329226
```

Coincide exactamente (la mínima diferencia en el último decimal es solo redondeo de punto flotante) — así se calcula por dentro cada número de esa ecuación.