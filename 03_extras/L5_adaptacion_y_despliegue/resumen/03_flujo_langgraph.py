# Este archivo agrega LangGraph al resumen práctico de L5.
"""Caso 4: flujo de respuesta, métrica y recomendación de despliegue."""

# Carga las variables globales antes de crear el modelo.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain, LangGraph y Pydantic.
from time import perf_counter
from typing import NotRequired, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

# Define la recomendación tipada que termina el flujo.
class RecomendacionServing(BaseModel):
    destino: NotRequired[str]
    motivo: str

# Define el estado de la consulta de serving.
class EstadoServing(TypedDict):
    consulta: str
    latencia_ms: NotRequired[float]
    recomendacion: NotRequired[dict[str, object]]

# Mide una llamada LangChain real y conserva la latencia en el estado.
def responder(state: EstadoServing) -> dict:
    inicio = perf_counter()
    ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(state["consulta"])
    return {"latencia_ms": round((perf_counter() - inicio) * 1000, 1)}

# Elige una arquitectura a partir de la latencia medida.
def recomendar(state: EstadoServing) -> dict:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(RecomendacionServing)
    pedido = f"Latencia observada: {state['latencia_ms']} ms. Elegí Docker o Kubernetes y justificá en una oración."
    return {"recomendacion": extractor.invoke(pedido).model_dump()}

# Conecta respuesta, medición y recomendación.
grafo = StateGraph(EstadoServing)
grafo.add_node("responder", responder)
grafo.add_node("recomendar", recomendar)
grafo.add_edge(START, "responder")
grafo.add_edge("responder", "recomendar")
grafo.add_edge("recomendar", END)
entrada: EstadoServing = {"consulta": "Explica LoRA en una oración."}
resultado = grafo.compile().invoke(entrada)

# Muestra la recomendación final de serving.
print(resultado["recomendacion"])
