import sys
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import pandera.pandas as pa

from schema import schema_sensores

RUTA = Path(__file__).parent.parent / "data" / "sensores.csv"


def cargar(ruta=RUTA):
    df = pd.read_csv(ruta)
    try:
        df_validado = schema_sensores.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        print("EL GUARDIA DETUVO EL LOTE: los datos no cumplen el contrato.")
        print(f"Filas del lote: {len(df)} | Errores encontrados: {len(err.failure_cases)}")
        print(err.failure_cases.to_string(index=False))
        sys.exit(1)
    return df_validado


def main():
    df = cargar()
    features = ["bodega_id", "temperatura_c", "humedad_pct", "ocupacion_pct", "alertas_dia"]
    X, y = df[features], df["consumo_kwh"]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["bodega_id"]),
        ("num", StandardScaler(), ["temperatura_c", "humedad_pct", "ocupacion_pct", "alertas_dia"]),
    ])
    modelo = Pipeline([("pre", pre), ("reg", LinearRegression())])
    corte = len(df) - 40
    modelo.fit(X.iloc[:corte], y.iloc[:corte])
    mae = mean_absolute_error(y.iloc[corte:], modelo.predict(X.iloc[corte:]))
    print(f"Lote validado OK ({len(df)} filas). MAE: {mae:.0f} kWh")


if __name__ == "__main__":
    main()
