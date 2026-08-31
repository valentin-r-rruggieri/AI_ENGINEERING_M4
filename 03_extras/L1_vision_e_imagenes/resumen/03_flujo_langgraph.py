# Este archivo agrega LangGraph al resumen práctico de L1.
"""Caso 4: flujo visual con estado, agente y decisión tipada."""

# Carga las variables globales antes de crear el modelo.
from dotenv import load_dotenv
load_dotenv()

# Importa imagen, LangChain, LangGraph y Pydantic.
import base64
from pathlib import Path
from typing import NotRequired, TypedDict, cast
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

# Define la respuesta del nodo visual.
class DecisionVisual(BaseModel):
    titular: str
    confianza: float = Field(ge=0, le=1)
    accion: str

# Define el estado que viaja entre nodos del grafo.
class EstadoVision(TypedDict):
    imagen_base64: str
    decision: NotRequired[dict[str, object]]

# Define la actualización parcial que devuelve el nodo del grafo.
class ActualizacionVision(TypedDict):
    decision: dict[str, object]

# Prepara la imagen que ingresa al primer nodo.
raiz = Path(__file__).resolve().parents[3]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")

# Analiza la imagen y devuelve una decisión Pydantic convertida a diccionario.
def analizar_formulario(state: EstadoVision) -> ActualizacionVision:
    extractor = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(DecisionVisual)
    mensaje = HumanMessage(content=[
        {"type": "text", "text": "Identifica al titular y recomendá aceptar o revisar el formulario."},
        {"type": "image", "base64": state["imagen_base64"], "mime_type": "image/png"},
    ])
    return {"decision": extractor.invoke([mensaje]).model_dump()}

# Conecta inicio, nodo visual y final en un flujo explícito.
grafo = StateGraph(EstadoVision)
grafo.add_node("analizar_formulario", analizar_formulario)
grafo.add_edge(START, "analizar_formulario")
grafo.add_edge("analizar_formulario", END)
# Convierte la salida genérica de LangGraph al estado declarado para Pylance.
entrada: EstadoVision = {"imagen_base64": imagen_base64}
resultado = cast(EstadoVision, grafo.compile().invoke(entrada))

# Muestra el estado final del flujo.
print(resultado.get("decision", {}))
