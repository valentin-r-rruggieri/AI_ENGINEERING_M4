# Este archivo forma parte del recorrido práctico de DSPy.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Múltiples salidas declaradas en una signature.

GUÍA DOCENTE
CUÁNDO USAR: cuando una sola entrada debe producir resultados con roles diferentes.
DIFERENCIA: campos separados son más fáciles de evaluar que un párrafo combinado.
EN CLASE: asignar una responsabilidad clara a cada OutputField.
"""

# Importa DSPy para definir los campos de la tarea.
import dspy

# Declara una entrada y dos resultados con propósitos distintos.
class RevisarClausula(dspy.Signature):
    """Revisa una cláusula contractual."""

    clausula: str = dspy.InputField()
    resumen: str = dspy.OutputField(desc="significado en lenguaje claro")
    riesgo: str = dspy.OutputField(desc="riesgo principal o sin riesgo")

# Prepara el predictor y muestra sus campos esperados.
revisor = dspy.Predict(RevisarClausula)
print("Predictor:", type(revisor).__name__)
print("Outputs esperados: resumen, riesgo")

# Resumen final: este ejercicio divide una respuesta compleja en campos.
# Agrega un output recomendacion y define una descripción precisa.
