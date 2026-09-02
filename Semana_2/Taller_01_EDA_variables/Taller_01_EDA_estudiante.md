# Taller — Análisis exploratorio de variables categóricas y numéricas

### Dataset: `StudentsPerformance.csv`

**Instrucciones generales:**
- Trabaja en un notebook de Jupyter (Colab o local).
- Copia el archivo `StudentsPerformance.csv` en la misma carpeta que tu notebook.
- Donde veas `# TU CÓDIGO AQUÍ`, reemplázalo por tu solución.
- Responde las preguntas de reflexión en una celda de texto (Markdown), no como comentario de código.
- Duración estimada: 45-60 minutos.

---

## Paso 0 — Preparación

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("StudentsPerformance.csv")
df.head()
```

---

## Parte 1 — Variables categóricas

### Ejercicio 1.1 — Frecuencias absolutas y relativas
Para la columna `gender`, obtén:
- El conteo de valores por categoría.
- El porcentaje que representa cada categoría sobre el total.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 1.2 — Segunda variable categórica
Repite el ejercicio 1.1 pero con la columna `test preparation course`.

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de reflexión 1:** ¿El dataset está balanceado en `gender`? ¿Y en `test preparation course`? ¿Por qué podría importar esto si más adelante quisieras comparar el desempeño entre grupos?

### Ejercicio 1.3 — Visualización comparativa
Crea una figura con **dos gráficos de barras lado a lado** (uno para `gender` y otro para `test preparation course`), usando `plt.subplots`.

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# TU CÓDIGO AQUÍ

plt.tight_layout()
plt.show()
```

---

## Parte 2 — Variables numéricas

### Ejercicio 2.1 — Estadísticas descriptivas
Obtén el resumen estadístico (`count`, `mean`, `std`, `min`, cuartiles, `max`) de la columna `math score`.

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de reflexión 2:** Compara el valor de `mean` con el de `50%` (mediana). ¿Son parecidos o muy distintos? ¿Qué te sugiere eso sobre la forma de la distribución?

### Ejercicio 2.2 — Histogramas
Genera un histograma para cada una de las tres variables numéricas (`math score`, `reading score`, `writing score`) en una sola figura, con 15 intervalos (`bins`).

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de reflexión 3:** Observando los histogramas, ¿la forma se parece a una "campana" (distribución normal)? ¿Hay alguna variable con una cola más larga hacia un lado (asimetría)?

### Ejercicio 2.3 — Comparación de las tres variables
Usa `df.describe()` (sin seleccionar una sola columna) para comparar `mean`, `std`, `min` y `max` de las tres materias al mismo tiempo.

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de reflexión 4:** ¿Cuál de las tres materias tiene mayor dispersión (`std`)? ¿Cuál tiene el rango más amplio entre `min` y `max`?

---

## Parte 3 — Reto integrador (opcional)

Elige **una variable categórica** (por ejemplo `lunch` o `parental level of education`) y **una variable numérica** (por ejemplo `math score`). Usa `groupby` para calcular el promedio de la variable numérica según cada categoría.

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de cierre:** ¿Se observan diferencias notables en el promedio entre categorías? ¿Qué hipótesis plantearías para explicar esa diferencia (o su ausencia)?
