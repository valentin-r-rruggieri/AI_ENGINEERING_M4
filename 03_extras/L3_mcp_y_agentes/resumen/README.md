# L3 — Tres casos prácticos de MCP y agentes

Los casos conectan una capacidad MCP, un agente LangChain y una API tipada. El
primer archivo prepara el servidor; el tercero expone `app` para ejecutarlo con
`uvicorn 02_api_agente:app --reload` desde esta carpeta.

- `00`, `01`, `02` y `04`: cuatro usos de LangChain con MCP, tools y FastAPI.
- `03` y `05`: flujos LangGraph para tool, respuesta y routing.
