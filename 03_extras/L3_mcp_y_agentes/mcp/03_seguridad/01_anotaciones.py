# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Anotaciones de seguridad y comportamiento de una tool.

GUÍA DOCENTE
CUÁNDO USAR: para informar al host si una acción lee, escribe o puede destruir.
DIFERENCIA: las anotaciones orientan al cliente; no reemplazan autorización real.
EN CLASE: discutir cuándo una interfaz debe pedir confirmación humana.
"""

# Importa FastMCP y las anotaciones estándar del protocolo.
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

# Crea el servidor que expone una consulta cerrada y de solo lectura.
mcp = FastMCP("Seguridad")

# Marca explícitamente la tool como no destructiva y de solo lectura.
@mcp.tool(
    title="Consultar política",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def consultar_politica(nombre: str) -> str:
    """Consulta una política incluida en el catálogo local."""
    return f"Política {nombre}: revisión humana obligatoria bajo confianza 0.80."

# Informa qué capacidad quedó preparada.
print("Tool de solo lectura registrada: consultar_politica")

# Resumen final: este ejercicio describe el riesgo operativo de una tool.
# Diseña las anotaciones que usarías para una tool capaz de borrar datos.
