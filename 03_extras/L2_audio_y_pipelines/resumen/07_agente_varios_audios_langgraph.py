# Este archivo forma parte del resumen integrador de audio y pipelines.
# Ejecutalo para ver los pasos ASR -> clasificación como un grafo visible.

"""Flujo LangGraph para transcribir y revisar varios audios reales.

GUÍA DOCENTE
CUÁNDO USAR: cuando una decisión depende de pasos de audio que se deben auditar.
DIFERENCIA: LangGraph conserva el estado entre nodos; LangChain interpreta el texto final.
EN CLASE: recorrer primero la transcripción y después la decisión de calidad.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Path, tipos del estado y el cliente de transcripción real.
from pathlib import Path
from typing import NotRequired, TypedDict, cast

from openai import OpenAI

# Importa el modelo LangChain, LangGraph y Pydantic para el nodo de decisión.
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


# Define el resultado uniforme de la revisión del audio.
class FichaAudio(BaseModel):
    archivo: str = ""
    tipo_audio: str
    transcripcion: str = Field(min_length=1)
    calidad_estimada: str
    accion: str
    motivo: str


# Define el estado de entrada y los datos que agregan los nodos del flujo.
class EstadoAudio(TypedDict):
    archivo: str
    descripcion: str
    transcripcion: NotRequired[str]
    ficha: NotRequired[dict[str, object]]


# Declara la actualización que aporta el nodo de transcripción.
class ActualizacionTranscripcion(TypedDict):
    transcripcion: str


# Declara la actualización que aporta el nodo de revisión LangChain.
class ActualizacionFicha(TypedDict):
    ficha: dict[str, object]


# Ubica los archivos WAV compartidos por todos los ejercicios de L2.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data"
cliente_audio = OpenAI()


# Convierte un WAV en texto y deja esa transcripción disponible para el siguiente nodo.
def transcribir_audio(state: EstadoAudio) -> ActualizacionTranscripcion:
    ruta_audio = carpeta_datos / state["archivo"]
    with ruta_audio.open("rb") as archivo_audio:
        respuesta_asr = cliente_audio.audio.transcriptions.create(
            model="whisper-1",
            file=archivo_audio,
            language="es",
        )
    return {"transcripcion": str(respuesta_asr.text)}


# Recibe el texto del primer nodo y produce una decisión Pydantic con LangChain.
def clasificar_audio(state: EstadoAudio) -> ActualizacionFicha:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(FichaAudio)
    pedido = (
        f"Archivo: {state['archivo']}. Caso: {state['descripcion']}. "
        f"Transcripción: {state.get('transcripcion', '')}. "
        "Identificá el tipo de audio, calidad estimada, acción y motivo sin inventar palabras."
    )
    ficha_agente = FichaAudio.model_validate(extractor.invoke(pedido))
    ficha = FichaAudio.model_validate({**ficha_agente.model_dump(), "archivo": state["archivo"]})
    return {"ficha": ficha.model_dump()}


# Conecta la transcripción real con la interpretación posterior en un flujo explícito.
grafo = StateGraph(EstadoAudio)
grafo.add_node("transcribir_audio", transcribir_audio)
grafo.add_node("clasificar_audio", clasificar_audio)
grafo.add_edge(START, "transcribir_audio")
grafo.add_edge("transcribir_audio", "clasificar_audio")
grafo.add_edge("clasificar_audio", END)
aplicacion = grafo.compile()

# Repite tres casos contrastantes para comparar los estados finales del grafo.
casos = [
    ("llamada_soporte.wav", "llamada de soporte normal"),
    ("indicacion_medica_ruido.wav", "indicación médica con ruido"),
    ("reunion_equipo_rapido.wav", "reunión de equipo acelerada"),
]

# Ejecuta el flujo completo una vez por archivo y muestra su contrato final.
for nombre_archivo, descripcion in casos:
    entrada: EstadoAudio = {"archivo": nombre_archivo, "descripcion": descripcion}
    resultado = cast(EstadoAudio, aplicacion.invoke(entrada))
    print(resultado.get("ficha", {}))

# Resumen final: el grafo separa claramente ASR de la decisión de negocio.
# Cambiá un caso por un archivo con pausas y compará la transcripción y la acción.
