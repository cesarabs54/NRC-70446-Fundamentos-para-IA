# Análisis del apartado 3: Calidad de datos

## 1. Valores nulos
Se usa `df.isnull().sum()` para contar datos faltantes por columna.

**Resultado:** todas las columnas tienen `0` nulos.  
**Interpretación:** no hay datos vacíos, así que no se requiere imputación ni eliminación por este motivo.

## 2. Duplicados
Se usa `df.duplicated().sum()` para detectar filas repetidas exactas.

**Resultado:** `0` filas duplicadas.  
**Interpretación:** no hay registros repetidos que distorsionen frecuencias, promedios o correlaciones.

## 3. Valores atípicos (IQR) en `math score`
Se aplica el método del rango intercuartílico (IQR):

- `Q1` = percentil 25
- `Q3` = percentil 75
- `IQR = Q3 - Q1`
- Límites:
  - inferior = `Q1 - 1.5 * IQR`
  - superior = `Q3 + 1.5 * IQR`

Se consideran atípicos los valores fuera de esos límites.

**Resultado del notebook:** límites `[27.0, 107.0]` y `8` atípicos en `math score` (todos por debajo del límite inferior).  
**Interpretación:** existen casos con puntajes de matemáticas inusualmente bajos. El boxplot se usa para confirmarlo visualmente.

## Conclusión general
La calidad del dataset es **buena**: no hay nulos ni duplicados.  
El único punto de atención son los **8 valores extremos bajos** en matemáticas, que deben reportarse y revisarse por su posible impacto en medias y en modelos predictivos.
