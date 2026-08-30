# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extracción visual con una salida validada por Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando una imagen debe convertirse en datos confiables.
DIFERENCIA: una descripción libre no garantiza nombres ni tipos de campos.
EN CLASE: explicar el schema antes de observar la respuesta del modelo.
"""

# Importa utilidades estándar para la clave, Base64 y rutas.
import base64
import os
from pathlib import Path

# Importa el cliente de OpenAI y el modelo de validación.
from openai import OpenAI
from pydantic import BaseModel, Field

# Define exactamente los campos que debe devolver el modelo.
class Formulario(BaseModel):
    titular: str
    documento: str
    confianza: float = Field(ge=0, le=1)

# Prepara la imagen como una data URL.
raiz = Path(__file__).resolve().parents[4]
imagen = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")

if os.getenv("OPENAI_API_KEY"):
    # Pide a Responses API que produzca directamente el modelo Pydantic.
    cliente = OpenAI()
    respuesta = cliente.responses.parse(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": "Extrae titular, documento y confianza."},
            {"type": "input_image", "image_url": f"data:image/png;base64,{imagen_base64}"},
        ]}],
        text_format=Formulario,
    )
    print(respuesta.output_parsed.model_dump())
else:
    print("Falta OPENAI_API_KEY. Schema preparado:", Formulario.model_json_schema())

# Resumen final: este ejercicio une visión con validación estructurada.
# Agrega un campo obligatorio al schema y observa cómo cambia la extracción.
