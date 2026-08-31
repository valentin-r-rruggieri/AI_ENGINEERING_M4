# Caso adicional LangGraph de L2: routing según calidad de audio.
"""Grafo que decide entre procesar una transcripción o pedir repetición."""
from dotenv import load_dotenv
load_dotenv()

from typing import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph

class EstadoAudio(TypedDict):
    wer: float
    destino: NotRequired[str]

def decidir_calidad(state: EstadoAudio) -> dict:
    return {"destino": "repetir_audio" if state["wer"] > 0.15 else "procesar_transcripcion"}

grafo = StateGraph(EstadoAudio)
grafo.add_node("decidir_calidad", decidir_calidad)
grafo.add_edge(START, "decidir_calidad")
grafo.add_edge("decidir_calidad", END)
entrada: EstadoAudio = {"wer": 0.21}
print(grafo.compile().invoke(entrada))
