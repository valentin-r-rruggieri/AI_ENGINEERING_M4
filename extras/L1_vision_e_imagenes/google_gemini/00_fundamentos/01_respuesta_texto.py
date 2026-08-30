# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Primera respuesta de texto con Gemini.

GUÍA DOCENTE
CUÁNDO USAR: para resolver una tarea breve con una entrada textual.
DIFERENCIA: generate_content también acepta imágenes y otros contenidos.
EN CLASE: localizar modelo, contents y response.text.
"""

# Importa os para comprobar la API key.
import os

# Importa el cliente de Google Gen AI.
from google import genai

# Prepara una pregunta corta y verificable.
pregunta = "Explica BPE en una oración para un estudiante de IA."

if os.getenv("GEMINI_API_KEY"):
    # Envía la pregunta al modelo y muestra el texto generado.
    cliente = genai.Client()
    respuesta = cliente.models.generate_content(model="gemini-2.5-flash", contents=pregunta)
    print(respuesta.text)
else:
    print("Falta GEMINI_API_KEY. Pregunta preparada:", pregunta)

# Resumen final: este ejercicio obtiene una respuesta textual de Gemini.
# Cambia la audiencia de la pregunta y compara el vocabulario utilizado.
