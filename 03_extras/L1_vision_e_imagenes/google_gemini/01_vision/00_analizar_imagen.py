# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Análisis visual de un formulario con Gemini.

GUÍA DOCENTE
CUÁNDO USAR: cuando el contenido depende del texto y del diseño de una imagen.
DIFERENCIA: el modelo multimodal observa layout además del OCR interno.
EN CLASE: comparar una descripción libre con una extracción estructurada.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os y Path para validar la clave y localizar el recurso.
import os
from pathlib import Path

# Importa Base64 y los objetos LangChain para enviar una imagen local.
import base64

from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Localiza el formulario didáctico incluido en L1.
raiz = Path(__file__).resolve().parents[4]
ruta_imagen = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

# Prepara la imagen y solicita una descripción por medio de LangChain.
imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")
modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
mensaje = HumanMessage(content=[
    {"type": "text", "text": "Enumera los campos visibles del formulario."},
    {"type": "image", "base64": imagen_base64, "mime_type": "image/png"},
])
respuesta = modelo.invoke([mensaje])
print(respuesta.text)
# Resumen final: este ejercicio envía texto e imagen en una misma solicitud.
# Cambia la imagen por la versión borrosa y compara los campos detectados.
