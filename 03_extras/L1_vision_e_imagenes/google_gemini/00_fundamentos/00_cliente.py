# Este archivo forma parte del recorrido práctico de Google Gemini.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Creación del wrapper LangChain para Gemini.

GUÍA DOCENTE
CUÁNDO USAR: antes de enviar texto o imágenes a modelos Gemini.
DIFERENCIA: LangChain conserva la misma interfaz al cambiar de proveedor.
EN CLASE: explicar credenciales, wrapper y selección de modelo.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la variable de entorno.
import os

# Importa el wrapper LangChain para modelos Gemini.
from langchain_google_genai import ChatGoogleGenerativeAI

# Crea el wrapper que se reutiliza en las llamadas posteriores.
modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
print("Wrapper creado correctamente:", type(modelo).__name__)

# Resumen final: este ejercicio crea un wrapper LangChain sin exponer la clave.
# Ejecutalo con y sin GEMINI_API_KEY para observar la diferencia.
