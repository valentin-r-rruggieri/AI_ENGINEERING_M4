# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Grafo mínimo con estado y dos nodos.

GUÍA DOCENTE
CUÁNDO USAR: cuando un workflow necesita pasos y estado explícitos.
DIFERENCIA: cada nodo recibe el estado y devuelve solo sus cambios.
EN CLASE: seguir START, nodos, edges y END.
"""

# Importa TypedDict para el estado y componentes de LangGraph.
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# Define los datos que pueden circular por el grafo.
class Estado(TypedDict):
    texto: str
    longitud: int

# Crea dos transformaciones pequeñas y visibles.
def limpiar(estado: Estado) -> dict[str, str]:
    return {"texto": estado["texto"].strip().lower()}

def medir(estado: Estado) -> dict[str, int]:
    return {"longitud": len(estado["texto"])}

# Conecta los nodos en un orden fijo.
constructor = StateGraph(Estado)
constructor.add_node("limpiar", limpiar)
constructor.add_node("medir", medir)
constructor.add_edge(START, "limpiar")
constructor.add_edge("limpiar", "medir")
constructor.add_edge("medir", END)
grafo = constructor.compile()

# Ejecuta el flujo y muestra su estado final.
print(grafo.invoke({"texto": "  Contrato Vigente  ", "longitud": 0}))

# Resumen final: este ejercicio transforma un estado mediante dos nodos.
# Invierte los nodos y explica por qué cambia la longitud.
