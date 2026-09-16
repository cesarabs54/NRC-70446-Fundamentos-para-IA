# **Anexo:** Fundamentos para IA

### ***Anexo.***

**Descripción:** sigan las instrucciones de la actividad:

1. ### ***Dataset*****:**

  Para esta práctica, pueden utilizar uno de los siguientes conjuntos de datos:

  - Boston Housing dataset:  [BostonHousing.csv](BostonHousing.csv)  
  [https://www.kaggle.com/datasets/arunjangir245/boston-housing-dataset](https://www.kaggle.com/datasets/arunjangir245/boston-housing-dataset)

  - Students Performance: [StudentsPerformance.csv](StudentsPerformance.csv)    
  [https://www.kaggle.com/datasets/spscientist/students-performance-in-exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)

  - Netflix TV Shows and Movies: ([credits.csv](credits.csv) y [titles.csv](titles.csv))  
  [https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies](https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies)

2. ## **Productos a entregar:**

  * Portafolio (Presentación) con secciones y evidencias (tablas, gráficas, interpretación).

  * *Notebook* ([**Google Colab**](https://colab.research.google.com/), [**Jupyter**](https://jupyter.org/) o [**Anaconda**](https://www.anaconda.com/download)) con el procedimiento reproducible (código + salidas).

3. ## **Pasos sugeridos para la entrega final:**

Paso 1. Cargar el *dataset* (CSV) en Python

  * Importar librerías
  * Leer archivo
  * Comprender el *dataset*

Paso 2. Contexto y planteamiento del problema (obligatorio)

  Redacten:
  * ¿Qué representa el *dataset*?
  * ¿Cuál es el problema que quieren responder con inferencia?
  * Planteen una pregunta investigable y dos hipótesis (H0 y H1).

Ejemplos de preguntas válidas

  * ¿Existe diferencia significativa en el puntaje/variable X entre grupos A y B?
  * ¿La variable X se relaciona con Y (correlación)?
  * ¿El promedio de X es diferente a un valor objetivo?

Paso 3. Identificación de variables y tipo de variable seleccionen mínimo:

  * 1 variable dependiente (preferiblemente numérica).
  * 1 variable independiente (categórica con 2+ grupos o numérica si es correlación).

Paso 4. Descripción y tamaño de muestra

  Incluyan:

  * Número total de registros (n)
  * Si hay grupos: tamaño por grupo (n1, n2, n3…)
  * Criterio de inclusión/exclusión (si filtraron datos) Paso 5\. Estadística descriptiva y visualización

Paso 5. Estadística descriptiva y visualización

  Para las variables elegidas:

  * Medidas descriptivas (media, mediana, desviación, min/max, cuartiles)
  * Visualizaciones mínimas:
    * Histograma o densidad para la variable numérica
    * Boxplot/violin por grupo (si hay grupos)
    * Scatter si analizan relación numérica-numérica

Paso 6. Validación de supuestos (inferencial)

  A. Normalidad (obligatorio)
    
  Evaluar normalidad de la variable dependiente:

  * Por muestra completa o por grupo (si hay grupos)

  Interpretación esperada

  * Si p-value < 0.05: evidencia contra normalidad
  * Si p-value ≥ 0.05: no se rechaza normalidad (con cautela)

Paso 7. Selección del análisis inferencial (según el caso)

  El equipo debe justificar qué prueba usar según:

  * Tipo de variables
  * Normalidad
  * Homogeneidad de varianzas
  * Tamaño de muestra

Paso 8. Resultados e interpretación para el problema planteado

Incluyan:

  * Resultado de la prueba (estadístico, p-value)
  * Decisión sobre H0

Paso 9. Conclusiones del portafolio

Responder:

  * ¿Qué aprendieron sobre supuestos?
  * ¿Qué limitaciones tuvo el *dataset*?
  * ¿Qué análisis adicional harían si tuvieran más datos?