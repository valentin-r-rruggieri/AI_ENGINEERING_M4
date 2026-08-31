# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Routing previo a una capacidad remota.

GUÍA DOCENTE
CUÁNDO USAR: para permitir una tool solo cuando el estado cumple una política.
DIFERENCIA: el routing es control de flujo; no reemplaza permisos del servidor MCP.
EN CLASE: separar política del cliente y autorización del servidor.
"""

# Importa TypedDict y componentes del grafo.
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# Define si el usuario cuenta con permiso para consultar.
class Estado(TypedDict):
    autorizado: bool
    resultado: str

# Selecciona consulta o rechazo según el estado.
def decidir(estado: Estado) -> str:
    return "consultar" if estado["autorizado"] else "rechazar"

def consultar(estado: Estado) -> dict[str, str]:
    return {"resultado": "Aquí se llamaría la tool MCP autorizada."}

def rechazar(estado: Estado) -> dict[str, str]:
    return {"resultado": "Acceso rechazado antes de llamar la tool."}

# Construye y ejecuta el control previo.
constructor = StateGraph(Estado)
constructor.add_node("consultar", consultar)
constructor.add_node("rechazar", rechazar)
constructor.add_conditional_edges(START, decidir, {"consultar": "consultar", "rechazar": "rechazar"})
constructor.add_edge("consultar", END)
constructor.add_edge("rechazar", END)
grafo = constructor.compile()
print(grafo.invoke({"autorizado": False, "resultado": ""}))

# Resumen final: este ejercicio aplica una política antes de una tool remota.
# Cambia autorizado a True y observa la rama habilitada.
