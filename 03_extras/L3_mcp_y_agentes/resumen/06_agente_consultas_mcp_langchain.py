# Este archivo forma parte del resumen integrador de MCP y agentes.
# Ejecutalo para ver a un agente consultar una capacidad antes de responder.

"""Agente LangChain que resuelve varias consultas mediante tools estilo MCP.

GUÍA DOCENTE
CUÁNDO USAR: cuando el modelo necesita un dato verificable antes de responder.
DIFERENCIA: la tool aporta el hecho; el agente interpreta ese hecho para la persona usuaria.
EN CLASE: mostrar que esta misma capacidad puede publicarse luego desde el servidor MCP.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa LangChain para declarar las tools y crear el agente que las utiliza.
from langchain.agents import create_agent
from langchain.tools import tool

# Importa Pydantic para validar la respuesta entregada después de consultar la tool.
from pydantic import BaseModel


# Define el contrato final que recibiría una interfaz de contratos.
class InformeContrato(BaseModel):
    codigo: str = ""
    estado: str = ""
    accion: str = ""
    explicacion: str


# Declara una tool pequeña con la misma intención que una tool publicada por MCP.
@tool
def consultar_estado_contrato(codigo: str) -> str:
    """Devuelve el estado verificable del contrato solicitado."""
    catalogo = {"C-100": "vigente", "C-200": "en revisión", "C-300": "vencido"}
    return catalogo.get(codigo, "inexistente")


# Crea un agente que debe llamar a la tool antes de construir su salida estructurada.
agente = create_agent(
    model="openai:gpt-4o-mini",
    tools=[consultar_estado_contrato],
    response_format=InformeContrato,
    system_prompt=(
        "Sos un asistente de contratos. Consultá siempre la tool antes de responder. "
        "Si está vigente, recomendá continuar; si está en revisión, recomendá revisión humana; "
        "si está vencido o es inexistente, recomendá no avanzar."
    ),
)

# Prueba tres consultas para enseñar que el agente no responde siempre lo mismo.
for codigo in ["C-100", "C-200", "C-300"]:
    pedido = f"Necesito saber qué hacer con el contrato {codigo}."
    respuesta = agente.invoke({"messages": [{"role": "user", "content": pedido}]})["structured_response"]
    estado_verificado = consultar_estado_contrato.invoke({"codigo": codigo})
    accion_verificada = {
        "vigente": "continuar",
        "en revisión": "revisión humana",
        "vencido": "no avanzar",
        "inexistente": "no avanzar",
    }[estado_verificado]
    informe = InformeContrato.model_validate({
        **respuesta.model_dump(),
        "codigo": codigo,
        "estado": estado_verificado,
        "accion": accion_verificada,
    })
    print(informe.model_dump())

# Resumen final: la tool evita que el agente invente un estado contractual.
# Cambiá C-300 por un código inexistente y compará la acción recomendada.
