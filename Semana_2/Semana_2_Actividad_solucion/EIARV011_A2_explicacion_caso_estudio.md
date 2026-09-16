# Explicación breve de cada instrucción (`EIARV011_A2_analisis.ipynb`)

1. `import pandas as pd` → Importa Pandas para manejo de datos tabulares.  
2. `import numpy as np` → Importa NumPy para operaciones numéricas.  
3. `import seaborn as sns` → Importa Seaborn para visualización estadística.  
4. `pd.set_option('display.max_columns', None)` → Permite mostrar todas las columnas del DataFrame.

5. `df = pd.read_csv("StudentsPerformance.csv")` → Carga el archivo CSV en `df`.  
6. `df.head()` → Muestra las primeras 5 filas.

7. `print("Filas y columnas:", df.shape)` → Imprime tamaño del dataset.  
8. `df.columns` → Muestra los nombres de columnas.  
9. `df.dtypes` → Muestra tipos de datos por columna.  
10. `df.info()` → Resume estructura, no nulos y memoria.

11. `df.isnull().sum()` → Cuenta valores nulos por columna.  
12. `print("Filas duplicadas:", df.duplicated().sum())` → Cuenta registros duplicados.

13. `Q1 = df["math score"].quantile(0.25)` → Calcula el primer cuartil.  
14. `Q3 = df["math score"].quantile(0.75)` → Calcula el tercer cuartil.  
15. `IQR = Q3 - Q1` → Calcula rango intercuartílico.  
16. `limite_inferior = Q1 - 1.5 * IQR` → Define límite inferior de atípicos.  
17. `limite_superior = Q3 + 1.5 * IQR` → Define límite superior de atípicos.  
18. `atipicos = df[(...)]` → Filtra valores atípicos en matemáticas.  
19. `print(f"Limites: ...")` → Imprime límites calculados.  
20. `print("Cantidad de valores atipicos...", atipicos.shape[0])` → Muestra cuántos atípicos hay.  
21. `atipicos` → Muestra las filas atípicas.

22. `from matplotlib import pyplot as plt` → Importa Matplotlib para gráficos.  
23. `plt.figure(figsize=(6, 4))` → Crea figura de tamaño 6x4.  
24. `sns.boxplot(x=df["math score"])` → Grafica boxplot de matemáticas.  
25. `plt.title("Boxplot - Math Score")` → Coloca título.  
26. `plt.show()` → Muestra la gráfica.

27. `print(df["gender"].value_counts())` → Frecuencias absolutas de género.  
28. `print()` → Inserta línea en blanco.  
29. `print(df["gender"].value_counts(normalize=True) * 100)` → Porcentajes de género.

30. `print(df["test preparation course"].value_counts())` → Frecuencias absolutas del curso de preparación.  
31. `print()` → Línea en blanco.  
32. `print(df["test preparation course"].value_counts(normalize=True) * 100)` → Porcentajes del curso.

33. `fig, axes = plt.subplots(1, 2, figsize=(12, 4))` → Crea 2 subgráficos en una fila.  
34. `df["gender"].value_counts().plot(...)` → Barra de frecuencias por género.  
35. `df["test preparation course"].value_counts().plot(...)` → Barra de frecuencias del curso.  
36. `plt.tight_layout()` → Ajusta espaciado entre gráficos.  
37. `plt.show()` → Muestra la figura.

38. `df["math score"].describe()` → Estadísticos descriptivos de matemáticas.  
39. `df["reading score"].describe()` → Estadísticos descriptivos de lectura.

40. `df[["math score", "reading score", "writing score"]].hist(figsize=(10, 4), bins=15)` → Histogramas de las tres notas.  
41. `plt.tight_layout()` → Ajusta el diseño.  
42. `plt.show()` → Muestra histogramas.

43. `df[["math score", "reading score", "writing score"]].corr()` → Calcula correlaciones entre notas.  
44. `df.groupby("test preparation course")["math score"].mean()` → Promedio de matemáticas según preparación.  
45. `df["average score"] = df[[...]].mean(axis=1)` → Crea promedio general por estudiante.  
46. `df.groupby("parental level of education")["average score"].mean().sort_values(ascending=False)` → Promedio por nivel educativo de padres, ordenado de mayor a menor.

47. Última celda vacía (`source: ""`) → No ejecuta ninguna instrucción.
