# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Generación de una imagen sintética para pruebas.

GUÍA DOCENTE
CUÁNDO USAR: para crear casos visuales cuando faltan datos reales o son sensibles.
DIFERENCIA: generar datos sintéticos no reemplaza validar con casos reales.
EN CLASE: identificar qué elementos del prompt controlan el caso de prueba.
"""

# Importa utilidades para leer la clave, decodificar la imagen y guardar el resultado.
import base64
import os
from pathlib import Path

# Importa el cliente oficial de OpenAI.
from openai import OpenAI

# Describe un formulario ficticio sin datos personales reales.
prompt = "Formulario bancario ficticio, texto legible, fondo blanco, datos inventados, estilo escaneado"
salida = Path(__file__).resolve().parent / "formulario_sintetico.png"

if os.getenv("OPENAI_API_KEY"):
    # Solicita una sola imagen y decodifica la respuesta Base64.
    cliente = OpenAI()
    respuesta = cliente.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")
    salida.write_bytes(base64.b64decode(respuesta.data[0].b64_json))
    print("Imagen guardada en:", salida)
else:
    print("Falta OPENAI_API_KEY. Prompt preparado:", prompt)

# Resumen final: este ejercicio genera un caso visual sintético.
# Agrega ruido o inclinación al prompt y compara la dificultad del documento.
