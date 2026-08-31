# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Salida JSON de Gemini validada por un schema.

GUÍA DOCENTE
CUÁNDO USAR: cuando otra aplicación consumirá los datos extraídos.
DIFERENCIA: response_schema restringe la forma de la respuesta.
EN CLASE: inspeccionar el modelo Pydantic antes de llamar a Gemini.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa utilidades para credenciales, archivos y Base64.
import base64
import os
from pathlib import Path

# Importa LangChain y Pydantic para el contrato estructurado.
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Define el contrato de salida del formulario.
class Formulario(BaseModel):
    titular: str
    documento: str
    confianza: float = Field(ge=0, le=1)

# Localiza la imagen reutilizada en el recorrido.
raiz = Path(__file__).resolve().parents[4]
ruta_imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

# Solicita el schema Pydantic mediante el wrapper estructurado de LangChain.
imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")
modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
extractor = modelo.with_structured_output(Formulario)
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Extrae los datos del formulario."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
formulario = extractor.invoke([mensaje])
print(formulario.model_dump())
# Resumen final: este ejercicio combina visión, JSON y Pydantic.
# Agrega un campo obligatorio y observa cómo cambia la respuesta.
