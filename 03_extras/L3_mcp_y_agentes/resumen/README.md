# L3 — Casos prácticos de MCP y agentes

Los casos unen MCP, LangChain, LangGraph, Pydantic y FastAPI. Abrí primero el
Markdown del caso y después ejecutá el `.py` asociado.

## Recorrido recomendado para clase

| Orden | Caso práctico | Concepto principal |
|---:|---|---|
| 1 | [00 — Catálogo MCP](00_catalogo_mcp.md) | Tool, resource y prompt. |
| 2 | [01 — Agente de catálogo](01_agente_catalogo.md) | Tool antes de responder. |
| 3 | [02 — API de agente](02_api_agente.md) | FastAPI, entrada y salida tipada. |
| 4 | [03 — Flujo LangGraph](03_flujo_langgraph.md) | Handoff tool → agente. |
| 5 | [04 — Agente de política](04_agente_politica.md) | Política como dato verificable. |
| 6 | [05 — Routing](05_routing_langgraph.md) | Regla determinista de destino. |
| 7 | [06 — Consultas LangChain](06_agente_consultas_mcp_langchain.md) | Agente y tres estados contractuales. |
| 8 | [07 — Consultas LangGraph](07_agente_consultas_mcp_langgraph.md) | Estado auditable y salida Pydantic. |

[Teoría transversal de L3](TEORIA_L3_MCP_Y_AGENTES.md) reúne el mapa de MCP,
tools, resources, prompts, LangChain, LangGraph, Pydantic y FastAPI.

Los casos conectan una capacidad MCP, un agente LangChain y una API tipada. El
primer archivo prepara el servidor; el tercero expone `app` para ejecutarlo con
`uvicorn 02_api_agente:app --reload` desde esta carpeta.

- `00`, `01`, `02` y `04`: cuatro usos de LangChain con MCP, tools y FastAPI.
- `03` y `05`: flujos LangGraph para tool, respuesta y routing.
- `06`: agente LangChain que consulta tres contratos antes de responder.
- `07`: el mismo handoff como LangGraph: capacidad MCP primero y agente después.
