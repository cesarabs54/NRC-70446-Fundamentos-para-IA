# Aplicación interactiva — Semana 6

Recurso didáctico interactivo de apoyo a la Semana 6 ("Estadística inferencial I: prueba de
hipótesis"), inspirado en
[rodanmuro.github.io/material_didactico_machine_learning](https://rodanmuro.github.io/material_didactico_machine_learning/).

Complementa el notebook docente
[`EIARV011_A6_Notebook.ipynb`](../../Semana_6/Semana_6_Actividad_solucion_profesor/EIARV011_A6_Notebook.ipynb)
(carpeta `Semana_6_Actividad_solucion_profesor`) y los documentos conceptuales de la semana
(`01_Estadistica_inferencial_conceptos.md`, `02_Pruebas_Hipotesis_conceptos.md`,
`03_Regla_definir_tamaño_muestra_optima.md`, en `Semana_6/`); no los reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 5 módulos.
- **`muestra_y_descriptiva.html`** (módulo 1) — Tamaño de la muestra y de los grupos, histograma
  superpuesto por grupo y diagrama de caja, con tabla de estadística descriptiva
  (equivalente a `df.groupby(...).describe()`). Elige cualquier combinación de variable de
  agrupación (curso de preparación, género, almuerzo, grupo étnico, nivel educativo de los
  padres) y puntaje (matemáticas, lectura, escritura). Cubre las Secciones 1, 3, 4 y 5 del
  notebook.
- **`supuestos_normalidad_varianza.html`** (módulo 2) — Normalidad por grupo (prueba de
  Jarque-Bera, calculada en vivo, con histograma contra la campana normal) y homogeneidad de
  varianzas (Levene), con un veredicto combinado sobre qué prueba corresponde — incluye las 5
  variables de agrupación del *dataset* (2 o más grupos). Cubre la Sección 6 del notebook.
- **`eleccion_prueba.html`** (módulo 3) — Calcula en vivo, lado a lado, la prueba correspondiente:
  con 2 grupos, t de Student (pooled), t de Welch y Mann-Whitney U; con 3 o más grupos (grupo
  étnico, nivel educativo de los padres), ANOVA de un factor y Kruskal-Wallis. En ambos casos
  resalta la recomendada según el flujo de decisión (normalidad + homogeneidad de varianzas) y
  separa explícitamente "¿hay diferencia?" (p-value) de "¿cuánta?" (diferencia de medias). Cubre
  las Secciones 6 a 8 del notebook y los Ejercicios 2 y 8 de `02_Pruebas_Hipotesis_conceptos.md`.
- **`caso_guiado.html`** (módulo 4) — Recorrido narrado, paso a paso (acordeón), del caso
  documentado en el notebook (curso de preparación → nota de matemáticas), con los números
  reales de `scipy.stats` y enlaces "Ver en vivo" hacia los módulos 1 a 3 para reproducir cada
  cálculo. Cierra con una sección de práctica para intentar otras combinaciones de variables.
- **`tamano_muestra.html`** (módulo 5) — Los dos tipos de error (matriz H0 verdadera/falsa ×
  rechazar/no rechazar), una calculadora en vivo de Cohen's d (con curvas normales superpuestas
  que muestran el solapamiento entre grupos) y de tamaño de muestra necesario según la potencia
  deseada (`n = 2(z_α/2 + z_β)² / d²`), y una demostración con los primeros 10 estudiantes de
  cada grupo vs. el grupo completo para ilustrar el error tipo II en acción. Basado en
  `03_Regla_definir_tamaño_muestra_optima.md` y los Ejercicios 6-8 de
  `02_Pruebas_Hipotesis_conceptos.md`/`Taller_03_Prueba_Hipotesis_conceptos.md`.

Todos los módulos usan `StudentsPerformance.csv` (notas de 1000 estudiantes, el mismo del
notebook) y comparten `data.js`. Cada módulo tiene un enlace «← Recurso interactivo Semana 6» de
vuelta a `index.html`.

Los módulos 1, 2, 3 y 5 incluyen, bajo cada gráfica o tabla, un desplegable **«Ver código Python
equivalente»** con el fragmento de `pandas`/`scipy`/`seaborn`/`statsmodels` que reproduce ese
mismo cálculo o gráfico sobre el `DataFrame` `df` del notebook — se actualiza según la variable
de agrupación y el puntaje elegidos, e incluye un botón «Copiar» para pegarlo directamente en un
notebook real.

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

Requiere pandas (ya está en el entorno del proyecto). Toma el CSV de
`Semana_6/Semana_6_Actividad_solucion_profesor/StudentsPerformance.csv`, filtra a los casos
completos en las 8 columnas del *dataset* y renombra cada columna a una clave JS corta (por
ejemplo, `test preparation course` → `testPrep`).

## Sobre la prueba de normalidad

Los módulos 2 y 3 usan la prueba de **Jarque-Bera** (asimetría y curtosis, con *p-value* exacto
vía chi-cuadrado) como sustituto de **Shapiro-Wilk**, calculado en el notebook con
`scipy.stats.shapiro`. Shapiro-Wilk no tiene una implementación simple en JavaScript vanilla;
Jarque-Bera es una prueba formal distinta pero con el mismo objetivo, y con estos datos suele
coincidir con Shapiro-Wilk en la conclusión práctica (rechazar o no rechazar normalidad), aunque
no son el mismo cálculo ni dan el mismo *p-value*.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) y jStat (distribuciones t, F,
chi-cuadrado y normal para los p-valores y para el cálculo de potencia de los módulos 2, 3 y 5)
vía CDN.
