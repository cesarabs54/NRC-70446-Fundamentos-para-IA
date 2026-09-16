
## Qué mide r (coeficiente de correlación de Pearson)

r responde: *"cuando `math score` sube, ¿`reading score` tiende a subir también (y qué tan consistentemente)?"* Va de -1 (relación inversa perfecta) a +1 (relación directa perfecta), pasando por 0 (sin relación lineal).

## Paso 1 — La fórmula de r

$$r = \frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i-\bar{x})^2 \cdot \sum_{i=1}^{n}(y_i-\bar{y})^2}}$$

Donde $x$ = `math score`, $y$ = `reading score`, y $\bar{x}$, $\bar{y}$ son sus promedios.

**La idea intuitiva:** para cada estudiante, mides si está *arriba del promedio en ambas variables a la vez* (o *abajo en ambas a la vez*) — eso suma positivo al numerador. Si está arriba en una y abajo en la otra, resta. Si casi todos los estudiantes se mueven "juntos" en las dos variables, la suma sale grande y positiva; el denominador solo normaliza el resultado para que quede entre -1 y 1.

Con los 1000 estudiantes, esa cuenta da:

$$r = 0.8176 \approx 0.818$$

## Paso 2 — De r a un p-value: ¿es significativo?

Un r = 0.818 en una muestra de 1000 podría, en teoría, salir por puro azar aunque en la población real no exista relación (ρ = 0). Para saberlo, r se convierte en un estadístico t:

$$t = r\sqrt{\frac{n-2}{1-r^2}} = 0.818\sqrt{\frac{998}{1-0.818^2}} = 44.86$$

con $df = n-2 = 998$ grados de libertad. (Este es el mismo tipo de estadístico t que usaste para comparar medias — aquí se usa para poner a prueba una correlación en vez de una diferencia de medias.)

## Paso 3 — El p-value

$$p = 2\times P(T_{998}\geq 44.86) \approx 1.79\times10^{-241}$$

Un t = 44.86 es un número descomunal (recuerda: t ≈ 10 ya era "casi imposible" en el ejercicio de género/escritura). Aquí es más de 4 veces eso — el p-value es tan diminuto que la computadora ya casi no tiene forma de escribirlo con precisión (1.79×10⁻²⁴¹, un número con 241 ceros).

## Verificación con el CSV real

```
r manual  = 0.817579663672054
t_r       = 44.85511738154363, df = 998
p manual  = 1.787753109906064e-241

scipy.stats.pearsonr: r=0.8175796636720541, p=1.7877531099062542e-241
```

Coincide exactamente. **H0: ρ=0** se rechaza sin ninguna duda: la relación entre `math score` y `reading score` es real, fuerte y positiva.