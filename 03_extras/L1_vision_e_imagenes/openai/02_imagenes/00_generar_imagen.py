# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Generación de una imagen sintética para pruebas.

GUÍA DOCENTE
CUÁNDO USAR: para crear casos visuales cuando faltan datos reales o son sensibles.
DIFERENCIA: generar datos sintéticos no reemplaza validar con casos reales.
EN CLASE: identificar qué elementos del prompt controlan el caso de prueba.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa utilidades para leer la clave, decodificar la imagen y guardar el resultado.
import base64
import os
from pathlib import Path

# Importa LangChain para redactar el prompt de manera controlada.
from langchain_openai import ChatOpenAI

# Importa el cliente oficial: generar una imagen es un endpoint especializado,
# no un mensaje de chat que pueda reemplazarse por ChatOpenAI.
from openai import OpenAI

# Define el pedido mínimo que LangChain convertirá en un prompt visual claro.
pedido_docente = "un formulario bancario ficticio, legible, blanco y estilo escaneado"
salida = Path(__file__).resolve().parent / "formulario_sintetico.png"

# Usa el wrapper de LangChain para preparar una instrucción visual completa.
modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta_prompt = modelo.invoke(
    "Redacta un prompt corto para generar "
    f"{pedido_docente}. Exige datos inventados y sin datos personales reales."
)
prompt = str(respuesta_prompt.content)

# Solicita una imagen con el endpoint especializado y decodifica Base64.
cliente = OpenAI()
respuesta = cliente.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")
salida.write_bytes(base64.b64decode(respuesta.data[0].b64_json))
print("Imagen guardada en:", salida)
# Resumen final: LangChain redacta el prompt y el endpoint especializado crea la imagen.
# Agrega ruido o inclinación al prompt y compara la dificultad del documento.
