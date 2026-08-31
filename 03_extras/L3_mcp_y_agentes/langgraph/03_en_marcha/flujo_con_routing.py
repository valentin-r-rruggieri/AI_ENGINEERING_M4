# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Flujo corto con estado, routing y dos resultados posibles.

GUÍA DOCENTE
CUÁNDO USAR: cuando una condición debe decidir explícitamente el próximo nodo.
DIFERENCIA: el routing está en código y no queda oculto dentro del modelo.
EN CLASE: dibujar ambos caminos antes de compilar el grafo.
"""

# Importa TypedDict para declarar el estado compartido.
from typing import TypedDict

# Importa los componentes utilizados para construir el grafo.
from langgraph.graph import END, START, StateGraph

# Define los datos que viajan entre los nodos.
class Estado(TypedDict):
    confianza: float
    decision: str

# Define los dos resultados posibles del flujo.
def aprobar(estado: Estado) -> dict[str, str]:
    return {"decision": "aprobado automáticamente"}

def revisar(estado: Estado) -> dict[str, str]:
    return {"decision": "enviar a revisión humana"}

# Selecciona el siguiente nodo usando un umbral visible.
def elegir_ruta(estado: Estado) -> str:
    return "aprobar" if estado["confianza"] >= 0.85 else "revisar"

# Construye, conecta y compila el grafo.
constructor = StateGraph(Estado)
constructor.add_node("aprobar", aprobar)
constructor.add_node("revisar", revisar)
constructor.add_conditional_edges(START, elegir_ruta, {"aprobar": "aprobar", "revisar": "revisar"})
constructor.add_edge("aprobar", END)
constructor.add_edge("revisar", END)
grafo = constructor.compile()

# Ejecuta un caso pequeño y muestra el estado final.
print(grafo.invoke({"confianza": 0.82, "decision": ""}))

# Resumen final: este ejercicio integra estado, routing y control explícito.
# Cambia confianza a 0.90 y observa qué nodo recibe la ejecución.
