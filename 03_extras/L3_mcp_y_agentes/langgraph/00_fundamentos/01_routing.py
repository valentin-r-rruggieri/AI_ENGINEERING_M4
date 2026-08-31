# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Routing condicional según confianza.

GUÍA DOCENTE
CUÁNDO USAR: cuando el estado determina el próximo paso del workflow.
DIFERENCIA: una edge fija siempre sigue el mismo camino; routing puede bifurcar.
EN CLASE: probar un valor a cada lado del umbral.
"""

# Importa TypedDict y los componentes del grafo.
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# Define confianza y decisión final.
class Estado(TypedDict):
    confianza: float
    decision: str

# Selecciona la rama sin modificar el estado.
def elegir_rama(estado: Estado) -> str:
    return "aprobar" if estado["confianza"] >= 0.85 else "revisar"

# Cada nodo escribe una decisión distinta.
def aprobar(estado: Estado) -> dict[str, str]:
    return {"decision": "automatizado"}

def revisar(estado: Estado) -> dict[str, str]:
    return {"decision": "revision_humana"}

# Construye la bifurcación condicional.
constructor = StateGraph(Estado)
constructor.add_node("aprobar", aprobar)
constructor.add_node("revisar", revisar)
constructor.add_conditional_edges(START, elegir_rama, {"aprobar": "aprobar", "revisar": "revisar"})
constructor.add_edge("aprobar", END)
constructor.add_edge("revisar", END)
grafo = constructor.compile()

print(grafo.invoke({"confianza": 0.82, "decision": ""}))

# Resumen final: este ejercicio dirige el flujo mediante una regla explícita.
# Cambia confianza a 0.90 y observa la otra rama.
