# Ejercicios — Fundamentos de Python para Ciencia de Datos
### Versión ESTUDIANTE
### Basado en la sesión "Python para principiantes aplicado a Ciencia de Datos"

**Instrucciones generales:**
- Resuelve cada ejercicio en una celda de Jupyter Notebook.
- Antes de cada bloque de ejercicios de la Parte 2, ejecuta primero el bloque de **preparación del dataset** (más abajo) — todos los ejercicios de esa parte dependen de él.
- Donde veas `# TU CÓDIGO AQUÍ`, reemplázalo por tu solución.
- No borres los `print()` sugeridos: te ayudan a verificar tu propio resultado.

---

## Parte 1 — Fundamentos de Python

### Ejercicio 1.1 — Variables y tipos de datos
Declara una variable `x` con el valor `3`, imprime su valor y su tipo de dato. Después declara una variable `nombre_curso` con un texto (por ejemplo el nombre de este curso) y muestra su tipo.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 1.2 — Operaciones aritméticas
Con `a = 15` y `b = 4`, calcula e imprime: suma, resta, multiplicación, división, potencia, división entera y módulo.

```python
a = 15
b = 4

# TU CÓDIGO AQUÍ
```

### Ejercicio 1.3 — Listas
Dada la lista `casos = [120, 45, 300, 15, 210]`, obtén e imprime:
- el primer elemento
- el último elemento (sin usar el número de posición directamente)
- la longitud de la lista
- la suma total
- el valor mínimo y el máximo

Después agrega el valor `500` al final de la lista y ordénala de mayor a menor.

```python
casos = [120, 45, 300, 15, 210]

# TU CÓDIGO AQUÍ
```

**Pregunta de reflexión:** si la lista tiene 6 elementos después del `append`, ¿qué pasaría si intentas acceder a `casos[6]`? ¿Por qué?

### Ejercicio 1.4 — Diccionarios
Crea un diccionario que relacione el código de 3 países (por ejemplo `"MX"`, `"CO"`, `"US"`) con su nombre completo. Consulta el valor de uno de ellos e imprime también todas las claves y todos los valores del diccionario.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 1.5 — Funciones y control de flujo
Escribe una función `clasificar_riesgo(casos)` que reciba un número de casos confirmados y regrese:
- `"bajo"` si es menor a 100
- `"medio"` si está entre 100 y 300 (inclusive)
- `"alto"` si es mayor a 300

Prueba tu función con los valores `50`, `150` y `400`.

```python
def clasificar_riesgo(casos):
    # TU CÓDIGO AQUÍ
    pass
```

### Ejercicio 1.6 — Comparaciones booleanas
Con `x = 7`, evalúa e imprime si `x` es igual a 5, distinto de 5, mayor a 5, y si cumple al mismo tiempo `x > 5` y `x < 10`.

```python
x = 7

# TU CÓDIGO AQUÍ
```

### Ejercicio 1.7 — Importar módulos
Importa la librería `random` y usa la función `randint` para generar un número entero aleatorio entre 1 y 100. Después importa `pandas` y `numpy` con sus alias estándar (`pd` y `np`).

```python
# TU CÓDIGO AQUÍ
```

---

## Parte 2 — Pandas aplicado a un dataset tipo COVID-19

### Preparación del dataset (ejecutar antes de la Parte 2)

**Paso 1.** Descarga el archivo `covid_19_data.csv` (te lo compartió tu profesor) y colócalo **en la misma carpeta** donde vas a guardar tu notebook de Jupyter. Así podrás leerlo solo por su nombre, sin escribir la ruta completa de tu computadora.

El archivo tiene la misma estructura que el dataset original de Johns Hopkins usado en el video:
`SNo`, `ObservationDate`, `Province/State`, `Country/Region`, `Last Update`, `Confirmed`, `Deaths`, `Recovered`. Incluye 5 países (`Mainland China`, `US`, `Australia`, `Mexico`, `France`), algunos con detalle de provincia/estado y otros solo a nivel país, con fechas del `2020-01-22` al `2020-04-20`.

**Paso 2.** Léelo indicando cuáles columnas son de tipo fecha.

```python
import pandas as pd

data = pd.read_csv("covid_19_data.csv", parse_dates=["ObservationDate", "Last Update"])
```

### Ejercicio 2.1 — Exploración inicial
Muestra los primeros 5 registros, los últimos 5, y la forma general (filas, columnas) del DataFrame `data`.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.2 — Información y tipos de dato
Usa el método adecuado para revisar el tipo de dato de cada columna. Confirma que `ObservationDate` está registrada como fecha (`datetime`) y no como texto.

```python
# TU CÓDIGO AQUÍ
```
**Pregunta de reflexión:** si `ObservationDate` apareciera como `object` (texto), ¿qué parámetro de `pd.read_csv` usarías para corregirlo?

### Ejercicio 2.3 — Estadísticas básicas
Obtén estadísticas descriptivas generales del DataFrame (conteo, media, min, max, percentiles).

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.4 — Valores únicos
Obtén la lista de países distintos presentes en el dataset.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.5 — Filtrado de filas
Crea un DataFrame llamado `mexico` que contenga únicamente los registros de México. Verifica con el método de valores únicos que el filtro funcionó correctamente.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.6 — Última fecha disponible
Imprime cuál es la última fecha de observación registrada en el dataset (equivalente a "hasta cuándo está actualizado el archivo").

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.7 — Agrupar y agregar (`groupby`)
Obtén, para cada país, el número máximo de casos confirmados registrado en un solo día. Guarda el resultado en una variable llamada `casos_max_pais` y asegúrate de que quede como un DataFrame "plano" (sin el país como índice).

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.8 — Ordenar resultados
Ordena el resultado del ejercicio anterior de mayor a menor número de casos confirmados.

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.9 — Visualización de barras
Usando `plotly.express`, genera una gráfica de barras con el top de países por casos confirmados máximos (usa el resultado del ejercicio 2.8).

```python
import plotly.express as px

# TU CÓDIGO AQUÍ
```

### Ejercicio 2.10 — Serie de tiempo
Grafica (gráfica de línea) cómo evolucionaron los casos confirmados en México a lo largo del tiempo (usa el DataFrame `mexico` del ejercicio 2.5).

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.11 — Tabla dinámica (`pivot_table`)
Construye una tabla que sume el total de confirmados, muertes y recuperados agrupando por país y provincia/estado.

```python
# TU CÓDIGO AQUÍ
```

**Reto adicional:** a partir de la tabla anterior, filtra para ver solo los datos de `"Mainland China"` (pista: investiga el método `.loc`).

```python
# TU CÓDIGO AQUÍ
```

### Ejercicio 2.12 — Muertes totales por fecha
Calcula y grafica el total de muertes (sumando todos los países) por fecha de observación.

```python
# TU CÓDIGO AQUÍ
```

---

## Parte 3 — Reto integrador (opcional)

Usando el mismo dataset:
1. Filtra únicamente los registros de `"US"`.
2. Calcula, para cada mes, el promedio de recuperados acumulados (pista: usa `.dt.month` sobre la columna de fecha para crear una columna nueva llamada `mes`).
3. Ordena el resultado de mayor a menor promedio.
4. Grafica el resultado como gráfica de barras.

```python
# TU CÓDIGO AQUÍ
```

**Pregunta de cierre:** ¿qué tipo de análisis (descriptivo, predictivo o prescriptivo) corresponde a todo lo que hicimos en este ejercicio? ¿Qué haría falta para llevarlo al siguiente nivel de análisis?
