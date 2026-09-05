# MCP: tools, resources, prompts y transportes

Este recorrido usa FastMCP sobre el SDK MCP actual compatible. Los ejemplos básicos
prueban las primitivas en memoria; los últimos muestran STDIO y Streamable HTTP.
Para publicar y consumir un servidor por una conexión real, continuá con la
carpeta hermana [`fastmcp`](../fastmcp/README.md).

```powershell
pip install -r 03_extras/L3_mcp_y_agentes/mcp/requirements.txt
python 03_extras/L3_mcp_y_agentes/mcp/00_fundamentos/00_servidor.py
```

Para explorar un servidor con Inspector: `mcp dev ruta/al/archivo.py`.
Para el integrador HTTP, entrá en `04_en_marcha` y ejecutá
`uvicorn servidor_completo:app --reload`.
