# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Callback Langfuse para una llamada LangChain.

GUÍA DOCENTE
CUÁNDO USAR: para capturar automáticamente prompts, generaciones y tokens.
DIFERENCIA: el callback escucha eventos del framework sin envolver cada función.
EN CLASE: localizar config.callbacks en la invocación.
"""

# Importa os, cliente, callback y modelo LangChain.
import os
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI

# Requiere credenciales de OpenAI y Langfuse para una traza real.
configurado = all(os.getenv(nombre) for nombre in [
    "OPENAI_API_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
])

if configurado:
    # Pasa el handler a la configuración de la llamada.
    handler = CallbackHandler()
    modelo = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    respuesta = modelo.invoke(
        "Resume: el contrato aumenta de 12 a 18 meses.",
        config={"callbacks": [handler]},
    )
    print(respuesta.content)
    get_client().flush()
else:
    print("Configurá OPENAI_API_KEY y las dos claves de Langfuse.")

# Resumen final: este ejercicio instrumenta LangChain mediante callbacks.
# Agrega metadata a config y localízala en la observación.
