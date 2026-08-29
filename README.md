# Taller Semana 4 — El guardia que faltaba 🛡️

**Empieza leyendo [`ENUNCIADO_TALLER.md`](ENUNCIADO_TALLER.md).**

## Qué hay aquí
```
contrato-datos-ml/
├── ENUNCIADO_TALLER.md   <- LÉEME PRIMERO
├── data/sensores.csv     <- los datos (una muestra de la red de bodegas)
├── src/entrenar.py       <- el pipeline del analista: entrena pero NO valida nada
├── requirements.txt
└── README.md
```

## Arranque
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/entrenar.py           # corre el pipeline actual (sin validación)
```

## Tu trabajo (resumen — el detalle está en el ENUNCIADO)
2. Escríbelo en `src/schema.py` con pandera.
3. Mete el guardia en `cargar()` dentro de `entrenar.py`.
4. Crea `src/romper_datos.py`: corrompe los datos a propósito y demuestra que el contrato los atrapa.
5. Documenta en tu README y trabaja con ≥5 commits.

El profesor evaluará tu contrato contra un lote real del proveedor que no has visto.

**Fase 1 — Conocer los datos y su contrato.**

Cada fila de `sensores.csv` es la lectura de UNA bodega en UN dia. Para que
el pipeline de consumo energetico entrene con datos que tienen sentido
fisico y de negocio, TODA fila debe cumplir:

- fecha
    Texto con formato AAAA-MM-DD. Nunca debe estár vacia (sin fecha no hay lectura).

- bodega_id
    Texto categorico. Solo puede ser una de las bodegas que SI existen hoy
    en la red: BOG-01, BAQ-04, CAL-03, MED-02. Nunca debe estár vacia.

- temperatura_c
    Numero decimal, en grados Celsius. Una bodega de red de frio se mueve en un rango  entre -30C y 45C  Un valor por ejemplo de 999 de un (sensor danado) queda claramente afuera. Nunca debe estár vacia.

- humedad_pct
    Numero, en porcentaje. Por definicion de porcentaje, entre 0 y 100.Nunca debe estár vacia.

- ocupacion_pct
    Numero, en porcentaje. Igual que humedad: entre 0 y 100. Nunca debe estár vacia.

- alertas_dia
    Numero entero, conteo de alertas del dia. No puede ser negativo (no
    existen "-2 alertas"). Se acota a 50. Nunca debe estár vacia.

- consumo_kwh
    Numero, el consumo energetico del dia en kWh , es la variable objetivo
    del modelo. Debe ser positiva.
