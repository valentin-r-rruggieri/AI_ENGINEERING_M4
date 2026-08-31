# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extractor visual con decisión de revisión humana.

GUÍA DOCENTE
CUÁNDO USAR: para convertir un documento en datos con control de calidad.
DIFERENCIA: una confianza baja deriva el caso sin descartar el resultado.
EN CLASE: recorrer entrada, schema, extracción y regla de negocio.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa las herramientas necesarias para el pipeline.
import base64
import os
from pathlib import Path
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Define la salida que espera el proceso de negocio.
class Documento(BaseModel):
    tipo: str
    titular: str
    identificador: str
    confianza: float = Field(ge=0, le=1)

# Prepara el recurso y el umbral de revisión.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
umbral = 0.85

# Extrae un JSON conforme al modelo definido mediante LangChain.
imagen_base64 = base64.b64encode(ruta.read_bytes()).decode("utf-8")
modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
extractor = modelo.with_structured_output(Documento)
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Clasifica y extrae este documento."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
documento = extractor.invoke([mensaje])
# Muestra el dato validado y la decisión derivada.
print(documento.model_dump())
print("Revisión humana:", documento.confianza < umbral)

# Resumen final: este pipeline produce datos y una decisión operativa.
# Modifica el umbral para discutir precisión frente a automatización.
