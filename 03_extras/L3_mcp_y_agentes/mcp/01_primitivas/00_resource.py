# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Resource MCP identificado por una URI.

GUÍA DOCENTE
CUÁNDO USAR: para exponer información que el cliente decide leer.
DIFERENCIA: una resource aporta contexto; una tool ejecuta una acción.
EN CLASE: relacionar URI, parámetro y contenido devuelto.
"""

# Importa asyncio, Client y FastMCP para registrar y leer el recurso.
import asyncio
from fastmcp import Client, FastMCP

# Crea un servidor con un recurso parametrizado.
mcp = FastMCP("Contratos")

# Publica datos de una cláusula mediante su identificador.
@mcp.resource("contrato://clausula/{numero}")
def leer_clausula(numero: str) -> str:
    """Devuelve una cláusula contractual de demostración."""
    return f"Cláusula {numero}: la vigencia será de doce meses."

# Lee el recurso con un cliente en memoria.
async def probar_resource() -> None:
    async with Client(mcp) as cliente:
        resultado = await cliente.read_resource("contrato://clausula/4")
        print(resultado[0].text)

# Ejecuta la demostración lineal.
asyncio.run(probar_resource())

# Resumen final: este ejercicio expone contexto direccionable por URI.
# Cambia el número de la URI y observa cómo llega a la función.
