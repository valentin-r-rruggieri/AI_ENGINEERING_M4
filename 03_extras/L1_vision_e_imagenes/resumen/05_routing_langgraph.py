# Caso adicional LangGraph de L1: routing según confianza visual.
"""Grafo que deriva una imagen a aceptación o revisión humana."""
from dotenv import load_dotenv
load_dotenv()

from typing import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph

class EstadoRevision(TypedDict):
    confianza: float
    destino: NotRequired[str]

def decidir_destino(state: EstadoRevision) -> dict:
    return {"destino": "revision_humana" if state["confianza"] < 0.85 else "aceptacion_automatica"}

grafo = StateGraph(EstadoRevision)
grafo.add_node("decidir_destino", decidir_destino)
grafo.add_edge(START, "decidir_destino")
grafo.add_edge("decidir_destino", END)
entrada: EstadoRevision = {"confianza": 0.78}
print(grafo.compile().invoke(entrada))
