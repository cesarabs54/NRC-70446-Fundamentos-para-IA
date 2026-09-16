
## Qué mide R²

R² responde: *"de toda la variación que hay en `writing score` entre los 1000 estudiantes, ¿qué proporción logra 'explicar' mi modelo usando solo `reading score`?"* Va de 0 (el modelo no explica nada) a 1 (el modelo explica el 100% de la variación).

## Paso 1 — Dos formas de medir "variación"

**Variación total** (cuánto se aleja cada estudiante del promedio general de `writing score`, sin usar el modelo para nada):

$$SS_{tot} = \sum_{i=1}^{n}(y_i - \bar{y})^2 = 230{,}677.08$$

**Variación que sobra después de usar el modelo** (cuánto se aleja cada estudiante de lo que el modelo *predijo* para él, con su propio `reading score`):

$$SS_{res} = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2 = 20{,}470.86$$

donde $\hat{y}_i = -0.6676 + 0.9935 \times \text{reading}_i$ (la predicción del Ejercicio 4, aplicada a cada estudiante).

## Paso 2 — La fórmula de R²

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{20{,}470.86}{230{,}677.08} = 1 - 0.0887 = 0.9113 \approx 0.911$$

**La idea intuitiva:** si el modelo fuera perfecto, $SS_{res}$ sería 0 (ningún estudiante se aleja de su predicción) y R²=1. Si el modelo no sirviera para nada, $SS_{res}$ sería casi igual a $SS_{tot}$ (predecir con el modelo no reduce el error respecto a solo usar el promedio general) y R²≈0. Aquí, el modelo **redujo el error en un 91.1%** comparado con no usar `reading score` en absoluto.

## Atajo para regresión lineal simple: R² = r²

Con solo **una** variable predictora, hay una forma mucho más corta de llegar al mismo número: elevar al cuadrado la correlación de Pearson que ya calculaste.

$$R^2 = r^2 = 0.9546^2 = 0.9113$$

(0.9546 es la correlación entre `reading score` y `writing score` — nota que es distinta al 0.818 del ejercicio anterior, porque esa era math vs. reading; esta es reading vs. writing.) Este atajo **solo funciona con un predictor**; en regresión múltiple (varias variables predictoras) hay que usar la fórmula de $SS_{res}/SS_{tot}$.

## Verificación con el CSV real

```
SS_res = 20470.863689389345
SS_tot = 230677.084
R² manual (1 - SSres/SStot) = 0.9112574888913137

r = 0.9545980771462478,  r² = 0.9112574888913136
```

Las dos formas de calcularlo coinciden exactamente: **R² = 0.911**.