# Este archivo forma parte del resumen integrador de adaptación y despliegue.
# Ejecutalo para ver la métrica de capacidad antes de la recomendación del agente.

"""Flujo LangGraph que calcula carga por réplica y recomienda un despliegue.

GUÍA DOCENTE
CUÁNDO USAR: cuando se quiere justificar una arquitectura con una métrica simple.
DIFERENCIA: LangGraph calcula y conserva el estado; LangChain propone la decisión final.
EN CLASE: recorrer perfil -> carga por réplica -> recomendación y observabilidad.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa tipos para declarar el estado del grafo y evitar datos implícitos.
from typing import NotRequired, TypedDict, cast

# Importa LangChain, LangGraph y Pydantic para el nodo final de arquitectura.
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


# Define la recomendación que queda disponible al final del flujo.
class DecisionDespliegue(BaseModel):
    perfil: str = ""
    destino: str
    replicas: int = Field(ge=1)
    observabilidad: str
    motivo: str


# Define los datos de entrada y la métrica generada por el primer nodo.
class EstadoServing(TypedDict):
    perfil: str
    peticiones_por_minuto: int
    latencia_objetivo_ms: int
    replicas_actuales: int
    carga_por_replica: NotRequired[float]
    decision: NotRequired[dict[str, object]]


# Define las actualizaciones parciales que devuelven los nodos del flujo.
class ActualizacionCarga(TypedDict):
    carga_por_replica: float


class ActualizacionDecision(TypedDict):
    decision: dict[str, object]


# Calcula una métrica comprensible antes de pedir una recomendación al agente.
def medir_carga(state: EstadoServing) -> ActualizacionCarga:
    carga = state["peticiones_por_minuto"] / state["replicas_actuales"]
    return {"carga_por_replica": round(carga, 1)}


# Usa las métricas del estado para producir una decisión validada por Pydantic.
def recomendar_despliegue(state: EstadoServing) -> ActualizacionDecision:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(DecisionDespliegue)
    pedido = (
        f"Perfil: {state['perfil']}. Peticiones por minuto: {state['peticiones_por_minuto']}. "
        f"Latencia objetivo: {state['latencia_objetivo_ms']} ms. "
        f"Carga por réplica: {state.get('carga_por_replica', 0.0)}. "
        "Recomendá local, Docker o Kubernetes; definí réplicas y observabilidad."
    )
    decision_agente = DecisionDespliegue.model_validate(extractor.invoke(pedido))
    decision = DecisionDespliegue.model_validate({**decision_agente.model_dump(), "perfil": state["perfil"]})
    return {"decision": decision.model_dump()}


# Conecta medición y recomendación para que la justificación sea revisable.
grafo = StateGraph(EstadoServing)
grafo.add_node("medir_carga", medir_carga)
grafo.add_node("recomendar_despliegue", recomendar_despliegue)
grafo.add_edge(START, "medir_carga")
grafo.add_edge("medir_carga", "recomendar_despliegue")
grafo.add_edge("recomendar_despliegue", END)
aplicacion = grafo.compile()

# Ejecuta perfiles con carga moderada y alta para comparar las recomendaciones.
perfiles: list[EstadoServing] = [
    {"perfil": "api de equipo", "peticiones_por_minuto": 40, "latencia_objetivo_ms": 1200, "replicas_actuales": 1},
    {"perfil": "servicio público", "peticiones_por_minuto": 300, "latencia_objetivo_ms": 500, "replicas_actuales": 2},
]

# Inicia el mismo grafo por cada perfil y muestra la decisión de arquitectura.
for perfil in perfiles:
    entrada: EstadoServing = perfil
    resultado = cast(EstadoServing, aplicacion.invoke(entrada))
    print(resultado.get("decision", {}))

# Resumen final: la decisión no reemplaza las métricas; se apoya en ellas.
# Duplicá las réplicas del servicio público y compará la carga por réplica obtenida.
