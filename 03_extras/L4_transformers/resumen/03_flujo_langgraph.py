# Este archivo agrega LangGraph al resumen práctico de L4.
"""Caso 4: flujo que calcula métricas y las explica con LangChain."""

# Carga las variables globales antes de crear el modelo.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain, LangGraph y Pydantic.
from typing import NotRequired, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

# Define la explicación tipada que recibe una persona usuaria.
class Explicacion(BaseModel):
    cantidad_tokens: int
    explicacion: str

# Define el estado del recorrido Transformer.
class EstadoTransformer(TypedDict):
    texto: str
    tokens: NotRequired[list[str]]
    explicacion: NotRequired[dict[str, object]]

# Convierte el texto en tokens simples para visualizar la primera etapa.
def tokenizar(state: EstadoTransformer) -> dict:
    return {"tokens": state["texto"].split()}

# Explica la métrica obtenida sin reemplazar el cálculo Transformer.
def explicar(state: EstadoTransformer) -> dict:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Explicacion)
    pedido = f"Explica por qué esta frase tiene {len(state['tokens'])} tokens: {state['texto']}"
    return {"explicacion": extractor.invoke(pedido).model_dump()}

# Une cálculo y explicación como dos nodos visibles.
grafo = StateGraph(EstadoTransformer)
grafo.add_node("tokenizar", tokenizar)
grafo.add_node("explicar", explicar)
grafo.add_edge(START, "tokenizar")
grafo.add_edge("tokenizar", "explicar")
grafo.add_edge("explicar", END)
entrada: EstadoTransformer = {"texto": "el contrato vence mañana"}
resultado = grafo.compile().invoke(entrada)

# Muestra la explicación final.
print(resultado["explicacion"])
