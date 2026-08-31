# Este archivo resume L1 mediante un agente de revisión documental.
# Lee cada bloque y modifica una variable por vez.

"""Caso 3: agente que compara visión, OCR y reglas de revisión.

GUÍA DOCENTE
CUÁNDO USAR: cuando una extracción visual necesita evidencia adicional de OCR.
DIFERENCIA: OCR lee caracteres; el agente decide si ambas evidencias son suficientes.
EN CLASE: separar evidencia, regla de negocio y respuesta para el cliente.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa herramientas para imagen, agente LangChain y contrato tipado.
import base64
import os
from pathlib import Path
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define la salida completa de una revisión que puede escalar a una persona.
class DecisionRevision(BaseModel):
    datos_detectados: list[str] = Field(min_length=1)
    coincidencia_con_ocr: bool
    confianza: float = Field(ge=0, le=1)
    requiere_revision_humana: bool
    respuesta_para_cliente: str

# Reutiliza una imagen con dificultad y un OCR local como evidencia adicional.
raiz = Path(__file__).resolve().parents[3]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_cafe.png"
texto_ocr = "Titular: Ana Pérez. Documento: 30111222."

# Une la evidencia OCR con la imagen para que el agente compare ambas fuentes.
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
mensaje = HumanMessage(content=[
    {"type": "text", "text": f"OCR previo: {texto_ocr}. Compará el OCR con la imagen y decidí si requiere revisión humana."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
agente = create_agent(model=ChatOpenAI(model="gpt-4o", temperature=0), tools=[], response_format=DecisionRevision,
                      system_prompt="Sos un revisor documental prudente. Si OCR e imagen no coinciden, pedí revisión humana.")
turno = agente.invoke({"messages": [mensaje]})
resultado = DecisionRevision.model_validate(turno["structured_response"])
# Muestra la respuesta final que combina evidencia técnica y comunicación humana.
print(resultado.model_dump())

# Resumen final: el agente visual contrasta imagen y OCR antes de responder.
# Cambiá coincidencia_con_ocr a False y justificá la acción resultante.
