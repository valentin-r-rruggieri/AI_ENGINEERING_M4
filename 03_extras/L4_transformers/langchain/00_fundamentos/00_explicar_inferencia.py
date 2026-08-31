# Este archivo forma parte del recorrido práctico de LangChain aplicado a Transformers.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Explica una inferencia Transformer mediante una cadena LangChain.

GUÍA DOCENTE
CUÁNDO USAR: después de una inferencia numérica, para comunicar su significado.
DIFERENCIA: el Transformer calcula logits; LangChain transforma el resultado en lenguaje claro.
EN CLASE: ejecutar primero los tensores y luego explicar este postproceso.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la clave de OpenAI.
import os

# Importa el prompt y el wrapper LangChain.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Representa una salida pequeña producida por un clasificador Transformer.
resultado_transformer = {"etiqueta": "POSITIVE", "confianza": 0.96}

# Convierte los datos técnicos en una explicación breve para un usuario.
prompt = ChatPromptTemplate.from_template("Explicá este resultado sin jerga: {resultado}")
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta = cadena.invoke({"resultado": resultado_transformer})
print(respuesta.content)
# Resumen final: LangChain comunica la salida, pero no reemplaza el Transformer.
# Cambiá la etiqueta y compará la explicación.
