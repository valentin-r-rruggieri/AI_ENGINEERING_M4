# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Callback Langfuse para una llamada LangChain.

GUÍA DOCENTE
CUÁNDO USAR: para capturar automáticamente prompts, generaciones y tokens.
DIFERENCIA: el callback escucha eventos del framework sin envolver cada función.
EN CLASE: localizar config.callbacks en la invocación.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os, cliente, callback y modelo LangChain.
import os
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI

# Pasa el handler a la configuración de la llamada.
handler = CallbackHandler()
modelo = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
respuesta = modelo.invoke(
    "Resume: el contrato aumenta de 12 a 18 meses.",
    config={"callbacks": [handler]},
)
print(respuesta.content)
get_client().flush()

# Resumen final: este ejercicio instrumenta LangChain mediante callbacks.
# Agrega metadata a config y localízala en la observación.
