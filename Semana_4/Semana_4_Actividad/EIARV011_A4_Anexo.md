
***Anexo.*** 

**Fundamentos para IA**

**Descripción:** Sigan las instrucciones de la actividad: 

**1) Reconocimiento de *frameworks* de IA en Python (conceptual)**

    En el documento, incluyan un apartado corto (máximo 15 líneas) donde expliquen:
    ● ¿Qué es un *framework* y qué es una librería?
    ● Mencionar al menos 4 *frameworks*/librerías comunes en IA (ej.: Scikit-learn, TensorFlow, PyTorch, Hugging Face).
    ● ¿Para qué tipo de tareas se usan? (clasificación, regresión, visión, NLP, *clustering*, etc.) 

**2) Selección y carga del *dataset*** 

    Usen el *dataset* de: Netflix TV *Shows and Movies*
    https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies
    
    Deben cargarlo con Pandas y mostrar: [**archivo**](credits.csv)
    
    ● head(), shape, info()
    ● selección de 2 variables numéricas y 1 categórica (si existe)
    ● Corregir nombres de columnas, formatos (por ejemplo, números como texto) ● Decidir qué hacer con las variables: eliminar, imputar, o dejar “pendiente”
    ● Convertir a `float/int`, manejar nulos para cálculos (`dropna` o imputación simple)
    ● Tratar outliers sólo si afectan las visualizaciones o estadísticas 

**3) Implementación con NumPy (cálculo y transformación)** 

    En el documento deben demostrar al menos 4 acciones usando NumPy con variables numéricas del *dataset*, por ejemplo:
    ● Convertir columna a arreglo np.array 
    ● Estadísticos: media, mediana, percentiles 
    ● Operaciones vectorizadas (sin ciclos) 

**4) Implementación con SciPy (análisis / estadística)** 

    Aplicar mínimo 2 procedimientos con SciPy: 

    ● Opciones sugeridas (escojan 2):     
    ● correlación (Pearson/Spearman)     
    ● prueba de normalidad (Shapiro u otra)     
    ● t-*test* o comparación de medias (si tiene grupos)     
    ● z-*score* para detección de atípicos     
    ● algún ajuste simple (si aplica) 

**5) Visualización con Matplotlib (mínimo 3 gráficas)** 

    ● El taller debe incluir 3 gráficos diferentes hechos con Matplotlib, por ejemplo: histograma de una variable numérica, *scatter* entre dos numéricas, *boxplot* por categoría (si existe). 

**6) Visualización con Seaborn (mínimo 3 gráficas)** 

    Repetir el análisis visual con Seaborn (mínimo 3), comparando la facilidad/ventajas: *histplot* o *displot*, *scatterplot* o *lmplot*, *boxplot* / *violinplot*, *heatmap* de correlación. 

**7) Pensamiento crítico** 

    Con lo anterior respondan: 
    
    ● ¿Cuándo conviene usar Matplotlib y cuándo Seaborn? (ejemplo concreto del taller) ● ¿Qué ventajas aporta NumPy frente a trabajar solo con Pandas? ● ¿Qué aportó SciPy que no era tan directo con NumPy/Pandas?
    ● Si el objetivo fuera construir un modelo IA (predicción), ¿qué herramienta sumarían y por qué? (ej: scikit-learn, TensorFlow, etc.)
    ● ¿Qué limitaciones detectaron en su *dataset* para aplicar análisis estadístico o visual? 
