# Datos de prueba — PIM4 LegalMove

Este directorio contiene **2 pares de contratos** (4 imágenes PNG) para probar el pipeline.

## Estructura

```
test_contracts/
├── pair1_simple/              # Par 1: cambios simples
│   ├── contrato_original.png   # Contrato de servicios (4 cláusulas)
│   ├── adenda_simple.png       # Adenda que modifica 1 cláusula (duración)
│   └── expected.json           # Golden case: resultado esperado
├── pair2_complex/              # Par 2: cambios complejos
│   ├── contrato_original.png   # Contrato de confidencialidad (3 cláusulas)
│   ├── adenda_compleja.png     # Adenda con 3 tipos de cambio
│   └── expected.json           # Golden case: resultado esperado
├── generate_data.py            # Script que regenera las imágenes
└── README.md                   # Este archivo
```

## Par 1 — Cambios simples

**Contrato:** Comercial de servicios (4 cláusulas: pago, duración, territorio, confidencialidad).

**Adenda:** Modifica únicamente la cláusula 2 (duración: 12 → 18 meses).

| Tipo de cambio | Cláusula | Detalle |
|---|---|---|
| Modificación | 2 | Duración: 12 → 18 meses |

**Resultado esperado:**
```json
{
  "sections_changed": ["duration"],
  "topics_touched": ["duracion contractual"],
  "summary_of_the_change": "La duracion del contrato se extiende de 12 a 18 meses."
}
```

## Par 2 — Cambios complejos

**Contrato:** Confidencialidad (3 cláusulas: territorio, restricción de uso, duración).

**Adenda:** 3 tipos de cambio distintos (adición, eliminación, modificación).

| Tipo de cambio | Cláusula | Detalle |
|---|---|---|
| Modificación | 1 | Alcance: Argentina → Argentina + Uruguay + Paraguay |
| Eliminación | 2 | Se remueve la restricción de uso |
| Adición | 4 (nueva) | Difusión controlada a subcontratistas |

**Resultado esperado:**
```json
{
  "sections_changed": ["service_territory", "use_restriction", "controlled_disclosure"],
  "topics_touched": ["alcance territorial", "restriccion de uso", "difusion controlada a terceros"],
  "summary_of_the_change": "Modificacion: el alcance territorial se amplia..."
}
```

## Regenerar las imágenes

```bash
python data/test_contracts/generate_data.py
```

Las imágenes se generan con Pillow (PIL) dibujando texto sobre un lienzo blanco, simulando documentos escaneados.
