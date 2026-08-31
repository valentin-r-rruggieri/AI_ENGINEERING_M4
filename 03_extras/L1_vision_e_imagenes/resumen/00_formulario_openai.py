# Este archivo resume L1 mediante un agente visual de apertura de cuenta.
# Lee cada bloque y modifica una variable por vez.

"""Caso 1: agente LangChain que ve un formulario y responde una decisión.

GUÍA DOCENTE
CUÁNDO USAR: cuando una imagen inicia un proceso de negocio automatizado.
DIFERENCIA: el agente razona sobre la imagen; Pydantic controla su respuesta.
EN CLASE: seguir imagen, agente, schema, decisión y mensaje para la persona usuaria.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa utilidades para enviar la imagen y consultar la clave.
import base64
import os
from pathlib import Path

# Importa el agente LangChain, el mensaje multimodal y el contrato de salida.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define todo lo que el agente debe responder a la aplicación de apertura.
class RespuestaApertura(BaseModel):
    titular: str
    documento: str
    importe_solicitado: float = Field(ge=0)
    confianza: float = Field(ge=0, le=1)
    requiere_revision: bool
    respuesta_para_cliente: str = Field(min_length=10)

# Reutiliza la imagen de formulario real creada para L1.
raiz = Path(__file__).resolve().parents[3]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
umbral_revision = 0.85

# Convierte la imagen al bloque multimodal que entiende ChatOpenAI.
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Analiza el formulario. Extrae sus datos y decide si debe revisarlo una persona."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
# Crea un agente real: su respuesta queda limitada al schema Pydantic.
agente = create_agent(
    model=ChatOpenAI(model="gpt-4o", temperature=0), tools=[], response_format=RespuestaApertura,
    system_prompt=(f"Sos un analista de formularios. Marcá revisión si confianza es menor a {umbral_revision}. "
                   "No inventes datos ilegibles y respondé de forma amable para el cliente."),
)
turno = agente.invoke({"messages": [mensaje]})
resultado = RespuestaApertura.model_validate(turno["structured_response"])
# Muestra el contrato que la interfaz puede consumir sin interpretar texto libre.
print(resultado.model_dump())

# Resumen final: el agente ve, extrae, decide y responde usando un schema tipado.
# Cambia el umbral a 0.95 y discutí qué solicitudes pasarían a revisión.
