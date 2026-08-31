# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Primera respuesta de texto con el wrapper ChatOpenAI.

GUÍA DOCENTE
CUÁNDO USAR: para enviar una instrucción simple a un modelo de OpenAI.
DIFERENCIA: LangChain unifica la forma de invocar distintos proveedores.
EN CLASE: identificar modelo, prompt y contenido antes de ejecutar.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar si la clave necesaria está disponible.
import os

# Importa el wrapper de LangChain para OpenAI.
from langchain_openai import ChatOpenAI

# Define una instrucción corta cuyo resultado sea fácil de revisar.
instruccion = "Explica self-attention en una sola oración para un estudiante."

# Crea el wrapper y solicita una respuesta breve.
modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta = modelo.invoke(instruccion)
print(respuesta.content)
# Resumen final: este ejercicio envía texto mediante LangChain y lee content.
# Cambia la audiencia del prompt y compara cómo varía la explicación.
