# AEM4L3 | MCP GitHub completo en Python

## Objetivo

En L3, los conceptos base de MCP se trabajan en notebooks. Esta carpeta Python queda reservada para un unico MCP completo, funcional y usable desde clientes reales: **GitHub por STDIO**.

La progresion queda asi:

| Archivo | Rol | Para que sirve |
|---|---|---|
| `e01_github_mcp_server.py` | MCP Server real | Expone GitHub como tools, resources y prompts por STDIO |
| `e02_openai_host_usa_mcp_github.py` | Host de demostracion | Usa OpenAI + MCP Client para llamar al server GitHub |
| `github_mcp_utils.py` | Helper interno | Ejecuta GitHub REST API y escribe audit log local |

## Requisitos

Instalar dependencias:

```bash
cd /Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises
/Users/valentin/AI_ENGINEERING_M4/.venv/bin/python -m pip install -r requirements.txt
```

Variables en `.env`:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
GITHUB_TOKEN=...
```

`GITHUB_TOKEN` debe permitir crear repositorios y escribir contenido. El MCP GitHub crea repos privados por defecto y no expone ninguna tool de borrado.

## MCP GitHub real

Servidor:

```bash
cd /Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises
/Users/valentin/AI_ENGINEERING_M4/.venv/bin/python AEM4L3_mcp/e01_github_mcp_server.py
```

Host demo con OpenAI:

```bash
cd /Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises
/Users/valentin/AI_ENGINEERING_M4/.venv/bin/python AEM4L3_mcp/e02_openai_host_usa_mcp_github.py
```

Tools:

- `github_create_repo(name, description, private=True)`.
- `github_upsert_file(owner, repo, path, content, commit_message, branch="main")`.
- `github_get_repo(owner, repo)`.

Resources:

- `github://config`.
- `github://capabilities`.
- `github://security-policy`.
- `github://audit/recent`.
- `github://templates/readme-basic`.

Prompts:

- `repo_bootstrap_prompt(project_name, goal)`.
- `repo_readme_prompt(project_name, goal, audience="desarrolladores")`.
- `safe_github_action_prompt(action_summary)`.
- `repo_review_prompt(owner, repo)`.

Regla docente:

```text
Tool ejecuta; resource informa; prompt guia.
```

## Probar desde Antigravity

Agregar este server MCP por STDIO:

macOS:

```json
{
  "mcpServers": {
    "aem4l3-github": {
      "command": "/Users/valentin/AI_ENGINEERING_M4/.venv/bin/python",
      "args": [
        "/Users/valentin/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

Windows con `.venv` creada:

```json
{
  "mcpServers": {
    "aem4l3-github": {
      "command": "C:/Users/Usuario/Desktop/Clases/AI_ENGINEERING_M4/.venv/Scripts/python.exe",
      "args": [
        "C:/Users/Usuario/Desktop/Clases/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

Si aparece `executable file not found`, primero crear la venv e instalar dependencias:

```powershell
cd C:\Users\Usuario\Desktop\Clases\AI_ENGINEERING_M4
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\python_puro\AEM4_python_exercises\requirements.txt
```

Si no queres depender de `.venv`, podes usar el launcher de Windows `py`:

```json
{
  "mcpServers": {
    "aem4l3-github": {
      "command": "py",
      "args": [
        "-3",
        "C:/Users/Usuario/Desktop/Clases/AI_ENGINEERING_M4/python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

En ese caso las dependencias tienen que estar instaladas en ese Python:

```powershell
py -3 -m pip install -r C:\Users\Usuario\Desktop\Clases\AI_ENGINEERING_M4\python_puro\AEM4_python_exercises\requirements.txt
```

Para probar en clase:

```text
Usa el MCP aem4l3-github para crear un repositorio privado llamado aem4l3-mcp-demo y agregar un README.md inicial.
```

Para probar resources y prompts:

```text
Lee el resource github://capabilities del MCP aem4l3-github y explicame que tools tienen side effects.
```

```text
Usa el prompt safe_github_action_prompt para revisar el riesgo antes de crear un repo privado llamado aem4l3-mcp-demo-antigravity.
```

```text
Lee github://audit/recent y resumime las ultimas acciones ejecutadas sin mostrar secretos.
```

## Probar desde VS Code

VS Code usa `.vscode/mcp.json` para servidores MCP de workspace. En este repo ya queda creado un ejemplo que usa `envFile` y lee `GITHUB_TOKEN` desde `.env`, sin hardcodear el token.

Archivo:

```text
/Users/valentin/AI_ENGINEERING_M4/.vscode/mcp.json
```

Contenido equivalente:

```json
{
  "servers": {
    "aem4l3Github": {
      "type": "stdio",
      "command": "/Users/valentin/AI_ENGINEERING_M4/.venv/bin/python",
      "args": [
        "${workspaceFolder}/python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py"
      ],
      "envFile": "${workspaceFolder}/python_puro/AEM4_python_exercises/.env"
    }
  }
}
```

Pasos en VS Code:

1. Abrir Command Palette.
2. Ejecutar `MCP: Open Workspace Folder MCP Configuration`.
3. Confirmar que aparece `aem4l3Github`.
4. Iniciar el server y habilitar sus tools en Chat.
5. Pedirle a Copilot/Agent que use el MCP para crear un repo privado o agregar un archivo.

## Auditoria

Los eventos del MCP GitHub se guardan localmente en:

```text
data/github_mcp_audit_log.jsonl
```

Ese log esta ignorado por Git y no guarda tokens.
