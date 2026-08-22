# Taller Semana 4 — "El guardia que faltaba" 🛡️📦

## El contexto

Trabajas en el equipo de datos de **una operadora logística que administra la red de frío
de cientos de bodegas** por todo el país. Cada bodega manda todos los días sus lecturas de
sensores (temperatura, humedad, ocupación, alertas) y con eso un modelo predice el
**consumo energético** para planear la operación y detectar desperdicio.

El analista junior (sí, el mismo) dejó el pipeline andando. Entrena bien, predice bien…
**mientras los datos vengan limpios.** Pero los datos los manda un proveedor externo, y los
proveedores externos cambian cosas sin avisar: un sensor se daña y manda 999, alguien
reporta humedad de 150%, aparece una bodega que no existe. El pipeline del analista **no
valida nada** — se traga la basura, entrena con ella y produce predicciones absurdas con
total confianza. Nadie se entera hasta que la factura de energía no cuadra.

Tu misión: **ponerle un contrato de datos al pipeline** para que la basura se detenga en la
puerta, y demostrar que funciona metiéndole datos corruptos a propósito.

## La escala real

El CSV que recibes (`data/sensores.csv`) es una muestra. En producción, este pipeline
ingiere el lote diario de cientos de bodegas, automáticamente, sin que nadie mire fila por
fila. Por eso la validación tiene que ser **código que corre solo** en cada ingesta — no una
revisión manual. Un contrato bien escrito es lo que separa "nos dimos cuenta a tiempo" de
"lo descubrimos en la factura del mes".

## Misión

**Fase 1 — Conocer los datos y su contrato.**
Explora `sensores.csv` y define, en español primero, las reglas que estos datos SIEMPRE
deben cumplir. Piensa en cada columna:
- ¿Qué tipo es? ¿Puede venir vacía?
- Si es número, ¿en qué rango tiene sentido? (una temperatura de red de frío no es 999; una
  humedad o una ocupación en % viven entre 0 y 100)
- Si es categórica, ¿cuál es la lista cerrada de valores válidos? (las bodegas que existen)

**Fase 2 — Escribir el schema pandera.**
Traduce esas reglas a un `schema.py` con `pa.DataFrameSchema`. Usa los checks que
correspondan: `in_range`, `isin`, `gt`/`ge`, `nullable=False`. Cada columna, su tipo y sus
reglas.

**Fase 3 — Poner el guardia en la puerta.**
Integra la validación al inicio del pipeline: modifica la función `cargar()` en
`entrenar.py` para que valide con el schema (usando `lazy=True`) ANTES de devolver los
datos. Si los datos no cumplen, el pipeline debe detenerse con un reporte claro.

**Fase 4 — Probar que el contrato funciona (¡lo divertido!).**
Crea un script `romper_datos.py` que tome `sensores.csv`, le meta **al menos 4 tipos de
corrupción distintos a propósito** (un valor fuera de rango, una categoría inválida, un
nulo, un tipo equivocado…), guarde el resultado, e intente validarlo. Debe imprimir el
reporte de `failure_cases` mostrando que tu contrato atrapó cada problema, con su fila.
Documenta en el README qué corrompiste y qué atrapó el contrato.

## Entregable

```
contrato-datos-ml/
├── data/sensores.csv
├── src/
│   ├── schema.py        # tu contrato de datos (Fase 2)
│   ├── entrenar.py      # con cargar() validando (Fase 3)
│   └── romper_datos.py  # la prueba de que el contrato atrapa basura (Fase 4)
├── requirements.txt
└── README.md            # con "El contrato" y "Prueba de corrupción"
```

Más **≥5 commits** que narren el proceso.

## Cómo se evalúa (examen oculto)

Al final, el profesor tiene un **lote real del proveedor** (`sensores_lote_proveedor.csv`)
con problemas plantados que tú nunca viste. Ejecutará tu schema contra ese lote. Tu contrato
se mide por:

| Criterio | Peso | Qué se evalúa |
|---|---|---|
| El contrato atrapa la basura del lote oculto | 35% | Tu schema detecta los problemas del CSV del proveedor. Entre más tipos de error atrape, mejor. |
| El guardia está en el pipeline | 25% | cargar() valida con lazy=True ANTES de entrenar; si los datos son malos, se detiene. |
| Prueba de corrupción propia | 20% | romper_datos.py mete ≥4 tipos de corrupción y muestra que el contrato los caza. |
| Calidad + Git | 20% | schema legible, checks correctos por columna, README claro, ≥5 commits. |

## Pistas sin espóiler

- Empieza simple: un schema de solo tipos que ya corra, y ve agregando checks (como en la
  demo). No intentes el contrato perfecto de una.
- Para los rangos, mira los datos reales: `df.describe()` te dice el mínimo y máximo de cada
  columna numérica. El rango del contrato debe ser un poco más amplio que lo observado, pero
  sin dejar pasar imposibles físicos (una humedad de 150% nunca es válida).
- Para `isin`, `df["bodega_id"].unique()` te da la lista de valores que existen hoy.
- Usa SIEMPRE `lazy=True` al validar: quieres ver TODOS los errores del lote de una, no solo
  el primero.
- Cuidado con `nullable`: el nulo silencioso es el error más peligroso. Decide columna por
  columna cuáles pueden venir vacías (casi ninguna debería).
- Prueba tu propio contrato antes de entregar: si tu `romper_datos.py` mete un error y el
  contrato NO lo atrapa, tu schema tiene un hueco. Ahí es donde aprendes.

## La defensa (al cierre)

Prepárate para responder: *"si el proveedor empieza a mandar la temperatura en Fahrenheit
en vez de Celsius, ¿tu contrato lo atraparía? ¿Por qué sí o por qué no?"* — una pregunta
sobre los límites de la validación que vale oro discutir.
