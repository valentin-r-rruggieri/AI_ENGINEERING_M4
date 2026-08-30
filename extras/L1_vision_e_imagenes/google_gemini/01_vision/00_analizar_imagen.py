# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Análisis visual de un formulario con Gemini.

GUÍA DOCENTE
CUÁNDO USAR: cuando el contenido depende del texto y del diseño de una imagen.
DIFERENCIA: el modelo multimodal observa layout además del OCR interno.
EN CLASE: comparar una descripción libre con una extracción estructurada.
"""

# Importa os y Path para validar la clave y localizar el recurso.
import os
from pathlib import Path

# Importa Gemini y Pillow para enviar una imagen local.
from google import genai
from PIL import Image

# Localiza el formulario didáctico incluido en L1.
raiz = Path(__file__).resolve().parents[4]
ruta_imagen = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

if os.getenv("GEMINI_API_KEY"):
    # Abre la imagen y solicita una descripción de sus campos.
    cliente = genai.Client()
    imagen = Image.open(ruta_imagen)
    respuesta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=["Enumera los campos visibles del formulario.", imagen],
    )
    print(respuesta.text)
else:
    print("Falta GEMINI_API_KEY. Imagen preparada:", ruta_imagen.name)

# Resumen final: este ejercicio envía texto e imagen en una misma solicitud.
# Cambia la imagen por la versión borrosa y compara los campos detectados.
