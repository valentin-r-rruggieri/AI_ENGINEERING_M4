# Este archivo resume L1 mediante un agente de control de calidad visual.
# Lee cada bloque y modifica una variable por vez.

"""Caso 2: agente visual con OpenAI o Gemini para controlar calidad.

GUÍA DOCENTE
CUÁNDO USAR: cuando hay que decidir si una imagen es apta antes de extraerla.
DIFERENCIA: el proveedor cambia, pero LangChain y Pydantic mantienen la interfaz.
EN CLASE: comparar calidad visual, campos legibles y acción recomendada.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa utilidades para escoger el proveedor y preparar la imagen.
import base64
import os
from pathlib import Path

# Importa los dos wrappers LangChain y el modelo de salida compartido.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define el informe que permite actuar sobre una imagen de baja calidad.
class ControlCalidadVisual(BaseModel):
    campos_legibles: list[str] = Field(min_length=1)
    problema_visual: str
    confianza: float = Field(ge=0, le=1)
    accion: str
    respuesta_para_operador: str

# Usa el formulario borroso para que el caso tenga una decisión interesante.
raiz = Path(__file__).resolve().parents[3]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_borroso.png"
proveedor = os.getenv("PROVEEDOR_VISION", "openai").lower()
# Selecciona una fábrica de wrappers sin construir el proveedor no elegido.
fabricas_modelo = {
    "openai": lambda: ChatOpenAI(model="gpt-4o", temperature=0),
    "gemini": lambda: ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0),
}
modelo = fabricas_modelo[proveedor]()

# Codifica la imagen y crea un mensaje que ambos proveedores comprenden.
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Evalúa legibilidad, campos visibles y acción operativa para este formulario."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
agente = create_agent(model=modelo, tools=[], response_format=ControlCalidadVisual,
                      system_prompt="Sos un auditor visual. Nunca inventes campos: si no se leen, pedí una nueva imagen.")
turno = agente.invoke({"messages": [mensaje]})
resultado = ControlCalidadVisual.model_validate(turno["structured_response"])

# Muestra la salida que se usaría para orientar a una persona operadora.
print({"proveedor": proveedor, **resultado.model_dump()})

# Resumen final: se puede cambiar de proveedor sin cambiar el contrato de calidad.
# Definí PROVEEDOR_VISION=gemini y compará la respuesta con el mismo schema.
