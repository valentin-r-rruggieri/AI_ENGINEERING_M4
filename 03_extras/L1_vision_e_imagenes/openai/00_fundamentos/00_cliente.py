# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Wrapper ChatOpenAI de LangChain y lectura segura de la API key.

GUÍA DOCENTE
CUÁNDO USAR: antes de realizar cualquier llamada a los modelos de OpenAI.
DIFERENCIA: crear el cliente no consume tokens; ejecutar una respuesta sí.
EN CLASE: explicar por qué las claves se guardan en variables de entorno.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para consultar las variables de entorno del proceso.
import os

# Importa el wrapper de LangChain para los modelos de OpenAI.
from langchain_openai import ChatOpenAI

# Crea el modelo LangChain utilizando automáticamente OPENAI_API_KEY.
modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print("Wrapper creado correctamente:", type(modelo).__name__)

# Resumen final: este ejercicio prepara un wrapper LangChain sin exponer secretos.
# Eliminá temporalmente la variable de entorno y observá el mensaje producido.
