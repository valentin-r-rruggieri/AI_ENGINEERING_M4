# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Transcripción local con Whisper tiny.

GUÍA DOCENTE
CUÁNDO USAR: cuando se desea ejecutar ASR local sin enviar audio a una API.
DIFERENCIA: el cómputo y la descarga del modelo ocurren en la propia máquina.
EN CLASE: comparar privacidad, latencia y precisión con una API remota.
"""

# Importa Path para localizar el audio, tipos para aclarar la salida y wave para leer WAV sin usar ffmpeg.
from pathlib import Path
from typing import Any, cast
import wave
import warnings

# Importa NumPy para convertir muestras PCM en números que entiende el modelo.
import numpy as np

# Importa pipeline y logging de Transformers para ejecutar ASR local sin avisos deprecados.
from transformers import pipeline
from transformers.utils import logging as logging_transformers

# Oculta avisos internos deprecados de esta versión sin silenciar errores reales.
warnings.filterwarnings("ignore", message="The input name `inputs` is deprecated.*", category=FutureWarning)
warnings.filterwarnings("ignore", message="Passing a tuple of `past_key_values` is deprecated.*", category=FutureWarning)
logging_transformers.set_verbosity_error()

# Reutiliza un audio de la clase L2.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"

# Lee el WAV como muestras numéricas para no depender de ffmpeg en Windows.
with wave.open(str(audio), "rb") as archivo_wav:
    frecuencia_original = archivo_wav.getframerate()
    muestras = np.frombuffer(archivo_wav.readframes(archivo_wav.getnframes()), dtype=np.int16)

# Normaliza enteros PCM de 16 bits al rango aproximado entre -1 y 1.
muestras = muestras.astype(np.float32) / 32768.0

# Reescala a 16 kHz, la frecuencia esperada por Whisper, con un ejemplo simple.
frecuencia_modelo = 16_000
posiciones_originales = np.arange(len(muestras))
cantidad_destino = round(len(muestras) * frecuencia_modelo / frecuencia_original)
posiciones_destino = np.linspace(0, len(muestras) - 1, cantidad_destino)
muestras_16khz = np.interp(posiciones_destino, posiciones_originales, muestras).astype(np.float32)

# Carga Whisper tiny en CPU y transcribe las muestras ya preparadas.
transcriptor = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1,
)
resultado = cast(dict[str, Any], transcriptor({"raw": muestras_16khz, "sampling_rate": frecuencia_modelo}))

# Muestra únicamente el texto reconocido.
print(str(resultado["text"]))

# Resumen final: este ejercicio ejecuta ASR local con un modelo pequeño.
# Cambia al audio con ruido y compara las palabras incorrectas.
