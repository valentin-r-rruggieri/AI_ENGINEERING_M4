# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline local de transcripción y evaluación.

GUÍA DOCENTE
CUÁNDO USAR: cuando el audio debe procesarse sin enviarlo a una API externa.
DIFERENCIA: el modelo se descarga y ejecuta localmente, consumiendo CPU y memoria.
EN CLASE: comparar privacidad, latencia y precisión con OpenAI Whisper.
"""

# Importa Path para localizar el audio de la clase.
from pathlib import Path

# Importa WER y pipeline para evaluar una transcripción local.
from jiwer import wer
from transformers import pipeline

# Localiza el audio y define la transcripción esperada.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"
referencia = "tomar un comprimido cada ocho horas"

# Carga un Whisper pequeño y realiza la transcripción en CPU.
transcriptor = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1,
)
resultado = transcriptor(str(audio))
transcripcion = resultado["text"].strip().lower()

# Imprime la salida y su error de palabras.
print("Transcripción:", transcripcion)
print("WER:", round(wer(referencia, transcripcion), 3))

# Resumen final: este pipeline une ASR local y evaluación WER.
# Cambia a whisper-base y compara tiempo, memoria y resultado.
