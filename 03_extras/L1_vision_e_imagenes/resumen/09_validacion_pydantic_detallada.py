# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para ver cómo las descripciones Pydantic guían una extracción visual.

"""Contrato Pydantic detallado para una solicitud bancaria.

GUÍA DOCENTE
CUÁNDO USAR: cuando la salida de visión debe ser utilizable por una API o base de datos.
DIFERENCIA: los tipos validan forma; las descriptions explican significado al modelo.
EN CLASE: leer cada description antes de ejecutar la extracción sobre la imagen.
"""

# Carga una sola vez las claves globales del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 y Path para preparar el documento visual de entrada.
import base64
from datetime import date
from pathlib import Path
from typing import Literal

# Importa LangChain para enviar imagen y schema Pydantic al modelo visual.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Importa validadores para normalizar y cruzar los campos de la solicitud.
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# Define un contrato rico: cada description llega al modelo como contexto del campo.
class SolicitudCredito(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titular: str = Field(min_length=5, description="Nombre completo del solicitante. No incluir la etiqueta del campo.")
    dni: str = Field(description="DNI argentino de ocho dígitos. Omitir puntos, espacios y texto adicional.")
    monto_solicitado_ars: float = Field(gt=0, description="Importe solicitado en ARS. Convertir $ 50.000,00 en 50000.0.")
    fecha_nacimiento: date = Field(description="Fecha de nacimiento ISO AAAA-MM-DD. Convertir desde DD/MM/AAAA.")
    telefono: str = Field(description="Teléfono argentino solo con dígitos, incluyendo código de área y sin guiones.")
    firma_presente: bool = Field(description="True solo si se observa una firma manuscrita en el recuadro de firma.")
    calidad_documento: Literal["aceptable", "baja", "critica"] = Field(description="Aceptable si se lee todo; baja si hay dudas; crítica si faltan datos.")
    requiere_revision: bool = Field(description="True cuando la calidad sea baja o crítica, o falte un dato relevante.")

    # Elimina separadores antes de validar que el DNI tiene ocho dígitos.
    @field_validator("dni", mode="before")
    @classmethod
    def normalizar_dni(cls, valor: object) -> str:
        return "".join(caracter for caracter in str(valor) if caracter.isdigit())

    # Conserva solamente números para que la API no reciba formatos telefónicos distintos.
    @field_validator("telefono", mode="before")
    @classmethod
    def normalizar_telefono(cls, valor: object) -> str:
        return "".join(caracter for caracter in str(valor) if caracter.isdigit())

    # Revisa que las decisiones de calidad y revisión sean coherentes entre sí.
    @model_validator(mode="after")
    def cruzar_calidad_y_revision(self) -> "SolicitudCredito":
        if self.calidad_documento == "aceptable" and self.requiere_revision:
            raise ValueError("Un documento aceptable no requiere revisión.")
        if self.calidad_documento != "aceptable" and not self.requiere_revision:
            raise ValueError("Un documento con dudas debe requerir revisión.")
        return self


# Ubica el mismo formulario limpio para aislar el efecto del schema detallado.
raiz = Path(__file__).resolve().parents[3]
ruta_imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")

# Extrae las descripciones para mostrarlas antes del resultado real del agente.
schema = SolicitudCredito.model_json_schema()
descripciones = {
    campo: definicion.get("description", "")
    for campo, definicion in schema["properties"].items()
}

# Crea un agente cuya salida estructurada incorpora todas las descripciones anteriores.
agente = create_agent(
    model=ChatOpenAI(model="gpt-4o", temperature=0),
    tools=[],
    response_format=SolicitudCredito,
    system_prompt="Sos analista de solicitudes de crédito. Extraé solo datos visibles y obedecé la description de cada campo.",
)

# Analiza la imagen y deja que Pydantic normalice y valide la respuesta final.
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Extraé y validá esta solicitud bancaria con el contrato indicado."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
solicitud = SolicitudCredito.model_validate(agente.invoke({"messages": [mensaje]})["structured_response"])

# Muestra primero qué significa cada campo y después la salida normalizada.
print({"descripciones_para_la_ia": descripciones, "solicitud_validada": solicitud.model_dump(mode="json")})

# Resumen final: las descriptions convierten un JSON genérico en un contrato semántico.
# Ejecutalo con la imagen manchada y discutí qué regla obliga a revisar el documento.
