# Taller — Primeros pasos con Scikit-learn, TensorFlow y PyTorch
### Versión ESTUDIANTE

**Instrucciones generales:**
- Trabaja en un notebook de Jupyter (Colab o local) con `scikit-learn`, `tensorflow` y `torch` instalados.
- Donde veas `# TU CÓDIGO AQUÍ`, reemplázalo por tu solución.
- Responde las preguntas de reflexión en una celda de texto (Markdown), no como comentario de código.
- Duración estimada: 60-90 minutos.
- Este taller retoma la actividad del anexo ("probar el *framework* en 3 minutos") y los criterios técnicos vistos en la Semana 3 (preprocesamiento, soporte GPU/rendimiento, facilidad de entrenamiento, interpretabilidad, comunidad/documentación e integración para despliegue).

---

## Paso 0 — Preparación: confirmar que los tres *frameworks* están disponibles

```python
import sklearn
import tensorflow as tf
import torch

print("scikit-learn:", sklearn.__version__)
print("tensorflow:", tf.__version__)
print("torch:", torch.__version__)
```

**Pregunta de reflexión 0:** Si alguno de los tres imports falla, ¿qué comando usarías para instalarlo? (pista: `pip install ...`)

---

## Parte 1 — Scikit-learn: machine learning clásico

### Ejercicio 1.1 — Regresión lineal simple

Entrena un modelo de regresión lineal con estos datos y predice el valor para `X = 5`.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X = [[1], [2], [3], [4]]
y = [2, 4, 6, 8]

# TU CÓDIGO AQUÍ
# 1. Crea el modelo (LinearRegression)
# 2. Entrénalo con fit(X, y)
# 3. Predice el valor para X=5
# 4. Calcula el error (mean_squared_error) sobre los datos de entrenamiento
```

### Ejercicio 1.2 — Clasificación con datos reales (Iris)

Carga el dataset `iris` (incluido en scikit-learn), separa entrenamiento/prueba y entrena un clasificador `KNeighborsClassifier`.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()

# TU CÓDIGO AQUÍ
# 1. Divide iris.data / iris.target en train/test (train_test_split, test_size=0.2)
# 2. Crea un KNeighborsClassifier(n_neighbors=3) y entrénalo
# 3. Predice sobre el conjunto de prueba
# 4. Calcula el accuracy con accuracy_score
```

**Pregunta de reflexión 1:** ¿Qué tan fácil te resultó pasar de "tener los datos" a "tener un modelo entrenado" con scikit-learn? ¿Podrías explicar, en una frase, por qué el modelo tomó cada decisión (interpretabilidad)?

---

## Parte 2 — TensorFlow/Keras: deep learning de alto nivel

### Ejercicio 2.1 — Red neuronal de regresión

Construye una red con una sola neurona que aprenda la misma relación del Ejercicio 1.1 (`y = 2x`).

```python
import numpy as np
import tensorflow as tf

X = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([2.0, 4.0, 6.0, 8.0])

# TU CÓDIGO AQUÍ
# 1. Crea un tf.keras.Sequential con una capa Input(shape=(1,)) y una Dense(1)
# 2. Compílalo con optimizer="sgd" y loss="mse"
# 3. Entrénalo con fit(X, y, epochs=200)
# 4. Predice el valor para X=5
```

> **Nota:** a diferencia de scikit-learn, Keras espera que los datos vengan como arrays de NumPy (`np.array(...)`), no como listas planas de Python.

### Ejercicio 2.2 — Clasificación de imágenes pequeñas (dígitos escritos a mano)

Usa el dataset `load_digits` (imágenes de 8×8 píxeles) para clasificar dígitos del 0 al 9.

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
X = digits.data / 16.0   # normalizamos los píxeles a [0, 1]
y = digits.target

# TU CÓDIGO AQUÍ
# 1. Divide X, y en train/test (test_size=0.2)
# 2. Crea un tf.keras.Sequential:
#    - Input(shape=(64,))
#    - Dense(32, activation="relu")
#    - Dense(10, activation="softmax")
# 3. Compílalo con optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
# 4. Entrénalo con fit(X_train, y_train, epochs=20)
# 5. Evalúalo con evaluate(X_test, y_test)
```

**Pregunta de reflexión 2:** Compara cuántas líneas de código necesitaste para llegar a un modelo entrenado en el Ejercicio 1.2 (scikit-learn) frente al Ejercicio 2.2 (Keras). ¿En qué se nota que TensorFlow está pensado para redes neuronales y scikit-learn para modelos clásicos?

---

## Parte 3 — PyTorch: control explícito del entrenamiento

### Ejercicio 3.1 — Tensores básicos

```python
import torch

# TU CÓDIGO AQUÍ
# 1. Crea un tensor `a` con los valores [1.0, 2.0, 3.0]
# 2. Crea un tensor `b` de unos con torch.ones(3)
# 3. Súmalos e imprime el resultado
# 4. Imprime la forma (shape) de `a`
# 5. Imprime si hay GPU disponible con torch.cuda.is_available()
```

### Ejercicio 3.2 — Bucle de entrenamiento manual

Completa el bucle de entrenamiento para el mismo problema `y = 2x`, pero esta vez con PyTorch, donde cada paso del entrenamiento es explícito.

```python
import torch
import torch.nn as nn

X = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]])

modelo = nn.Linear(1, 1)
opt = torch.optim.SGD(modelo.parameters(), lr=0.01)
perdida = nn.MSELoss()

for _ in range(200):
    # TU CÓDIGO AQUÍ
    # 1. Reinicia los gradientes (opt.zero_grad())
    # 2. Calcula el error: perdida(modelo(X), y)
    # 3. Retropropaga el error (error.backward())
    # 4. Actualiza los pesos (opt.step())

print(modelo(torch.tensor([[5.0]])))
```

**Pregunta de reflexión 3:** En Keras, todo el entrenamiento ocurre dentro de una sola línea (`model.fit(...)`). En PyTorch tuviste que escribir cada paso (`zero_grad`, `backward`, `step`). ¿Qué ventaja y qué desventaja le ves a esta diferencia?

---

## Parte 4 — Reto integrador (opcional)

Resolviste el mismo problema (`y = 2x`) con los tres *frameworks*: scikit-learn (Ejercicio 1.1), TensorFlow (Ejercicio 2.1) y PyTorch (Ejercicio 3.2).

Completa esta tabla comparativa con tu propia experiencia:

| Criterio | Scikit-learn | TensorFlow | PyTorch |
|---|---|---|---|
| Líneas de código aproximadas | | | |
| Facilidad de entrenamiento (1-5) | | | |
| Nivel de control sobre el entrenamiento (1-5) | | | |
| ¿Lo usarías para un modelo en producción? | | | |

**Pregunta de cierre:** Retomando la pregunta orientadora del foro: según lo que hiciste en este taller, ¿qué criterio técnico (preprocesamiento, soporte GPU/rendimiento, facilidad de entrenamiento, interpretabilidad, comunidad/documentación o integración para despliegue) pesaría más para ti al elegir un *framework*, según el tipo de problema y los datos disponibles?
