# ¿Cuál es la matemática detrás de la regresión lineal?
# https://platzi.com/blog/cual-es-la-matematica-detras-de-la-regresion-lineal/

import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

path = r"/Semana_8/StudentsPerformance.csv"

with open(path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

def col(name):
    return np.array([float(r[name]) for r in rows])

math = col("math score")
reading = col("reading score")
writing = col("writing score")

print("=" * 70)
print("1) REGRESION SIMPLE: reading ~ math  (para comparar con el calculo a mano)")
print("=" * 70)
X = math.reshape(-1, 1)
y = reading
model = LinearRegression()
model.fit(X, y)
pred = model.predict(X)
print(f"b0 (intercept_) = {model.intercept_:.4f}")
print(f"b1 (coef_[0])   = {model.coef_[0]:.4f}")
print(f"r2 (score)      = {model.score(X, y):.4f}")
print(f"r2 (r2_score)   = {r2_score(y, pred):.4f}")
print(f"RMSE            = {np.sqrt(mean_squared_error(y, pred)):.4f}")

print()
print("=" * 70)
print("2) REGRESION MULTIPLE: writing ~ math + reading")
print("=" * 70)
X2 = np.column_stack([math, reading])
y2 = writing
model2 = LinearRegression()
model2.fit(X2, y2)
pred2 = model2.predict(X2)
print(f"b0 (intercept_)              = {model2.intercept_:.4f}")
print(f"b_math  (coef_[0])           = {model2.coef_[0]:.4f}")
print(f"b_reading (coef_[1])         = {model2.coef_[1]:.4f}")
print(f"r2 (score)                   = {model2.score(X2, y2):.4f}")
print(f"RMSE                         = {np.sqrt(mean_squared_error(y2, pred2)):.4f}")

print()
print("Ecuacion: writing_pred = {:.3f} + {:.3f}*math + {:.3f}*reading".format(
    model2.intercept_, model2.coef_[0], model2.coef_[1]))

print()
print("=" * 70)
print("3) Prediccion de ejemplo: estudiante con math=80, reading=85")
print("=" * 70)
ejemplo = np.array([[80, 85]])
pred_ejemplo = model2.predict(ejemplo)
print(f"writing predicho = {pred_ejemplo[0]:.2f}")

print()
print("=" * 70)
print("4) Primeras 5 predicciones vs valores reales (regresion multiple)")
print("=" * 70)
for i in range(5):
    print(f"math={math[i]:.0f} reading={reading[i]:.0f}  writing_real={writing[i]:.0f}  writing_pred={pred2[i]:.2f}  residuo={writing[i]-pred2[i]:.2f}")
