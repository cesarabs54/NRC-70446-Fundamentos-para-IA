# Aplicación interactiva — Semana 1

Recurso didáctico interactivo de apoyo a la Semana 1
("Introducción a Python para inteligencia artificial").

Complementa los [ejercicios de clase](../../Semana_1/semana_1_estudiante.md)
(y su [versión profesor](../../Semana_1/semana_1_profesor.md)); no los reemplaza.

## Estructura

- **`index.html`** — página de entrada con tarjetas hacia los 4 módulos.
- **`tipos_operadores.html`** (módulo 1) — REPL paso a paso (Ejercicio 1),
  quiz de tipos de datos sobre las variables de un experimento (Ejercicio 2)
  y comparador de dos modelos con sliders de accuracy (error, diferencia,
  comparación booleana — Ejercicio 3).
- **`estructuras_datos.html`** (módulo 2) — lista de accuracy con
  append/remove/sort animado (Ejercicio 4), demo de inmutabilidad de tuplas
  con el `TypeError` real (Ejercicio 5), conversión de lista con duplicados
  a `set` (Ejercicio 5) y diccionario de experimento con inserción de llave
  (Ejercicio 6).
- **`control_flujo.html`** (módulo 3) — gauge en vivo que clasifica un
  experimento según su accuracy (Ejercicio 7), selector de optimizador con
  `match/case` (Ejercicio 7), trazador paso a paso del bucle que acumula
  suma y mejor modelo (Ejercicio 8), y llamada interactiva a las funciones
  `clasificar_experimento` y `promedio_accuracy` (Ejercicio 9).
- **`errores_archivos_modulos.html`** (módulo 4) — validador
  `try/except` de accuracy con valores de ejemplo válidos e inválidos
  (Ejercicio 10), flujo animado de escritura/lectura de `historial.txt`
  (Ejercicio 11) y diagrama de `import` entre `experimentos.py` y `main.py`
  (Ejercicio 12).

Ningún módulo depende de un dataset externo ni de un intérprete de Python real:
todo el comportamiento se simula con JavaScript embebido directamente en cada
HTML, reproduciendo fielmente el resultado esperado de cada ejercicio. Cada
módulo tiene un enlace «← Recurso interactivo Semana 1» de vuelta a
`index.html`.

## Cómo previsualizar

Abrir `index.html` directamente en el navegador (doble clic) y navegar desde
ahí, o abrir cualquier módulo suelto. No requiere servidor ni build step.

## Stack

HTML + CSS + JS vanilla, sin build step. D3.js (visualización) vía CDN en los
módulos 1 y 3.
