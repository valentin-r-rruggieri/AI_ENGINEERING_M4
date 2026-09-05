# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Cliente real que prueba el MCP de clima contra una API externa.

GUÍA DOCENTE
CUÁNDO USAR: para verificar el camino agente → MCP → proveedor antes de sumar un LLM.
DIFERENCIA: este script es cliente; no conoce ni importa la lógica de Open-Meteo.
EN CLASE: ejecutar y comparar respuestas de distintas ciudades.
"""

# Importa asyncio para mantener la sesión MCP asíncrona.
import asyncio
# Importa Path y sys para localizar servidor y CLI dentro del entorno activo.
from pathlib import Path
import sys

# Importa el cliente MCP y el transporte que inicia el servidor real por STDIO.
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

# Ubica el servidor de API pública sin depender de la carpeta actual.
ruta_servidor = Path(__file__).resolve().parents[1] / "01_apis_y_proveedores" / "00_api_publica_openmeteo.py"
# Usa la CLI FastMCP del entorno virtual para iniciar el servidor local real.
ruta_fastmcp = Path(sys.executable).with_name("fastmcp.exe")
transporte = StdioTransport(
    command=str(ruta_fastmcp),
    args=["run", f"{ruta_servidor}:mcp", "--transport", "stdio", "--no-banner"],
    cwd=str(ruta_servidor.parent),
)


# Solicita el clima atravesando el protocolo MCP y la API externa real.
async def probar_clima() -> None:
    async with Client(transporte) as cliente:
        resultado = await cliente.call_tool("consultar_clima", {"ciudad": "Buenos Aires"})
        print(resultado.data)


# Ejecuta la prueba lineal y visible para la clase.
asyncio.run(probar_clima())

# Resumen final: el resultado llegó desde Open-Meteo a través de FastMCP.
# Cambiá Buenos Aires por otra ciudad y compará los datos vivos.
