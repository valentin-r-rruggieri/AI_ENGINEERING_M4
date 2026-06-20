# AEM4L3 | Notebooks de introduccion a MCP

Estos notebooks estan pensados como base conceptual antes de abrir los scripts Python completos.

| Notebook | Tema | Se conecta con |
|---|---|---|
| `E01_resuelto_clasificar_primitivas.ipynb` | Problema ad hoc y por que MCP | `e01_tool_calling_ad_hoc_vs_mcp.py` |
| `E02_resuelto_tool_ecommerce_schema.ipynb` | MCP Host, MCP Client y MCP Server | `e04_github_mcp_server.py`, `e05_openai_host_usa_mcp_github.py` |
| `E03_resuelto_versionado_schema.ipynb` | Tools, resources y prompts | `e04_github_mcp_server.py` |
| `E04_resuelto_elegir_transporte.ipynb` | STDIO vs HTTP/streaming | `e04_github_mcp_server.py`, Antigravity |
| `E05_para_resolver_mcp_rrhh.ipynb` | Contratos, schemas y errores | `e02_scopes_y_autorizacion.py`, `e03_versionado_schemas.py` |
| `E06_para_resolver_versionado_tool_bancaria.ipynb` | GitHub MCP paso a paso | `github_mcp_utils.py`, `e04_github_mcp_server.py` |
| `E07_inicial_tool_resource_prompt.ipynb` | Seguridad, scopes, tenant isolation y confused deputy | `e06_mcp_integrador_soporte.py` |
| `E08_avanzado_mcp_universidad.ipynb` | Caso integrador de la lecture | `e06_mcp_integrador_soporte.py` |

Orden recomendado:

1. E01-E04 para bases.
2. Python E01-E05 para practica real.
3. E07-E08 y Python E06 para governance.
