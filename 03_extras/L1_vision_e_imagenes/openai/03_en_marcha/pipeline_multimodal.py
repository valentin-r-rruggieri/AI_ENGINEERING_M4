# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline corto de imagen a decisión validada.

GUÍA DOCENTE
CUÁNDO USAR: para automatizar documentos manteniendo un umbral de revisión humana.
DIFERENCIA: el pipeline no solo extrae; también valida y decide si revisar.
EN CLASE: seguir imagen, Base64, modelo Pydantic y decisión final.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa utilidades estándar para preparar la entrada.
import base64
import os
from pathlib import Path

# Importa LangChain y Pydantic para extracción y validación.
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Modela el resultado final que consumirá el sistema de negocio.
class Solicitud(BaseModel):
    titular: str
    documento: str
    importe: float = Field(ge=0)
    confianza: float = Field(ge=0, le=1)

# Prepara la imagen incluida en los ejercicios de L1.
raiz = Path(__file__).resolve().parents[4]
imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
umbral_revision = 0.85

# Extrae datos por medio del wrapper LangChain y el schema Pydantic.
modelo = ChatOpenAI(model="gpt-4o", temperature=0)
extractor = modelo.with_structured_output(Solicitud, method="json_schema")
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Extrae titular, documento, importe y confianza."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
solicitud = extractor.invoke([mensaje])
requiere_revision = solicitud.confianza < umbral_revision
print(solicitud.model_dump())
print("Revisión humana:", requiere_revision)
# Resumen final: este pipeline extrae, valida y deriva una decisión operativa.
# Cambia el umbral de revisión y analiza el impacto en automatización y riesgo.
