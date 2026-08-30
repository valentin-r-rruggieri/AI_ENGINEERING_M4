# Guía de defensa — 30 minutos

## 0–3 min: problema

LegalMove reduce la revisión manual inicial de una adenda: recibe dos imágenes y devuelve, con un contrato JSON fijo, qué cláusulas cambiaron, qué temas toca la adenda y un resumen trazable.

## 3–8 min: arquitectura

Mostrá el diagrama del README. Explicá que GPT-4o Vision transcribe sin comparar; el primer agente arma contexto; el segundo compara usando ese handoff; Pydantic valida la salida.

## 8–13 min: demo simple

Ejecutá:

```powershell
python -m src.main data/test_contracts/caso_simple/contrato_original.png data/test_contracts/caso_simple/adenda.png
```

Se deben identificar el monto y el vencimiento.

## 13–19 min: demo compleja

Ejecutá el caso complejo. Mostrá que el resumen distingue explícitamente una MODIFICACIÓN territorial, una ELIMINACIÓN de restricción de uso y una ADICIÓN de seguridad.

## 19–23 min: Langfuse

Buscá `contract-analysis`. Recorré las cinco etapas y una generación hija. Señalá input, output, modelo, tokens, latencia, estado y metadata de archivo.

## 23–27 min: código y validación

Abrí `models.py`, `contextualization_agent.py`, `extraction_agent.py` y `pipeline.py`. Corré `pytest -q` para demostrar que los fallos de entrada y el handoff están cubiertos sin API real.

## 27–30 min: preguntas frecuentes

**¿Por qué GPT-4o?** Porque recibe imágenes y texto, útil para contratos escaneados; el prompt exige transcripción fiel.

**¿Por qué dos agentes?** Separar contexto de extracción evita que un solo prompt decida estructura y cambios a la vez. El segundo recibe un artefacto explícito del primero.

**¿Por qué Pydantic si el proveedor ya estructura?** Es una segunda barrera local, controla campos extras y hace estable el contrato que consume otro sistema.

**¿Qué pasa si falta una clave o una imagen?** La CLI informa un mensaje corto por stderr y devuelve código 1. No produce un JSON parcial.

**¿Cómo se protege un contrato real?** Claves solo en `.env`, mínimo registro de datos en Langfuse, acceso restringido, retención definida y revisión humana antes de efectos legales.
