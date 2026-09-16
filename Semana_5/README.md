# Aplicación interactiva — Semana 5

Recurso didáctico interactivo de apoyo a la Semana 5 ("Estadística básica y visualización de
datos"), inspirado en
[rodanmuro.github.io/material_didactico_machine_learning](https://rodanmuro.github.io/material_didactico_machine_learning/).

Complementa la [guía de estadística básica](../../Semana_5/01_%20Estadistica_basica/01_Estadistica_Basica.md)
y el [taller de visualización](../../Semana_5/02_Taller_01_visualizacion_de_datos/Taller_01_Visualizacion_de_datos.md);
no los reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`centro_dispersion.html`** (módulo 1) — Media, mediana, moda (histograma) y cuartiles/IQR con
  detección de valores atípicos (diagrama de caja), sobre la variable y el filtro por curso de
  preparación que elijas. Cubre las Secciones 3 y 4 de la guía.
- **`que_grafico_usar.html`** (módulo 2) — Selector de 5 situaciones (conteo o promedio por
  grupo, distribución, comparación entre grupos, relación, proporción) que renderiza en vivo el
  gráfico recomendado (barras, histograma, boxplot, dispersión o pastel). Cubre la Sección 5 de
  la guía y la tabla "¿Por qué visualizar los datos?" del taller. Al final incluye el "Reto
  final" del taller: las mismas 3 preguntas, con un botón para cargarlas en el explorador y un
  desplegable con la respuesta de `Taller_01_Visualizacion_de_datos_profesor.ipynb`.
- **`bins_escala_eje.html`** (módulo 3) — Dos demostraciones aisladas de cómo los parámetros de
  un gráfico cambian la impresión visual sin cambiar los datos: un slider de número de *bins* en
  un histograma (Ejercicio 2b del taller) y un interruptor de rango del eje Y en un gráfico de
  barras de promedios por grupo (Ejercicio 6b del taller).
- **`hipotesis_prueba.html`** (módulo 4) — Flujo completo de estadística inferencial: elige una
  pregunta (2 grupos, 3+ grupos o correlación), revisa H0/H1, la homogeneidad de varianzas
  (Levene, calculado en vivo) y un indicador aproximado de normalidad (asimetría), ejecuta la
  prueba correspondiente (t de Student, ANOVA + Kruskal-Wallis, o correlación de Pearson) y lee
  la decisión sobre H0. Cubre las Secciones 6 a 10 de la guía.

Todos los módulos usan `StudentsPerformance.csv` (notas de 1000 estudiantes) y comparten
`data.js`. Cada módulo tiene un enlace «← Recurso interactivo Semana 5» de vuelta a
`index.html`.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde ahí, o abrir
cualquier módulo suelto. No requiere servidor: los datos se cargan desde `data.js` con una
etiqueta `<script>`, no con `fetch`, así que funciona igual en `file://` que publicado en
GitHub Pages.

## Cómo regenerar los datos

Si `StudentsPerformance.csv` cambia, regenerar `data.js` con:

```bash
python build_data.py
```

Requiere pandas (ya está en el entorno del proyecto). Filtra a los casos completos en las 8
columnas del *dataset* y renombra cada columna a una clave JS corta (por ejemplo,
`test preparation course` → `testPrep`).

## Sobre la prueba de normalidad

El módulo 4 usa un indicador aproximado de normalidad (asimetría de la muestra), calculado en
JavaScript en el navegador. El notebook docente de la semana (`02_Ejercicios_aplicacion_profesor.ipynb`)
aplica la prueba exacta de Shapiro-Wilk (`scipy.stats.shapiro`); ambos indicadores suelen
coincidir en su conclusión práctica, pero no son el mismo cálculo.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) y jStat (distribuciones t, F y
chi-cuadrado para los p-valores del módulo 4) vía CDN.
