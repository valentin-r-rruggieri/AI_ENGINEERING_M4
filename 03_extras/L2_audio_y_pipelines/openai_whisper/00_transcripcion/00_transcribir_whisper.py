# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Transcripción de un audio con la API de OpenAI.

GUÍA DOCENTE
CUÁNDO USAR: para convertir voz grabada en texto antes de un análisis posterior.
DIFERENCIA: ASR transcribe; un LLM posterior interpreta o resume el texto.
EN CLASE: escuchar el audio y anticipar posibles errores antes de ejecutar.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para validar la clave y Path para localizar el audio.
import os
from pathlib import Path

# Importa LangChain para presentar la transcripción dentro de una cadena.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Importa el cliente oficial utilizado por el endpoint específico de Whisper.
# La transcripción de archivos es una operación de audio, no un mensaje de chat.
from openai import OpenAI

# Reutiliza un audio didáctico existente en la clase L2.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"

# Abre el archivo en binario y solicita su transcripción.
cliente = OpenAI()
with audio.open("rb") as archivo_audio:
    transcripcion = cliente.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=archivo_audio,
    )

# Crea una cadena LangChain para normalizar la salida sin alterar el contenido.
prompt = ChatPromptTemplate.from_template(
    "Devolvé solamente este texto transcripto, sin agregar información: {texto}"
)
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
texto_limpio = cadena.invoke({"texto": transcripcion.text}).content
print(texto_limpio)
# Resumen final: este ejercicio transforma audio en texto.
# Cambia el audio por indicacion_medica_ruido.wav y compara la transcripción.
