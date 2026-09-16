"""
Genera data.js a partir de titles.csv (dataset de Netflix usado en el taller
de Semana 4) para el módulo interactivo de correlación y prueba t.

Filtra a los casos completos en las columnas necesarias y escribe un arreglo
JS compacto, listo para cargarse con <script src="data.js"> (sin fetch, sin
problemas de CORS al abrir index.html directamente con file://).

Uso:
    python build_data.py
"""
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.parent.parent
TITLES_CSV = REPO_ROOT / "Semana_4" / "Semana_4_Actividad" / "titles.csv"
OUTPUT_JS = BASE_DIR / "data.js"

COLUMNS = ["type", "imdb_score", "tmdb_score", "runtime", "imdb_votes", "release_year"]


def main():
    df = pd.read_csv(TITLES_CSV)
    subset = df[COLUMNS].dropna()

    subset = subset.astype({
        "imdb_score": "float64",
        "tmdb_score": "float64",
        "runtime": "int64",
        "imdb_votes": "int64",
        "release_year": "int64",
    })

    records = subset.to_dict(orient="records")

    js = "// Generado por build_data.py a partir de titles.csv — no editar a mano.\n"
    js += f"const NETFLIX_DATA = {json.dumps(records, separators=(',', ':'))};\n"
    OUTPUT_JS.write_text(js, encoding="utf-8")

    print(f"Escrito {OUTPUT_JS} con {len(records)} registros.")
    print(subset["type"].value_counts().to_string())


if __name__ == "__main__":
    main()
