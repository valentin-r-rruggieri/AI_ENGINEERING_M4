# Este archivo forma parte del recorrido práctico de LangChain aplicado a audio.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Postprocesa una transcripción de audio con ChatOpenAI.

GUÍA DOCENTE
CUÁNDO USAR: después de ASR, para convertir texto hablado en un resumen útil.
DIFERENCIA: Whisper transcribe; LangChain coordina la tarea posterior sobre el texto.
EN CLASE: separar claramente ASR, prompt y respuesta final.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la clave antes de invocar el modelo.
import os

# Importa prompt y wrapper LangChain para OpenAI.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Simula una transcripción ya obtenida por el paso anterior del pipeline.
transcripcion = "El paciente debe tomar un comprimido cada ocho horas y volver a control el lunes."

# Encadena un prompt corto con el wrapper del modelo.
prompt = ChatPromptTemplate.from_template("Resumí en una oración: {transcripcion}")
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta = cadena.invoke({"transcripcion": transcripcion})
print(respuesta.content)
# Resumen final: LangChain toma la salida ASR como entrada de una segunda tarea.
# Cambiá la transcripción y observá cómo varía el resumen.
