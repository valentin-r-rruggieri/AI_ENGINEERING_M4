# MCP: tools, resources, prompts y transportes

Este recorrido usa MCP Python SDK v2. Los ejemplos básicos prueban el protocolo en memoria;
los últimos muestran STDIO y Streamable HTTP.

```powershell
pip install -r 03_extras/L3_mcp_y_agentes/mcp/requirements.txt
python 03_extras/L3_mcp_y_agentes/mcp/00_fundamentos/00_servidor.py
```

Para explorar un servidor con Inspector: `mcp dev ruta/al/archivo.py`.
Para el integrador HTTP, entrá en `04_en_marcha` y ejecutá
`uvicorn servidor_completo:app --reload`.
