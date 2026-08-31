# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""ToolNode preparado con una tool local.

GUÍA DOCENTE
CUÁNDO USAR: cuando un nodo debe ejecutar tool calls solicitadas por el modelo.
DIFERENCIA: ToolNode administra mensajes de tool; la función conserva la lógica.
EN CLASE: probar la tool sola antes de conectarla al grafo.
"""

# Importa el decorador de tools y el nodo preconstruido.
from langchain.tools import tool
from langgraph.prebuilt import ToolNode

# Define una capacidad determinista.
@tool
def buscar_clausula(numero: int) -> str:
    """Busca una cláusula contractual por número."""
    return f"Cláusula {numero}: vigencia de doce meses."

# Agrupa la tool dentro de un nodo reutilizable.
nodo_tools = ToolNode([buscar_clausula])

# Prueba la lógica y muestra qué tool conoce el nodo.
print(buscar_clausula.invoke({"numero": 4}))
print("Tools del nodo:", list(nodo_tools.tools_by_name))

# Resumen final: este ejercicio prepara una capacidad para un grafo de agente.
# Agrega una segunda tool y verifica los nombres disponibles.
