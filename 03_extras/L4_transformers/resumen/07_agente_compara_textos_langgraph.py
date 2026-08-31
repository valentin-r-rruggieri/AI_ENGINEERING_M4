# Este archivo forma parte del resumen integrador de Transformers.
# Ejecutalo para recorrer tokenización, forma de atención y explicación en un grafo.

"""Flujo LangGraph que explica métricas de dos textos de entrada.

GUÍA DOCENTE
CUÁNDO USAR: cuando se quiere separar las etapas que alimentan un Transformer.
DIFERENCIA: LangGraph conserva las métricas; LangChain las traduce a lenguaje claro.
EN CLASE: recorrer texto -> tokens -> forma de atención -> explicación tipada.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa los tipos usados para representar el estado entre nodos.
from typing import NotRequired, TypedDict, cast

# Importa LangChain, LangGraph y Pydantic para el nodo final de explicación.
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


# Define la explicación final que se obtiene a partir de las métricas calculadas.
class ExplicacionEntrada(BaseModel):
    texto: str = ""
    tokens: list[str] = []
    forma_atencion: str = ""
    explicacion: str


# Define el estado inicial y las actualizaciones agregadas durante el flujo.
class EstadoTransformer(TypedDict):
    texto: str
    tokens: NotRequired[list[str]]
    forma_atencion: NotRequired[str]
    explicacion: NotRequired[dict[str, object]]


# Define las actualizaciones que devuelven los tres nodos explícitos.
class ActualizacionTokens(TypedDict):
    tokens: list[str]


class ActualizacionAtencion(TypedDict):
    forma_atencion: str


class ActualizacionExplicacion(TypedDict):
    explicacion: dict[str, object]


# Divide el texto en tokens para representar la primera etapa del Transformer.
def tokenizar_texto(state: EstadoTransformer) -> ActualizacionTokens:
    return {"tokens": state["texto"].split()}


# Calcula la dimensión didáctica de una matriz de self-attention.
def calcular_atencion(state: EstadoTransformer) -> ActualizacionAtencion:
    cantidad_tokens = len(state.get("tokens", []))
    return {"forma_atencion": f"({cantidad_tokens}, {cantidad_tokens})"}


# Usa LangChain para explicar las métricas obtenidas sin reemplazar el cálculo local.
def explicar_transformer(state: EstadoTransformer) -> ActualizacionExplicacion:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ExplicacionEntrada)
    pedido = (
        f"Texto: {state['texto']}. Tokens: {state.get('tokens', [])}. "
        f"Forma de self-attention: {state.get('forma_atencion', '')}. "
        "Explicá qué cambia entre entradas cortas y largas."
    )
    explicacion_agente = ExplicacionEntrada.model_validate(extractor.invoke(pedido))
    explicacion = ExplicacionEntrada.model_validate({
        **explicacion_agente.model_dump(),
        "texto": state["texto"],
        "tokens": state.get("tokens", []),
        "forma_atencion": state.get("forma_atencion", ""),
    })
    return {"explicacion": explicacion.model_dump()}


# Conecta las tres etapas que hacen visible el recorrido de los datos.
grafo = StateGraph(EstadoTransformer)
grafo.add_node("tokenizar_texto", tokenizar_texto)
grafo.add_node("calcular_atencion", calcular_atencion)
grafo.add_node("explicar_transformer", explicar_transformer)
grafo.add_edge(START, "tokenizar_texto")
grafo.add_edge("tokenizar_texto", "calcular_atencion")
grafo.add_edge("calcular_atencion", "explicar_transformer")
grafo.add_edge("explicar_transformer", END)
aplicacion = grafo.compile()

# Ejecuta el mismo grafo con una frase corta y otra más larga para compararlas.
for texto in ["el contrato vence mañana", "el contrato de servicios vence mañana y requiere una adenda firmada"]:
    entrada: EstadoTransformer = {"texto": texto}
    resultado = cast(EstadoTransformer, aplicacion.invoke(entrada))
    print(resultado.get("explicacion", {}))

# Resumen final: la forma de atención se calcula antes de que el agente la explique.
# Cambiá una entrada y usá los nodos para localizar qué métrica se modifica.
