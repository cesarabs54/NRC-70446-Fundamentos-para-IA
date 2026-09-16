# Portafolio de evidencias: Análisis inferencial de datos

Guía de referencia sobre qué debe contener el portafolio de la actividad **EIARV011_A6** (Semana 6 — Fundamentos para IA), construida a partir del enunciado de la actividad y su anexo.

---

## 1. Qué es y para qué sirve

El portafolio es el **producto principal a evaluar** de la actividad. No es un resumen ni una portada con enlaces: es la compilación estructurada y visual de todo el proceso de análisis inferencial —desde el planteamiento del problema hasta las conclusiones— construida en una herramienta digital (Genially, Wix o Google Sites) y **exportada como PDF** con todo su contenido visible.

El *notebook* (Colab, Jupyter o Anaconda) es un segundo entregable independiente: contiene el código reproducible y las salidas ejecutadas. El portafolio debe mostrar los resultados de ese notebook (tablas, gráficas, cifras), no limitarse a enlazarlo.

---

## 2. Estructura completa

### 2.1 Portada
- Título del trabajo.
- Nombre completo del estudiante (o de cada integrante, si es un equipo de trabajo).
- Nombre del curso y número de la semana.
- Nombre del docente.
- Fecha de entrega.

### 2.2 Tabla de contenido
Estructura clara y precisa de las secciones del portafolio (ver el anexo de la actividad para el formato sugerido).

### 2.3 Introducción
Debe responder, como mínimo:
- ¿Cuál es el propósito del portafolio?
- ¿Cuál es la importancia del análisis inferencial en la toma de decisiones basada en datos?
- Breve descripción del contexto del *dataset* trabajado y el problema planteado.

### 2.4 Contenido (núcleo del portafolio)

Cada uno de estos puntos debe aparecer como una sección propia, con evidencia real (no solo texto):

1. **Contexto del *dataset* y planteamiento del problema, con hipótesis (H0 y H1)**
   - ¿Qué representa el *dataset*?
   - ¿Cuál es el problema que se quiere responder con inferencia?
   - Pregunta investigable clara.
   - Hipótesis nula (H0) y alternativa (H1) formuladas explícitamente — no basta con que aparezcan sueltas dentro de un `print()` del código; deben quedar escritas en el portafolio.

2. **Identificación y clasificación de variables**
   - Variable dependiente (idealmente numérica) y variable independiente (categórica con 2+ grupos, o numérica si es un análisis de correlación).
   - Tipo de cada variable y justificación de por qué se eligió.

3. **Descripción de la muestra y tamaño de los grupos**
   - Número total de registros (n).
   - Tamaño por grupo (n1, n2, n3…) si aplica.
   - Criterios de inclusión/exclusión, si se filtraron datos (valores nulos, duplicados, etc.).

4. **Estadística descriptiva y visualización de datos**
   - Medidas descriptivas: media, mediana, desviación estándar, mínimo/máximo, cuartiles.
   - Visualizaciones mínimas, **insertadas como imágenes reales generadas por el propio análisis** (no ilustraciones genéricas):
     - Histograma o densidad de la variable numérica.
     - Boxplot o violin plot por grupo (si aplica).
     - Diagrama de dispersión si se analiza relación numérica-numérica.

5. **Evaluación de supuestos**
   - **Normalidad (obligatorio):** prueba de Shapiro-Wilk (por muestra completa y/o por grupo), con estadístico, p-value e interpretación (p < 0.05 → evidencia contra normalidad; p ≥ 0.05 → no se rechaza, con cautela).
   - **Homogeneidad de varianzas** (si aplica): prueba de Levene, con estadístico, p-value e interpretación.

6. **Selección y justificación del análisis inferencial**
   - Explicar la prueba elegida en función de: tipo de variables, resultado de normalidad, resultado de homogeneidad de varianzas y tamaño de muestra.
   - Ejemplos de decisión correcta:
     - 2 grupos, normalidad y homogeneidad cumplidas → t de Student.
     - 2 grupos, normalidad **no** cumplida → U de Mann-Whitney (recomendable reportar también t de Student o t de Welch como verificación de sensibilidad, y aclararlo así).
     - Más de 2 grupos → ANOVA (con prueba post-hoc de Tukey si el ANOVA es significativo) o Kruskal-Wallis si no se cumple normalidad.
     - Dos variables numéricas → correlación de Pearson (o Spearman si no hay normalidad).

7. **Presentación e interpretación de resultados**
   - Resultado de la prueba: estadístico y p-value.
   - Decisión sobre H0 (se rechaza / no se rechaza) con el nivel de significancia usado (α = 0.05).
   - Interpretación en función del problema planteado (qué significa el resultado en términos del contexto real del *dataset*, no solo en términos estadísticos).
   - Idealmente, complementar el p-value con una medida del tamaño del efecto (d de Cohen, correlación biserial por rangos, η², etc.) y aclarar que significancia estadística no equivale a relevancia práctica ni a causalidad (más aún si el *dataset* es observacional).

### 2.5 Conclusiones
Reflexión argumentada que responda:
- ¿Qué se aprendió sobre los supuestos estadísticos?
- ¿Qué limitaciones tuvo el *dataset*?
- ¿Qué análisis adicionales o mejoras futuras se podrían hacer con más información?

### 2.6 Referencias bibliográficas
En formato APA. Deben incluir como mínimo la fuente del *dataset* y, si se citaron, los recursos básicos/complementarios del curso. Si se usó una herramienta de IA como apoyo (redacción, estructuración de referencias, etc.), es buena práctica declararlo explícitamente y aclarar qué se validó de forma propia.

---

## 3. Requisitos de forma y de entrega

- **Coherencia visual y organizativa** en todo el portafolio (mismo estilo, orden lógico entre secciones).
- **Ortografía y redacción** cuidadas: máximo 4 errores para no perder puntos en ese criterio (0 errores = puntaje máximo).
- El archivo a subir a la plataforma debe ser **un único PDF, exportado completo desde la herramienta digital usada** (Genially, Wix o Google Sites) — no la portada con enlaces, ni un documento aparte que solo remita al portafolio.
- Adjuntar el **enlace público del notebook** (Colab o Jupyter) con permisos de visualización habilitados para "cualquier persona con el enlace".
- Verificar que el código del notebook sea reproducible y que **las salidas estén visibles** (todas las celdas ejecutadas, sin errores).
- Nombrar el archivo como: `primerapellido_primernombre_nombredelaactividad` (ej. `romero_luis_portafoliodeevidencias`).

---

## 4. Rúbrica de evaluación (resumen)

| Criterio | Insuficiente (1.9) | Regular (2.9) | Bueno (3.9) | Excelente (5) |
|---|---|---|---|---|
| **Ortografía, gramática, cohesión y coherencia** | 8+ errores, ideas inconexas, sin referencias | 5-7 errores, ambiguo, referencias sin formato APA | 1-4 errores, claro pero con imprecisiones, errores menores en APA | Sin errores, claro y fluido, referencias en APA correcto |
| **Planteamiento del problema y coherencia inferencial** | Hipótesis mal formuladas o sin relación con el análisis | Hipótesis ambiguas, inconsistencias metodológicas | Preguntas e hipótesis adecuadas, leves imprecisiones | Pregunta clara, H0/H1 bien estructuradas, alineación total problema-supuestos-prueba-conclusiones |
| **Aplicación del análisis estadístico e interpretación de resultados** | Prueba incorrecta o sin interpretación | Aplicación parcial o interpretación superficial | Pruebas correctas, justificación/interpretación con limitaciones menores | Descriptiva correcta, supuestos validados, prueba justificada, interpretación rigurosa del estadístico y el p-value |
| **Integración de visualización, análisis y reflexión crítica** | Sin integración visual/analítica ni reflexión | Visualizaciones básicas, poca articulación | Visualizaciones y análisis adecuados, reflexión general | Visualizaciones e integración plena, comprensión clara de supuestos, limitaciones y proyecciones futuras |

*(Puntajes máximos por criterio: 0.5 / 1.5 / 1.5 / 1.5 → total 5.0)*

---

## 5. Errores frecuentes a evitar

Con base en la revisión de entregas reales de esta actividad, estos son los problemas que más bajan la nota y son fáciles de prevenir:

1. **Subir solo la portada con enlaces en el PDF**, dejando el desarrollo real únicamente en Genially/Sites/Colab. El PDF entregado a la plataforma debe ser la exportación *completa* del portafolio.
2. **No editar la plantilla del portafolio.** Elegir una plantilla de Genially/Wix y dejar el texto de ejemplo ("Lorem ipsum...", "Escribe un título aquí...") sin reemplazar. Es el error más grave y frecuente: el portafolio debe revisarse página por página antes de compartir el enlace.
3. **Enlace de Colab sin permisos o roto.** Confirmar que el enlace configurado como "Cualquier persona con el enlace puede ver" abre correctamente desde una ventana distinta (idealmente de incógnito) antes de entregarlo.
4. **No formular H0/H1 de forma explícita** en el portafolio (aparecen solo dentro del código, no como texto redactado).
5. **Elegir la prueba equivocada:** aplicar t de Student o ANOVA sin haber comprobado realmente normalidad y homogeneidad de varianzas, o ignorar el resultado de esas pruebas cuando contradice la prueba elegida.
6. **Mostrar solo texto, sin las gráficas reales** generadas por el propio análisis (o usar imágenes genéricas/ilustrativas en su lugar).
7. **Entregar el desarrollo de otra actividad** (por ejemplo, el taller de librerías de Python) en vez del análisis inferencial pedido esta semana.
8. **No incluir referencias**, o incluir una lista de referencias que no corresponde al trabajo entregado (copiada de otra entrega o plantilla).

---

## 6. Bibliografía recomendada

Referencias en español, de editoriales colombianas y españolas, que fortalecen el desarrollo de la actividad y son citables en formato APA dentro del portafolio.

**Estadística inferencial y prueba de hipótesis**

- González García, L. M., y Jiménez, J. A. (2025). *Inferencia estadística*. Editorial Universidad Nacional de Colombia. https://portaldelibros.unal.edu.co/gpd-inferencia-estadyustica-9789585057685-68a8cc712975c.html
- Díaz, M. (2019). *Estadística inferencial aplicada* (2.ª ed.). Editorial Universidad del Norte. https://editorial.uninorte.edu.co/gpd-estadistica-inferencial-aplicada-2-edicion-9789587893526.html

**Python para análisis de datos**

- McKinney, W. (2022). *Python para análisis de datos* (3.ª ed.). Anaya Multimedia. https://anayamultimedia.es/libro/titulos-especiales/python-para-analisis-de-datos-wes-mckinney-9788441546837/
- Toro López, F. J. (2022). *Ciencia de los datos con Python*. Ecoe Ediciones. https://www.ecoeediciones.com/wp-content/uploads/2022/05/Ciencia-de-los-datos-con-python-1ra-edicion-contenido.pdf

**Visualización de datos**

- Nussbaumer Knaflic, C. (2018). *Storytelling con datos: Visualización de datos para profesionales*. Anaya Multimedia. https://www.casadellibro.com.co/libro-storytelling-con-datos-visualizacion-de-datos-para-profesionales/9788441539303/5897321

**Big Data / análisis con Python (complementaria)**

- *Big Data: Análisis de datos con Python*. Editorial Garceta. https://www.garceta.es/catalogo/libro.php?ISBN=978-84-1622-883-6

---

## 7. Fuentes

- Enunciado de la actividad: `EIARV011_A6.md`
- Anexo con los pasos sugeridos: `EIARV011_A6_Anexo.md`
