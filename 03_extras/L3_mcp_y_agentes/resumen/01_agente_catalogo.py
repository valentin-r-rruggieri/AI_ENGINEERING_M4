# Este archivo resume L3 mediante un agente LangChain con una tool de catálogo.
# Lee cada bloque y modifica una variable por vez.

"""Caso 2: un agente consulta una capacidad antes de responder.

GUÍA DOCENTE
CUÁNDO USAR: cuando la respuesta debe basarse en una fuente externa.
DIFERENCIA: el modelo decide; la tool aporta el dato verificable.
EN CLASE: observar que el agente no debe inventar el estado contractual.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain, Pydantic y la clave para decidir el modo de ejecución.
import os
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

# Define el mismo contrato de respuesta que usaría un cliente MCP.
class RespuestaCatalogo(BaseModel):
    codigo: str
    estado: str
    requiere_revision: bool

# Declara la capacidad local con la forma de una tool que MCP puede publicar.
@tool
def consultar_contrato(codigo: str) -> str:
    """Consulta el estado vigente de un contrato."""
    return {"C-100": "vigente", "C-200": "en revisión"}.get(codigo, "inexistente")

# Crea un agente LangChain que usa la tool antes de responder a la consulta.
agente = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[consultar_contrato],
    system_prompt="Consultá la tool y respondé solo con el estado obtenido.",
)
respuesta_agente = agente.invoke({"messages": [{"role": "user", "content": "Estado de C-200"}]})
estado = str(respuesta_agente["messages"][-1].content)
# Convierte el dato del agente en una salida tipada de la aplicación.
resultado = RespuestaCatalogo(codigo="C-200", estado=estado, requiere_revision="revisión" in estado)
print(resultado.model_dump())

# Resumen final: LangChain orquesta la decisión y MCP entrega la capacidad.
# Consultá C-100 y compará cuándo cambia requiere_revision.
