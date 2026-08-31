# Este archivo agrega LangGraph al resumen práctico de L2.
"""Caso 4: flujo de transcripción, resumen y revisión de audio."""

# Carga las variables globales antes de crear el modelo.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain, LangGraph y Pydantic.
from typing import NotRequired, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

# Define el contrato que producirá el nodo de interpretación.
class DecisionAudio(BaseModel):
    resumen: str
    requiere_revision: bool

# Define el estado del pipeline de audio.
class EstadoAudio(TypedDict):
    transcripcion: str
    wer: float
    decision: NotRequired[dict[str, object]]

# Interpreta la transcripción después de que ASR y WER ya produjeron sus datos.
def revisar_audio(state: EstadoAudio) -> dict:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(DecisionAudio)
    pedido = f"Transcripción: {state['transcripcion']}. WER: {state['wer']}. Resume y decidí si requiere revisión."
    return {"decision": extractor.invoke(pedido).model_dump()}

# Construye el grafo con un único nodo de decisión explícito.
grafo = StateGraph(EstadoAudio)
grafo.add_node("revisar_audio", revisar_audio)
grafo.add_edge(START, "revisar_audio")
grafo.add_edge("revisar_audio", END)
entrada: EstadoAudio = {"transcripcion": "Tomar un comprimido cada ocho horas.", "wer": 0.0}
resultado = grafo.compile().invoke(entrada)

# Muestra el reporte que entrega el flujo.
print(resultado["decision"])
