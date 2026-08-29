# Taller Semana 4 — El guardia que faltaba 🛡️

Este repositorio implementa un pipeline de Machine Learning robusto para predecir el consumo energético de una red de bodegas (`consumo_kwh`), incorporando un contrato de datos estricto mediante **Pandera** para evitar el entrenamiento con datos corruptos, incompletos o fuera de rango.

## Estructura del Proyecto

contrato-datos-ml/
├── ENUNCIADO_TALLER.md  
├── data/
│   ├── sensores.csv    
│   └── sensores_corruptos.csv 
├── src/
│   ├── schema.py        
│   ├── entrenar.py       
│   └── romper_datos.py  
├── requirements.txt
└── README.md

## Requisitos y Configuración

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd src
python entrenar.py
python romper_datos.py
```

---

## El Contrato de Datos (`src/schema.py`)

Se define un esquema formal con `pandera` que valida rigurosamente cada lote de datos antes de permitir que llegue al modelo de regresión lineal. Las reglas en el guardia son:

| Columna | Tipo | Regla | Justificación |
| --- | --- | --- | --- |
| `fecha` | String | Formato `AAAA-MM-DD`, no nula | Indispensable para mantener la trazabilidad temporal. |
| `bodega_id` | Categoría | Valores permitidos: `BOG-01`, `BAQ-04`, `CAL-03`, `MED-02`, no nula | Rechaza bodegas fantasma o errores tipográficos del proveedor. |
| `temperatura_c` | Float | Rango entre `-30` y `45`, no nula | Acota la realidad física de la red de frío y atrapa sensores dañados (ej. valores de `999`). |
| `humedad_pct` | Float | Rango entre `0` y `100`, no nula | Limita la métrica estrictamente a porcentajes válidos. |
| `ocupacion_pct` | Float | Rango entre `0` y `100`, no nula | Garantiza coherencia en la capacidad de almacenamiento. |
| `alertas_dia` | Float / Int | Rango entre `0` y `50`, no nula | Previene conteos negativos absurdos y establece un techo operativo realista. |
| `consumo_kwh` | Float | Mayor a `0` y hasta `10000`, no nula | Variable objetivo del modelo; siempre debe reflejar un consumo positivo. |

La validación utiliza `lazy=True`. Esto significa que si un lote presenta múltiples fallos, el script no se detiene en el primer error, sino que recopila un reporte consolidado con todas las filas, columnas y valores problemáticos.
---

## Prueba de Corrupción (`src/romper_datos.py`)

Para verificar la efectividad de la validación, el script `romper_datos.py` inyecta a propósito **5 anomalías críticas** en distintas filas de `sensores.csv`:

1. **Fuera de rango:** `temperatura_c = 999` (Fila 0).
2. **Categoría inválida:** `bodega_id = "XXX-99"` (Fila 5).
3. **Nulo silencioso:** `alertas_dia = NaN` (Fila 10).
4. **Error de tipado:** `consumo_kwh = "mil doscientos"` (Fila 15).
5. **Fuera de rango superior:** `humedad_pct = 150` (Fila 20).
---

## Análisis Técnico: El Límite del Contrato (Unidades y Escalas)

> **¿Qué pasaría si el proveedor envía la temperatura en Fahrenheit en lugar de Celsius?**

El contrato actual **no detectaría** este error por sí solo. El esquema valida que `temperatura_c` esté `in_range(-30, 45)`. Si una lectura real en Fahrenheit (por ejemplo, `40 °F`) se interpreta numéricamente como Celsius, pero no es la unidad correcta o la escala correcta.