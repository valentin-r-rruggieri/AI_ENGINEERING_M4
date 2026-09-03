# Este archivo forma parte del resumen integrador de audio y pipelines.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Auditor LangChain para detectar errores críticos aunque el WER sea bajo.

GUÍA DOCENTE
CUÁNDO USAR: cuando una palabra incorrecta puede cambiar una decisión importante.
DIFERENCIA: WER mide todos los errores; el auditor detecta términos de riesgo.
EN CLASE: cambiar "ocho" por "dos" y discutir por qué una sola palabra importa.
"""

# Carga una sola vez las credenciales compartidas del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa la métrica, LangChain y Pydantic para combinar número, contexto y decisión.
from typing import Literal

from jiwer import wer
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Define el contrato que debe devolver el auditor de calidad.
class AuditoriaAudio(BaseModel):
    wer: float = Field(ge=0, description="Tasa de error de palabras calculada.")
    terminos_criticos_afectados: list[str] = Field(description="Términos que cambiaron o faltan.")
    nivel_riesgo: Literal["bajo", "medio", "alto"]
    accion: Literal["continuar", "revisar_transcripcion", "pedir_audio_nuevo"]
    motivo: str = Field(min_length=15)


# Declara una referencia y una hipótesis que difieren en una palabra clínica sensible.
referencia = "Tomar un comprimido cada ocho horas durante cinco días."
transcripcion = "Tomar un comprimido cada dos horas durante cinco días."
terminos_criticos = ["ocho horas", "cinco días", "comprimido"]

# Mide el error global antes de pedir una interpretación al modelo.
error_wer = round(wer(referencia.lower(), transcripcion.lower()), 3)
afectados = [termino for termino in terminos_criticos if termino not in transcripcion.lower()]

# Pide una decisión estructurada; el agente no diagnostica ni modifica la indicación.
auditor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(AuditoriaAudio)
resultado = auditor.invoke(
    "Auditá esta transcripción de una indicación médica. No des consejos médicos. "
    "Si cambia una frecuencia, elegí revisión de transcripción. "
    f"Referencia: {referencia} Transcripción: {transcripcion} "
    f"WER: {error_wer}. Términos faltantes: {afectados}."
)

# Valida una vez más el contrato antes de hacerlo visible.
auditoria = AuditoriaAudio.model_validate(resultado)
print(auditoria.model_dump())

# Resumen final: un WER pequeño puede esconder una sustitución de alto impacto.
# Cambiá "dos" por "ocho" y observá cómo cambia el riesgo y la acción.

