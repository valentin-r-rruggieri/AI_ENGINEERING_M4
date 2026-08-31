# Este archivo resume L3 mediante una API que expone una respuesta tipada.
# Lee la explicación y ejecutá uvicorn cuando quieras levantar el servicio.

"""Caso 3: exponer una consulta de agente mediante FastAPI.

GUÍA DOCENTE
CUÁNDO USAR: cuando una interfaz web necesita consumir un agente y sus tools.
DIFERENCIA: FastAPI expone HTTP; LangChain resuelve la interacción con el modelo.
EN CLASE: seguir request, validación Pydantic y response_model.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa FastAPI, LangChain y Pydantic para declarar el contrato HTTP.
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define entrada y salida explícitas para el endpoint.
class ConsultaContrato(BaseModel):
    codigo: str = Field(min_length=3)

class RespuestaCatalogo(BaseModel):
    codigo: str
    estado: str
    requiere_revision: bool
    explicacion_agente: str

# Crea una API pequeña que representa la frontera del agente.
app = FastAPI(title="Resumen L3: agente MCP")

@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}

@app.post("/consultar", response_model=RespuestaCatalogo)
def consultar(consulta: ConsultaContrato) -> RespuestaCatalogo:
    # Simula el dato que el agente obtiene desde la tool MCP del caso anterior.
    estado = {"C-100": "vigente", "C-200": "en revisión"}.get(consulta.codigo, "inexistente")
    explicacion = modelo.invoke(
        f"Explica en una oración el estado {estado} del contrato {consulta.codigo}."
    ).content
    return RespuestaCatalogo(
        codigo=consulta.codigo,
        estado=estado,
        requiere_revision="revisión" in estado,
        explicacion_agente=str(explicacion),
    )

# Prepara el modelo LangChain que el endpoint usa para su explicación.
modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Indica cómo iniciar el servicio sin usar un bloque main.
print("Ejecutá: uvicorn 02_api_agente:app --reload")

# Resumen final: una API tipada hace consumible el resultado de un agente.
# Probá POST /consultar con {\"codigo\": \"C-200\"} desde /docs.
