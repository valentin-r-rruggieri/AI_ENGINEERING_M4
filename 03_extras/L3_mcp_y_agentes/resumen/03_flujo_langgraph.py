# Este archivo agrega LangGraph al resumen práctico de L3.
"""Caso 4: routing de una consulta hacia una capacidad contractual."""

# Carga las variables globales antes de crear el modelo.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain, LangGraph y Pydantic.
from typing import NotRequired, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

# Define la respuesta producida luego de consultar el catálogo.
class RespuestaAgente(BaseModel):
    codigo: str
    respuesta: str

# Define el estado que pasa por los nodos del grafo.
class EstadoMCP(TypedDict):
    codigo: str
    estado_contrato: NotRequired[str]
    respuesta: NotRequired[dict[str, object]]

# Simula la respuesta verificable que una tool MCP devolvería.
def consultar_tool(state: EstadoMCP) -> dict:
    catalogo = {"C-100": "vigente", "C-200": "en revisión"}
    return {"estado_contrato": catalogo.get(state["codigo"], "inexistente")}

# Redacta la respuesta usando el dato que entregó la tool.
def responder_agente(state: EstadoMCP) -> dict:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(RespuestaAgente)
    pedido = f"Contrato {state['codigo']} con estado {state['estado_contrato']}. Respondé de forma breve."
    return {"respuesta": extractor.invoke(pedido).model_dump()}

# Ordena los nodos: tool primero, agente después.
grafo = StateGraph(EstadoMCP)
grafo.add_node("consultar_tool", consultar_tool)
grafo.add_node("responder_agente", responder_agente)
grafo.add_edge(START, "consultar_tool")
grafo.add_edge("consultar_tool", "responder_agente")
grafo.add_edge("responder_agente", END)
entrada: EstadoMCP = {"codigo": "C-200"}
resultado = grafo.compile().invoke(entrada)

# Muestra la respuesta final del agente.
print(resultado["respuesta"])
