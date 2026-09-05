# FastMCP — L3 MCP y agentes

FastMCP es la tecnología de alto nivel de este módulo para crear y consumir
servidores MCP reales con pocas líneas. Complementa FastAPI: **FastMCP publica
capacidades MCP para agentes**; **FastAPI publica endpoints HTTP de una app**.

| Orden | Archivo | Resultado |
|---:|---|---|
| 1 | [Servidor](00_fundamentos/00_servidor_contratos.md) | Tool, resource y prompt publicados. |
| 2 | [Cliente STDIO](00_fundamentos/01_cliente_stdio_real.md) | Consumo real y descubrimiento de capacidades. |
| 3 | [API pública](01_apis_y_proveedores/00_api_publica_openmeteo.md) | Tool FastMCP conectada a Open-Meteo. |
| 4 | [API propia](01_apis_y_proveedores/01_api_propia_clientes.md) | Token, URL configurable y frontera interna. |
| 5 | [Proveedor OpenAI](01_apis_y_proveedores/02_proveedor_openai.md) | MCP que encapsula una API de IA. |
| 6 | [Cliente de clima](02_en_marcha/00_cliente_clima_real.md) | Prueba real del MCP externo por STDIO. |
| 7 | [Agente integrador](../resumen/08_agente_fastmcp_real.md) | LangChain + FastMCP + Pydantic. |

## Inicio rápido

```powershell
# Desde la raíz del curso, una única vez.
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Cliente real por STDIO: el servidor se conecta desde el mismo archivo.
.\.venv\Scripts\python.exe .\03_extras\L3_mcp_y_agentes\fastmcp\00_fundamentos\01_cliente_stdio_real.py
```

Para dejar el MCP disponible fuera de tu máquina o para conectarlo desde una
web, publicalo con **Streamable HTTP**. STDIO sirve únicamente para el proceso
local que inicia el cliente.

```powershell
fastmcp run .\00_fundamentos\00_servidor_contratos.py:mcp --transport streamable-http --port 8001
```

La URL del protocolo es `http://127.0.0.1:8001/mcp/` en desarrollo. En una
publicación real será la URL HTTPS equivalente y se coloca en
`FASTMCP_CONTRATOS_URL`.
