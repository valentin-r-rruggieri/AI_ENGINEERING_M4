# Este archivo resume L2 mediante un caso práctico de calidad de transcripción.
# Lee cada bloque y modifica una variable por vez.

"""Caso 1: medir una transcripción de audio con WER.

GUÍA DOCENTE
CUÁNDO USAR: antes de confiar una acción a una transcripción automática.
DIFERENCIA: transcribir produce texto; WER mide distancia frente a una referencia.
EN CLASE: cambiar una palabra y observar el impacto porcentual.
"""

# Carga el .env para mantener el mismo punto de partida que los otros casos.
from dotenv import load_dotenv
load_dotenv()

# Importa la métrica y LangChain para interpretar la medición.
from jiwer import wer
from langchain_openai import ChatOpenAI

# Define una referencia humana y una salida de ASR pequeña.
referencia = "tomar un comprimido cada ocho horas"
transcripcion = "tomar un comprimido cada ocho horas"

# Calcula una medida objetiva de error de reconocimiento de voz.
error_wer = wer(referencia, transcripcion)

# Pide a LangChain una interpretación breve de la métrica obtenida.
explicacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    f"Explica en una oración qué significa WER={error_wer} para una transcripción médica."
).content

# Muestra datos técnicos y explicación del modelo.
print({"referencia": referencia, "transcripcion": transcripcion, "wer": round(error_wer, 3), "explicacion": explicacion})

# Resumen final: una WER baja es una señal, no una garantía clínica.
# Cambia comprimido por cápsula y observa el nuevo valor.
