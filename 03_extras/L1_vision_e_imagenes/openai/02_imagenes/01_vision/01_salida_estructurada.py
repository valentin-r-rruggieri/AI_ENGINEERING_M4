# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extracción visual con una salida validada por Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando una imagen debe convertirse en datos confiables.
DIFERENCIA: una descripción libre no garantiza nombres ni tipos de campos.
EN CLASE: explicar el schema antes de observar la respuesta del modelo.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa utilidades estándar para la clave, Base64 y rutas.
import base64
import os
from pathlib import Path

# Importa el mensaje multimodal, el wrapper LangChain y el modelo de validación.
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define exactamente los campos que debe devolver el modelo.
class Formulario(BaseModel):
    titular: str
    documento: str
    confianza: float = Field(ge=0, le=1)

# Prepara la imagen como una data URL.
raiz = Path(__file__).resolve().parents[4]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")

# Combina LangChain y Pydantic para pedir una salida estructurada nativa.
modelo = ChatOpenAI(model="gpt-4o", temperature=0)
extractor = modelo.with_structured_output(Formulario, method="json_schema")
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Extrae titular, documento y confianza."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
formulario = extractor.invoke([mensaje])
print(formulario.model_dump())
# Resumen final: este ejercicio une visión con validación estructurada.
# Agrega un campo obligatorio al schema y observa cómo cambia la extracción.
