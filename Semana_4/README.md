# Aplicación interactiva — Semana 4

Recurso didáctico interactivo de apoyo a la Semana 4
("Librerías para cálculo numérico, análisis y visualización de datos"),
inspirado en [rodanmuro.github.io/material_didactico_machine_learning](https://rodanmuro.github.io/material_didactico_machine_learning/).

Complementa el [taller de la semana](../../Semana_4/Semana_4_Actividad/EIARV011_A4_Taller.md); no lo reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`numpy_vectorizacion.html`** (módulo 1) — Compara construir + sumar cuadrados sobre
  un arreglo de tamaño N con un loop manual vs. un arreglo tipado (analogía de lista vs.
  `np.array`), con benchmark real en el navegador y su equivalente en código Python.
  No depende de `data.js` (usa arreglos sintéticos de tamaño N).
- **`numpy_estadisticos.html`** (módulo 2) — Media, mediana, desviación estándar y
  percentiles (`np.mean`, `np.median`, `np.std`, `np.percentile`) sobre una variable
  elegida, con filtro por tipo (MOVIE/SHOW) y slider de percentil.
- **`correlacion_ttest.html`** (módulo 3) — Correlación de Pearson y prueba t de dos
  muestras (Welch), usando el mismo dataset del taller.
- **`matplotlib_vs_seaborn.html`** (módulo 4) — Histograma, boxplot o dispersión,
  renderizados dos veces con los mismos datos: una vez recreando el estilo por defecto de
  Matplotlib (fondo blanco, sin cuadrícula) y otra el tema `darkgrid` que Seaborn aplica
  automáticamente (cuadrícula, paleta `deep`, KDE, agrupación por `type`, regresión con
  banda de incertidumbre), con el código Python equivalente de cada una.

Los módulos 2, 3 y 4 usan `titles.csv` (títulos de Netflix) y comparten `data.js`. Cada
módulo tiene un enlace «← Recurso interactivo Semana 4» de vuelta a `index.html`.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde ahí, o abrir
cualquier módulo suelto. No requiere servidor: los datos se cargan desde `data.js` con una
etiqueta `<script>`, no con `fetch`, así que funciona igual en `file://` que publicado en
GitHub Pages.

## Cómo regenerar los datos

Si `titles.csv` cambia, regenerar `data.js` con:

```bash
python build_data.py
```

Requiere pandas (ya está en el entorno del proyecto). Filtra a los casos completos en
`type, imdb_score, tmdb_score, runtime, imdb_votes, release_year`.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) y jStat (p-valor de la
prueba t) vía CDN.
