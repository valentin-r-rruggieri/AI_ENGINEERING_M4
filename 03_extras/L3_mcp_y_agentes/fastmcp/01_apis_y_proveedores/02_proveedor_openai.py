# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, publicá el servidor y modificá una capacidad por vez.

"""MCP que encapsula una llamada a un proveedor de IA: OpenAI.

GUÍA DOCENTE
CUÁNDO USAR: cuando varios agentes necesitan la misma capacidad de resumen.
DIFERENCIA: el cliente MCP solicita una capacidad; el servidor conserva la clave del proveedor.
EN CLASE: comparar este patrón con entregar la clave directamente a cada aplicación.
"""

# Importa os para leer modelo y clave del proveedor desde .env.
import os
# Importa dotenv para cargar las credenciales una sola vez.
from dotenv import load_dotenv
# Importa FastMCP para exponer el resumen como una tool MCP.
from fastmcp import FastMCP
# Importa el cliente asíncrono oficial del proveedor OpenAI.
from openai import AsyncOpenAI

# Carga las credenciales antes de que la tool intente crear el cliente.
load_dotenv()
# Crea el servidor que centraliza el acceso al proveedor de IA.
mcp = FastMCP("Resumen OpenAI")


# Publica una tool que conserva OPENAI_API_KEY del lado del servidor MCP.
@mcp.tool
async def resumir_texto(texto: str) -> dict[str, str]:
    """Resume un texto en español en una oración clara."""
    clave = os.getenv("OPENAI_API_KEY", "")
    if not clave or clave == "your-openai-key-here":
        return {"estado": "configuración pendiente", "detalle": "Completá OPENAI_API_KEY en .env."}

    cliente = AsyncOpenAI(api_key=clave)
    respuesta = await cliente.responses.create(
        model=os.getenv("OPENAI_AGENT_MODEL", "gpt-4o-mini"),
        input=f"Resumí en una sola oración en español, sin inventar datos:\n\n{texto}",
    )

    # Devuelve solo el resultado útil y no expone la respuesta técnica completa.
    return {"estado": "ok", "resumen": respuesta.output_text}

# Resumen final: FastMCP encapsula una API de IA como capacidad reutilizable.
# Cambiá el modelo en .env y comprobá que el contrato MCP no se modifica.
