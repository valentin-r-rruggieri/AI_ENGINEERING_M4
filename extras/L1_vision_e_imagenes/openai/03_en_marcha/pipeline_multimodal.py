# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline corto de imagen a decisión validada.

GUÍA DOCENTE
CUÁNDO USAR: para automatizar documentos manteniendo un umbral de revisión humana.
DIFERENCIA: el pipeline no solo extrae; también valida y decide si revisar.
EN CLASE: seguir imagen, Base64, modelo Pydantic y decisión final.
"""

# Importa utilidades estándar para preparar la entrada.
import base64
import os
from pathlib import Path

# Importa OpenAI y Pydantic para extracción y validación.
from openai import OpenAI
from pydantic import BaseModel, Field

# Modela el resultado final que consumirá el sistema de negocio.
class Solicitud(BaseModel):
    titular: str
    documento: str
    importe: float = Field(ge=0)
    confianza: float = Field(ge=0, le=1)

# Prepara la imagen incluida en los ejercicios de L1.
raiz = Path(__file__).resolve().parents[4]
imagen = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
umbral_revision = 0.85

if os.getenv("OPENAI_API_KEY"):
    # Extrae datos respetando el contrato definido por Solicitud.
    cliente = OpenAI()
    respuesta = cliente.responses.parse(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": "Extrae titular, documento, importe y confianza."},
            {"type": "input_image", "image_url": f"data:image/png;base64,{imagen_base64}"},
        ]}],
        text_format=Solicitud,
    )
    solicitud = respuesta.output_parsed
    requiere_revision = solicitud.confianza < umbral_revision
    print(solicitud.model_dump())
    print("Revisión humana:", requiere_revision)
else:
    # Usa un caso local para explicar la decisión sin consumir la API.
    solicitud = Solicitud(titular="Ana Pérez", documento="30111222", importe=1200, confianza=0.82)
    print(solicitud.model_dump())
    print("Revisión humana:", solicitud.confianza < umbral_revision)

# Resumen final: este pipeline extrae, valida y deriva una decisión operativa.
# Cambia el umbral de revisión y analiza el impacto en automatización y riesgo.
