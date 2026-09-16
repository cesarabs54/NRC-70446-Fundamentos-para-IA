"""
Genera data.js a partir de StudentsPerformance.csv (dataset de Kaggle usado en
el estudio de caso de Semana 2) para los módulos interactivos.

Filtra a las columnas relevantes y escribe un arreglo JS compacto, listo para
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
STUDENTS_CSV = REPO_ROOT / "Semana_2" / "Semana_2_Actividad" / "StudentsPerformance.csv"
OUTPUT_JS = BASE_DIR / "data.js"

RENAME = {
    "gender": "gender",
    "race/ethnicity": "group",
    "parental level of education": "parentalEducation",
    "lunch": "lunch",
    "test preparation course": "testPrep",
    "math score": "mathScore",
    "reading score": "readingScore",
    "writing score": "writingScore",
}


def main():
    df = pd.read_csv(STUDENTS_CSV)
    df = df.rename(columns=RENAME)[list(RENAME.values())]

    df = df.astype({
        "mathScore": "int64",
        "readingScore": "int64",
        "writingScore": "int64",
    })

    records = df.to_dict(orient="records")

    js = "// Generado por build_data.py a partir de StudentsPerformance.csv — no editar a mano.\n"
    js += f"const STUDENTS_DATA = {json.dumps(records, separators=(',', ':'))};\n"
    OUTPUT_JS.write_text(js, encoding="utf-8")

    print(f"Escrito {OUTPUT_JS} con {len(records)} registros.")
    print(f"Nulos por columna:\n{df.isnull().sum().to_string()}")
    print(f"Duplicados: {df.duplicated().sum()}")


if __name__ == "__main__":
    main()
