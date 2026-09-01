# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para leer una factura, una página de libro y una adenda contractual.

"""Agente LangChain de visión para tres tipos documentales diferentes.

GUÍA DOCENTE
CUÁNDO USAR: cuando un mismo pipeline debe clasificar y extraer datos de documentos distintos.
DIFERENCIA: el modelo recibe una imagen por vez, pero el schema mantiene una salida uniforme.
EN CLASE: comparar qué dato clave se espera de una factura, un libro y una adenda.
"""

# Carga una sola vez las claves globales del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 y Path para leer cada documento visual por separado.
import base64
from pathlib import Path
from typing import Literal

# Importa LangChain para el agente visual y Pydantic para la salida estructurada.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field


# Define un contrato común para los tres documentos, con descriptions orientadas a la IA.
class LecturaDocumento(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_documento: Literal["factura", "pagina_libro", "adenda_contractual"] = Field(
        description="Clasificación visual: factura comercial, página de libro o adenda contractual."
    )
    titulo: str = Field(description="Encabezado o título principal visible del documento.")
    identificador: str = Field(
        description="Factura: número de factura. Libro: número de página. Adenda: código de contrato."
    )
    datos_clave: list[str] = Field(
        min_length=2,
        description="Factura: emisor, cliente, fecha y total. Libro: capítulo, autor e idea central. Adenda: fecha y cambios de cláusulas."
    )
    resumen: str = Field(description="Resumen fiel de una o dos oraciones sin inventar información.")
    confianza: float = Field(ge=0, le=1, description="Confianza de lectura entre 0 y 1 según legibilidad visual.")


# Ubica los tres recursos generados específicamente para este ejercicio multdocumento.
raiz = Path(__file__).resolve().parents[3]
carpeta_documentos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/documentos_multitipo"

# Declara las tres imágenes y el tipo esperado para convertir la demo en una mini evaluación.
casos = [
    ("factura_demo.png", "factura"),
    ("pagina_libro_demo.png", "pagina_libro"),
    ("adenda_servicios_demo.png", "adenda_contractual"),
]

# Crea un único agente capaz de interpretar los tres tipos sin usar reglas por archivo.
agente = create_agent(
    model=ChatOpenAI(model="gpt-4o", temperature=0),
    tools=[],
    response_format=LecturaDocumento,
    system_prompt=(
        "Sos un agente de visión documental. Detectá el tipo por el contenido visible. "
        "Para una factura extraé emisor, número, fecha y total. Para un libro extraé título, "
        "capítulo, autor, página e idea central. Para una adenda extraé contrato, fecha, "
        "cambios de monto, vigencia y cláusulas. Si no se lee un dato, escribí [ILEGIBLE]."
    ),
)

# Repite exactamente el mismo flujo de visión con tres imágenes de naturaleza diferente.
for nombre_archivo, tipo_esperado in casos:
    ruta_documento = carpeta_documentos / nombre_archivo
    imagen_base64 = base64.b64encode(ruta_documento.read_bytes()).decode("utf-8")
    mensaje = HumanMessage(content=[
        {"type": "text", "text": "Identificá el documento, extraé sus datos clave y resumilo."},
        {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
    ])
    lectura = LecturaDocumento.model_validate(agente.invoke({"messages": [mensaje]})["structured_response"])

    # Muestra una salida comparable e indica si acertó la clasificación del caso.
    print({
        "archivo": nombre_archivo,
        "tipo_esperado": tipo_esperado,
        "clasificacion_correcta": lectura.tipo_documento == tipo_esperado,
        "lectura": lectura.model_dump(),
    })

# Resumen final: el mismo agente puede clasificar y leer contratos, libros y facturas.
# Agregá una cuarta imagen con un recibo y extendé el Literal y las descriptions del schema.
