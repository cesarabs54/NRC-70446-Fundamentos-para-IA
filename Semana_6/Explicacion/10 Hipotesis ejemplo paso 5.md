## Dos pruebas distintas, la misma pregunta: math score, hombres vs. mujeres

Este paso aplica **dos** herramientas al mismo problema — una que usa las medias (t de Student) y otra que usa solo el **orden** de los datos (Mann-Whitney U) — para ver si coinciden.

## 1. La prueba t de Student (misma fórmula que ya vimos, con estos datos)

Recordarás la fórmula del ejercicio de `writing score`: aquí es idéntica, solo cambian los números.

| | n | media | desv. estándar |
|---|---|---|---|
| Hombres | 482 | 68.7282 | 14.3563 |
| Mujeres | 518 | 63.6332 | 15.4915 |

$$s_p^2 = \frac{481\times14.36^2 + 517\times15.49^2}{998} = 223.24, \qquad SE = \sqrt{s_p^2\left(\tfrac{1}{482}+\tfrac{1}{518}\right)} = 0.947$$

$$t = \frac{68.7282 - 63.6332}{0.947} = 5.3832$$

Esta vez sale **positivo** (antes salió negativo con `writing score`) simplemente porque restamos *hombres − mujeres*, y aquí los hombres son quienes sacan más: el signo solo indica dirección. Con $df = 998$, ese t da $p = 9.12\times10^{-8}$ — verificado exacto contra `scipy`.

## 2. Mann-Whitney U — una lógica completamente distinta

En vez de comparar promedios, Mann-Whitney **ignora los valores exactos** y solo mira el **orden** (rangos): junta los 1000 estudiantes en una sola fila, del puntaje más bajo al más alto, y les asigna un número de puesto (1, 2, 3... 1000).

**Paso a paso:**

1. **Ordena a los 1000 juntos** y asigna un rango a cada uno (si hay empates, se reparte el rango promedio entre ellos).
2. **Suma los rangos que le tocaron a los hombres:** $R_1 = 264{,}310.5$.
3. **Calcula el estadístico U** para cada grupo:

$$U_1 = R_1 - \frac{n_1(n_1+1)}{2} = 264{,}310.5 - \frac{482\times483}{2} = 147{,}907.5$$

4. **La idea:** si no hubiera ninguna diferencia entre hombres y mujeres, la suma de rangos de los hombres debería ser "la esperada al azar": $\mu_U = \frac{n_1 n_2}{2} = 124{,}838$. La diferencia entre lo que obtuviste (147,907.5, si tomas el U más chico entre $U_1$ y $U_2$: 101,768.5) y lo esperado por azar (124,838) se mide en "unidades de variación esperada" ($\sigma_U = 4{,}563.7$):

$$z = \frac{101{,}768.5 - 124{,}838}{4{,}563.7} = -5.06$$

5. Ese $z$ se convierte en un p-value con la distribución normal: aproximadamente **4.30×10⁻⁷** (mi cálculo a mano da 4.30×10⁻⁷; `scipy` da 4.28×10⁻⁷ — la mínima diferencia es porque `scipy` aplica una **corrección por empates**, ya que muchos estudiantes comparten exactamente la misma nota entera, y eso ajusta ligeramente la varianza esperada).

## Verificación con el CSV real

```
t de Student:    t=5.383245869828983, df=998.0, p=9.120185549328806e-08   ✓ exacto
Mann-Whitney U:  U=147907.5, p=4.279076773478767e-07                       (mi aproximación: 4.30e-07, muy cerca)
```

## Por qué se usan ambas ("como verificación")

Recuerda el Ejercicio 4 de este mismo documento: Shapiro-Wilk señaló que ninguno de los dos grupos es perfectamente normal. Eso hace dudar de la prueba t (que técnicamente lo asume). Mann-Whitney **no necesita** ese supuesto — al basarse solo en el orden, funciona igual de bien aunque los datos no formen una campana perfecta. Como **las dos pruebas, con lógicas totalmente distintas, llegan a la misma conclusión** (p ≪ 0.05 en ambas → se rechaza H0), eso da mucha más confianza en el resultado que si solo hubieras usado una.