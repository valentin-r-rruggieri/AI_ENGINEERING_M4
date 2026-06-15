# AEM4L3 | MCP (Model Context Protocol)

## Objetivo

Ver que MCP no es "otra capa más": es la solución a wrappers inconsistentes, permisos demasiado amplios y cambios de schema sin control que rompen integraciones en producción.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_tool_calling_ad_hoc_vs_mcp.py` | 3 apps con funciones incompatibles | Contrato MCP unificado con Pydantic |
| `e02_scopes_y_autorizacion.py` | Permisos genéricos para todos | Principio de mínimo privilegio con scopes |
| `e03_versionado_schemas.py` | Cambios de campo rompen clientes | Versionado semántico: aditivo vs. rupturista |

---

## Cómo ejecutar

```bash
python AEM4L3_mcp/e01_tool_calling_ad_hoc_vs_mcp.py
python AEM4L3_mcp/e02_scopes_y_autorizacion.py
python AEM4L3_mcp/e03_versionado_schemas.py
```

---

## Conceptos clave

- **MCP:** protocolo que estandariza cómo los LLMs interactúan con herramientas externas.
- **Tool contract:** input_schema + output_schema + required_scope + version.
- **Scope:** permiso mínimo necesario para ejecutar una tool (`dominio:objeto:acción`).
- **Cambio aditivo:** agrega campos opcionales — no rompe clientes existentes.
- **Cambio rupturista:** renombra, elimina o cambia tipos de campos obligatorios — requiere nueva versión mayor.
