# Este archivo forma parte del recorrido práctico de DSPy.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Validación Pydantic posterior a una predicción DSPy.

GUÍA DOCENTE
CUÁNDO USAR: cuando el output del módulo debe respetar reglas de negocio.
DIFERENCIA: DSPy guía la generación; Pydantic valida el dato resultante.
EN CLASE: mantener separadas generación y validación.
"""

# Importa Pydantic para validar el resultado simulado del módulo.
from pydantic import BaseModel, Field

# Define el contrato que deberá cumplir el resultado.
class Revision(BaseModel):
    resumen: str = Field(min_length=10)
    riesgo: str
    confianza: float = Field(ge=0, le=1)

# Representa los campos que podría devolver un predictor DSPy.
salida_dspy = {
    "resumen": "La cláusula extiende la vigencia a dieciocho meses.",
    "riesgo": "Renovación automática sin aviso suficiente.",
    "confianza": 0.9,
}

# Valida antes de entregar la salida al siguiente componente.
revision = Revision.model_validate(salida_dspy)
print(revision.model_dump())

# Resumen final: este ejercicio usa Pydantic como frontera de confianza.
# Cambia confianza por 1.5 y observa qué regla bloquea la salida.
