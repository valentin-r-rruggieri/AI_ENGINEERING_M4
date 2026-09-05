# FastMCP con OpenAI como proveedor

## Objetivo

Centralizar una llamada a OpenAI dentro de un servidor MCP. Así, diferentes
clientes pueden pedir `resumir_texto` sin recibir `OPENAI_API_KEY` ni decidir
por su cuenta cómo se llama el modelo.

```mermaid
flowchart LR
    A[Host o agente] -->|tool MCP| B[FastMCP]
    B -->|clave desde .env| C[OpenAI Responses API]
    C --> D[Resumen]
    D --> B --> A
```

| Dato | Dónde queda |
|---|---|
| `texto` | Argumento visible y validable de la tool. |
| `OPENAI_API_KEY` | Solo en el entorno del servidor. |
| Modelo | Variable `OPENAI_AGENT_MODEL`. |
| Resumen | Respuesta MCP para el cliente. |

## Publicación

```powershell
fastmcp run .\02_proveedor_openai.py:mcp --transport streamable-http --port 8004
```

Para producción, publicá el endpoint mediante HTTPS y usá una clave de servicio
con permisos y límites apropiados. El ejemplo no tiene un fallback ficticio:
si no hay clave, informa qué variable falta.

## Práctica

Cambiale el nombre a la tool por `clasificar_texto` y devolvé una categoría
Pydantic. El cliente seguirá hablando MCP aunque cambie el proveedor interno.
