# AEM4L3 | MCP real + GitHub + governance

## Objetivo

Construir criterio y practica real de MCP:

1. Ver por que las integraciones ad hoc se rompen.
2. Separar MCP Host, MCP Client y MCP Server.
3. Exponer tools, resources y prompts.
4. Ejecutar un MCP server real de GitHub por STDIO.
5. Usar OpenAI como host que decide una accion y llama al MCP.
6. Cerrar con scopes, auditoria, versionado y riesgos operativos.

## Requisitos

Instalar dependencias desde la carpeta de ejercicios:

```bash
cd /Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises
pip install -r requirements.txt
```

Variables en `.env`:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
GITHUB_TOKEN=...
```

`GITHUB_TOKEN` debe permitir crear repositorios y escribir contenido. El ejercicio crea repos privados por defecto y no expone ninguna tool de borrado.

## Ejercicios Python

| Orden | Archivo | Tema | Qué muestra |
|---|---|---|---|
| E01 | `e01_tool_calling_ad_hoc_vs_mcp.py` | Ad hoc vs contrato | Texto libre fragil vs tool call estructurado |
| E02 | `e02_scopes_y_autorizacion.py` | Scopes | El LLM pide, pero `authorize()` decide |
| E03 | `e03_versionado_schemas.py` | Versionado | Cambios aditivos vs rupturistas y adaptador v1 -> v2 |
| E04 | `e04_github_mcp_server.py` | MCP Server real | FastMCP con GitHub tools, resource y prompt |
| E05 | `e05_openai_host_usa_mcp_github.py` | MCP Host + OpenAI | OpenAI elige tool, MCP ejecuta GitHub por STDIO |
| E06 | `e06_mcp_integrador_soporte.py` | Governance completa | tools/resources/prompts/scopes/audit/versionado |

## Comandos

Ejercicios conceptuales:

```bash
python AEM4L3_mcp/e01_tool_calling_ad_hoc_vs_mcp.py
python AEM4L3_mcp/e02_scopes_y_autorizacion.py
python AEM4L3_mcp/e03_versionado_schemas.py
```

Servidor MCP GitHub por STDIO:

```bash
python AEM4L3_mcp/e04_github_mcp_server.py
```

Host OpenAI que usa el server MCP por STDIO:

```bash
python AEM4L3_mcp/e05_openai_host_usa_mcp_github.py
```

Servidor MCP integrador de soporte:

```bash
python AEM4L3_mcp/e06_mcp_integrador_soporte.py
```

## Config Antigravity sugerida

Usar el server GitHub por STDIO:

```json
{
  "mcpServers": {
    "aem4l3-github": {
      "command": "python",
      "args": [
        "/Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises/AEM4L3_mcp/e04_github_mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

## Tools del MCP GitHub

- `github_create_repo(name, description, private=True)`: crea repo real privado por defecto.
- `github_upsert_file(owner, repo, path, content, commit_message, branch="main")`: crea o actualiza archivo con commit real.
- `github_get_repo(owner, repo)`: consulta metadata del repo.

Resource:

- `github://config`: muestra configuracion segura del server sin token.

Prompt:

- `repo_bootstrap_prompt(project_name, goal)`: plantilla para crear repo + README.

## Auditoria

Los eventos se guardan localmente en:

```text
data/github_mcp_audit_log.jsonl
data/support_mcp_audit_log.jsonl
```

Esos logs estan ignorados por Git y no guardan tokens ni contenido completo de archivos.
