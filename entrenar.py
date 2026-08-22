# pipeline de consumo energetico - red de bodegas
# el analista junior (si, el mismo). esta vez el modelo entrena sin problemas.
# lee los datos, entrena, y predice el consumo. cero validacion porque "los datos vienen bien".
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

RUTA = Path(__file__).parent.parent / "data" / "sensores.csv"

def cargar(ruta=RUTA):
    # ATENCION: aqui no se valida NADA. los datos entran tal cual lleguen.
    return pd.read_csv(ruta)

def main():
    df = cargar()
    features = ["bodega_id","temperatura_c","humedad_pct","ocupacion_pct","alertas_dia"]
    X, y = df[features], df["consumo_kwh"]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["bodega_id"]),
        ("num", StandardScaler(), ["temperatura_c","humedad_pct","ocupacion_pct","alertas_dia"]),
    ])
    modelo = Pipeline([("pre", pre), ("reg", LinearRegression())])
    corte = len(df) - 40
    modelo.fit(X.iloc[:corte], y.iloc[:corte])
    mae = mean_absolute_error(y.iloc[corte:], modelo.predict(X.iloc[corte:]))
    print(f"MAE: {mae:.0f} kWh")

if __name__ == "__main__":
    main()
