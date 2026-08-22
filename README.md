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
1. Define el contrato de tus datos (en español primero).
2. Escríbelo en `src/schema.py` con pandera.
3. Mete el guardia en `cargar()` dentro de `entrenar.py`.
4. Crea `src/romper_datos.py`: corrompe los datos a propósito y demuestra que el contrato los atrapa.
5. Documenta en tu README y trabaja con ≥5 commits.

El profesor evaluará tu contrato contra un lote real del proveedor que no has visto.
