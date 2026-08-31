# Caso adicional LangGraph de L5: routing de arquitectura de serving.
"""Grafo que decide entre un contenedor simple y un despliegue escalable."""
from dotenv import load_dotenv
load_dotenv()

from typing import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph

class EstadoServing(TypedDict):
    solicitudes_por_minuto: int
    destino: NotRequired[str]

def elegir_plataforma(state: EstadoServing) -> dict:
    return {"destino": "kubernetes" if state["solicitudes_por_minuto"] > 100 else "docker"}

grafo = StateGraph(EstadoServing)
grafo.add_node("elegir_plataforma", elegir_plataforma)
grafo.add_edge(START, "elegir_plataforma")
grafo.add_edge("elegir_plataforma", END)
entrada: EstadoServing = {"solicitudes_por_minuto": 300}
print(grafo.compile().invoke(entrada))
