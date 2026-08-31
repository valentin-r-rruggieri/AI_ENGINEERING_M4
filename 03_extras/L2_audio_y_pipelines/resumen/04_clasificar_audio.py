# Caso adicional LangChain de L2: clasificar el riesgo de una transcripción.
"""Cadena tipada que convierte una transcripción en una prioridad de atención."""
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class PrioridadAudio(BaseModel):
    prioridad: str
    motivo: str
    respuesta_operativa: str

transcripcion = "El paciente informa que tomó un comprimido fuera de horario."
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(PrioridadAudio)
resultado = extractor.invoke("Clasificá esta transcripción como baja, media o alta prioridad. No des diagnóstico médico: " + transcripcion)
print(resultado.model_dump())
