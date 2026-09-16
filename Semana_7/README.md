# Aplicación interactiva — Semana 7

Recurso didáctico interactivo de apoyo a la Semana 7 ("Estadística inferencial II: regresión lineal"),
inspirado en
[rodanmuro.github.io/material_didactico_machine_learning](https://rodanmuro.github.io/material_didactico_machine_learning/).

Complementa los documentos conceptuales de la semana
([`01_Regresion_lineal_conceptos_basicos.md`](../../Semana_7/01_Regresion_lineal_conceptos_basicos.md),
[`02_Cuando_utilizar_modelo_regresion_lineal.md`](../../Semana_7/02_Cuando_utilizar_modelo_regresion_lineal.md))
y el taller
[`Taller_02_Regresion_lineal_conceptos_basicos.md`](../../Semana_7/Taller_02_Regresion_lineal_conceptos_basicos.md),
en `Semana_7/`; no los reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`correlacion_minimos_cuadrados.html`** (módulo 1) — Elige cualquier par ordenado de notas (matemáticas,
  lectura, escritura) como X e Y — 6 combinaciones posibles. Diagrama de dispersión con la recta de mínimos
  cuadrados superpuesta, y cálculo en vivo de x̄, ȳ, Sxy, Sxx, b1, b0 y r (correlación de Pearson), con las
  fórmulas del documento. Cubre la Sección 3 de `01_Regresion_lineal_conceptos_basicos.md`.
- **`ajuste_residuos.html`** (módulo 2) — Para el mismo par X/Y, muestra la recta ajustada, un gráfico de
  residuos vs. valores ajustados, y las métricas SSres, SStot, R² y RMSE, calculadas en vivo. Al hacer clic
  en cualquier punto (en cualquiera de las dos gráficas) se resalta su residuo en ambas. Cubre la Sección 5
  de `01_Regresion_lineal_conceptos_basicos.md` y el Ejercicio 5 del taller.
- **`prueba_hipotesis_pendiente.html`** (módulo 3) — Dos partes: (a) para el par X/Y elegido, calcula
  SE(b1), el estadístico t, los grados de libertad y el p-value (dos colas, vía la distribución t de
  `jStat`), con el planteamiento de H0/H1 y el veredicto a α = 0.05; (b) reproduce el ejemplo aplicado del
  documento (género como variable dummy sobre `writing score`), mostrando que el coeficiente `b1` de esa
  regresión es exactamente la diferencia de medias entre grupos, con la prueba de Levene (homogeneidad de
  varianzas) calculada en vivo y la equivalencia con un t-test de dos muestras. Cubre la Sección 2 y el
  "Ejemplo aplicado" de la Sección 5 de `01_Regresion_lineal_conceptos_basicos.md`, y el Ejercicio 7 del
  taller.
- **`cuando_usar_prediccion.html`** (módulo 4) — Tres bloques: (a) una calculadora de predicción en vivo
  (elige X, Y y un valor de X) que marca con una alerta cuando el valor cae fuera del rango observado de
  esa variable (extrapolación); (b) una matriz de correlación en vivo entre las tres notas, para ilustrar la
  multicolinealidad entre `reading score` y `writing score`; (c) el checklist rápido del documento, como una
  lista de verificación real (casillas marcables). Cubre las Secciones 2.3, 2.4 y 3 de
  `02_Cuando_utilizar_modelo_regresion_lineal.md`.

Todos los módulos usan `StudentsPerformance.csv` (notas de 1000 estudiantes, el mismo de la Semana 6 y de
los documentos de la Semana 7) y comparten `data.js`. Cada módulo tiene un enlace «← Recurso interactivo
Semana 7» de vuelta a `index.html`.

Los cuatro módulos incluyen, bajo cada gráfica o tabla, un desplegable **«Ver código Python equivalente»**
con el fragmento de `pandas`/`scipy`/`statsmodels` que reproduce ese mismo cálculo sobre el `DataFrame` `df`
del taller — se actualiza según la variable X/Y elegida, e incluye un botón «Copiar» para pegarlo
directamente en un notebook real.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde ahí, o abrir cualquier módulo
suelto. No requiere servidor: los datos se cargan desde `data.js` con una etiqueta `<script>`, no con
`fetch`, así que funciona igual en `file://` que publicado en GitHub Pages.

## Cómo regenerar los datos

Si `StudentsPerformance.csv` cambia, regenerar `data.js` con:

```bash
python build_data.py
```

Requiere pandas (ya está en el entorno del proyecto). Toma el CSV de `Semana_7/StudentsPerformance.csv`
(a diferencia de Semana 6, aquí no hay una subcarpeta `..._Actividad_solucion_profesor`: el CSV vive
directamente en `Semana_7/`), filtra a los casos completos en las 8 columnas del *dataset* y renombra cada
columna a una clave JS corta (por ejemplo, `reading score` → `readingScore`), igual que en Semana 6.

## Diferencias respecto al patrón de Semana 6

- Semana 6 comparaba **grupos** (variable categórica de agrupación); Semana 7 compara **variables
  numéricas** (X, Y), así que los selectores son "Variable independiente (X)" / "Variable dependiente (Y)"
  en vez de "variable de agrupación" / "puntaje". Para evitar elegir X = Y, el selector de Y siempre excluye
  la opción actualmente elegida en X (y se ajusta automáticamente si X cambia a lo que tenía Y).
- El p-value del coeficiente de la pendiente (módulo 3) se calcula con la distribución t de Student de
  `jStat` (`jStat.studentt.cdf`), igual que en los módulos de Semana 6 — no hay nada nuevo que sustituir
  aquí, a diferencia de la normalidad (Jarque-Bera vs. Shapiro-Wilk) en Semana 6.
- La prueba de Levene del módulo 3 (caso aplicado de género) reutiliza exactamente la misma implementación
  en JavaScript de `Semana_6/eleccion_prueba.html` y `Semana_6/supuestos_normalidad_varianza.html`, sobre
  `writing score` agrupado por `gender`.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) y jStat (distribución t de Student para el
p-value del coeficiente, y distribución F para Levene, en el Módulo 3) vía CDN.
