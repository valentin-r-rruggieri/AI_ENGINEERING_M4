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
| 9 | [08 — Agente con FastMCP real](08_agente_fastmcp_real.md) | Cliente MCP real por STDIO o HTTP publicado. |
| 10 | [09 — Agente con API externa](09_agente_mcp_clima_real.md) | LangChain consume el MCP Open-Meteo creado en FastMCP. |

[Teoría transversal de L3](TEORIA_L3_MCP_Y_AGENTES.md) reúne el mapa de MCP,
tools, resources, prompts, LangChain, LangGraph, Pydantic y FastAPI.

Los casos `00` a `07` son ejercicios didácticos: algunos usan catálogos locales
para concentrarse en el concepto y no reemplazan una conexión MCP publicada.
El caso `08` sí conecta un cliente FastMCP a un servidor MCP real: por defecto
usa STDIO y, si se define `FASTMCP_CONTRATOS_URL`, consume el servidor HTTP ya
publicado. Es el caso recomendado para demostrar el flujo completo.

- `00`, `01`, `02` y `04`: cuatro usos de LangChain con MCP, tools y FastAPI.
- `03` y `05`: flujos LangGraph para tool, respuesta y routing.
- `06`: agente LangChain que consulta tres contratos antes de responder.
- `07`: el mismo handoff como LangGraph: capacidad MCP primero y agente después.
- `08`: FastMCP publica tools, resource y prompt; el agente LangChain consulta
  esa capacidad real y devuelve un informe Pydantic.
- `09`: el agente LangChain reutiliza el servidor Open-Meteo de `fastmcp/`,
  consulta datos vivos por MCP y entrega una recomendación Pydantic.
