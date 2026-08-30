# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Salida JSON de Gemini validada por un schema.

GUÍA DOCENTE
CUÁNDO USAR: cuando otra aplicación consumirá los datos extraídos.
DIFERENCIA: response_schema restringe la forma de la respuesta.
EN CLASE: inspeccionar el modelo Pydantic antes de llamar a Gemini.
"""

# Importa utilidades para credenciales y archivos.
import os
from pathlib import Path

# Importa Gemini, su configuración, Pillow y Pydantic.
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field

# Define el contrato de salida del formulario.
class Formulario(BaseModel):
    titular: str
    documento: str
    confianza: float = Field(ge=0, le=1)

# Localiza la imagen reutilizada en el recorrido.
raiz = Path(__file__).resolve().parents[4]
ruta_imagen = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

if os.getenv("GEMINI_API_KEY"):
    # Solicita JSON que respete el schema Pydantic.
    cliente = genai.Client()
    respuesta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=["Extrae los datos del formulario.", Image.open(ruta_imagen)],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Formulario,
        ),
    )
    formulario = Formulario.model_validate_json(respuesta.text)
    print(formulario.model_dump())
else:
    print("Falta GEMINI_API_KEY. Schema preparado:", Formulario.model_json_schema())

# Resumen final: este ejercicio combina visión, JSON y Pydantic.
# Agrega un campo obligatorio y observa cómo cambia la respuesta.
