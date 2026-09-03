# Este archivo forma parte del resumen integrador de audio y pipelines.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Flujo LangGraph: transcribir, medir WER y decidir el destino de una llamada.

GUÍA DOCENTE
CUÁNDO USAR: cuando cada paso del pipeline debe ser visible y auditable.
DIFERENCIA: LangGraph guarda el estado; LangChain produce el informe estructurado.
EN CLASE: recorrer transcripción, WER e informe antes de mostrar la decisión final.
"""

# Carga una sola vez las credenciales compartidas del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa rutas, tipos de estado, ASR, LangChain, LangGraph y Pydantic.
from pathlib import Path
from typing import NotRequired, TypedDict, cast

from jiwer import wer
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from pydantic import BaseModel, Field


# Define el reporte final que consume una operación de soporte.
class DecisionLlamada(BaseModel):
    wer: float = Field(ge=0)
    destino: str
    motivo: str


# Define el estado que cada nodo amplía durante el pipeline.
class EstadoLlamada(TypedDict):
    archivo: str
    referencia: str
    transcripcion: NotRequired[str]
    wer: NotRequired[float]
    decision: NotRequired[dict[str, object]]


# Localiza los datos y crea un cliente para la única transcripción del flujo.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data"
cliente_audio = OpenAI()


# Transcribe el WAV y agrega texto al estado compartido.
def transcribir_llamada(state: EstadoLlamada) -> dict[str, str]:
    with (carpeta_datos / state["archivo"]).open("rb") as archivo_audio:
        respuesta_asr = cliente_audio.audio.transcriptions.create(
            model="whisper-1",
            file=archivo_audio,
            language="es",
        )
    return {"transcripcion": str(respuesta_asr.text)}


# Calcula la métrica objetiva antes de pedir una decisión semántica.
def medir_calidad(state: EstadoLlamada) -> dict[str, float]:
    error_wer = round(wer(state["referencia"].lower(), state["transcripcion"].lower()), 3)
    return {"wer": error_wer}


# Convierte la métrica y el texto en un destino de negocio validado.
def decidir_destino(state: EstadoLlamada) -> dict[str, dict[str, object]]:
    extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(DecisionLlamada)
    decision = extractor.invoke(
        "Analizá calidad de transcripción de soporte. "
        "Con WER mayor a 0.15 elegí revisión humana o pedir nuevo audio; "
        "con WER menor o igual elegí procesar soporte. "
        f"WER: {state['wer']}. Transcripción: {state['transcripcion']}"
    )
    return {"decision": DecisionLlamada.model_validate(decision).model_dump()}


# Conecta pasos visibles y lineales: ASR, métrica y decisión.
grafo = StateGraph(EstadoLlamada)
grafo.add_node("transcribir_llamada", transcribir_llamada)
grafo.add_node("medir_calidad", medir_calidad)
grafo.add_node("decidir_destino", decidir_destino)
grafo.add_edge(START, "transcribir_llamada")
grafo.add_edge("transcribir_llamada", "medir_calidad")
grafo.add_edge("medir_calidad", "decidir_destino")
grafo.add_edge("decidir_destino", END)

# Ejecuta una variante con ruido para mostrar un caso que puede requerir escalamiento.
entrada: EstadoLlamada = {
    "archivo": "llamada_soporte_ruido.wav",
    "referencia": (carpeta_datos / "transcripts/llamada_soporte_reference.txt").read_text(encoding="utf-8"),
}
resultado = cast(EstadoLlamada, grafo.compile().invoke(entrada))
print(resultado.get("decision", {}))

# Resumen final: el grafo vuelve auditable cada etapa antes de decidir.
# Probá llamada_soporte.wav y compará WER, motivo y destino.

