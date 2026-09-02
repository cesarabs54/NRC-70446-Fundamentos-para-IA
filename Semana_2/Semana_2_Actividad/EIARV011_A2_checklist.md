# Checklist de evaluación — EIARV011_A2 (Estudio de caso: Consulta en un Dataset)

Estudiante(s): ______________________________  Fecha de revisión: __________

## 1. Entrega (requisito de admisibilidad — si falla, no se califica)

- [ ] Se entregó un único archivo PDF con el desarrollo del taller.
- [ ] Se adjuntó el enlace público del notebook (Colab o Jupyter) con permisos de visualización habilitados (verificar que el enlace abre sin solicitar acceso).
- [ ] No hay indicios de plagio total ni de que se haya entregado una actividad distinta a la solicitada.

## 2. Formato del documento

- [ ] Tipo de letra Arial, tamaño 11.
- [ ] Interlineado 1.5.

## 3. Estructura del estudio de caso

- [ ] **Objeto de estudio**: identifica y describe el problema/situación relacionado con usar Python para leer y analizar un CSV, con foco en columnas/variables.
- [ ] **Actores y contextos**: describe actores involucrados y el entorno tecnológico (Python, librerías de ciencia de datos usadas).
- [ ] **Objetivos**: define objetivos claros (procesar datos con Python, explorar/analizar columnas, interpretar resultados).
- [ ] **Informe final**: desarrolla los tres puntos pedidos (comprensión de variables, diagnóstico de calidad, análisis por variable) — ver secciones 5-7.

## 4. Contenido técnico mínimo en el notebook

- [ ] Importación de librerías (pandas y afines).
- [ ] Lectura del CSV (`StudentsPerformance.csv`).
- [ ] Visualización inicial del dataset (ej. `head()`).
- [ ] El notebook corre sin errores de principio a fin.

## 5. Comprensión de variables (columnas)

- [ ] Tamaño del dataset: número de filas y columnas.
- [ ] Nombres de todas las columnas.
- [ ] Tipos de datos de cada columna (`dtypes`).
- [ ] Resumen general (ej. `info()` / `describe()`).
- [ ] Diccionario de datos: naturaleza (numérica/categórica), formato y propósito de cada columna.

## 6. Diagnóstico de calidad de datos

- [ ] Valores nulos por columna.
- [ ] Registros duplicados (o justificación de que no aplica).
- [ ] Valores atípicos identificados en al menos 1 variable numérica.
- [ ] Para cada problema detectado, se propone una solución o tratamiento claro y argumentado.

## 7. Análisis exploratorio por variable

- [ ] Al menos 2 variables categóricas: frecuencias y porcentajes (`value_counts()`, `value_counts(normalize=True)`).
- [ ] Al menos 2 variables numéricas: media, mediana, mínimo, máximo, desviación estándar (`describe()`).
- [ ] Interpretación de los valores obtenidos (no solo tablas/salidas sin explicar).

## 8. Preguntas del informe final (anexo)

- [ ] ¿Qué fenómeno, proceso o contexto representa el dataset?
- [ ] ¿Cuáles son las 5 variables más importantes para describir el caso y por qué?
- [ ] ¿Qué hallazgos se observan en la distribución de variables (categóricas y numéricas)?
- [ ] ¿Qué relación relevante encontraron entre las variables? (mínimo 2)
- [ ] ¿Qué problemas de calidad de datos detectaron y cómo los abordan?
- [ ] Con base en lo observado: ¿qué pregunta de IA o problema predictivo podría plantearse a futuro con este dataset? (ej: clasificación, regresión, clustering)

## 9. Calificación según rúbrica (máx. 5.0)

**Presentación, organización y ortografía** (máx. 0.5)
- [ ] 0 — Plagio total / otra actividad / no entregado
- [ ] 0.1 — Páginas muy alejadas del rango; 8+ errores
- [ ] 0.2 — Páginas alejadas significativamente; 5-7 errores
- [ ] 0.3 — Páginas cercanas al rango; 1-4 errores
- [ ] 0.5 — Páginas dentro del rango; 0 errores

**Análisis del dataset** (máx. 1.5)
- [ ] 0 — Plagio total / otra actividad / no entregado
- [ ] 0.6 — Confuso o incompleto, faltan variables clave
- [ ] 0.9 — Superficial, cubre solo algunas variables/relaciones
- [ ] 1.2 — Claro, cubre la mayoría de variables/relaciones, falta profundidad en algunos puntos
- [ ] 1.5 — Completo y detallado: variables, distribución (categóricas y numéricas), relaciones, conclusiones bien fundamentadas

**Identificación de problemas de calidad de datos** (máx. 1.5)
- [ ] 0 — Plagio total / otra actividad / no entregado
- [ ] 0.6 — No identifica problemas o soluciones incorrectas/irrelevantes
- [ ] 0.9 — Identifica pocos problemas, soluciones poco claras
- [ ] 1.2 — Identifica algunos problemas, soluciones generales/mejorables
- [ ] 1.5 — Identifica y aborda varios problemas con soluciones claras y argumentadas

**Aplicación de conceptos de ciencia de datos en Python** (máx. 1.5)
- [ ] 0 — Plagio total / otra actividad / no entregado
- [ ] 0.6 — Uso inapropiado o incorrecto de Python
- [ ] 0.9 — Uso limitado, varios errores en análisis/interpretación
- [ ] 1.2 — Uso adecuado, podría profundizar más
- [ ] 1.5 — Dominio completo, análisis exploratorio adecuado, resultados bien interpretados

**Puntaje total: _____ / 5.0**

## Observaciones y retroalimentación

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
