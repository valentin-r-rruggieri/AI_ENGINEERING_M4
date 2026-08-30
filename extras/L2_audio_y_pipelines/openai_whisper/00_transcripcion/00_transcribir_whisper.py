# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Transcripción de un audio con la API de OpenAI.

GUÍA DOCENTE
CUÁNDO USAR: para convertir voz grabada en texto antes de un análisis posterior.
DIFERENCIA: ASR transcribe; un LLM posterior interpreta o resume el texto.
EN CLASE: escuchar el audio y anticipar posibles errores antes de ejecutar.
"""

# Importa os para validar la clave y Path para localizar el audio.
import os
from pathlib import Path

# Importa el cliente oficial utilizado para transcribir.
from openai import OpenAI

# Reutiliza un audio didáctico existente en la clase L2.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"

if os.getenv("OPENAI_API_KEY"):
    # Abre el archivo en binario y solicita su transcripción.
    cliente = OpenAI()
    with audio.open("rb") as archivo_audio:
        transcripcion = cliente.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=archivo_audio,
        )
    print(transcripcion.text)
else:
    print("Falta OPENAI_API_KEY. Audio preparado:", audio.name)

# Resumen final: este ejercicio transforma audio en texto.
# Cambia el audio por indicacion_medica_ruido.wav y compara la transcripción.
