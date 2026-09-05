# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Cliente real que consume el servidor FastMCP por STDIO.

GUÍA DOCENTE
CUÁNDO USAR: para probar un servidor MCP local antes de publicarlo por HTTP.
DIFERENCIA: el cliente no importa las tools; las descubre a través del protocolo.
EN CLASE: iniciar el cliente y observar que FastMCP crea la conexión al servidor.
"""

# Importa asyncio porque el cliente MCP mantiene una sesión asíncrona.
import asyncio
# Importa Path para señalar el archivo del servidor real que se ejecutará por STDIO.
from pathlib import Path
# Importa sys para localizar la CLI FastMCP instalada en este entorno virtual.
import sys

# Importa el cliente de FastMCP para conectarse a un servidor MCP real.
from fastmcp import Client
# Importa el transporte que crea un proceso STDIO mediante la CLI oficial.
from fastmcp.client.transports import StdioTransport

# Ubica el servidor vecino sin depender de la carpeta desde la que se ejecute el script.
ruta_servidor = Path(__file__).with_name("00_servidor_contratos.py")
# Usa la CLI del mismo entorno virtual para publicar el objeto mcp por STDIO.
ruta_fastmcp = Path(sys.executable).with_name("fastmcp.exe")
transporte_stdio = StdioTransport(
    command=str(ruta_fastmcp),
    args=["run", f"{ruta_servidor}:mcp", "--transport", "stdio", "--no-banner"],
    cwd=str(ruta_servidor.parent),
)


# Abre una sesión real, descubre capacidades y consume una de cada tipo.
async def consumir_servidor() -> None:
    async with Client(transporte_stdio) as cliente:
        tools = await cliente.list_tools()
        respuesta_tool = await cliente.call_tool("consultar_estado_contrato", {"codigo": "C-200"})
        respuesta_recurso = await cliente.read_resource("legalmove://politica-operativa")
        respuesta_prompt = await cliente.get_prompt("revisar_contrato", {"codigo": "C-200"})

        # Muestra datos recibidos por el protocolo, no llamados directos a funciones locales.
        print("Tools descubiertas:", [tool.name for tool in tools])
        print("Contrato consultado:", respuesta_tool.data)
        print("Política leída:", respuesta_recurso)
        print("Prompt solicitado:", respuesta_prompt)


# Ejecuta la sesión asíncrona al correr este ejercicio corto.
asyncio.run(consumir_servidor())

# Resumen final: este cliente consumió tool, resource y prompt por una sesión MCP real.
# Cambiá C-200 por C-300 y compará la respuesta recibida.
