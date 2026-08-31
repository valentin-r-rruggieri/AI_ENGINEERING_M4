# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Transcripción local con Whisper tiny.

GUÍA DOCENTE
CUÁNDO USAR: cuando se desea ejecutar ASR local sin enviar audio a una API.
DIFERENCIA: el cómputo y la descarga del modelo ocurren en la propia máquina.
EN CLASE: comparar privacidad, latencia y precisión con una API remota.
"""

# Importa Path para localizar el audio y pipeline para ejecutar ASR.
from pathlib import Path
from transformers import pipeline

# Reutiliza un audio de la clase L2.
raiz = Path(__file__).resolve().parents[4]
audio = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/indicacion_medica.wav"

# Carga Whisper tiny en CPU y transcribe el archivo.
transcriptor = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1,
)
resultado = transcriptor(str(audio))

# Muestra únicamente el texto reconocido.
print(resultado["text"])

# Resumen final: este ejercicio ejecuta ASR local con un modelo pequeño.
# Cambia al audio con ruido y compara las palabras incorrectas.
