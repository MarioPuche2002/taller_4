import pandera.pandas as pa
from pandera.pandas import Column, Check, DataFrameSchema

BODEGAS_VALIDAS = ["BOG-01", "BAQ-04", "CAL-03", "MED-02"]

schema_sensores = DataFrameSchema(
    {
        "fecha": Column(
            str,
            checks=Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"),
            nullable=False,
            coerce=False,
        ),
        "bodega_id": Column(
            str,
            checks=Check.isin(BODEGAS_VALIDAS),
            nullable=False,
            coerce=False,
        ),
        "temperatura_c": Column(
            float,
            checks=Check.in_range(-30.0, 45.0),
            nullable=False,
            coerce=True,
        ),
        "humedad_pct": Column(
            float,
            checks=Check.in_range(0, 100),
            nullable=False,
            coerce=True,
        ),
        "ocupacion_pct": Column(
            float,
            checks=Check.in_range(0, 100),
            nullable=False,
            coerce=True,
        ),
        "alertas_dia": Column(
            float,
            checks=[Check.ge(0), Check.le(50)],
            nullable=False,
            coerce=True,
        ),
        "consumo_kwh": Column(
            float,
            checks=[Check.gt(0), Check.le(10000)],
            nullable=False,
            coerce=True,
        ),
    },
    strict=True,
    ordered=False,
)
