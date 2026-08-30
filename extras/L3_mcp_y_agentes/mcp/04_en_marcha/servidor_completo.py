# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servidor MCP completo con tool, resource y prompt.

GUÍA DOCENTE
CUÁNDO USAR: como referencia mínima de un servidor consumible por varios hosts.
DIFERENCIA: cada primitiva conserva una responsabilidad distinta.
EN CLASE: probar las tres primitivas con Inspector antes de integrar un agente.
"""

# Importa Annotated, MCPServer y Field para capacidades tipadas.
from typing import Annotated
from mcp.server import MCPServer
from pydantic import Field

# Crea el servidor integrador.
mcp = MCPServer("LegalMove MCP")

# Publica una tool de comparación determinista.
@mcp.tool()
def comparar_plazos(
    plazo_original: Annotated[int, Field(ge=1)],
    plazo_nuevo: Annotated[int, Field(ge=1)],
) -> dict[str, int | str]:
    """Compara dos plazos contractuales expresados en meses."""
    diferencia = plazo_nuevo - plazo_original
    return {"diferencia": diferencia, "cambio": "aumento" if diferencia > 0 else "reducción o igualdad"}

# Publica una resource que aporta una política estable.
@mcp.resource("politica://revision")
def politica_revision() -> str:
    """Devuelve la política local de revisión humana."""
    return "Revisar todo cambio de plazo mayor a seis meses."

# Publica un prompt reutilizable por el host.
@mcp.prompt()
def auditar_cambio(jurisdiccion: str) -> str:
    """Prepara una auditoría adaptada a una jurisdicción."""
    return f"Audita el cambio contractual para la jurisdicción {jurisdiccion}."

# Expone las capacidades mediante Streamable HTTP en /mcp.
app = mcp.streamable_http_app()
print("Ejecutá: uvicorn servidor_completo:app --reload")

# Resumen final: este servidor reúne las tres primitivas de MCP.
# Agrega una tool de solo lectura y documenta sus anotaciones.
