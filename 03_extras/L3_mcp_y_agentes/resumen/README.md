# L3 — Casos prácticos de MCP y agentes

Los casos conectan una capacidad MCP, un agente LangChain y una API tipada. El
primer archivo prepara el servidor; el tercero expone `app` para ejecutarlo con
`uvicorn 02_api_agente:app --reload` desde esta carpeta.

- `00`, `01`, `02` y `04`: cuatro usos de LangChain con MCP, tools y FastAPI.
- `03` y `05`: flujos LangGraph para tool, respuesta y routing.
- `06`: agente LangChain que consulta tres contratos antes de responder.
- `07`: el mismo handoff como LangGraph: capacidad MCP primero y agente después.
