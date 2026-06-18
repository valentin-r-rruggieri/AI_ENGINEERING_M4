# PIM4 | Proyecto Integrador LegalMove

## Objetivo

Integrar todo lo aprendido en el módulo en un pipeline real: comparación de contratos con agentes, validación con Pydantic y trazabilidad con spans. Cada ejercicio muestra la versión frágil vs. la versión robusta.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_comparador_basico_vs_agentes.py` | Un prompt monolítico mezcla contextualización y extracción | Dos agentes con responsabilidades separadas |
| `e02_output_libre_vs_pydantic.py` | El agente devuelve texto libre que nadie puede procesar | ContractChangeOutput con Pydantic v2 y validadores de negocio |
| `e03_sin_logs_vs_langfuse.py` | Si el pipeline falla, no sabemos en qué paso | Trazabilidad con spans: input, output y latencia de cada paso |

---

## Cómo ejecutar

Desde la raíz del repositorio:

```bash
python proyecto_integrador/python/PIM4_legalmove/e01_comparador_basico_vs_agentes.py
python proyecto_integrador/python/PIM4_legalmove/e02_output_libre_vs_pydantic.py
python proyecto_integrador/python/PIM4_legalmove/e03_sin_logs_vs_langfuse.py
```

---

## Conceptos clave

- **ContextualizationAgent:** mapea las secciones del contrato SIN extraer cambios finales.
- **ExtractionAgent:** usa el mapa de contexto para extraer qué cambió exactamente.
- **ContractChangeOutput:** schema Pydantic que valida `sections_changed`, `topics_touched` y `summary_of_the_change`.
- **Span:** unidad de trazabilidad — captura nombre, input preview, output preview y latencia.
- **Trace:** colección de spans que representa la ejecución completa del pipeline.
- **Langfuse:** plataforma de observabilidad para LLMs; los ejercicios usan llamadas reales a OpenAI y trazas locales de apoyo.
