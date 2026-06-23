# AEM4L3 | Guia de alumno: construir un MCP paso a paso

Estos notebooks estan pensados como una guia de alumno. No son apuntes del docente ni slides: cada notebook explica un concepto, muestra tablas y diagramas textuales, ejecuta un ejemplo minimo en Python y conecta ese paso con el MCP GitHub real de la clase.

La clase queda unificada en un solo caso conductor:

```text
Usuario -> Host Antigravity/VS Code/OpenAI -> MCP Client -> MCP Server GitHub -> GitHub API
```

Los notebooks no usan Mermaid. Los diagramas son textuales para que se lean bien en cualquier entorno de notebooks y para que el alumno pueda copiarlos, modificarlos y explicarlos con sus palabras.

## Ruta modular paso a paso

| Notebook | Tema | Resultado |
|---|---|---|
| `00_ad_hoc_problem.ipynb` | Problema ad hoc | Entender por que MCP existe |
| `01_mcp_mental_model.ipynb` | Host, Client y Server | Separar responsabilidades |
| `02_mcp_server_minimo.ipynb` | Catalogo MCP | Publicar tools, resources y prompts |
| `03_tools.ipynb` | Tools | Diferenciar lectura y side effects |
| `04_resources.ipynb` | Resources | Exponer contexto sin ejecutar acciones |
| `05_prompts.ipynb` | Prompts | Reutilizar instrucciones sin ejecutar GitHub |
| `06_mcp_client.ipynb` | MCP Client | Descubrir y consumir capacidades |
| `07_contracts_schemas.ipynb` | Contratos y schemas | Validar inputs/outputs con Python puro |
| `08_versioning.ipynb` | Versionado | Detectar cambios aditivos y breaking changes |
| `09_transports.ipynb` | Transporte | Comparar STDIO vs HTTP |
| `10_security_audit.ipynb` | Seguridad y auditoria | Tokens, repos privados y audit logs |
| `11_integrador_github_repo_copilot.ipynb` | Integrador GitHub | Simular el MCP completo antes del server real |

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

## Como usar esta guia

1. Abrir `00` a `11` en orden y ejecutar cada celda.
2. Resolver o revisar `E01` a `E08` para reforzar cada bloque.
3. Abrir el MCP real en Python:

```text
python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py
python_puro/AEM4_python_exercises/AEM4L3_mcp/e02_openai_host_usa_mcp_github.py
```

4. Probar el flujo real con OpenAI + MCP local o desde Antigravity.

Frase guia:

```text
Tool ejecuta; resource informa; prompt guia.
```
