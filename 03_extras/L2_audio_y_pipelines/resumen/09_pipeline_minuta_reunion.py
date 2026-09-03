# Este archivo forma parte del resumen integrador de audio y pipelines.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline de reunión: audio real, Whisper, LangChain y minuta Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando una reunión debe terminar en decisiones y tareas visibles.
DIFERENCIA: ASR transcribe las palabras; el agente organiza el trabajo posterior.
EN CLASE: comparar transcripción literal con una minuta accionable.
"""

# Carga una sola vez las credenciales compartidas del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Path y el cliente de audio para transcribir un WAV real.
from pathlib import Path

from openai import OpenAI

# Importa LangChain y Pydantic para transformar texto en una minuta validada.
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Define los datos que una persona necesita después de escuchar una reunión.
class MinutaReunion(BaseModel):
    resumen: str = Field(min_length=20)
    decisiones: list[str] = Field(min_length=1)
    tareas: list[str] = Field(min_length=1)
    requiere_revision: bool
    motivo_revision: str


# Localiza el audio y su texto de referencia dentro de los recursos de L2.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data"
ruta_audio = carpeta_datos / "reunion_equipo.wav"

# Transcribe una reunión real con Whisper antes de interpretarla.
cliente_audio = OpenAI()
with ruta_audio.open("rb") as archivo_audio:
    respuesta_asr = cliente_audio.audio.transcriptions.create(
        model="whisper-1",
        file=archivo_audio,
        language="es",
    )
transcripcion = str(respuesta_asr.text)

# Convierte la transcripción en una minuta; no agrega decisiones que no estén en el texto.
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(MinutaReunion)
minuta = extractor.invoke(
    "Creá una minuta breve. Usá solo la transcripción. "
    "No inventes responsables ni fechas. Marcá revisión si falta contexto. "
    f"Transcripción: {transcripcion}"
)

# Muestra primero lo que entendió ASR y luego la estructura utilizable por el equipo.
print({"transcripcion": transcripcion, "minuta": MinutaReunion.model_validate(minuta).model_dump()})

# Resumen final: un pipeline de reunión une audio, ASR y acciones verificables.
# Cambiá el archivo por reunion_equipo_rapido.wav y compará la minuta resultante.

