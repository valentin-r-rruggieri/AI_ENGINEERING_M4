# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Creación del cliente de Gemini.

GUÍA DOCENTE
CUÁNDO USAR: antes de enviar texto o imágenes a modelos Gemini.
DIFERENCIA: el cliente usa GEMINI_API_KEY sin incluirla en el código.
EN CLASE: explicar credenciales, cliente y selección de modelo.
"""

# Importa os para comprobar la variable de entorno.
import os

# Importa el SDK actual de Google Gen AI.
from google import genai

# Comprueba la clave antes de crear el cliente.
clave_disponible = bool(os.getenv("GEMINI_API_KEY"))

if clave_disponible:
    # Crea el cliente que se reutiliza en las llamadas posteriores.
    cliente = genai.Client()
    print("Cliente creado correctamente:", type(cliente).__name__)
else:
    print("Configurá GEMINI_API_KEY antes de llamar a Gemini.")

# Resumen final: este ejercicio crea el cliente sin exponer la clave.
# Ejecutalo con y sin GEMINI_API_KEY para observar la diferencia.
