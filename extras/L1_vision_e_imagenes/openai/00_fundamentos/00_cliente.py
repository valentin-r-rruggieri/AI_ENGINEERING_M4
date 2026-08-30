# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Cliente de OpenAI y lectura segura de la API key.

GUÍA DOCENTE
CUÁNDO USAR: antes de realizar cualquier llamada a los modelos de OpenAI.
DIFERENCIA: crear el cliente no consume tokens; ejecutar una respuesta sí.
EN CLASE: explicar por qué las claves se guardan en variables de entorno.
"""

# Importa os para consultar las variables de entorno del proceso.
import os

# Importa el cliente oficial que centraliza las llamadas a la API.
from openai import OpenAI

# Lee la clave sin escribirla ni mostrarla en pantalla.
clave_disponible = bool(os.getenv("OPENAI_API_KEY"))

if clave_disponible:
    # Crea el cliente utilizando automáticamente OPENAI_API_KEY.
    cliente = OpenAI()
    print("Cliente creado correctamente:", type(cliente).__name__)
else:
    # Explica cómo habilitar el ejemplo sin provocar un error confuso.
    print("Configurá OPENAI_API_KEY antes de realizar llamadas a OpenAI.")

# Resumen final: este ejercicio prepara un cliente sin exponer secretos.
# Eliminá temporalmente la variable de entorno y observá el mensaje producido.
