import sys
from pathlib import Path

import pandas as pd
import pandera.pandas as pa

from schema import schema_sensores

RUTA_ORIGINAL = Path(__file__).parent.parent / "data" / "sensores.csv"
RUTA_CORRUPTA = Path(__file__).parent.parent / "data" / "sensores_corruptos.csv"


def corromper(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.loc[0, "temperatura_c"] = 999

    df.loc[5, "bodega_id"] = "XXX-99"

    df.loc[10, "alertas_dia"] = None

    df["consumo_kwh"] = df["consumo_kwh"].astype(object)
    df.loc[15, "consumo_kwh"] = "mil doscientos"

    df.loc[20, "humedad_pct"] = 150

    return df


def main():
    df = pd.read_csv(RUTA_ORIGINAL)
    df_corrupto = corromper(df)
    df_corrupto.to_csv(RUTA_CORRUPTA, index=False)
    print(f"Lote corrupto guardado en: {RUTA_CORRUPTA}")
    print("Corrupciones plantadas: fila 0 (temperatura=999), "
          "fila 5 (bodega_id inexistente), fila 10 (alertas_dia nulo), "
          "fila 15 (consumo_kwh como texto), fila 20 (humedad_pct=150).")
    print()

    try:
        schema_sensores.validate(df_corrupto, lazy=True)
        print("ERROR: el contrato NO detecto ningun problema. Revisa el schema.")
        sys.exit(1)
    except pa.errors.SchemaErrors as err:
        print(f"El contrato atrapo {len(err.failure_cases)} problema(s):\n")
        print(err.failure_cases.to_string(index=False))


if __name__ == "__main__":
    main()
