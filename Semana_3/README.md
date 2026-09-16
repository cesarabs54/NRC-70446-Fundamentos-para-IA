# Aplicación interactiva — Semana 3

Recurso didáctico interactivo de apoyo a la Semana 3
("Frameworks para Inteligencia Artificial: scikit-learn, TensorFlow y PyTorch").

Complementa el [taller de la semana](../../Semana_3/Semana_3_Taller_frameworks/Semana_taller_01.md)
y el [foro de discusión](../../Semana_3/Semana_3_Foro/EIARV011_F3_Foro.md); no los reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`entrenamiento_tres_estilos.html`** (módulo 1) — resuelve el mismo problema
  `y = 2x` del taller con los tres frameworks: solución cerrada en scikit-learn,
  descenso de gradiente dentro de un `fit()` de una línea en Keras, y el mismo
  descenso de gradiente expuesto paso a paso (`zero_grad → backward → step`) en
  PyTorch. Curva de pérdida en vivo y código Python real de cada estilo.
- **`knn_interactivo.html`** (módulo 2) — clasificador `KNeighborsClassifier`
  interactivo sobre un dataset sintético de 3 clases (análogo a Iris): haz clic
  para soltar un punto nuevo, ajusta `k` y observa qué vecinos deciden su clase.
- **`radar_frameworks.html`** (módulo 3) — radar comparando scikit-learn,
  TensorFlow y PyTorch en los 6 criterios técnicos del foro (preprocesamiento,
  GPU/rendimiento, facilidad de entrenamiento, interpretabilidad,
  comunidad/documentación, despliegue), con selector de escenario de aplicación.
- **`lineas_codigo_control.html`** (módulo 4) — el mismo modelo `y = 2x` lado a
  lado en los tres frameworks con conteo de líneas, y la tabla comparativa del
  reto integrador del taller con respuesta sugerida para revelar en clase.

Ningún módulo depende de un dataset externo: cada uno usa datos sintéticos
pequeños embebidos directamente en su HTML. Cada módulo tiene un enlace
«← Recurso interactivo Semana 3» de vuelta a `index.html`.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde
ahí, o abrir cualquier módulo suelto. No requiere servidor ni build step.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) vía CDN.
