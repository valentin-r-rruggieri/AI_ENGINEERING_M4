# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tool MCP con schema generado desde type hints.

GUÍA DOCENTE
CUÁNDO USAR: cuando el modelo necesita ejecutar una acción o cálculo.
DIFERENCIA: la docstring describe la tool y los tipos forman su contrato.
EN CLASE: inspeccionar nombre, argumentos y retorno antes de llamar.
"""

# Importa asyncio para ejecutar el cliente y componentes MCP.
import asyncio
from fastmcp import Client, FastMCP

# Crea el servidor que expondrá el cálculo.
mcp = FastMCP("Calculadora")

# Registra una función Python como tool MCP.
@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b

# Define una prueba en memoria que recorre el protocolo real.
async def probar_tool() -> None:
    async with Client(mcp) as cliente:
        resultado = await cliente.call_tool("sumar", {"a": 2, "b": 3})
        print(resultado.data)

# Ejecuta la prueba directamente, sin bloque __main__.
asyncio.run(probar_tool())

# Resumen final: este ejercicio publica y llama una tool tipada.
# Cambia b por un texto y observa cómo el protocolo valida el argumento.
