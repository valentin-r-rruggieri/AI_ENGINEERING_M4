# Caso adicional LangGraph de L4: routing según tamaño de secuencia.
"""Grafo que selecciona una estrategia de atención según cantidad de tokens."""

# Carga la configuración común aunque este flujo sea local.
from dotenv import load_dotenv
load_dotenv()

# Importa el grafo y el estado tipado del recorrido.
from typing import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph

# Define los datos necesarios para decidir una estrategia de atención.
class EstadoTokens(TypedDict):
    cantidad_tokens: int
    estrategia: NotRequired[str]

# Elige una estrategia según el tamaño que haría costosa la atención estándar.
def elegir_estrategia(state: EstadoTokens) -> dict:
    estrategia = "atencion_estandar" if state["cantidad_tokens"] <= 512 else "atencion_eficiente"
    return {"estrategia": estrategia}

# Construye el routing de una sola decisión y muestra su resultado.
grafo = StateGraph(EstadoTokens)
grafo.add_node("elegir_estrategia", elegir_estrategia)
grafo.add_edge(START, "elegir_estrategia")
grafo.add_edge("elegir_estrategia", END)
entrada: EstadoTokens = {"cantidad_tokens": 800}
print(grafo.compile().invoke(entrada))
