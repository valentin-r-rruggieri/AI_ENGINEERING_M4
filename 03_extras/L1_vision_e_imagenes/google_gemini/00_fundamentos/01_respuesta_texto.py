# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Primera respuesta de texto con Gemini mediante LangChain.

GUÍA DOCENTE
CUÁNDO USAR: para resolver una tarea breve con una entrada textual.
DIFERENCIA: el mismo método invoke funciona con proveedores distintos.
EN CLASE: localizar modelo, prompt y respuesta de LangChain.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la API key.
import os

# Importa el wrapper LangChain para Gemini.
from langchain_google_genai import ChatGoogleGenerativeAI

# Prepara una pregunta corta y verificable.
pregunta = "Explica BPE en una oración para un estudiante de IA."

# Envía la pregunta al wrapper y muestra el texto generado.
modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
respuesta = modelo.invoke(pregunta)
print(respuesta.text)
# Resumen final: este ejercicio obtiene una respuesta textual de Gemini.
# Cambia la audiencia de la pregunta y compara el vocabulario utilizado.
