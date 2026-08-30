# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extractor visual con decisión de revisión humana.

GUÍA DOCENTE
CUÁNDO USAR: para convertir un documento en datos con control de calidad.
DIFERENCIA: una confianza baja deriva el caso sin descartar el resultado.
EN CLASE: recorrer entrada, schema, extracción y regla de negocio.
"""

# Importa las herramientas necesarias para el pipeline.
import os
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field

# Define la salida que espera el proceso de negocio.
class Documento(BaseModel):
    tipo: str
    titular: str
    identificador: str
    confianza: float = Field(ge=0, le=1)

# Prepara el recurso y el umbral de revisión.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
umbral = 0.85

if os.getenv("GEMINI_API_KEY"):
    # Extrae un JSON conforme al modelo definido.
    cliente = genai.Client()
    respuesta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=["Clasifica y extrae este documento.", Image.open(ruta)],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Documento),
    )
    documento = Documento.model_validate_json(respuesta.text)
else:
    # Mantiene una demostración local cuando no hay credenciales.
    documento = Documento(tipo="formulario", titular="Ana Pérez", identificador="30111222", confianza=0.81)

# Muestra el dato validado y la decisión derivada.
print(documento.model_dump())
print("Revisión humana:", documento.confianza < umbral)

# Resumen final: este pipeline produce datos y una decisión operativa.
# Modifica el umbral para discutir precisión frente a automatización.
