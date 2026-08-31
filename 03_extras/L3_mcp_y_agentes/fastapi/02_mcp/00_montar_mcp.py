# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Montaje de MCP dentro de una aplicación FastAPI.

GUÍA DOCENTE
CUÁNDO USAR: cuando una API web y un servidor MCP comparten proceso.
DIFERENCIA: la aplicación host debe iniciar el session manager del MCP montado.
EN CLASE: identificar /salud y /mcp como interfaces distintas.
"""

# Importa el lifespan, FastAPI y el servidor MCP v2.
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mcp.server import MCPServer

# Crea el MCP y registra una tool pequeña.
mcp = MCPServer("MCP montado")

@mcp.tool()
def duplicar(numero: int) -> int:
    """Duplica un número entero."""
    return numero * 2

# Crea primero la subaplicación para inicializar el session manager.
aplicacion_mcp = mcp.streamable_http_app(streamable_http_path="/")

# Mantiene activo el administrador de sesiones durante toda la API.
@asynccontextmanager
async def lifespan(aplicacion: FastAPI):
    async with mcp.session_manager.run():
        yield

# Publica la API normal y monta MCP en /mcp.
app = FastAPI(lifespan=lifespan)

@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}

app.mount("/mcp", aplicacion_mcp)
print("Ejecutá Uvicorn; MCP quedará disponible en /mcp")

# Resumen final: este ejercicio aloja HTTP tradicional y MCP juntos.
# Quita el lifespan y observa por qué falla la primera sesión MCP.
