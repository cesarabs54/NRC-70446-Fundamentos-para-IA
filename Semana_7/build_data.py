"""
Genera data.js a partir de StudentsPerformance.csv (mismo dataset usado en
Semana 6 y en los documentos conceptuales de Semana 7) para los cuatro
módulos interactivos de regresión lineal.

Filtra a los casos completos y escribe un arreglo JS compacto, listo para
cargarse con <script src="data.js"> (sin fetch, sin problemas de CORS al abrir
index.html directamente con file://).

Uso:
    python build_data.py
"""
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.parent.parent
CSV_PATH = REPO_ROOT / "Semana_7" / "StudentsPerformance.csv"
OUTPUT_JS = BASE_DIR / "data.js"

NUMERIC_COLUMNS = ["math score", "reading score", "writing score"]
CATEGORICAL_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]
# Claves JS cortas, sin espacios ni barras, para cada columna original.
KEY_MAP = {
    "gender": "gender",
    "race/ethnicity": "ethnicity",
    "parental level of education": "parentEducation",
    "lunch": "lunch",
    "test preparation course": "testPrep",
    "math score": "mathScore",
    "reading score": "readingScore",
    "writing score": "writingScore",
}


def main():
    df = pd.read_csv(CSV_PATH)
    subset = df[NUMERIC_COLUMNS + CATEGORICAL_COLUMNS].dropna()
    subset = subset.astype({c: "int64" for c in NUMERIC_COLUMNS})
    subset = subset.rename(columns=KEY_MAP)

    records = subset.to_dict(orient="records")

    js = "// Generado por build_data.py a partir de StudentsPerformance.csv — no editar a mano.\n"
    js += f"const STUDENTS_DATA = {json.dumps(records, separators=(',', ':'), ensure_ascii=False)};\n"
    OUTPUT_JS.write_text(js, encoding="utf-8")

    print(f"Escrito {OUTPUT_JS} con {len(records)} registros.")


if __name__ == "__main__":
    main()
