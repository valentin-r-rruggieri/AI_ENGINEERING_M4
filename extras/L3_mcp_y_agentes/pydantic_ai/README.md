# PydanticAI: agentes tipados y MCP

Recorrido por agentes, `output_type`, tools, dependencias, MCPToolset y handoffs.
Los scripts usan `OPENAI_API_KEY` para llamadas reales y conservan ejemplos locales cuando
la clave no está configurada.

```powershell
pip install -r extras/L3_mcp_y_agentes/pydantic_ai/requirements.txt
$env:OPENAI_API_KEY="tu-clave"
python extras/L3_mcp_y_agentes/pydantic_ai/00_fundamentos/00_agente.py
```

Terminá con `04_en_marcha/agente_tipado_con_tool.py`. La implementación completa de
LegalMove está separada en `../../PI_legalmove/pydantic_ai`.
