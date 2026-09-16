# Ejercicios de aplicación: Estadística básica y descriptiva/inferencial

**Curso:** Fundamentos para Inteligencia Artificial — NRC 94103
**Semana 5:** Estadística básica y visualización de datos
**Basado en:** [`01_Estadistica_basica.md`](01_Estadistica_basica.md) — guía conceptual para el Portafolio de evidencias (Semana 6, `EIARV011_A6`)
**Datos:** [`StudentsPerformance.csv`](StudentsPerformance.csv) — notas de 1000 estudiantes (matemáticas, lectura y escritura), más variables de contexto (género, tipo de almuerzo, curso de preparación, nivel educativo de los padres, grupo étnico).

Este notebook desarrolla, con código Python real y ejecutado, un ejercicio práctico por cada una de las 10 secciones de `01_Estadistica_basica.md`. La numeración de los apartados coincide con la de esa guía, para que puedas ir de la explicación conceptual al código y viceversa.


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('StudentsPerformance.csv')

print(f"Filas (estudiantes): {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")
df.head()
```

    Filas (estudiantes): 1000
    Columnas: 8
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>gender</th>
      <th>race/ethnicity</th>
      <th>parental level of education</th>
      <th>lunch</th>
      <th>test preparation course</th>
      <th>math score</th>
      <th>reading score</th>
      <th>writing score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>female</td>
      <td>group B</td>
      <td>bachelor's degree</td>
      <td>standard</td>
      <td>none</td>
      <td>72</td>
      <td>72</td>
      <td>74</td>
    </tr>
    <tr>
      <th>1</th>
      <td>female</td>
      <td>group C</td>
      <td>some college</td>
      <td>standard</td>
      <td>completed</td>
      <td>69</td>
      <td>90</td>
      <td>88</td>
    </tr>
    <tr>
      <th>2</th>
      <td>female</td>
      <td>group B</td>
      <td>master's degree</td>
      <td>standard</td>
      <td>none</td>
      <td>90</td>
      <td>95</td>
      <td>93</td>
    </tr>
    <tr>
      <th>3</th>
      <td>male</td>
      <td>group A</td>
      <td>associate's degree</td>
      <td>free/reduced</td>
      <td>none</td>
      <td>47</td>
      <td>57</td>
      <td>44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>male</td>
      <td>group C</td>
      <td>some college</td>
      <td>standard</td>
      <td>none</td>
      <td>76</td>
      <td>78</td>
      <td>75</td>
    </tr>
  </tbody>
</table>
</div>



## 1. Tipos de variables

**Ejercicio.** Clasifica automáticamente cada columna del *dataset* como cuantitativa o cualitativa, e identifica la variable dependiente y la independiente para la pregunta: *"¿el curso de preparación influye en la nota de matemáticas?"*


```python
columnas_numericas = df.select_dtypes(include='number').columns.tolist()
columnas_categoricas = df.select_dtypes(exclude='number').columns.tolist()

print("Variables cuantitativas (numéricas):")
for c in columnas_numericas:
    print(f"  - {c}")

print("\nVariables cualitativas (categóricas):")
for c in columnas_categoricas:
    print(f"  - {c}  ({df[c].nunique()} categorías: {sorted(df[c].unique())})")

print("\nPara la pregunta '¿el curso de preparación influye en la nota de matemáticas?':")
print("  Variable dependiente   -> 'math score'              (cuantitativa continua)")
print("  Variable independiente -> 'test preparation course' (cualitativa nominal, 2 categorías)")
```

    Variables cuantitativas (numéricas):
      - math score
      - reading score
      - writing score
    
    Variables cualitativas (categóricas):
      - gender  (2 categorías: ['female', 'male'])
      - race/ethnicity  (5 categorías: ['group A', 'group B', 'group C', 'group D', 'group E'])
      - parental level of education  (6 categorías: ["associate's degree", "bachelor's degree", 'high school', "master's degree", 'some college', 'some high school'])
      - lunch  (2 categorías: ['free/reduced', 'standard'])
      - test preparation course  (2 categorías: ['completed', 'none'])
    
    Para la pregunta '¿el curso de preparación influye en la nota de matemáticas?':
      Variable dependiente   -> 'math score'              (cuantitativa continua)
      Variable independiente -> 'test preparation course' (cualitativa nominal, 2 categorías)
    

## 2. Población, muestra y tamaño de los grupos

**Ejercicio.** Calcula el tamaño total de la muestra (n) y el tamaño de cada grupo para dos variables independientes candidatas: `test preparation course` y `race/ethnicity`.


```python
n_total = len(df)
print(f"Tamaño total de la muestra: n = {n_total}\n")

print("Tamaño por grupo — test preparation course:")
print(df['test preparation course'].value_counts())

print("\nTamaño por grupo — race/ethnicity:")
print(df['race/ethnicity'].value_counts().sort_index())
```

    Tamaño total de la muestra: n = 1000
    
    Tamaño por grupo — test preparation course:
    test preparation course
    none         642
    completed    358
    Name: count, dtype: int64
    
    Tamaño por grupo — race/ethnicity:
    race/ethnicity
    group A     89
    group B    190
    group C    319
    group D    262
    group E    140
    Name: count, dtype: int64
    

## 3. Estadística descriptiva: el "dato típico"

**Ejercicio.** Calcula la media, la mediana y la moda de las tres variables numéricas (`math score`, `reading score`, `writing score`) y compáralas en una sola tabla.

**Fórmulas:** $\bar{x} = \dfrac{\sum_{i=1}^{n} x_i}{n}$ (media); la mediana es el valor central de los datos ordenados; la moda es el valor más frecuente. Ver [Sección 3 de la guía conceptual](01_Estadistica_basica.md#3-estadística-descriptiva-el-dato-típico-paso-5-del-anexo).


```python
resumen_centro = pd.DataFrame({
    'media':   df[['math score', 'reading score', 'writing score']].mean(),
    'mediana': df[['math score', 'reading score', 'writing score']].median(),
    'moda':    df[['math score', 'reading score', 'writing score']].mode().iloc[0],
}).round(2)

resumen_centro
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>media</th>
      <th>mediana</th>
      <th>moda</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>math score</th>
      <td>66.09</td>
      <td>66.0</td>
      <td>65</td>
    </tr>
    <tr>
      <th>reading score</th>
      <td>69.17</td>
      <td>70.0</td>
      <td>72</td>
    </tr>
    <tr>
      <th>writing score</th>
      <td>68.05</td>
      <td>69.0</td>
      <td>74</td>
    </tr>
  </tbody>
</table>
</div>



**Interpretación:** en las tres materias, la media y la mediana están muy cerca entre sí, lo que indica distribuciones bastante simétricas, sin un grupo extremo que distorsione el promedio (ver Sección 4 para confirmarlo con la dispersión).

## 4. Estadística descriptiva: qué tan parejos son los datos

**Ejercicio.** Para `math score`, calcula el rango, la desviación estándar y los cuartiles (Q1, Q2, Q3). Luego, usando la regla del rango intercuartílico (IQR), identifica cuántos estudiantes tienen una nota de matemáticas atípica (*outlier*).

**Fórmulas:**

$$
R = x_{\text{máx}} - x_{\text{mín}}, \qquad
s = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}, \qquad
IQR = Q_3 - Q_1
$$

Límites para detectar *outliers*: $Q_1 - 1.5 \times IQR$ y $Q_3 + 1.5 \times IQR$.

Ver [Sección 4 de la guía conceptual](01_Estadistica_basica.md#4-estadística-descriptiva-qué-tan-parejos-son-los-datos-paso-5-del-anexo).


```python
math = df['math score']

rango = math.max() - math.min()
desviacion = math.std()  # ddof=1 por defecto: desviación estándar muestral, s = sqrt(sum((x-x̄)²)/(n-1))
q1, q2, q3 = math.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = math[(math < limite_inferior) | (math > limite_superior)]

print(f"Rango:               {rango}")
print(f"Desviación estándar: {desviacion:.2f}")
print(f"Q1 = {q1}, Q2 (mediana) = {q2}, Q3 = {q3}")
print(f"IQR = {iqr}")
print(f"Límites para outliers: [{limite_inferior:.1f}, {limite_superior:.1f}]")
print(f"Número de estudiantes con math score atípico: {len(outliers)}")
print(f"Valores atípicos encontrados: {sorted(outliers.tolist())}")
```

    Rango:               100
    Desviación estándar: 15.16
    Q1 = 57.0, Q2 (mediana) = 66.0, Q3 = 77.0
    IQR = 20.0
    Límites para outliers: [27.0, 107.0]
    Número de estudiantes con math score atípico: 8
    Valores atípicos encontrados: [0, 8, 18, 19, 22, 23, 24, 26]
    

## 5. Qué gráfico usar para cada análisis

**Ejercicio.** Construye los tres gráficos mínimos que pide el taller: (a) un histograma de `math score` con la media y la mediana marcadas, (b) un boxplot de `math score` comparando los grupos de `test preparation course`, y (c) un diagrama de dispersión entre `reading score` y `writing score`.


```python
media = math.mean()
mediana = math.median()

plt.figure(figsize=(8, 5))
plt.hist(math, bins=20, color='#5a7d9a', edgecolor='white')
plt.axvline(media, color='#c0392b', linestyle='--', linewidth=2, label=f'Media ({media:.1f})')
plt.axvline(mediana, color='#27ae60', linestyle=':', linewidth=2, label=f'Mediana ({mediana:.1f})')
plt.title('Distribución de math score (histograma)')
plt.xlabel('math score')
plt.ylabel('Número de estudiantes')
plt.legend()
plt.tight_layout()
plt.show()
```


    
![png](02_Ejercicios_aplicacion_files_profesor/output_12_0.png)
    



```python
grupos_prep = [df.loc[df['test preparation course'] == g, 'math score']
               for g in ['none', 'completed']]

plt.figure(figsize=(7, 5))
plt.boxplot(grupos_prep, tick_labels=['none', 'completed'])
plt.title('math score según test preparation course (boxplot)')
plt.xlabel('test preparation course')
plt.ylabel('math score')
plt.tight_layout()
plt.show()
```


    
![png](02_Ejercicios_aplicacion_files_profesor/output_13_0.png)
    



```python
plt.figure(figsize=(6, 6))
plt.scatter(df['reading score'], df['writing score'], alpha=0.4, color='#5a7d9a')
plt.title('reading score vs. writing score (diagrama de dispersión)')
plt.xlabel('reading score')
plt.ylabel('writing score')
plt.tight_layout()
plt.show()
```


    
![png](02_Ejercicios_aplicacion_files_profesor/output_14_0.png)
    


**Interpretación:** el histograma confirma la simetría de `math score` (media y mediana casi coinciden); el boxplot deja ver que el grupo `completed` tiene una caja desplazada hacia notas más altas que el grupo `none`; y la nube de puntos de lectura vs. escritura muestra una tendencia lineal creciente muy marcada, señal de una correlación fuerte (se calcula en la Sección 6).

## 6. De describir a inferir: correlación entre variables numéricas

**Ejercicio.** Calcula la matriz de correlación entre las tres variables numéricas e identifica el par de variables más fuertemente correlacionado.


```python
matriz_corr = df[['math score', 'reading score', 'writing score']].corr().round(3)
matriz_corr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>math score</th>
      <th>reading score</th>
      <th>writing score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>math score</th>
      <td>1.000</td>
      <td>0.818</td>
      <td>0.803</td>
    </tr>
    <tr>
      <th>reading score</th>
      <td>0.818</td>
      <td>1.000</td>
      <td>0.955</td>
    </tr>
    <tr>
      <th>writing score</th>
      <td>0.803</td>
      <td>0.955</td>
      <td>1.000</td>
    </tr>
  </tbody>
</table>
</div>




```python
corr_lectura_escritura = df['reading score'].corr(df['writing score'])
corr_mate_lectura = df['math score'].corr(df['reading score'])
corr_mate_escritura = df['math score'].corr(df['writing score'])

print(f"Correlación lectura-escritura: {corr_lectura_escritura:.3f}  (la más fuerte)")
print(f"Correlación matemáticas-lectura: {corr_mate_lectura:.3f}")
print(f"Correlación matemáticas-escritura: {corr_mate_escritura:.3f}")
print()
print("Recordatorio: una correlación alta (aquí, 0.955 entre lectura y escritura) indica una")
print("asociación estadística fuerte, pero por sí sola NO demuestra que una habilidad cause la otra.")
```

    Correlación lectura-escritura: 0.955  (la más fuerte)
    Correlación matemáticas-lectura: 0.818
    Correlación matemáticas-escritura: 0.803
    
    Recordatorio: una correlación alta (aquí, 0.955 entre lectura y escritura) indica una
    asociación estadística fuerte, pero por sí sola NO demuestra que una habilidad cause la otra.
    

## 7. Formulación de hipótesis: H0 y H1

**Ejercicio.** Redacta formalmente H0 y H1 para la pregunta *"¿el curso de preparación influye en la nota de matemáticas?"*, y calcula el promedio de cada grupo como primer indicio antes de aplicar la prueba formal (Secciones 8-10).

**Notación formal:** $H_0: \mu_1 = \mu_2$ vs. $H_1: \mu_1 \neq \mu_2$, donde $\mu_1$ y $\mu_2$ son los promedios poblacionales de `math score` en cada grupo. Ver [Sección 7 de la guía conceptual](01_Estadistica_basica.md#7-formulación-de-hipótesis-h0-y-h1-paso-2-del-anexo).


```python
H0 = "El promedio de 'math score' es igual entre los estudiantes que completaron el curso de preparación y los que no."
H1 = "El promedio de 'math score' es diferente entre los estudiantes que completaron el curso de preparación y los que no."

print("H0:", H0)
print("H1:", H1)
print()

promedios_por_grupo = df.groupby('test preparation course')['math score'].agg(['count', 'mean']).round(2)
print("Promedio observado por grupo (evidencia descriptiva, todavía no es una prueba formal):")
print(promedios_por_grupo)
```

    H0: El promedio de 'math score' es igual entre los estudiantes que completaron el curso de preparación y los que no.
    H1: El promedio de 'math score' es diferente entre los estudiantes que completaron el curso de preparación y los que no.
    
    Promedio observado por grupo (evidencia descriptiva, todavía no es una prueba formal):
                             count   mean
    test preparation course              
    completed                  358  69.70
    none                       642  64.08
    

## 8. Validación de supuestos: normalidad y homogeneidad de varianzas

**Ejercicio.** Evalúa si `math score` cumple el supuesto de normalidad (prueba de Shapiro-Wilk) y si los dos grupos de `test preparation course` tienen varianzas homogéneas (prueba de Levene).

**Fórmulas:**

Shapiro-Wilk (cuanto más cerca de 1, más "normal" es la distribución):

$$
W = \frac{\left(\sum_{i=1}^{n} a_i\, x_{(i)}\right)^2}{\sum_{i=1}^{n} (x_i - \bar{x})^2}
$$

Levene (con $Z_{ij} = |x_{ij} - \tilde{x}_i|$, la distancia de cada dato a la mediana de su grupo):

$$
W = \frac{N-k}{k-1} \cdot \frac{\sum_{i=1}^{k} n_i (\bar{Z}_{i\cdot} - \bar{Z}_{\cdot\cdot})^2}{\sum_{i=1}^{k}\sum_{j=1}^{n_i} (Z_{ij} - \bar{Z}_{i\cdot})^2}
$$

Ver [Sección 8 de la guía conceptual](01_Estadistica_basica.md#8-validación-de-supuestos-normalidad-y-homogeneidad-de-varianzas-paso-6-del-anexo).


```python
alpha = 0.05

stat_shapiro, p_shapiro = stats.shapiro(df['math score'])
print(f"Shapiro-Wilk sobre 'math score': estadístico = {stat_shapiro:.4f}, p-value = {p_shapiro:.6f}")
if p_shapiro < alpha:
    print(f"  p < {alpha} -> hay evidencia en contra de la normalidad estricta.")
else:
    print(f"  p >= {alpha} -> no se rechaza la normalidad.")

grupo_none = df.loc[df['test preparation course'] == 'none', 'math score']
grupo_completed = df.loc[df['test preparation course'] == 'completed', 'math score']

stat_levene, p_levene = stats.levene(grupo_none, grupo_completed)
print(f"\nLevene sobre 'math score' por grupo: estadístico = {stat_levene:.4f}, p-value = {p_levene:.4f}")
if p_levene < alpha:
    print(f"  p < {alpha} -> las varianzas NO son homogéneas.")
else:
    print(f"  p >= {alpha} -> no se rechaza la homogeneidad de varianzas (los grupos tienen dispersión comparable).")
```

    Shapiro-Wilk sobre 'math score': estadístico = 0.9932, p-value = 0.000145
      p < 0.05 -> hay evidencia en contra de la normalidad estricta.
    
    Levene sobre 'math score' por grupo: estadístico = 0.5330, p-value = 0.4655
      p >= 0.05 -> no se rechaza la homogeneidad de varianzas (los grupos tienen dispersión comparable).
    

## 9. Selección y ejecución de la prueba estadística inferencial

**Ejercicio.** Con 2 grupos y varianzas homogéneas (Sección 8), aplica la prueba t de Student para muestras independientes sobre `math score` según `test preparation course`. Adicionalmente, aplica ANOVA para comparar `math score` entre los 5 grupos de `race/ethnicity`, y compárala con su alternativa no paramétrica (Kruskal-Wallis).

**Fórmulas:**

Prueba t de Student:

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{1/n_1 + 1/n_2}}, \qquad
s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}}
$$

ANOVA de un factor:

$$
F = \frac{\text{MSB}}{\text{MSW}}
$$

(varianza entre grupos sobre varianza dentro de los grupos — ver fórmulas completas de MSB y MSW en la Sección 9 de la guía conceptual).

Kruskal-Wallis (versión no paramétrica de ANOVA, sobre los rangos $R_i$ de cada grupo, con $N$ el total de datos):

$$
H = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N+1)
$$

Correlación de Pearson:

$$
r = \frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i-\bar{x})^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar{y})^2}}
$$

Ver [Sección 9 de la guía conceptual](01_Estadistica_basica.md#9-selección-de-la-prueba-estadística-inferencial-paso-7-del-anexo).


```python
t_stat, p_t = stats.ttest_ind(grupo_none, grupo_completed, equal_var=True)
print("Prueba t de Student (2 grupos: test preparation course)")
print(f"  t = {t_stat:.3f}, p-value = {p_t:.3e}")

grupos_etnia = [g['math score'].values for _, g in df.groupby('race/ethnicity')]

f_stat, p_anova = stats.f_oneway(*grupos_etnia)
print("\nANOVA de un factor (5 grupos: race/ethnicity)")
print(f"  F = {f_stat:.3f}, p-value = {p_anova:.3e}")

h_stat, p_kruskal = stats.kruskal(*grupos_etnia)
print("\nKruskal-Wallis (alternativa no paramétrica para 5 grupos)")
print(f"  H = {h_stat:.3f}, p-value = {p_kruskal:.3e}")

correlacion_r, p_corr = stats.pearsonr(df['reading score'], df['writing score'])
print("\nCorrelación de Pearson (reading score vs. writing score)")
print(f"  r = {correlacion_r:.3f}, p-value = {p_corr:.3e}")
```

    Prueba t de Student (2 grupos: test preparation course)
      t = -5.705, p-value = 1.536e-08
    
    ANOVA de un factor (5 grupos: race/ethnicity)
      F = 14.594, p-value = 1.373e-11
    
    Kruskal-Wallis (alternativa no paramétrica para 5 grupos)
      H = 57.079, p-value = 1.191e-11
    
    Correlación de Pearson (reading score vs. writing score)
      r = 0.955, p-value = 0.000e+00
    

## 10. Resultados e interpretación: estadístico, p-value y decisión sobre H0

**Ejercicio.** Escribe una función que, dado un *p-value* y un nivel de significancia (alfa = 0.05), devuelva en texto la decisión sobre H0. Aplícala a los cuatro resultados de la Sección 9 y redacta la conclusión final para el portafolio.

**Fórmula:** $p = P\big(|T| \geq |t_{\text{obs}}| \mid H_0 \text{ verdadera}\big)$ para una prueba de dos colas. Ver [Sección 10 de la guía conceptual](01_Estadistica_basica.md#10-resultados-e-interpretación-el-estadístico-de-prueba-y-el-p-value-paso-8-del-anexo).


```python
def decidir_H0(p_value, alpha=0.05):
    if p_value < alpha:
        return "se RECHAZA H0 (evidencia suficiente a favor de H1)"
    else:
        return "NO se rechaza H0 (evidencia insuficiente para afirmar un efecto)"

resultados = {
    "Prueba t (test preparation course -> math score)": p_t,
    "ANOVA (race/ethnicity -> math score)": p_anova,
    "Kruskal-Wallis (race/ethnicity -> math score)": p_kruskal,
    "Correlación de Pearson (reading score vs. writing score)": p_corr,
}

for nombre, p in resultados.items():
    print(f"{nombre}")
    print(f"  p-value = {p:.3e}  ->  {decidir_H0(p)}\n")

print("Conclusión para el portafolio (ejemplo con la prueba t):")
print("Con un nivel de significancia del 5%, se rechaza la hipótesis nula: la muestra aporta")
print("evidencia de que el curso de preparación está asociado con una nota de matemáticas más")
print("alta. Esta asociación estadística no implica, por sí sola, una relación de causalidad.")
```

    Prueba t (test preparation course -> math score)
      p-value = 1.536e-08  ->  se RECHAZA H0 (evidencia suficiente a favor de H1)
    
    ANOVA (race/ethnicity -> math score)
      p-value = 1.373e-11  ->  se RECHAZA H0 (evidencia suficiente a favor de H1)
    
    Kruskal-Wallis (race/ethnicity -> math score)
      p-value = 1.191e-11  ->  se RECHAZA H0 (evidencia suficiente a favor de H1)
    
    Correlación de Pearson (reading score vs. writing score)
      p-value = 0.000e+00  ->  se RECHAZA H0 (evidencia suficiente a favor de H1)
    
    Conclusión para el portafolio (ejemplo con la prueba t):
    Con un nivel de significancia del 5%, se rechaza la hipótesis nula: la muestra aporta
    evidencia de que el curso de preparación está asociado con una nota de matemáticas más
    alta. Esta asociación estadística no implica, por sí sola, una relación de causalidad.
    

---

### Cierre

Cada sección de este notebook reproduce, con código real, el mismo recorrido conceptual de `01_Estadistica_basica.md`: clasificar variables, describir la muestra, resumir con medidas de tendencia central y dispersión, visualizar, plantear hipótesis, validar supuestos, elegir la prueba correcta y, finalmente, interpretar el resultado en función de H0. Este mismo flujo es el que debes reproducir con el *dataset* que elijas para el Portafolio de evidencias (`EIARV011_A6`, Semana 6).
