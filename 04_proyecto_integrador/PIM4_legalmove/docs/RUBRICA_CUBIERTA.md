# Rúbrica cubierta

| Criterio | Implementación | Evidencia rápida |
|---|---|---|
| Imagen a texto con GPT-4o Vision | `src/image_parser.py` | Base64, MIME, validación e `input_image` en Responses API. |
| Dos agentes LangChain | `src/agents/` | Roles `Analista Senior de Contratos` y `Auditor Legal`. |
| Handoff entre agentes | `src/pipeline.py` | `mapa_contextual` pasa al extractor junto con los dos textos. |
| Structured output | `src/agents/extraction_agent.py` | `ProviderStrategy(ContractChangeOutput, strict=True)`. |
| Pydantic estricto | `src/models.py` | Tres campos exactos, sin extras, listas no vacías y limpieza. |
| Validación final | `src/pipeline.py` | `ContractChangeOutput.model_validate()` en `pydantic_validation`. |
| Observabilidad Langfuse v4 | `src/observability.py` | `start_as_current_observation()` y callback LangChain. |
| Jerarquía de trazas | `src/pipeline.py` | Traza raíz `contract-analysis` y cinco etapas. |
| CLI ejecutable | `src/main.py` | `python -m src.main contrato.png adenda.png`. |
| Dos casos de prueba | `data/test_contracts/` | Caso simple y complejo con imágenes y `expected.json`. |
| Manejo de errores | `src/errors.py`, `src/image_parser.py` | Imagen inválida, timeout, límite, red y respuesta vacía. |
| Pruebas sin APIs | `tests/` | Ejecutar `pytest -q`: clientes y trazas simulados. |
| Documentación de defensa | `README.md`, `docs/GUIA_DEFENSA_30_MIN.md` | Instalación, demo, decisiones y preguntas frecuentes. |

La validación humana consiste en ejecutar ambos casos con credenciales reales y revisar en Langfuse la traza y sus generaciones hijas.
