# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Primera respuesta de texto con Responses API.

GUÍA DOCENTE
CUÁNDO USAR: para enviar una instrucción simple a un modelo de OpenAI.
DIFERENCIA: Responses API unifica entradas de texto, imágenes y herramientas.
EN CLASE: identificar modelo, input y output_text antes de ejecutar.
"""

# Importa os para comprobar si la clave necesaria está disponible.
import os

# Importa el cliente oficial de OpenAI.
from openai import OpenAI

# Define una instrucción corta cuyo resultado sea fácil de revisar.
instruccion = "Explica self-attention en una sola oración para un estudiante."

if os.getenv("OPENAI_API_KEY"):
    # Crea el cliente y solicita una respuesta breve.
    cliente = OpenAI()
    respuesta = cliente.responses.create(model="gpt-4.1-mini", input=instruccion)
    print(respuesta.output_text)
else:
    # Muestra qué se enviaría sin inventar una respuesta del modelo.
    print("Falta OPENAI_API_KEY. Instrucción preparada:", instruccion)

# Resumen final: este ejercicio envía texto y lee output_text.
# Cambia la audiencia del prompt y compara cómo varía la explicación.
