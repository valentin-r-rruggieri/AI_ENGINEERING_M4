# Este archivo forma parte del recorrido práctico de DSPy.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extracción declarativa de un cambio contractual.

GUÍA DOCENTE
CUÁNDO USAR: para prototipar una tarea estructurada con pocos campos.
DIFERENCIA: DSPy expresa la tarea y Pydantic protege el resultado final.
EN CLASE: seguir signature, predictor, datos y validación.
"""

# Importa os, DSPy y Pydantic para ejecución y validación.
import os
import dspy
from pydantic import BaseModel

# Define la tarea declarativa que compara dos textos.
class Comparar(dspy.Signature):
    """Compara dos cláusulas y describe el cambio principal."""

    original: str = dspy.InputField()
    nueva: str = dspy.InputField()
    cambio: str = dspy.OutputField()
    riesgo: str = dspy.OutputField()

# Define la frontera validada que usará la aplicación.
class CambioValidado(BaseModel):
    cambio: str
    riesgo: str

# Prepara dos fragmentos pequeños.
original = "La vigencia será de 12 meses."
nueva = "La vigencia será de 18 meses y se renovará automáticamente."

if os.getenv("OPENAI_API_KEY"):
    # Configura el modelo y ejecuta el predictor.
    dspy.configure(lm=dspy.LM("openai/gpt-4.1-mini"))
    resultado = dspy.Predict(Comparar)(original=original, nueva=nueva)
    cambio = CambioValidado(cambio=resultado.cambio, riesgo=resultado.riesgo)
else:
    # Conserva una salida local para explicar la validación sin API.
    cambio = CambioValidado(
        cambio="La vigencia aumenta de 12 a 18 meses.",
        riesgo="Se incorpora renovación automática.",
    )

print(cambio.model_dump())

# Resumen final: este pipeline combina prompting declarativo y validación.
# Modifica únicamente la cláusula nueva y revisa los campos obtenidos.
