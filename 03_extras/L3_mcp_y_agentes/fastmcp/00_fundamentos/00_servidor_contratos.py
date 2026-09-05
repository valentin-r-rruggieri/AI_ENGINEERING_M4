# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, publica el servidor y modifica una capacidad por vez.

"""Servidor MCP real con una tool, un resource y un prompt.

GUÍA DOCENTE
CUÁNDO USAR: cuando una capacidad debe poder ser consumida por varios agentes.
DIFERENCIA: FastMCP publica el protocolo MCP; FastAPI publica endpoints HTTP propios.
EN CLASE: ejecutar este archivo mediante la CLI de FastMCP, no con python directo.
"""

# Importa FastMCP para declarar un servidor MCP con decoradores simples.
from fastmcp import FastMCP

# Crea el servidor que se publicará por STDIO o por Streamable HTTP.
mcp = FastMCP(
    "LegalMove Contratos",
    instructions="Consultá el estado contractual y aplicá la política operativa disponible.",
)

# Define datos didácticos dentro del servidor real. En producción provendrían de una base o API.
contratos = {
    "C-100": {"estado": "vigente", "cliente": "Estudio Rivera", "vence": "2027-06-30"},
    "C-200": {"estado": "en revisión", "cliente": "Norte Salud", "vence": "2026-10-15"},
    "C-300": {"estado": "vencido", "cliente": "Delta Logística", "vence": "2025-12-31"},
}


# Expone una acción que un cliente MCP puede descubrir e invocar remotamente.
@mcp.tool
def consultar_estado_contrato(codigo: str) -> dict[str, str]:
    """Devuelve el estado, cliente y fecha de vencimiento de un contrato."""
    contrato = contratos.get(codigo.upper())
    if contrato is None:
        return {"codigo": codigo.upper(), "estado": "no encontrado"}
    return {"codigo": codigo.upper(), **contrato}


# Expone conocimiento estable mediante una URI, sin confundirlo con una tool.
@mcp.resource("legalmove://politica-operativa")
def politica_operativa() -> str:
    """Describe qué acción debe tomar el agente para cada estado contractual."""
    return (
        "vigente: continuar el proceso; "
        "en revisión: derivar a revisión humana; "
        "vencido: bloquear la firma hasta renovar."
    )


# Expone una plantilla reutilizable que un host puede solicitar antes de conversar.
@mcp.prompt
def revisar_contrato(codigo: str) -> str:
    """Crea la instrucción de auditoría para el contrato indicado."""
    return f"Consultá el contrato {codigo} y recomendá una acción según la política operativa."

# Resumen final: este módulo declara un servidor MCP real y no lo inicia al importarlo.
# Publicalo con: fastmcp run 00_servidor_contratos.py:mcp
