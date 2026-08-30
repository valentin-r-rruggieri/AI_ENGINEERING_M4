# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""LegalMove expresado como un grafo de dos agentes.

GUÍA DOCENTE
CUÁNDO USAR: cuando el handoff debe quedar explícito y ser extensible.
DIFERENCIA: LangGraph conserva el estado entre nodos especializados.
EN CLASE: inspeccionar estado inicial, contexto y output validado.
"""

# Importa os, tipos, LangGraph, OpenAI y Pydantic.
import os
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field

# Define el contrato común a los tres frameworks.
class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resumen_ejecutivo: str = Field(min_length=10)
    cambios_detectados: list[str] = Field(min_length=1)
    riesgos_legales: list[str]

# Declara el estado completo del workflow.
class Estado(TypedDict):
    original: str
    nuevo: str
    contexto: str
    resultado: ContractChangeOutput | None

# Prepara los modelos solo cuando existe la credencial.
modelo = ChatOpenAI(model="gpt-4.1-mini", temperature=0) if os.getenv("OPENAI_API_KEY") else None
modelo_salida = modelo.with_structured_output(ContractChangeOutput, method="json_schema") if modelo else None

# El primer nodo construye contexto sin extraer cambios.
def contextualizar(estado: Estado) -> dict[str, str]:
    if modelo:
        respuesta = modelo.invoke(f"Describe tema y estructura sin listar cambios. Original: {estado['original']} Nuevo: {estado['nuevo']}")
        return {"contexto": str(respuesta.content)}
    return {"contexto": "Ambas cláusulas regulan vigencia y renovación."}

# El segundo nodo produce el contrato de salida.
def extraer(estado: Estado) -> dict[str, ContractChangeOutput]:
    if modelo_salida:
        salida = modelo_salida.invoke(f"Contexto: {estado['contexto']} Original: {estado['original']} Nuevo: {estado['nuevo']}")
        return {"resultado": salida}
    salida = ContractChangeOutput(
        resumen_ejecutivo="Se amplía la vigencia y se incorpora renovación automática.",
        cambios_detectados=["El plazo aumenta de 12 a 18 meses.", "Se agrega renovación por 12 meses."],
        riesgos_legales=["La renovación automática puede requerir aviso previo."],
    )
    return {"resultado": salida}

# Compila y ejecuta el handoff.
constructor = StateGraph(Estado)
constructor.add_node("contextualizador", contextualizar)
constructor.add_node("extractor", extraer)
constructor.add_edge(START, "contextualizador")
constructor.add_edge("contextualizador", "extractor")
constructor.add_edge("extractor", END)
grafo = constructor.compile()
estado_final = grafo.invoke({
    "original": "Vigencia de 12 meses sin renovación automática.",
    "nuevo": "Vigencia de 18 meses con renovación automática por 12 meses.",
    "contexto": "",
    "resultado": None,
})
print(estado_final["resultado"].model_dump_json(indent=2))

# Resumen final: este grafo implementa un handoff y una salida tipada.
# Agrega una rama de revisión humana cuando el resultado tenga riesgos.
