# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tools MCP preparadas para un grafo.

GUÍA DOCENTE
CUÁNDO USAR: cuando los nodos consumen capacidades publicadas por otro servicio.
DIFERENCIA: el grafo controla el flujo; MCP provee las capacidades.
EN CLASE: iniciar el MCP antes de cargar sus tools.
"""

# Importa asyncio y el adaptador MCP de LangChain/LangGraph.
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# Declara el servidor HTTP que debe estar activo.
servidores = {
    "legalmove": {
        "transport": "http",
        "url": "http://127.0.0.1:8000/mcp",
    }
}

# Recupera las tools que luego podrían pasar a ToolNode.
async def cargar() -> None:
    try:
        cliente = MultiServerMCPClient(servidores)
        tools = await cliente.get_tools()
        print("Tools para el grafo:", [tool.name for tool in tools])
    except Exception as error:
        print("Iniciá primero el servidor MCP. Detalle:", type(error).__name__)

# Ejecuta la carga sin bloque __main__.
asyncio.run(cargar())

# Resumen final: este ejercicio desacopla flujo y capacidades remotas.
# Conecta las tools obtenidas a un ToolNode del ejemplo anterior.
