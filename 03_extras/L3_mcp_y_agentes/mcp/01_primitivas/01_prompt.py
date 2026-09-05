# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Prompt MCP reutilizable y parametrizado.

GUÍA DOCENTE
CUÁNDO USAR: para compartir una plantilla de interacción entre clientes.
DIFERENCIA: el prompt propone instrucciones; no ejecuta una acción por sí mismo.
EN CLASE: diferenciar template del mensaje finalmente generado.
"""

# Importa asyncio, Client y FastMCP para registrar y solicitar el prompt.
import asyncio
from fastmcp import Client, FastMCP

# Crea el servidor de plantillas legales.
mcp = FastMCP("Prompts legales")

# Registra un prompt que adapta la instrucción al tipo de contrato.
@mcp.prompt()
def revisar_contrato(tipo: str) -> str:
    """Prepara una revisión contractual especializada."""
    return f"Actúa como auditor legal y revisa este contrato de tipo {tipo}."

# Solicita el prompt mediante el cliente MCP.
async def probar_prompt() -> None:
    async with Client(mcp) as cliente:
        resultado = await cliente.get_prompt("revisar_contrato", {"tipo": "alquiler"})
        print(resultado.messages[0].content.text)

# Ejecuta la demostración sin función main.
asyncio.run(probar_prompt())

# Resumen final: este ejercicio publica una instrucción reutilizable.
# Cambia el tipo de contrato y revisa qué parte del mensaje permanece estable.
