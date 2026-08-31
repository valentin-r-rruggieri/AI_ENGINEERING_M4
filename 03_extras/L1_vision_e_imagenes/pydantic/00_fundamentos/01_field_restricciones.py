# Este archivo forma parte del recorrido práctico de Pydantic.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Restricciones de campos con Field.

GUÍA DOCENTE
CUÁNDO USAR: cuando un tipo correcto todavía puede contener un valor inválido.
DIFERENCIA: float valida el tipo; Field agrega límites de negocio.
EN CLASE: distinguir validación técnica de validación del dominio.
"""

# Importa BaseModel y Field para agregar restricciones.
from pydantic import BaseModel, Field

# Limita confianza al intervalo cerrado entre cero y uno.
class Prediccion(BaseModel):
    etiqueta: str = Field(min_length=1)
    confianza: float = Field(ge=0, le=1)

# Crea una predicción válida y muestra el resultado.
prediccion = Prediccion(etiqueta="aprobado", confianza=0.91)
print(prediccion.model_dump())

# Muestra también el schema que podría compartir una API.
print(Prediccion.model_json_schema()["properties"])

# Resumen final: este ejercicio agrega límites explícitos a los campos.
# Cambia confianza por 1.2 y lee qué restricción aparece en el error.
