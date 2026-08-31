# Este archivo forma parte del recorrido práctico de OpenAI Whisper.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline corto de audio, transcripción y evaluación.

GUÍA DOCENTE
CUÁNDO USAR: para medir una transcripción remota contra un texto de referencia.
DIFERENCIA: transcribir produce texto; WER cuantifica sus errores de palabras.
EN CLASE: escuchar el audio y revisar la referencia antes de ejecutar.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os y Path para validar la clave y localizar el audio.
import os
from pathlib import Path

# Importa la cadena LangChain, el cliente de audio especializado y la métrica WER.
from jiwer import wer
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI

# Prepara el audio y una referencia breve para la evaluación.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"
referencia = "tomar un comprimido cada ocho horas"

# Transcribe el audio solamente cuando existe una clave configurada.
cliente = OpenAI()
with audio.open("rb") as archivo_audio:
    respuesta = cliente.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=archivo_audio,
    )
transcripcion = respuesta.text.lower()
# Usa LangChain para producir un resumen clínico corto de la transcripción.
prompt = ChatPromptTemplate.from_template(
    "Resume en una oración esta indicación médica, sin agregar datos: {texto}"
)
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
resumen = cadena.invoke({"texto": transcripcion}).content
# Muestra texto, resumen y métrica para comprobar el pipeline.
print("Transcripción:", transcripcion)
print("Resumen LangChain:", resumen)
print("WER:", round(wer(referencia, transcripcion), 3))

# Resumen final: este pipeline une Whisper, LangChain y evaluación WER.
# Cambia una palabra de la transcripción simulada y observa cómo aumenta el WER.
