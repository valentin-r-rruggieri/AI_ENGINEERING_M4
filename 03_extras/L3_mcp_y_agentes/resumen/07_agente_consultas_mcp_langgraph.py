# Este archivo forma parte del resumen integrador de MCP y agentes.
# Ejecutalo para ver la consulta de una tool y la respuesta como nodos separados.

"""Flujo LangGraph que consulta una capacidad contractual y genera una acción.

GUÍA DOCENTE
CUÁNDO USAR: cuando se necesita hacer visible el handoff entre una tool y un agente.
DIFERENCIA: LangGraph ordena los pasos; LangChain valida la respuesta final.
EN CLASE: señalar que el primer nodo obtiene el hecho y el segundo lo comunica.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa los tipos necesarios para declarar un estado claro y tipado.
from typing import NotRequired, TypedDict, cast

# Importa LangChain, LangGraph y Pydantic para construir el flujo de dos nodos.
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


# Define el contrato final que queda disponible después del handoff.
class InformeContrato(BaseModel):
    codigo: str = ""
    estado: str = ""
    accion: str = ""
    explicacion: str


# Define el estado de entrada y las claves agregadas por cada nodo.
class EstadoContrato(TypedDict):
    codigo: str
    estado: NotRequired[str]
    informe: NotRequired[dict[str, object]]


# Define las actualizaciones parciales de la capacidad y del agente.
class ActualizacionEstado(TypedDict):
    estado: str


class ActualizacionInforme(TypedDict):
    informe: dict[str, object]


# Consulta un catálogo local que representa la respuesta de una tool MCP.
def consultar_capacidad_mcp(state: EstadoContrato) -> ActualizacionEstado:
    catalogo = {"C-100": "vigente", "C-200": "en revisión", "C-300": "vencido"}
    return {"estado": catalogo.get(state["codigo"], "inexistente")}


# Usa el dato entregado por la tool para crear una respuesta validada por Pydantic.
def responder_agente(state: EstadoContrato) -> ActualizacionInforme:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(InformeContrato)
    pedido = (
        f"Contrato {state['codigo']}; estado verificado: {state.get('estado', 'inexistente')}. "
        "Elegí continuar, revisión humana o no avanzar y explicalo en una oración."
    )
    informe_agente = InformeContrato.model_validate(extractor.invoke(pedido))
    acciones = {
        "vigente": "continuar",
        "en revisión": "revisión humana",
        "vencido": "no avanzar",
        "inexistente": "no avanzar",
    }
    informe = InformeContrato.model_validate({
        **informe_agente.model_dump(),
        "codigo": state["codigo"],
        "estado": state.get("estado", "inexistente"),
        "accion": acciones[state.get("estado", "inexistente")],
    })
    return {"informe": informe.model_dump()}


# Conecta tool -> agente para hacer el handoff visible en el grafo.
grafo = StateGraph(EstadoContrato)
grafo.add_node("consultar_capacidad_mcp", consultar_capacidad_mcp)
grafo.add_node("responder_agente", responder_agente)
grafo.add_edge(START, "consultar_capacidad_mcp")
grafo.add_edge("consultar_capacidad_mcp", "responder_agente")
grafo.add_edge("responder_agente", END)
aplicacion = grafo.compile()

# Ejecuta los mismos tres contratos para comparar las salidas del agente.
for codigo in ["C-100", "C-200", "C-300"]:
    entrada: EstadoContrato = {"codigo": codigo}
    resultado = cast(EstadoContrato, aplicacion.invoke(entrada))
    print(resultado.get("informe", {}))

# Resumen final: el estado permite comprobar que el agente recibió el resultado de la tool.
# Cambiá el estado de C-200 en el catálogo y explicá qué nodo cambia primero.
