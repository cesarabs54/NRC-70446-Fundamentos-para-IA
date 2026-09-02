# Fundamentos de Python para Ciencia de Datos e IA
### Docente: Cesar Alfonso Bolado Silva
### Notas de clase — Especialización en Inteligencia Artificial / Curso: Fundamentos para IA
### Basado en el video sesión "Python para principiantes aplicado a Ciencia de Datos"

---

## 1. Contexto: ¿dónde vive Python en un proyecto de datos?

### 1.1 Ciencia de datos ≈ intersección de tres campos
La ciencia de datos se suele representar como la intersección de:
- **Estadística y matemáticas**
- **Ciencias computacionales / tecnología**
- **Conocimiento de dominio (negocio)**

Sin conocimiento de negocio, un análisis técnicamente correcto puede no generar impacto. Sin la parte matemática/computacional, el conocimiento de negocio no se puede escalar ni automatizar.

### 1.2 Roles típicos en un equipo de datos (mundo ideal)
| Rol | Programación | Visualización/Comunicación | Manejo de datos | Estadística | Machine Learning | Ingeniería de software | Álgebra lineal/Cálculo |
|---|---|---|---|---|---|---|---|
| Analista de datos | Alta | Alta | Media | Media | Baja | Baja | Baja |
| Científico de datos | Alta | Alta | Alta | Alta | Alta | Media | Media |
| Ingeniero de datos | Alta | Baja | Alta | Baja | Media | Alta | Baja |
| Ingeniero de ML | Alta | Baja | Media | Media | Alta | Alta | Alta |

**Punto para discusión en clase:** estas responsabilidades varían mucho entre empresas; en equipos pequeños una sola persona cubre varios roles.

### 1.3 ¿Por qué Python?
- Es, junto con SQL, una de las combinaciones de herramientas más usadas en la industria de datos hoy en día.
- Alternativa relevante: **R** (muy fuerte en estadística), pero Python tiene comunidad más grande → más soporte, más librerías, más respuestas a problemas comunes.
- Python es de propósito general: sirve para análisis de datos, backend, automatización, scripting, IA, etc.

### 1.4 Proceso típico de un proyecto de analítica de datos
1. **Entender el contexto / problema de negocio** (si esto falla, todo lo demás falla).
2. **Entender qué datos existen** y en qué formato.
3. **Preparar los datos** (limpieza, transformación) — consume la mayor parte del tiempo del proyecto.
4. **Explorar los datos** (EDA).
5. **Modelar / generar conclusiones** → llevar a producción o a una decisión.

### 1.5 Tres tipos de análisis (son incrementales, no alternativos)
1. **Descriptivo** → *¿qué pasó / qué está pasando?* (estadísticas, dashboards).
2. **Predictivo** → *¿qué va a pasar?* (regresión, clasificación, series de tiempo).
3. **Prescriptivo** → *¿qué debería hacer al respecto?* (requiere haber resuelto 1 y 2 primero).

> Ejemplo de clase: dashboards de COVID-19 (descriptivo) → modelos que proyectan curva de contagios (predictivo) → decisiones de confinamiento basadas en datos, caso Corea del Sur (prescriptivo).

---

## 2. Fundamentos del lenguaje Python

### 2.1 Variables y tipos de datos básicos
```python
x = 3
print(x)        # muestra el valor
type(x)         # muestra el tipo de dato -> int
help(x)         # documentación sobre el objeto/función
```
Tipos básicos: enteros (`int`), decimales (`float`), texto (`str`), booleanos (`bool`), listas (`list`), diccionarios (`dict`).

### 2.2 Operaciones aritméticas
Python funciona como una calculadora: suma `+`, resta `-`, multiplicación `*`, división `/`, potencia `**`, división entera `//`, módulo `%`.

### 2.3 Listas
```python
l = [2, 1, 8, 3]
l[0]        # primer elemento -> 2  (indexado desde 0)
l[-1]       # último elemento -> 3
len(l)      # número de elementos
sum(l)      # suma de elementos
min(l)      # elemento menor
max(l)      # elemento mayor
l.append(10)   # agrega un elemento al final
l.sort()       # ordena ascendente (por default)
l.sort(reverse=True)  # ordena descendente
```
**Punto clave para remarcar:** las listas están indexadas desde 0. Si una lista tiene 4 elementos, el último es `l[3]`, no `l[4]` (`l[4]` produce `IndexError`).

### 2.4 Diccionarios
Estructura de clave-valor: en vez de acceder por posición numérica, se accede por una "clave" (key).
```python
paises = {"CA": "Canadá", "MX": "México"}
paises["CA"]     # -> "Canadá"
```

### 2.5 Comparaciones booleanas
```python
x == 5   # ¿es igual?
x != 5   # ¿es distinto?
x > 5, x < 5, x >= 5, x <= 5
```
Se pueden concatenar condiciones con `and` / `or` para verificar varias condiciones al mismo tiempo (útil en estructuras `if`).

### 2.6 Control de flujo
`if / elif / else`, `for`, `while` — guían el flujo de ejecución del programa según condiciones.

### 2.7 Funciones
```python
def sumar(a, b):
    return a + b
```
Se define con `def`, nombre, parámetros entre paréntesis, y opcionalmente un `return` para regresar un resultado.

### 2.8 Módulos e importación
Python permite reutilizar código que otras personas ya escribieron (librerías/módulos), en vez de reescribir todo desde cero.
```python
import pandas as pd          # importar librería completa con un alias
from random import randint   # importar una función específica de un módulo
```
Usar un **alias** (`as pd`, `as np`) es una convención muy común: evita escribir el nombre completo de la librería cada vez que se llama un método.

### 2.9 Manejo de archivos
Python puede leer/escribir/editar archivos (`.txt`, `.csv`, etc.) de forma nativa, pero en ciencia de datos casi siempre se delega esto a **pandas**, que simplifica muchísimo la lectura de datos tabulares.

---

## 3. Librerías clave para ciencia de datos e IA

| Librería | Para qué se usa |
|---|---|
| **pandas** | Lectura, exploración, limpieza y transformación de datos tabulares (la librería más usada en la práctica diaria) |
| **NumPy** | Operaciones numéricas y con matrices/arreglos de forma eficiente |
| **Matplotlib / Seaborn** | Visualización de datos (gráficas estáticas) |
| **Plotly Express** | Visualización interactiva (gráficas con hover, zoom, etc.) |
| **scikit-learn** | Modelos de machine learning |
| **BeautifulSoup / Scrapy** | Web scraping (extraer información de páginas web) |

**Idea pedagógica central:** pandas busca *tabular* la información sin importar de dónde venga (CSV, Excel, JSON, HTML, bases de datos, APIs). Una vez tabulada, se manipula siempre de forma parecida.

---

## 4. Pandas en la práctica: el DataFrame

Un **DataFrame** es la estructura central de pandas: se puede pensar como una hoja de Excel dentro de Python (filas = registros, columnas = variables).

### 4.1 Leer datos
```python
data = pd.read_csv("covid_data.csv")
```
Otros formatos: `pd.read_excel()`, `pd.read_json()`, `pd.read_html()`, conexión a bases de datos con `pd.read_sql()`.

### 4.2 Exploración inicial
```python
data.head()      # primeros 5 registros (o head(n) para los primeros n)
data.tail()      # últimos 5 registros
data.shape       # (número de filas, número de columnas)
data.info()      # tipo de dato por columna, nulos, memoria usada
data.describe()  # estadísticas básicas (media, min, max, percentiles...)
```

### 4.3 Tipos de dato y fechas
Por default, pandas lee las columnas de fecha como texto (`object`). Para poder ordenar/filtrar por fecha, hay que indicarle explícitamente cuáles columnas son fechas:
```python
data = pd.read_csv("covid_data.csv", parse_dates=["ObservationDate", "Last Update"])
data.info()   # ahora esas columnas aparecen como datetime64
```
**Por qué importa:** solo se pueden hacer operaciones temporales (ordenar cronológicamente, filtrar por rango de fechas, graficar series de tiempo) si el tipo de dato es `datetime`, no texto.

### 4.4 Selección de columnas y valores únicos
```python
data["Country/Region"]              # selecciona una columna (Serie de pandas)
data["Country/Region"].unique()     # lista de valores distintos en esa columna
```
Útil para: explorar categorías disponibles, y verificar que un filtro funcionó correctamente.

### 4.5 Filtrado de filas
```python
china = data[data["Country/Region"] == "Mainland China"]
mexico = data[data["Country/Region"] == "Mexico"]
```
**Buena práctica de exploración:** después de filtrar, verificar con `.unique()` que solo quedó lo esperado, y revisar con `.head()`/`.tail()` el resultado. También conviene explorar qué tan granular es el dato (por ejemplo, algunos países reportan por provincia/estado y otros no) antes de decidir a qué nivel se puede hacer el análisis.

### 4.6 Agrupar y agregar (`groupby`)
```python
data.groupby("Country/Region")["Confirmed"].max()
```
Esto responde: *"para cada país, ¿cuál fue el número máximo de confirmados registrado en un solo día?"*. Otras funciones de agregación: `.sum()`, `.min()`, `.mean()`, `.count()`.

`groupby` cambia la estructura de índices del resultado; `.reset_index()` regresa el resultado a un DataFrame "plano", fácil de seguir usando con la notación habitual.
```python
casos_pais = data.groupby("Country/Region")["Confirmed"].max().reset_index()
```

### 4.7 Ordenar (`sort_values`)
```python
casos_pais.sort_values("Confirmed", ascending=False)   # de mayor a menor
casos_pais.sort_values("Confirmed", ascending=True)    # de menor a mayor (default)
```

### 4.8 Tablas dinámicas (`pivot_table`)
```python
resumen = data.pivot_table(
    index=["Country/Region", "Province/State"],
    aggfunc="sum"
)
```
El **índice** (index) es la estructura que pandas usa para localizar información eficientemente (no hay que recorrer fila por fila). `pivot_table` permite reorganizar y agregar datos según distintos niveles (país, provincia, fecha, etc.) según lo que necesite el análisis.

Para filtrar dentro de un índice de varios niveles (MultiIndex), se usa `.loc`:
```python
resumen.loc["Mexico"]
```

---

## 5. Visualización con Plotly Express

```python
import plotly.express as px

fig = px.bar(
    casos_pais.sort_values("Confirmed", ascending=False).iloc[:20],
    x="Country/Region", y="Confirmed",
    title="Casos confirmados por país (Top 20)"
)
fig.show()
```
```python
fig = px.line(
    data[data["Country/Region"] == "US"],
    x="ObservationDate", y="Confirmed",
    hover_data=["Province/State"],
    title="Evolución de casos confirmados en EE.UU."
)
fig.show()
```
**Idea para remarcar en clase:** la visualización es "la cereza del pastel". El mejor análisis pierde valor si no se comunica de forma clara y convincente. Plotly Express agrega interactividad (hover, zoom) casi gratis en comparación con matplotlib estático.

---

## 6. Errores comunes / buenas prácticas a reforzar en clase

1. **Indexado desde 0**: fuente típica de errores para quien viene de otros lenguajes o de matemáticas puras.
2. **No asumir que los datos son correctos**: si algo se ve raro (ej. el número de muertes acumuladas *baja* de un día a otro), no saltar a la conclusión de "el dato está mal": investigar primero.
3. **Explorar antes de transformar**: usar `.info()`, `.describe()`, `.unique()` antes de filtrar/agrupar, para saber qué nivel de detalle realmente permiten los datos.
4. **Guardar resultados intermedios en variables**: si no se asigna el resultado de una operación a una variable, no se puede reutilizar después (ej. `pivot = data.pivot_table(...)` en vez de solo ejecutar la instrucción sin capturarla).
5. **Fechas como texto vs. `datetime`**: revisar siempre `data.info()` después de leer un archivo para confirmar el tipo de cada columna.
6. **Jupyter Notebook**: se ejecuta por celdas (no todo el script de una sola vez), lo que facilita explorar datos de forma iterativa; el número entre corchetes `[ ]` indica el orden de ejecución de esa celda dentro de la sesión.

---

## 7. Conexión con las siguientes semanas del curso

- Este contenido corresponde principalmente a la **Semana 1** (fundamentos de Python) y sienta las bases de la **Semana 2** (Python para ciencia de datos con pandas).
- NumPy y SciPy (cálculo numérico) se profundizan en la **Semana 4**.
- Matplotlib y Seaborn (visualización estática) se profundizan en la **Semana 4-5**.
- El proceso de "análisis predictivo" mencionado aquí (ej. proyectar cómo evolucionarán los casos) es la puerta de entrada conceptual a **Regresión Lineal (Semana 7)** y **Regresión Logística (Semana 8)**.
