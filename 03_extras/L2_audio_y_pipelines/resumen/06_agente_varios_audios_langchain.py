# Este archivo forma parte del resumen integrador de audio y pipelines.
# Ejecutalo para comparar tres audios reales con problemas diferentes.

"""Agente LangChain que transcribe, identifica y deriva una acción por audio.

GUÍA DOCENTE
CUÁNDO USAR: cuando llegan audios de distinto tipo y con distinta calidad.
DIFERENCIA: Whisper convierte audio en texto; LangChain interpreta el texto obtenido.
EN CLASE: comparar el audio normal, el ruidoso y el acelerado antes de decidir.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Path para localizar los WAV y OpenAI para ejecutar Whisper real.
from pathlib import Path

from openai import OpenAI

# Importa LangChain y Pydantic para clasificar cada transcripción de forma uniforme.
from langchain.agents import create_agent
from pydantic import BaseModel, Field


# Define la ficha que devuelve el agente después de recibir una transcripción real.
class FichaAudio(BaseModel):
    archivo: str = ""
    tipo_audio: str
    transcripcion: str = Field(min_length=1)
    calidad_estimada: str
    accion: str
    motivo: str


# Ubica los audios generados para la lecture sin depender de la carpeta actual.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data"

# Declara tres casos contrastantes para explicar cómo cambia el pipeline.
casos = [
    ("llamada_soporte.wav", "llamada de soporte normal"),
    ("indicacion_medica_ruido.wav", "indicación médica con ruido"),
    ("reunion_equipo_rapido.wav", "reunión de equipo acelerada"),
]

# Crea el cliente ASR y el agente que interpreta la transcripción resultante.
cliente_audio = OpenAI()
agente = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    response_format=FichaAudio,
    system_prompt=(
        "Sos analista de audio. Usá solo la transcripción entregada. Identificá si es "
        "soporte, indicación médica, reunión u otro. Indicá calidad estimada y recomendá "
        "automatizar, revisión humana o pedir un nuevo audio. No inventes palabras ausentes."
    ),
)

# Envía cada WAV a Whisper y luego entrega el texto real al agente LangChain.
for nombre_archivo, descripcion in casos:
    ruta_audio = carpeta_datos / nombre_archivo
    with ruta_audio.open("rb") as archivo_audio:
        respuesta_asr = cliente_audio.audio.transcriptions.create(
            model="whisper-1",
            file=archivo_audio,
            language="es",
        )
    transcripcion = str(respuesta_asr.text)

    # Pide una decisión tipada que una tipo de audio, calidad y siguiente acción.
    pedido = (
        f"Archivo: {nombre_archivo}. Caso: {descripcion}. "
        f"Transcripción de Whisper: {transcripcion}"
    )
    respuesta = agente.invoke({"messages": [{"role": "user", "content": pedido}]})["structured_response"]
    ficha = FichaAudio.model_validate({**respuesta.model_dump(), "archivo": nombre_archivo})
    print(ficha.model_dump())

# Resumen final: el mismo flujo permite comparar fuentes y calidades distintas.
# Cambiá uno de los nombres por una variante entrecortada y compará la acción sugerida.
