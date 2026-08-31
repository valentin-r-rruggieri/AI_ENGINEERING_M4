# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para comparar un formulario limpio, borroso, roto y manchado con café.

"""Agente LangChain para detectar datos y calidad de documentos bancarios.

GUÍA DOCENTE
CUÁNDO USAR: cuando una imagen puede contener información útil pero su calidad cambia.
DIFERENCIA: LangChain orquesta el mensaje, el modelo visual y el schema Pydantic.
EN CLASE: explicar que el modelo debe extraer solo datos visibles y pedir revisión ante dudas.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 para enviar cada imagen al modelo de visión.
import base64
from pathlib import Path

# Importa LangChain para crear el agente y enviar un mensaje multimodal.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Importa Pydantic para exigir una respuesta consistente en los cuatro casos.
from pydantic import BaseModel, Field


# Define el contrato que debe devolver el agente para cada documento revisado.
class RevisionDocumento(BaseModel):
    archivo: str = ""
    datos_detectados: list[str] = Field(min_length=1)
    calidad: str
    accion: str
    confianza: float = Field(ge=0, le=1)
    motivo: str


# Ubica la carpeta compartida que contiene las cuatro imágenes del ejercicio.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data"

# Declara los cuatro casos para que el mismo agente los evalúe con el mismo criterio.
casos = [
    ("formulario_bancario_limpio.png", "formulario normal y legible"),
    ("formulario_bancario_borroso.png", "formulario borroso"),
    ("formulario_bancario_roto.png", "formulario roto o incompleto"),
    ("formulario_bancario_cafe.png", "formulario manchado con café"),
]

# Crea un agente LangChain con salida estructurada validada por Pydantic.
agente = create_agent(
    model=ChatOpenAI(model="gpt-4o", temperature=0),
    tools=[],
    response_format=RevisionDocumento,
    system_prompt=(
        "Sos un analista documental bancario. Extraé únicamente datos que se vean "
        "en la imagen. Indicá calidad aceptable, baja o crítica. Recomendá aceptar, "
        "revisión humana o solicitar nuevo documento. Nunca inventes datos tapados."
    ),
)

# Recorre cada versión y convierte sus bytes a Base64 para el mensaje multimodal.
for nombre_archivo, descripcion in casos:
    ruta_imagen = carpeta_datos / nombre_archivo
    imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")

    # Pide al agente extraer datos y decidir qué hacer con esta calidad de documento.
    mensaje = HumanMessage(content=[
        {
            "type": "text",
            "text": f"Revisá este caso: {descripcion}. Indicá los datos visibles y una decisión.",
        },
        {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
    ])
    respuesta = agente.invoke({"messages": [mensaje]})["structured_response"]
    revision = RevisionDocumento.model_validate({**respuesta.model_dump(), "archivo": nombre_archivo})

    # Muestra una respuesta fácil de comparar con los otros tres casos.
    print(revision.model_dump())

# Resumen final: un agente puede usar visión y Pydantic para derivar una acción segura.
# Cambiá una imagen por otra dañada y observá cómo cambia calidad, confianza y acción.
