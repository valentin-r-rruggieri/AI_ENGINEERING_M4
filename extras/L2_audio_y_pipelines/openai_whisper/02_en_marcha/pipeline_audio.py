# Este archivo forma parte del recorrido práctico de OpenAI Whisper.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline corto de audio, transcripción y evaluación.

GUÍA DOCENTE
CUÁNDO USAR: para medir una transcripción remota contra un texto de referencia.
DIFERENCIA: transcribir produce texto; WER cuantifica sus errores de palabras.
EN CLASE: escuchar el audio y revisar la referencia antes de ejecutar.
"""

# Importa os y Path para validar la clave y localizar el audio.
import os
from pathlib import Path

# Importa el cliente de OpenAI y la métrica WER.
from jiwer import wer
from openai import OpenAI

# Prepara el audio y una referencia breve para la evaluación.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"
referencia = "tomar un comprimido cada ocho horas"

if os.getenv("OPENAI_API_KEY"):
    # Transcribe el audio solamente cuando existe una clave configurada.
    cliente = OpenAI()
    with audio.open("rb") as archivo_audio:
        respuesta = cliente.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=archivo_audio,
        )
    transcripcion = respuesta.text.lower()
else:
    # Usa una salida local para explicar el cálculo sin consumir la API.
    transcripcion = "tomar un comprimido cada ocho horas"
    print("Falta OPENAI_API_KEY: se usa una transcripción simulada.")

# Muestra tanto el texto como la métrica para comprobar el pipeline.
print("Transcripción:", transcripcion)
print("WER:", round(wer(referencia, transcripcion), 3))

# Resumen final: este pipeline une transcripción remota y evaluación WER.
# Cambia una palabra de la transcripción simulada y observa cómo aumenta el WER.
