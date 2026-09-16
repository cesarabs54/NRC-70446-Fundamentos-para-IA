# Aplicación interactiva — Semana 2

Recurso didáctico interactivo de apoyo a la Semana 2 ("Python para ciencia de datos").

Complementa el [estudio de caso de la semana](../../Semana_2/Semana_2_Actividad/EIARV011_A2.md)
("Consulta en un Dataset", ver también el [anexo](../../Semana_2/Semana_2_Actividad/EIARV011_A2_Anexo.md));
no lo reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`exploracion_inicial.html`** (módulo 1) — Tamaño del dataset, columnas, tipos de
  dato (categórica/numérica) y una vista de filas con `head()`, `tail()` y `sample()`
  controlable con botones y un slider de cantidad de filas.
- **`calidad_datos.html`** (módulo 2) — Nulos por columna (`isnull().sum()`),
  duplicados (`duplicated().sum()`) y detección de valores atípicos por regla de IQR
  sobre un boxplot, con selector de variable y slider del multiplicador `k`.
- **`variables_categoricas.html`** (módulo 3) — `value_counts()` interactivo: selector
  de columna categórica (gender, race/ethnicity, parental level of education, lunch,
  test preparation course) con toggle conteo/porcentaje.
- **`variables_numericas.html`** (módulo 4) — `describe()` con histograma sobre los
  tres puntajes, diagrama de dispersión con correlación de Pearson entre dos variables,
  y comparación de medias por grupo (`groupby(...).mean()`) con nota sobre correlación
  vs. causalidad.

Todos los módulos usan `StudentsPerformance.csv` (1000 registros, 8 columnas) vía
`data.js`. Cada módulo tiene un enlace «← Recurso interactivo Semana 2» de vuelta a
`index.html`.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde ahí, o
abrir cualquier módulo suelto. No requiere servidor: los datos se cargan desde
`data.js` con una etiqueta `<script>`, no con `fetch`, así que funciona igual en
`file://` que publicado en GitHub Pages.

## Cómo regenerar los datos

Si `StudentsPerformance.csv` cambia, regenerar `data.js` con:

```bash
python build_data.py
```

Requiere pandas (ya está en el entorno del proyecto).

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) vía CDN.
