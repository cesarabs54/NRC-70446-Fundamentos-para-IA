
# **Anexo**

Fundamentos para IA

***Anexo.*** **Consulta en un *Dataset***

**Descripción:** Descarguen el archivo y sigan las instrucciones de la actividad:

1. ## **Descarguen del archivo:**

   1. Descarguen el archivo de *Students Performance* accediendo al siguiente enlace:  
      [https://www.kaggle.com/datasets/spscientist/students-performance-in-exam](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) [s](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)  
   2. Hagan clic en "Descargar" para obtener el archivo CSV en sus dispositivos.

   3. Carguen en el *notebook*, y muestren: Importación de librerías, lectura del CSV, visualización inicial

2. **Comprensión de variables (columnas).** El equipo debe caracterizar el *dataset*:

   1. Tamaño: filas y columnas

   2. Nombres de columnas

   3. Tipos de datos

   4. Resumen general

3. **Calidad de datos:** Analicen:

   1. Valores nulos por columna

   2. Duplicados (si aplica)

   3. Valores atípicos (al menos en 1 variable numérica)

4. ## **Análisis exploratorio inicial:**

   1. Variables categóricas (mínimo 2): Frecuencias y porcentajes por ejemplo:  
      df\["columna\_cat"\].value\_counts() df\["columna\_cat"\].value\_counts(normalize=True) \* 100

   2. Variables numéricas (mínimo 2\) : Medidas: media, mediana, min, max, desviación, por ejemplo: df\["columna\_num"\].describe()

5. ## **Preguntas para el informe final:**

A continuación, se presentan las preguntas que guiarán el desarrollo del informe final. Deberá basarse en ellas para realizar un análisis completo del *dataset*:

   1. ¿Qué fenómeno, proceso o contexto representa el *dataset*?
   2. ¿Cuáles son las 5 variables más importantes para describir el caso y por qué?  
   3. ¿Qué hallazgos se observan en la distribución de variables (categóricas y numéricas)?
   4. ¿Qué relación relevante encontraron entre las variables? (mínimo 2)

   Preguntas para complementar el análisis:
   1. ¿Qué problemas de calidad de datos detectaron y cómo los abordan?
   2. Con base en lo observado: ¿qué pregunta de IA o problema predictivo podría plantearse a futuro con este *dataset*? (ej: clasificación, regresión, *clustering*)

6. ## **Recuerden que el informe debe cumplir con los siguientes lineamientos:**

* Presenten la información de manera clara, organizada, cuidando la redacción y ortografía.