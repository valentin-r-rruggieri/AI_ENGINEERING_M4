# AEM4L3 | Notebooks de introduccion a MCP

Estos notebooks estan pensados como base conceptual antes de abrir el MCP Python completo de GitHub.

La clase queda unificada en un solo caso:

```text
Usuario -> Host Antigravity/VS Code/OpenAI -> MCP Client -> MCP Server GitHub -> GitHub API
```

## Ruta modular paso a paso

| Notebook | Tema | Resultado |
|---|---|---|
| `00_ad_hoc_problem.ipynb` | Problema ad hoc | Entender por que MCP existe |
| `01_mcp_mental_model.ipynb` | Modelo mental MCP | Separar Host, Client y Server |
| `02_mcp_server_minimo.ipynb` | MCP Server minimo | Publicar catalogo de capacidades |
| `03_tools.ipynb` | Tools | Diferenciar tool pura y tool con side effect |
| `04_resources.ipynb` | Resources | Exponer datos/contexto controlado |
| `05_prompts.ipynb` | Prompts | Reutilizar plantillas versionadas |
| `06_mcp_client.ipynb` | MCP Client | Descubrir y consumir capacidades |
| `07_contracts_schemas.ipynb` | Contratos y schemas | Validar inputs/outputs con Pydantic |
| `08_versioning.ipynb` | Versionado | Detectar cambios aditivos y breaking changes |
| `09_transports.ipynb` | Transporte | Comparar STDIO vs HTTP |
| `10_security_audit.ipynb` | Seguridad y auditoria | Tokens, repos privados y audit logs |
| `11_integrador_github_repo_copilot.ipynb` | Integrador GitHub | Ejecutar un mini sistema MCP educativo |

## Notebooks puente

| Notebook | Tema | Se conecta con |
|---|---|---|
| `E01_resuelto_clasificar_primitivas.ipynb` | Problema ad hoc y primitivas MCP | `00_ad_hoc_problem.ipynb`, `03_tools.ipynb`, `04_resources.ipynb`, `05_prompts.ipynb` |
| `E02_resuelto_tool_ecommerce_schema.ipynb` | Schema de tool GitHub | `e01_github_mcp_server.py` |
| `E03_resuelto_versionado_schema.ipynb` | Versionado de schemas | `08_versioning.ipynb` |
| `E04_resuelto_elegir_transporte.ipynb` | STDIO vs HTTP/streaming | `e01_github_mcp_server.py`, Antigravity, VS Code |
| `E05_para_resolver_mcp_rrhh.ipynb` | Diseno guiado de capacidades | `03_tools.ipynb`, `04_resources.ipynb`, `05_prompts.ipynb` |
| `E06_para_resolver_versionado_tool_bancaria.ipynb` | Versionado de `github_upsert_file` | `08_versioning.ipynb` |
| `E07_inicial_tool_resource_prompt.ipynb` | Tool, resource y prompt juntos | `e01_github_mcp_server.py` |
| `E08_avanzado_mcp_universidad.ipynb` | Arquitectura completa de la lecture | `e01_github_mcp_server.py`, `e02_openai_host_usa_mcp_github.py` |

Orden recomendado:

1. `00` a `11` para construir el modelo mental paso a paso.
2. `E01` a `E08` como notebooks puente y de repaso.
3. Python `e01` y `e02` para probar el MCP GitHub real y el host OpenAI.
