# Este archivo resume L2 mediante un pipeline de audio completo.
# Lee cada bloque y modifica una variable por vez.

"""Caso 3: decidir si una transcripción de audio puede automatizarse.

GUÍA DOCENTE
CUÁNDO USAR: para unir ASR, WER, resumen y una decisión de riesgo.
DIFERENCIA: una buena transcripción no elimina la necesidad de reglas.
EN CLASE: recorrer audio, texto, métrica, tokenización y decisión.
"""

# Carga el .env para conservar la misma configuración de todos los casos.
from dotenv import load_dotenv
load_dotenv()

# Importa la métrica, LangChain y Pydantic para el reporte final.
from jiwer import wer
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define una salida que combina calidad técnica y decisión operativa.
class PipelineAudio(BaseModel):
    tokens_estimados: int = Field(ge=1)
    wer: float = Field(ge=0)
    resumen: str
    requiere_revision: bool

# Simula una transcripción obtenida desde Whisper y la tokeniza por palabras.
referencia = "tomar un comprimido cada ocho horas"
transcripcion = "tomar un comprimido cada ocho horas"
tokens_estimados = len(transcripcion.split())
error_wer = wer(referencia, transcripcion)

# Une las métricas en una regla simple, visible y discutible.
resultado = PipelineAudio(
    tokens_estimados=tokens_estimados,
    wer=round(error_wer, 3),
    resumen="Indicación farmacológica de frecuencia regular.",
    requiere_revision=error_wer > 0.1,
)

# Usa LangChain para redactar una explicación que acompaña el contrato.
explicacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    "Explica en una oración si una WER de " + str(resultado.wer) + " permite automatizar una indicación médica."
).content

# Imprime el pipeline completo en forma de contrato.
print({**resultado.model_dump(), "explicacion_langchain": explicacion})

# Resumen final: el caso conecta audio, WER, tokens y revisión humana.
# Modifica la transcripción y decidí qué umbral sería prudente.
