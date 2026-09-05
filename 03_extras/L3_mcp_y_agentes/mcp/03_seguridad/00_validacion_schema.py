# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Restricciones de argumentos en una tool MCP.

GUÍA DOCENTE
CUÁNDO USAR: para rechazar entradas inválidas antes de ejecutar la lógica.
DIFERENCIA: type hints validan tipos; Field agrega límites y descripciones.
EN CLASE: comprobar que la función no recibe valores fuera del contrato.
"""

# Importa Annotated y Field para enriquecer el schema de entrada.
from typing import Annotated, Literal
from pydantic import Field

# Importa FastMCP para publicar el schema generado desde la firma.
from fastmcp import FastMCP

# Crea un servidor con una tool validada.
mcp = FastMCP("Validación")

# Restringe cantidad, prioridad y descripción desde la firma.
@mcp.tool()
def crear_revision(
    contrato: Annotated[str, Field(min_length=3, description="ID del contrato")],
    prioridad: Literal["baja", "media", "alta"] = "media",
    paginas: Annotated[int, Field(ge=1, le=200)] = 1,
) -> dict[str, str | int]:
    """Crea una solicitud de revisión contractual."""
    return {"contrato": contrato, "prioridad": prioridad, "paginas": paginas}

# Muestra cómo probar la validación sin iniciar el servidor.
print("Tool registrada: crear_revision; paginas permitidas: 1 a 200")

# Resumen final: este ejercicio convierte restricciones en JSON Schema.
# Intenta enviar prioridad urgente desde Inspector y observa el rechazo.
