# Analogía: "Los dos salones y el Profe Levene"

## El montaje (dibújalo en el tablero)

Imagina que tienes **dos salones**: el salón de los **niños** (40 estudiantes) y el salón de las **niñas**
(40 estudiantes). En cada salón, ubicas a los estudiantes en tres filas según su nivel:

```
SALÓN DE NIÑOS (40)              SALÓN DE NIÑAS (40)
   Avanzados: 5                     Avanzadas: 5
   Intermedios: 30                  Intermedias: 30
   Básicos: 5                       Básicas: 5
```

**Punto clave que debes resaltar:** no importa que en el salón de niñas el nivel "intermedio" en realidad
tenga notas más altas que el "intermedio" de los niños (como en los datos reales: niñas promedian 72.47,
niños 63.31). Lo que Levene mira **no es quién va mejor en promedio** — eso lo compara otra prueba (la t de
Student). Levene solo mira **la forma en que cada salón está repartido**: ¿cuántos se salen de la fila de
en medio hacia los extremos?

## La pregunta del Profe Levene

El Profe Levene entra a los dos salones y solo hace una pregunta:

> **"¿En los dos salones hay la misma cantidad de estudiantes que se 'salen' del montón de en medio hacia
> los extremos (muy avanzados o muy básicos)?"**

En nuestro ejemplo: en el salón de niños, 10 de 40 son "extremos" (5 avanzados + 5 básicos) — el resto está
en la fila de en medio. En el salón de niñas, también 10 de 40 son "extremos" (5 + 5). **¡La misma
proporción de extremos en ambos salones!**

## El resultado: p = 0.934

- El Profe Levene compara los dos salones y ve que están **igual de "revueltos"**: ni el salón de niños ni
  el de niñas tiene más estudiantes raros/extremos que el otro.
- Como resultado, da un número **grande, casi 1** (0.934): "no encontré ninguna diferencia sospechosa en
  cómo está repartido cada salón".
- **Regla:** si ese número es mayor a 0.05, el Profe Levene dice *"tranquilos, los dos salones están
  parejos por dentro"*.

## La moraleja

> "El Profe Levene **no** nos dice si las niñas sacan mejor nota que los niños en promedio — eso lo
> responde después el Profe *t de Student*. El Profe Levene solo nos da luz verde: **'la variedad dentro de
> cada salón es parecida, así que sí puedo confiar en comparar los promedios de forma justa entre los dos
> salones'**."

**Frase resumen:**

> *Levene no compara quién es mejor — compara qué tan "revuelto" está cada grupo por dentro. Con
> p = 0.934, los dos grupos están igual de revueltos, así que la comparación de promedios (niños vs. niñas)
> se puede hacer con confianza.*

---------------------------------------------------------------------------

## La fórmula de Levene

`scipy.stats.levene` usa por defecto la variante de **Brown-Forsythe**, que centra cada grupo en su **mediana** (no en la media) — es más robusta si los datos no son perfectamente normales. La fórmula tiene 3 pasos:

### Paso 1 — Transformar cada dato en "qué tan lejos está de la mediana de su grupo"

$$Z_{ij} = |X_{ij} - \tilde{X}_i|$$

Donde $\tilde{X}_i$ es la mediana del grupo $i$. Con tus datos:

- Mediana hombres = **64.0** → cada hombre se reemplaza por $|nota - 64.0|$
- Mediana mujeres = **74.0** → cada mujer se reemplaza por $|nota - 74.0|$

Esto convierte "¿tienen la misma nota?" en "¿se alejan lo mismo de su propio centro?" — que es justo lo que Levene quiere medir (dispersión, no nivel).

### Paso 2 — Calcular el estadístico W (con la misma forma que un ANOVA, pero sobre los $Z_{ij}$)

$$W = \frac{N-k}{k-1} \cdot \frac{\sum_{i=1}^{k} n_i (\bar{Z}_{i\cdot} - \bar{Z}_{\cdot\cdot})^2}{\sum_{i=1}^{k}\sum_{j=1}^{n_i} (Z_{ij} - \bar{Z}_{i\cdot})^2}$$

- $N$ = tamaño total (1000), $k$ = número de grupos (2)
- $\bar{Z}_{i\cdot}$ = promedio de los $Z_{ij}$ dentro del grupo $i$ (el "alejamiento promedio" de cada grupo)
- $\bar{Z}_{\cdot\cdot}$ = promedio de **todos** los $Z_{ij}$ juntos
- **Numerador:** qué tan distintos son los alejamientos promedio *entre* grupos (¿un grupo se aleja más que el otro?)
- **Denominador:** qué tan distintos son los alejamientos *dentro* de cada grupo (el "ruido" normal)

Con tus datos, el numerador salió chiquito frente al denominador → **W = 0.006939** (casi cero: los dos grupos se alejan de su centro de forma casi idéntica).

### Paso 3 — Convertir W en p-value

$W$ sigue (bajo H0) una distribución **F** con $(k-1, N-k) = (1, 998)$ grados de libertad:

$$p = P(F_{1,998} \geq W)$$

Un $W$ tan pequeño (0.0069) cae muy cerca del centro de esa distribución F → **p = 0.9336**: casi cualquier resultado sería "más raro" que este, así que no hay nada sorprendente que explicar.

### Verificación: reproduje la fórmula a mano (sin `scipy.stats.levene`) y dio exactamente igual

```
scipy: statistic=0.006939404299938817, p-value=0.9336272510018057
manual: statistic=0.006939404299938817, p-value=0.9336272510018057
```

Coincide dígito por dígito — así es literalmente como `scipy` calcula ese 0.934 por dentro.