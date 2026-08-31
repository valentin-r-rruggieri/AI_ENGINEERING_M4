# Este archivo resume L2 mediante una indicación de audio estructurada.
# Lee cada bloque y modifica una variable por vez.

"""Caso 2: transformar una transcripción en una indicación validada.

GUÍA DOCENTE
CUÁNDO USAR: cuando una transcripción debe alimentar otro sistema con seguridad.
DIFERENCIA: LangChain interpreta el texto; Pydantic limita la forma de salida.
EN CLASE: distinguir transcripción literal de resumen operacional.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa la clave, LangChain y Pydantic para el contrato final.
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define los campos que el agente debe devolver después de escuchar el audio.
class ReporteAudio(BaseModel):
    transcripcion: str
    resumen: str
    requiere_revision: bool
    confianza: float = Field(ge=0, le=1)

# Reutiliza una transcripción de la práctica anterior.
texto_audio = "Tomar un comprimido cada ocho horas durante cinco días."

# Pide a LangChain una respuesta tipada y sin inventar datos médicos.
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ReporteAudio)
reporte = extractor.invoke(
    "Organiza esta indicación. Conserva el texto, resume sin agregar datos y marca revisión: " + texto_audio
)
# Muestra el resultado estructurado que consume un sistema posterior.
print(reporte.model_dump())

# Resumen final: la salida estructurada evita entregar un párrafo ambiguo.
# Cambia la frecuencia y analiza qué campos deben conservarse.
