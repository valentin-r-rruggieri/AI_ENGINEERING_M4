# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Word Error Rate mediante JiWER.

GUÍA DOCENTE
CUÁNDO USAR: para evaluar transcripciones contra referencias conocidas.
DIFERENCIA: JiWER evita reimplementar la distancia de edición.
EN CLASE: interpretar WER como proporción y no como porcentaje de confianza.
"""

# Importa wer desde JiWER para calcular la métrica estándar de ASR.
from jiwer import wer

# Define referencia y transcripción con una sustitución.
referencia = "tomar una tableta cada ocho horas"
transcripcion = "tomar una tableta cada seis horas"

# Calcula y muestra el error como valor y porcentaje.
error = wer(referencia, transcripcion)
print({"wer": round(error, 3), "porcentaje": f"{error * 100:.1f}%"})

# Deriva una regla pequeña de revisión.
umbral = 0.15
print("Revisión humana:", error > umbral)

# Resumen final: este ejercicio evalúa una transcripción con JiWER.
# Elimina una palabra y compara ese error con la sustitución original.
