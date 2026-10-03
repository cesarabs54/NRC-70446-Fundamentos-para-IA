# Semana 3 — Cuadro técnico consolidado

**Tema:** *Frameworks* para Inteligencia Artificial en Python: scikit-learn, TensorFlow/Keras y PyTorch, y los seis criterios técnicos para elegir uno (preprocesamiento, soporte GPU/rendimiento, facilidad de entrenamiento, interpretabilidad, comunidad/documentación e integración para despliegue).
**Datos de la semana:** no hay CSV. Los ejemplos usan el problema de juguete `y = 2x` (4 puntos) y dos conjuntos que vienen con scikit-learn: `iris` (150 flores, 4 variables, 3 clases) y `digits` (1 797 imágenes de 8×8 píxeles, 10 clases).
**Actividad calificada:** Foro «Herramientas de Python» (colaborativo, 5 puntos: pertinencia 2 + análisis 1 + abordaje 2; se suma a la evaluación final), con el Anexo «probar el *framework* en 3 minutos» (imprimir la versión de uno de los tres). El taller `Semana_taller_01` es práctica posterior y opcional: retoma el anexo y los materiales no le asignan nota (solo una «rúbrica rápida de participación» sugerida en la versión del profesor). La rúbrica del foro es coherente: los niveles suman 0.8 + 0.3 + 0.8 = 1.9, 1.2 + 0.5 + 1.2 = 2.9, 1.6 + 0.7 + 1.6 = 3.9 y 2 + 1 + 2 = 5.

> Todas las cifras de este documento se recalcularon ejecutando el código en Windows 11 (CPU; sin GPU utilizable), Python 3.11.9, NumPy 2.4.6, scikit-learn 1.9.1, SciPy 1.17.1, TensorFlow 2.21.0 (Keras 3.15.1) y PyTorch 2.14.0+cpu: las mismas versiones que imprime `EIARV011_F3_Foro.ipynb`. Semillas fijas donde se indica; los tiempos dependen del equipo. Las marcadas con ✅ ya aparecen en los materiales del profesor (diapositivas, anexo, taller con su solución, retroalimentación del foro); las marcadas con ➕ son datos o alternativas que **no** están en ellos.
>
> **Archivos ignorados por Git que se usaron** (`*profesor*` está en `.gitignore`): `EIARV011_F3_Diapositivas_profesor.pptx` (mismo texto que `Semana_3_Diapositivas.pdf`, 16 diapositivas), `Semana_taller_01_profesor.md` y `.ipynb`, y los tres `.md` de `Semana_3_Foro_profesor/` (resumen de participación, retroalimentación general y material complementario). No se usaron las entregas ni las calificaciones.

---

## 1. Procedimientos de la semana (el mismo problema en tres *frameworks*)

| Etapa | scikit-learn | TensorFlow / Keras | PyTorch | Lo medido |
|---|---|---|---|---|
| Verificar el entorno (Anexo) | `import sklearn` · `sklearn.__version__` | `import tensorflow as tf` · `tf.__version__` | `import torch` · `torch.__version__` | 1.9.1 · 2.21.0 · 2.14.0+cpu (las del notebook del foro). `import` tarda ≈ 1.8 s · 5.1 s · 1.9 s (la primera ejecución con caché frío llegó a 17 s en scikit-learn y 7.6 s en TensorFlow) |
| Formato de los datos | Listas 2D, arrays o `DataFrame` | Solo `np.array` o tensores | Solo `torch.tensor` en `float32` | scikit-learn acepta la lista; Keras da `ValueError`; PyTorch da `TypeError` (lista y `ndarray`) o `RuntimeError` (`float64`) |
| Preprocesamiento | `StandardScaler`, `OneHotEncoder`, `SimpleImputer`, `Pipeline`, `ColumnTransformer` | capa `Normalization`, `tf.data.Dataset` | `Dataset`, `DataLoader` (visión: `torchvision`, que no viene con `torch`) | Todos esos nombres existen en las versiones instaladas; `import torchvision` falla |
| Definir el modelo | Elegir la clase: `LinearRegression()`, `KNeighborsClassifier(3)` | `Sequential([Input, Dense, …])` | `nn.Linear`, `nn.Sequential` | Mismo 64-32-10 de `digits`: 2 410 parámetros en Keras y en PyTorch; `LogisticRegression`, 650 |
| Configurar el entrenamiento | Hiperparámetros en el constructor | `compile(optimizer, loss, metrics)` | `optimizer` y `loss` como objetos aparte | — |
| Entrenar | `fit(X, y)` | `fit(X, y, epochs=…)` | Bucle: `zero_grad` → `backward` → `step` | `y = 2x`: 0.5 ms · 7.1 s · 0.04 s |
| Predecir | `predict` | `predict` | `modelo(x)` | `[10.]` · `[[9.79]]` · `tensor([[10.13]], grad_fn=…)` (sin semilla) |
| Evaluar | `score`, `accuracy_score`, `mean_squared_error` | `evaluate` | A mano (`argmax`, comparación) | — |
| Interpretar | `coef_`, `kneighbors`, `export_text` | `get_weights()` | `parameters()`, `state_dict()` | Ver sección 4.2 |
| Guardar y recargar | `joblib.dump` / `load` | `save("x.keras")` / `load_model` | `torch.save(state_dict)` + `load_state_dict` | Las tres recargan y predicen igual; ver sección 4.5 |

**Qué confirma el Anexo y qué no.** `print(__version__)` confirma que la librería se importa y qué versión es. No confirma que haya GPU (aquí hay una NVIDIA y las tres corren en CPU), ni que el código de otra versión funcione (caso de las listas en Keras 3, sección 4.4).

---

## 2. Salidas esperadas del material frente a lo medido

| Ejercicio | Lo que dice el material | Medido | ¿Coincide? |
|---|---|---|---|
| 1.1 Regresión `y = 2x` | `[10.]` y `mse: 0.0` | `[10.]`, `mse` 0.0; coeficiente 2.0 e intercepto 0.0 exactos | Sí |
| Ejemplo extra 1 del notebook (10 datos fijos) | `w ≈ 2.98`, `b ≈ 5.13` | `w` = 3.0606, `b` = 4.6667, predicción en 11 = 38.33, `mse` = 0.7697 | **No** (salvedad 1) |
| Ejemplo extra 2 del notebook (`seed 42`, ruido N(0, 5)) | `w ≈ 2.97`, `b ≈ 7.43`, pred ≈ 40.05, `mse ≈ 11.75` | 2.9655 · 7.4301 · 40.0505 · 11.7519 | Sí |
| 1.2 Iris, KNN `k = 3` | «cercano a 1.0», «suele dar 100 %» con `random_state=42` | 1.0 (30 de prueba: 10 + 9 + 11 aciertos). En 100 particiones: media 0.960, mín 0.900, máx 1.000; solo 22 de 100 dan 1.0 | Sí con esa partición (salvedad 3) |
| 2.1 Keras `y = 2x` | «cercano a `[[10.]]`» | Sin semilla 9.79; semilla 0: 9.7719; 30 semillas: 9.73 (9.57–9.90); ninguna llega a 0.05 de 10 | Aproximado, siempre por debajo (salvedad 2) |
| 2.2 Keras `digits` | «entre 0.93 y 0.98» | 10 semillas: 0.9575 (0.9528–0.9639) | Sí |
| 3.1 Tensores | `tensor([2., 3., 4.])`, `torch.Size([3])`, `cuda` en `False` | Igual | Sí (salvedad 7 sobre el motivo del `False`) |
| 3.2 PyTorch `y = 2x` | «cercano a 10» (diapositiva: «10.0») | Sin semilla 10.1269; semilla 0: 9.5797; 30 semillas: 9.83 (9.38–10.17); solo 1 de 30 queda a 0.01 de 10 | Aproximado (salvedad 2) |
| Aviso de Keras 3 con listas | `ValueError: Unrecognized data type` | Idéntico, también con listas anidadas, listas de enteros y en `predict` | Sí |
| Olvidar `zero_grad()` | «diverge o se vuelve inestable» | Semilla 0: pérdida 25.1 → 21.6 en el paso 200 (con `zero_grad`: 0.0605); predicción 4.04. Semillas 1–5: 4.65 · 3.94 · −0.67 · 3.98 · 4.78 | Sí, inestable: oscila, no llega a NaN |
| Parte 4: líneas de código | ~4-5 · ~8-10 · ~10-12 | Sin imports ni `print`: 4 · 8 · 10 (con imports: 8 · 11 · 13) | Sí con ese criterio |
| Reflexión 2: «Keras tarda notoriamente más» | Sí, incluso en CPU | `digits`: Keras 1.93 s; KNN 0.0004 s; regresión logística 0.057 s; bosque 0.24 s (medianas de 30, 10 y 5 repeticiones) | Sí |

---

## 3. Los seis criterios técnicos × *framework*

### 3.1 Matriz de criterios (diapositiva 7 y pregunta orientadora del foro)

| Criterio | scikit-learn | TensorFlow / Keras | PyTorch | Evidencia medida | Uso |
|---|---|---|---|---|---|
| Preprocesamiento | Utilidades maduras para tablas; acepta listas y `DataFrame` | Capa `Normalization` y `tf.data`; exige `np.array` | `Dataset` y `DataLoader`; exige tensores `float32` | Mensajes exactos de error en la sección 4.4 | ✅ idea · ➕ mensajes |
| Soporte GPU / rendimiento | Solo CPU en general; Array API experimental y parcial | GPU/TPU en Linux; **Windows nativo sin GPU desde TF 2.11** | CUDA según la *build* instalada | `tf.config.list_physical_devices("GPU")` = `[]` y la propia TF lo avisa; `torch` es `+cpu` y `cuda` da `False`; con tensores de PyTorch en CPU, `Ridge(solver="svd")` devuelve un tensor | ✅ idea · ➕ matices |
| Facilidad de entrenamiento | `fit` (4 líneas) | `compile` + `fit` (8) | Bucle manual (10) | `y = 2x`: 0.5 ms · 7.1 s · 0.04 s; `digits`: Keras 1.93 s, PyTorch propio 0.77 s | ✅ |
| Interpretabilidad | `coef_`, vecinos, reglas del árbol | `get_weights()`; 2 410 parámetros sin lectura directa | `parameters()`; igual que Keras | `y = 2x` en scikit-learn: `w` = 2.0, `b` = 0.0. En Keras: `w` ≈ 1.87, `b` ≈ 0.38. Árbol de iris: 5 hojas, solo pétalos | ✅ idea · ➕ evidencia |
| Comunidad y documentación | Documentación oficial con ejemplos cortos | Guía «Keras: Quickstart» | Tutorial «Learn the Basics» | No se mide con código; fuentes en `Foro_S3_Sugerencia_material_complementario.md` | ✅ |
| Integración para despliegue | `joblib` (577 B); API liviana | `.keras` (14.8 KB); Serving, LiteRT, TF.js | `state_dict` (1.98 KB); TorchScript y TorchServe en retirada | Carpeta del paquete: 42 MB (más NumPy 33 y SciPy 113) · 1 409 MB (más Keras 25) · 506 MB | ✅ idea · ➕ tamaños y estado |

### 3.2 Guía rápida para elegir

| Si el problema, los datos o el contexto es… | Primera opción | Por qué (evidencia) |
|---|---|---|
| Tabla pequeña o mediana, prototipo rápido | scikit-learn | `digits`: KNN 0.983 en menos de 1 ms y regresión logística 0.967 en 0.06 s, frente a la red de 32 neuronas con 0.958 en 1.93 s |
| Hay que explicar cada decisión (salud, crédito) | scikit-learn (regresión, árbol, KNN) | `coef_`, `export_text`, `kneighbors`; una red de 2 410 parámetros no se lee directamente |
| Imágenes, audio o texto a gran escala | TensorFlow/Keras o PyTorch | Las redes con GPU son su terreno; `digits` solo sirve de juguete |
| Experimentar con arquitecturas o entender el entrenamiento | PyTorch | Cada paso del bucle es visible (y se puede romper: sección 4.4) |
| Entrenar con GPU en Windows nativo | PyTorch con *build* CUDA (no probada aquí), o TensorFlow en WSL2/Colab | TF ≥ 2.11 no usa GPU en Windows nativo (medido); la *build* de PyTorch instalada aquí es `+cpu` |
| Llevar un modelo a una API pequeña | scikit-learn + `joblib` | 577 B para `y = 2x`; Flask/FastAPI (los cita la retroalimentación, no se probaron) |
| Móvil o navegador | TensorFlow (LiteRT, TF.js) | Lo dicen las diapositivas; no se probó |

Regla práctica: ante la duda, entrenar primero un modelo clásico como línea base antes de justificar una red neuronal.

---

## 4. Ejemplos guiados

### 4.1 El mismo problema, tres veces: `y = 2x`

| | scikit-learn | Keras | PyTorch |
|---|---|---|---|
| Cómo aprende | Mínimos cuadrados (solución exacta) | Descenso de gradiente: 4 datos < lote de 32, así que 1 paso por época → 200 pasos | Descenso de gradiente: 200 pasos |
| Predicción en `x = 5` (semilla 0) | 10.0 | 9.7719 | 9.5797 |
| 30 semillas | — | 9.73 (9.57–9.90) | 9.83 (9.38–10.17) |
| `w` aprendida (30 semillas) | 2.0 exacta | 1.87 (1.79–1.95) | 1.92 (1.70–2.08) |
| `b` aprendida (30 semillas) | 0.0 exacta | 0.38 (0.14–0.61) | 0.25 (−0.24–0.89) |
| Tiempo de entrenamiento | 0.5 ms | 7.06 s (6.41–7.89) | 0.04 s (0.03–0.22) |
| Archivo guardado | 577 B (`joblib`) | 14 819 B (`.keras`) | 1 981 B (`state_dict`) |

**Por qué no llega a 10.** Con 200 pasos y tasa 0.01 el descenso se queda corto. El Hessiano de la pérdida es [[15, 5], [5, 2]], con autovalores 16.70 y 0.30: una dirección se corrige 0.833 por paso, pero la otra solo 0.997, y tras 200 pasos aún queda el 54.9 % de su error. Descenso de gradiente hecho a mano desde (0, 0): 9.7655 en 200 pasos y 9.99 recién en el paso 1 253. Las dos redes empiezan distinto (Keras: `glorot_uniform` con sesgo 0, pesos en [−1.73, 1.72]; PyTorch: uniforme en [−1, 1] para peso y sesgo), por eso sus rangos difieren.

| Pasos / épocas (semilla 0) | 50 | 100 | 200 | 400 | 800 | 1 600 |
|---|---|---|---|---|---|---|
| Keras | 9.6413 | 9.6921 | 9.7719 | 9.8748 | 9.9623 | 9.9966 |
| PyTorch | 9.3400 | 9.4327 | 9.5797 | 9.7692 | 9.9305 | 9.9937 |

**Cómo se corrige:** más épocas o más tasa de aprendizaje. Con descenso de gradiente a mano, tasa 0.1 da 9.999 en 200 pasos; el límite de estabilidad es 2 / 16.70 = 0.1198 y con 0.12 la predicción se dispara (−11.6 a los 200 pasos). Buen ejemplo en clase de que un hiperparámetro mal elegido no da error, da un número casi correcto.

### 4.2 Interpretabilidad con `iris` (reflexión 1 del taller)

| Elemento | Resultado | Lectura |
|---|---|---|
| KNN `k = 3`, `random_state=42` | Exactitud 1.0 en 30 flores (10 setosa, 9 versicolor, 11 virginica) | Partición favorable: la media de 100 particiones es 0.960 (mín 0.900) |
| Una predicción | La primera flor de prueba (6.1, 2.8, 4.7, 1.2) es versicolor porque sus 3 vecinos (distancias 0.224, 0.300, 0.436) son versicolor | Es la explicación que pide el taller, con una flor concreta ✅ |
| Árbol de decisión `max_depth=3` ➕ | Exactitud 1.0 en la misma partición, 5 hojas | Reglas legibles: pétalo ≤ 2.45 → setosa; si no, pétalo ≤ 4.75 con ancho ≤ 1.65 → versicolor; pétalo > 4.75 con ancho ≤ 1.75 → versicolor; el resto → virginica |
| Importancias del árbol ➕ | Largo de pétalo 0.935, ancho de pétalo 0.065, sépalos 0 | El modelo ignora los sépalos: se puede explicar y auditar |

### 4.3 `digits`: ¿gana la red neuronal? (reflexión 2 del taller)

| Modelo | Exactitud (360 imágenes) | Entrenamiento | Parámetros · archivo | Uso |
|---|---|---|---|---|
| Keras 64-32-10, Adam, 20 épocas (taller 2.2) | 0.9575 (0.9528–0.9639; 10 semillas) | 1.93 s | 2 410 · `.keras` 49 996 B | ✅ |
| PyTorch 64-32-10, Adam, lotes de 32, 20 épocas (bucle propio) | 0.9514 (0.9444–0.9583; 10 semillas) | 0.77 s | 2 410 · `state_dict` 12 171 B | ➕ |
| scikit-learn `LogisticRegression` | 0.9667 | 0.057 s | 650 · `joblib` 6 119 B | ➕ |
| scikit-learn KNN `k = 3` | 0.9833 | 0.0004 s | Guarda todo el entrenamiento | ➕ |
| scikit-learn `RandomForest` (100 árboles) | 0.9722 | 0.24 s | `joblib` 5 071 049 B | ➕ |

**Lectura:** en un problema de este tamaño los modelos clásicos igualan o superan a la red y entrenan de 8 veces más rápido (bosque) a más de 1 000 (KNN, que apenas guarda los datos). Los tiempos de scikit-learn son medianas de 5 a 30 repeticiones; los de Keras y PyTorch, medias de 10 semillas. Es una sola partición de 360 imágenes (una imagen = 0.28 puntos), así que las diferencias de uno o dos puntos no son concluyentes; la de tiempo sí. La red solo gana cuando los datos o el hardware lo justifican. Un detalle de comparabilidad: `MLPClassifier(hidden_layer_sizes=(32,), max_iter=20)` da 0.9111 con la misma arquitectura, porque su lote por defecto es 200 (8 pasos por época) y no 32 (45 pasos): mismos nombres de hiperparámetros, comportamiento distinto.

### 4.4 Errores típicos y cómo se ven

| Situación | Mensaje real | Causa | Arreglo |
|---|---|---|---|
| Keras con lista | `ValueError: Unrecognized data type: x=[1.0, 2.0, 3.0, 4.0] (of type <class 'list'>)` | Keras 3 no convierte listas de Python | `np.array(...)` ✅ |
| scikit-learn con lista 1D | `ValueError: Expected 2D array, got 1D array instead` | Pide una columna por variable | `[[1], [2], …]` o `reshape(-1, 1)` ➕ |
| PyTorch con lista o `ndarray` | `TypeError: linear(): argument 'input' … must be Tensor, not list` | Solo recibe tensores | `torch.tensor(...)` ➕ |
| PyTorch con `float64` | `RuntimeError: mat1 and mat2 must have the same dtype, but got Double and Float` | Modelo en `float32`, datos en `float64` | `dtype=torch.float32` ➕ |
| Olvidar `opt.zero_grad()` | No hay error: la pérdida oscila (25.1 → 2.19 → 13.6 → … → 21.6) | Los gradientes se acumulan | Reiniciarlos en cada paso ✅ |
| `cuda.is_available()` en `False` | No hay error | *Build* `+cpu` instalada (`torch.version.cuda` es `None`), aunque el equipo tenga GPU | Instalar la *build* CUDA o usar Colab ➕ |

### 4.5 Despliegue mínimo: guardar, recargar y predecir igual

| | scikit-learn | Keras | PyTorch |
|---|---|---|---|
| Guardar | `joblib.dump(m, "x.joblib")` | `m.save("x.keras")` | `torch.save(m.state_dict(), "x.pt")` |
| Recargar | `joblib.load("x.joblib")` | `tf.keras.models.load_model("x.keras")` | `m2 = nn.Linear(1, 1)` + `m2.load_state_dict(torch.load("x.pt", weights_only=True))` |
| Predicción tras recargar (`y = 2x`, semilla 0, 200 pasos) | `[10.]`, idéntica | 9.77186, idéntica | 9.579676, idéntica |
| Tamaño `y = 2x` · `digits` | 577 B · 6 119 B (regresión logística) | 14 819 B · 49 996 B | 1 981 B · 12 171 B |

Aviso para PyTorch: el `state_dict` guarda solo los pesos, hay que reconstruir la arquitectura al recargar. `torch.jit.script` guardó el modelo en 2 959 B pero en 2.14.0 avisa que está en desuso (salvedad 4).

### 4.6 Código listo para pegar

Cada bloque es independiente. TensorFlow y PyTorch van en procesos distintos. Los archivos de ejemplo se escriben en la carpeta actual.

```python
# scikit-learn: y = 2x, iris (una partición vs. 100) y digits contra clásicos
import time
import joblib
import numpy as np
from sklearn.datasets import load_digits, load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = [[1], [2], [3], [4]], [2, 4, 6, 8]
m = LinearRegression().fit(X, y)
print(m.predict([[5]]), m.coef_, m.intercept_, mean_squared_error(y, m.predict(X)))
joblib.dump(m, "modelo_sklearn.joblib")
print("recargado:", joblib.load("modelo_sklearn.joblib").predict([[5]]))

iris = load_iris()
Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=3).fit(Xtr, ytr)
print("accuracy (random_state=42):", knn.score(Xte, yte))
accs = np.array([
    KNeighborsClassifier(n_neighbors=3).fit(a, c).score(b, d)
    for a, b, c, d in (train_test_split(iris.data, iris.target, test_size=0.2, random_state=rs) for rs in range(100))
])
print("100 particiones: media %.4f, mín %.2f, máx %.2f, con 1.0: %d%%" % (accs.mean(), accs.min(), accs.max(), 100 * (accs == 1).mean()))
dist, idx = knn.kneighbors(Xte[:1])
print("vecinos:", [iris.target_names[ytr[j]] for j in idx[0]], dist.round(3))
arbol = DecisionTreeClassifier(max_depth=3, random_state=42).fit(Xtr, ytr)
print(export_text(arbol, feature_names=list(iris.feature_names)))

d = load_digits()
Xtr, Xte, ytr, yte = train_test_split(d.data / 16.0, d.target, test_size=0.2, random_state=42)
for nombre, modelo in [("LogisticRegression", LogisticRegression(max_iter=1000)),
                       ("KNN k=3", KNeighborsClassifier(n_neighbors=3)),
                       ("RandomForest 100", RandomForestClassifier(n_estimators=100, random_state=42))]:
    t = time.perf_counter()
    modelo.fit(Xtr, ytr)
    print(f"{nombre:20s} exactitud {modelo.score(Xte, yte):.4f}  fit {time.perf_counter() - t:.3f} s")
```

```python
# Keras: y = 2x con semilla, épocas necesarias, error de la lista y digits (10 semillas, ≈ 1.5 min en CPU)
import numpy as np
import tensorflow as tf
import keras
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([2.0, 4.0, 6.0, 8.0])

def nuevo():
    m = tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)), tf.keras.layers.Dense(1)])
    m.compile(optimizer="sgd", loss="mse")
    return m

def entrenar(epocas):
    keras.utils.set_random_seed(0)
    m = nuevo()
    m.fit(X, y, epochs=epocas, verbose=0)
    return m

pred = lambda m: float(m.predict(np.array([5.0]), verbose=0)[0, 0])
m = entrenar(200)
print("200 épocas -> pred", round(pred(m), 4))
m.save("modelo_keras.keras")
print("recargado:", round(pred(tf.keras.models.load_model("modelo_keras.keras")), 6))
print("1600 épocas -> pred", round(pred(entrenar(1600)), 4))

try:
    nuevo().fit([1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.0], epochs=1, verbose=0)
except ValueError as e:
    print("lista plana ->", str(e).splitlines()[0])

print("GPU que ve TensorFlow:", tf.config.list_physical_devices("GPU"))

d = load_digits()
Xtr, Xte, ytr, yte = train_test_split(d.data / 16.0, d.target, test_size=0.2, random_state=42)
accs = []
for semilla in range(10):
    keras.utils.set_random_seed(semilla)
    clf = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    clf.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    clf.fit(Xtr, ytr, epochs=20, verbose=0)
    accs.append(clf.evaluate(Xte, yte, verbose=0)[1])
print("digits: media %.4f, mín %.4f, máx %.4f, parámetros %d" % (np.mean(accs), min(accs), max(accs), clf.count_params()))
```

```python
# PyTorch: y = 2x con semilla, 30 semillas, error de zero_grad, guardado y digits (10 semillas)
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]])

def entrenar(pasos, semilla=0, zero_grad=True):
    torch.manual_seed(semilla)
    m = nn.Linear(1, 1)
    opt = torch.optim.SGD(m.parameters(), lr=0.01)
    perdida = nn.MSELoss()
    for _ in range(pasos):
        if zero_grad:
            opt.zero_grad()
        perdida(m(X), y).backward()
        opt.step()
    return m

pred = lambda m: m(torch.tensor([[5.0]])).item()
for pasos in (200, 1600):
    print(pasos, "pasos -> pred", round(pred(entrenar(pasos)), 4))
p = np.array([pred(entrenar(200, s)) for s in range(30)])
print("30 semillas: media %.4f, mín %.4f, máx %.4f" % (p.mean(), p.min(), p.max()))
print("sin zero_grad (semilla 0):", round(pred(entrenar(200, 0, zero_grad=False)), 4))

m = entrenar(200)
torch.save(m.state_dict(), "modelo_torch.pt")
m2 = nn.Linear(1, 1)
m2.load_state_dict(torch.load("modelo_torch.pt", weights_only=True))
print("recargado:", round(pred(m2), 6))
for nombre, x in [("lista", [[5.0]]), ("float64", torch.tensor([[5.0]], dtype=torch.float64))]:
    try:
        m(x)
    except (TypeError, RuntimeError) as e:
        print(nombre, "->", type(e).__name__, str(e).splitlines()[0][:90])
print("cuda:", torch.cuda.is_available(), "| build CUDA:", torch.version.cuda)

d = load_digits()
Xtr, Xte, ytr, yte = train_test_split(d.data / 16.0, d.target, test_size=0.2, random_state=42)
Xtr, Xte = torch.tensor(Xtr, dtype=torch.float32), torch.tensor(Xte, dtype=torch.float32)
ytr, yte = torch.tensor(ytr), torch.tensor(yte)
accs = []
for semilla in range(10):
    torch.manual_seed(semilla)
    red = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
    opt = torch.optim.Adam(red.parameters(), lr=1e-3)
    perdida = nn.CrossEntropyLoss()
    for _ in range(20):
        orden = torch.randperm(len(Xtr))
        for i in range(0, len(orden), 32):
            lote = orden[i:i + 32]
            opt.zero_grad()
            perdida(red(Xtr[lote]), ytr[lote]).backward()
            opt.step()
    with torch.no_grad():
        accs.append((red(Xte).argmax(1) == yte).float().mean().item())
print("digits: media %.4f, mín %.4f, máx %.4f, parámetros %d" % (np.mean(accs), min(accs), max(accs), sum(q.numel() for q in red.parameters())))
```

---

## 5. Afirmaciones frecuentes en el foro: ¿se sostienen?

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| «Keras acepta listas como scikit-learn» | No (Keras 3) | `ValueError: Unrecognized data type` (sección 4.4) |
| «scikit-learn no usa GPU» | Casi: no hay soporte general, sí uno experimental y parcial | Array API: `Ridge(solver="svd")` devolvió un tensor de PyTorch; `LinearRegression` y KNN fallaron con tensores y no figuran en la lista de la documentación. Requiere `SCIPY_ARRAY_API=1` y `array_api_dispatch=True`. En GPU, solo por documentación, no se ejecutó |
| «TensorFlow es la opción para usar GPU» | Depende del sistema | Linux o WSL2, sí; Windows nativo con TF ≥ 2.11, no (medido: `[]` y el aviso de la propia librería) |
| «PyTorch es solo para investigación» | Falso, pero con matiz | Se despliega (sección 4.5), aunque TorchScript está en desuso y TorchServe en mantenimiento limitado (salvedad 4) |
| «TensorFlow usa grafos estáticos y PyTorch dinámicos» | Desactualizado | En TF 2 `tf.executing_eagerly()` es `True`; `fit` compila el paso a grafo internamente (salvedad 8) |
| «Una red neuronal siempre da mejor exactitud» | No | `digits`: KNN 0.983 y regresión logística 0.967 frente a Keras 0.958 (sección 4.3) |
| «Si `cuda.is_available()` da `False`, no hay GPU» | No necesariamente | Aquí hay GPU NVIDIA y da `False` por la *build* `+cpu` |
| «El resultado de `y = 2x` debe ser exactamente 10» | Solo en scikit-learn | Keras y PyTorch dan 9.4–10.2 según la inicialización (sección 4.1) |
| «Scikit-learn está construido sobre NumPy, SciPy y matplotlib» | Parcial | Dependencias declaradas: NumPy, SciPy, `joblib`, `narwhals`, `threadpoolctl`; matplotlib es opcional (salvedad 6) |

---

## 6. Salvedades que conviene conocer

1. **Ejemplo extra 1 del notebook del profesor.** En `Semana_taller_01_profesor.ipynb` (celda de texto con índice 7) se dice «`w ≈ 2.98`, `b ≈ 5.13`»; con los 10 datos fijos de la celda de código anterior (índice 6) salen `w` = 3.0606, `b` = 4.6667, predicción en 11 = 38.33 y `mse` = 0.7697 (a mano: S_xy / S_xx = 252.5 / 82.5). El segundo ejemplo, con semilla 42, sí coincide con lo escrito. Esas celdas (índices 6 a 11) solo están en el `.ipynb`, no en el `.md` ni en el PDF de solución.
2. **«Salida aproximada: 10.0» (diapositivas 12 y 14) y «cercano a 10» (taller 2.1 y 3.2).** Con 200 pasos y tasa 0.01 las redes no llegan a 10: Keras da 9.57–9.90 (siempre por debajo) y PyTorch 9.38–10.17; con semilla 0, 9.77 y 9.58. La diapositiva de PyTorch muestra `10.0`, pero la salida real lleva además `grad_fn=<AddmmBackward0>`. La causa y la corrección están en la sección 4.1. Solo la salida de scikit-learn (`[10.]`) es exacta.
3. **«Iris suele dar 100 %» con `random_state=42`.** Es cierto para esa partición, pero en 100 particiones aleatorias solo el 22 % da 1.0 y la media es 96.0 %. Con 30 flores de prueba, un error cuesta 3.3 puntos.
4. **Despliegue de PyTorch en la retroalimentación general** (`Foro_S3_Retroalimentacion_general.md` cita TorchServe, TorchScript y ONNX). En PyTorch 2.14.0, `torch.jit.script` emite `FutureWarning: torch.jit.script is deprecated. Please switch to torch.compile or torch.export`. TorchServe lleva el aviso oficial «Limited Maintenance» ([documentación](https://docs.pytorch.org/serve/README.html)) y su repositorio fue archivado el 7 de agosto de 2025 ([GitHub](https://github.com/pytorch/serve)). ONNX no se probó. Para el despliegue conviene mencionar `state_dict` más una API, o `torch.export`.
5. **Diapositiva 11 («TensorFlow Serving, Lite, TensorFlow.js»).** TensorFlow Lite pasó a llamarse LiteRT el 4 de septiembre de 2024 ([anuncio de Google](https://developers.googleblog.com/en/tensorflow-lite-is-now-litert/)). TensorFlow Serving y TensorFlow.js no se verificaron.
6. **Diapositiva 9 («construida sobre NumPy, SciPy y matplotlib»).** Las dependencias declaradas de scikit-learn 1.9.1 son NumPy, SciPy, `joblib`, `narwhals` y `threadpoolctl`. Con la importación de matplotlib bloqueada, `LinearRegression` funciona y `ConfusionMatrixDisplay` pide instalarlo. matplotlib es opcional, solo para graficar.
7. **Taller 3.1: «`cuda` será `False` en la mayoría de portátiles sin GPU dedicada».** Aquí hay una GPU NVIDIA (el driver reporta CUDA 13.1) y da `False` igual, porque se instaló la *build* `torch 2.14.0+cpu`. Además, TensorFlow ≥ 2.11 no usa GPU en Windows nativo: lo avisa la propia librería («Please use WSL2 or the TensorFlow-DirectML plugin») y lo dice la guía de instalación ([TensorFlow](https://www.tensorflow.org/install/pip)). Para quien use Windows, la Parte 2 correrá en CPU aunque tenga GPU.
8. **Diapositivas 11 y 13: «grafos de tensores» frente a «*define-by-run*».** La oposición está desactualizada: en TensorFlow 2 el modo por defecto también es inmediato (`tf.executing_eagerly()` = `True`) y `fit` compila el paso de entrenamiento a grafo por dentro (en la corrida aparecieron avisos de *retracing* de `tf.function` al repetir `predict` en un bucle).
9. **Numeración de la «Intervención 2».** El Anexo llama «Intervención 2» a probar el *framework* en tres minutos; el enunciado del foro y las diapositivas llaman «Intervención 2» a las réplicas a dos compañeros. Para calificar conviene decidir qué evidencia corresponde a cada una.
10. **Ejercicio 1.1 del taller.** Es el mismo ejemplo de la diapositiva 10 (mismos datos) y `Semana_taller_01.md` (versión del estudiante) ya trae el código resuelto debajo del `# TU CÓDIGO AQUÍ`; el `.ipynb` del estudiante lo deja en blanco.
11. **Entorno del taller.** `Semana_3_Taller_frameworks/Dockerfile` copia `requirements.txt` pero instala `docker-requirements.txt`, que está en la raíz del repositorio y no en esa carpeta, y su `COPY *.md .` no copia el `.ipynb`; no se probó el *build*. Además `requirements.txt` (`notebook`, `scikit-learn`, `tensorflow`) no incluye `torch`: con solo ese archivo, la Parte 3 falla con `ModuleNotFoundError`. La pregunta de reflexión 0 sugiere justo ese archivo.
12. **Versiones.** La nota del profesor dice «torch 2.13» y el notebook del foro imprime `2.14.0+cpu`. El resumen de participación reporta capturas de estudiantes con scikit-learn 1.6.1, TensorFlow 2.20.0 y PyTorch 2.11.0+cpu (versiones de Colab). Lo medido aquí vale para las versiones instaladas; el aviso de las listas en Keras lo da el profesor desde TF 2.16 (Keras 3) y aquí se comprobó en TF 2.21 con Keras 3.15.1.
13. **Alcance de las mediciones.** Una sola máquina (los tiempos cambian en otra) y una sola partición de `digits`; las 10 semillas de Keras y PyTorch varían la inicialización, no la partición. La GPU no se ejercitó: las tres librerías corrieron en CPU, así que lo dicho sobre GPU viene de la documentación, el aviso de TensorFlow y la prueba de Array API con tensores en CPU. El criterio «comunidad y documentación» no se puede medir con código.
