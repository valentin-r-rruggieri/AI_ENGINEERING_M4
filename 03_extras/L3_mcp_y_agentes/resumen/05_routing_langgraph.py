# Caso adicional LangGraph de L3: routing de consultas de agente.
"""Grafo que elige si una consulta necesita una tool contractual."""
from dotenv import load_dotenv
load_dotenv()

from typing import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph

class EstadoConsulta(TypedDict):
    consulta: str
    destino: NotRequired[str]

def elegir_capacidad(state: EstadoConsulta) -> dict:
    return {"destino": "tool_mcp" if "contrato" in state["consulta"].lower() else "respuesta_directa"}

grafo = StateGraph(EstadoConsulta)
grafo.add_node("elegir_capacidad", elegir_capacidad)
grafo.add_edge(START, "elegir_capacidad")
grafo.add_edge("elegir_capacidad", END)
entrada: EstadoConsulta = {"consulta": "Consultá el estado del contrato C-200"}
print(grafo.compile().invoke(entrada))
