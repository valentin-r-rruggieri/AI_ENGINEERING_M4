# Este archivo forma parte del recorrido práctico de DSPy.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Signature declarativa de entrada y salida.

GUÍA DOCENTE
CUÁNDO USAR: para describir qué debe hacer un módulo sin escribir un prompt largo.
DIFERENCIA: la signature declara campos; el módulo decide cómo pedir la respuesta.
EN CLASE: identificar input, output y descripción de cada campo.
"""

# Importa DSPy para declarar una firma de trabajo.
import dspy

# Define el contrato semántico de una tarea de resumen.
class ResumirContrato(dspy.Signature):
    """Resume un fragmento contractual en lenguaje claro."""

    texto: str = dspy.InputField(desc="fragmento del contrato")
    resumen: str = dspy.OutputField(desc="una oración clara")

# Crea un predictor sin ejecutar todavía un modelo.
predictor = dspy.Predict(ResumirContrato)

# Muestra la firma para reconocer sus entradas y salidas.
print("Módulo preparado:", type(predictor).__name__)
print("Signature:", ResumirContrato.__name__)

# Resumen final: este ejercicio separa la intención de la implementación del prompt.
# Agrega un output llamado riesgo y describe qué debería contener.
