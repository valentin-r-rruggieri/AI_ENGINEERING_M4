# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Carga de tools MCP para un agente LangChain.

GUÍA DOCENTE
CUÁNDO USAR: cuando las capacidades viven fuera del código del agente.
DIFERENCIA: MCP desacopla la tool del framework que la consume.
EN CLASE: iniciar primero el servidor MCP y luego listar sus tools.
"""

# Importa asyncio y el cliente MCP específico de LangChain.
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# Define una conexión al servidor creado en la carpeta MCP de L3.
configuracion = {
    "legalmove": {
        "transport": "http",
        "url": "http://127.0.0.1:8000/mcp",
    }
}

# Solicita las tools y muestra sus nombres.
async def cargar_tools() -> None:
    try:
        cliente = MultiServerMCPClient(configuracion)
        tools = await cliente.get_tools()
        print([tool.name for tool in tools])
    except Exception as error:
        print("Iniciá primero el servidor MCP en http://127.0.0.1:8000/mcp")
        print("Detalle breve:", type(error).__name__)

# Ejecuta el cliente sin bloque __main__.
asyncio.run(cargar_tools())

# Resumen final: este ejercicio transforma tools MCP en tools de LangChain.
# Agrega un segundo servidor a la configuración y compara la lista.
