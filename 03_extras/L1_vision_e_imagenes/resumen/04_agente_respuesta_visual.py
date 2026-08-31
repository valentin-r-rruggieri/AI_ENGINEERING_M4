# Caso adicional LangChain de L1: responder una consulta sobre una imagen.
"""Agente visual que identifica un documento y responde a una persona usuaria."""
from dotenv import load_dotenv
load_dotenv()

import base64
from pathlib import Path
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class RespuestaDocumento(BaseModel):
    tipo_documento: str
    dato_principal: str
    respuesta: str

raiz = Path(__file__).resolve().parents[3]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
agente = create_agent(model=ChatOpenAI(model="gpt-4o", temperature=0), tools=[], response_format=RespuestaDocumento,
                      system_prompt="Respondé solo con datos visibles en la imagen y no inventes información.")
mensaje = HumanMessage(content=[
    {"type": "text", "text": "¿Qué documento es y cuál es su dato principal? Respondé para el cliente."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
resultado = RespuestaDocumento.model_validate(agente.invoke({"messages": [mensaje]})["structured_response"])
print(resultado.model_dump())
