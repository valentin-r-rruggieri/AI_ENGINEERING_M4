# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline local de transcripción y evaluación.

GUÍA DOCENTE
CUÁNDO USAR: cuando el audio debe procesarse sin enviarlo a una API externa.
DIFERENCIA: el modelo se descarga y ejecuta localmente, consumiendo CPU y memoria.
EN CLASE: comparar privacidad, latencia y precisión con OpenAI Whisper.
"""

# Importa Path para localizar el audio, tipos para aclarar la salida y wave para leer WAV sin ffmpeg.
from pathlib import Path
from typing import Any, cast
import wave
import warnings

# Importa NumPy, WER y herramientas de Transformers para preparar ASR local.
import numpy as np
from jiwer import wer
from transformers import pipeline
from transformers.utils import logging as logging_transformers

# Oculta avisos internos deprecados de esta versión sin silenciar errores reales.
warnings.filterwarnings("ignore", message="The input name `inputs` is deprecated.*", category=FutureWarning)
warnings.filterwarnings("ignore", message="Passing a tuple of `past_key_values` is deprecated.*", category=FutureWarning)
logging_transformers.set_verbosity_error()

# Localiza el audio y la referencia humana completa del mismo caso.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"
ruta_referencia = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/transcripts/indicacion_medica_reference.txt"
referencia = ruta_referencia.read_text(encoding="utf-8").strip().lower()

# Lee el WAV como muestras PCM para no requerir ffmpeg instalado en Windows.
with wave.open(str(audio), "rb") as archivo_wav:
    frecuencia_original = archivo_wav.getframerate()
    muestras = np.frombuffer(archivo_wav.readframes(archivo_wav.getnframes()), dtype=np.int16)

# Normaliza los enteros del WAV y reescala el audio a los 16 kHz que usa Whisper.
muestras = muestras.astype(np.float32) / 32768.0
frecuencia_modelo = 16_000
posiciones_originales = np.arange(len(muestras))
cantidad_destino = round(len(muestras) * frecuencia_modelo / frecuencia_original)
posiciones_destino = np.linspace(0, len(muestras) - 1, cantidad_destino)
muestras_16khz = np.interp(posiciones_destino, posiciones_originales, muestras).astype(np.float32)

# Carga un Whisper pequeño y realiza la transcripción en CPU sobre las muestras.
transcriptor = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1,
)
# Esta tarea ASR devuelve un diccionario cuyo campo text contiene la transcripción.
resultado = cast(dict[str, Any], transcriptor({"raw": muestras_16khz, "sampling_rate": frecuencia_modelo}))
transcripcion = str(resultado["text"]).strip().lower()

# Imprime la salida y su error de palabras.
print("Transcripción:", transcripcion)
print("WER:", round(wer(referencia, transcripcion), 3))

# Resumen final: este pipeline une ASR local y evaluación WER.
# Cambia a whisper-base y compara tiempo, memoria y resultado.
