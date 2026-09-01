# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para comparar la extracción de GPT-4o con una respuesta conocida.

"""Golden case: formulario bancario limpio con resultado esperado.

GUÍA DOCENTE
CUÁNDO USAR: antes de evaluar casos borrosos, rotos o con ruido visual.
DIFERENCIA: un golden case tiene una imagen y una respuesta esperada verificable.
EN CLASE: explicar que no basta con que el modelo responda; hay que medir aciertos.
"""

# Carga una sola vez las claves globales del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 y Path para enviar el formulario limpio a GPT-4o Vision.
import base64
from pathlib import Path

# Importa LangChain y Pydantic para orquestar y validar la extracción.
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field


# Define los seis datos visibles que debe devolver el golden case.
class FormularioGolden(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titular: str = Field(description="Apellido y nombre completos visibles en el formulario.")
    dni: str = Field(description="DNI tal como aparece impreso, incluidos los puntos si están visibles.")
    monto_ars: float = Field(description="Monto solicitado en pesos argentinos, solo el número sin símbolo.")
    fecha_nacimiento: str = Field(description="Fecha de nacimiento visible con formato DD/MM/AAAA.")
    telefono: str = Field(description="Teléfono de contacto tal como aparece en el formulario.")
    firma_presente: bool = Field(description="True únicamente si la firma del solicitante se ve en la imagen.")


# Ubica la imagen limpia que se utiliza como fuente confiable de este caso dorado.
raiz = Path(__file__).resolve().parents[3]
ruta_imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")

# Declara el ground truth que una persona docente verificó previamente.
esperado = FormularioGolden(
    titular="Juan Pérez",
    dni="40.111.222",
    monto_ars=50000,
    fecha_nacimiento="12/05/1994",
    telefono="011-4567-8901",
    firma_presente=True,
)

# Crea un agente de visión con salida tipada igual a la respuesta esperada.
agente = create_agent(
    model=ChatOpenAI(model="gpt-4o", temperature=0),
    tools=[],
    response_format=FormularioGolden,
    system_prompt=(
        "Sos extractor de formularios bancarios. Leé únicamente lo visible. "
        "Para monto devolvé un número y para firma devolvé booleano. No inventes valores."
    ),
)

# Envía la imagen con una instrucción corta y valida la respuesta del modelo.
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Extraé los seis datos del formulario bancario limpio."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
extraido = FormularioGolden.model_validate(agente.invoke({"messages": [mensaje]})["structured_response"])

# Compara campo por campo con el golden truth para hacer visible la evaluación.
campos_correctos = [
    campo for campo in FormularioGolden.model_fields
    if getattr(extraido, campo) == getattr(esperado, campo)
]

# Muestra extracción, esperado y métrica simple de aciertos para discutir en clase.
print({
    "extraido": extraido.model_dump(),
    "esperado": esperado.model_dump(),
    "campos_correctos": campos_correctos,
    "precision_campos": round(len(campos_correctos) / len(FormularioGolden.model_fields), 2),
})

# Resumen final: el golden case convierte una demo visual en una evaluación repetible.
# Probá la misma evaluación con la imagen borrosa y observá qué campos dejan de coincidir.
