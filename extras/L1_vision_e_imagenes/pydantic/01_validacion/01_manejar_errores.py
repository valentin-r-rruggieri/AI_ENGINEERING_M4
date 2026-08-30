# Este archivo forma parte del recorrido práctico de Pydantic.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Lectura controlada de errores de validación.

GUÍA DOCENTE
CUÁNDO USAR: para convertir fallos técnicos en mensajes útiles para el usuario.
DIFERENCIA: capturar ValidationError conserva el detalle de cada campo.
EN CLASE: inspeccionar loc, type y msg de un error.
"""

# Importa los componentes para modelar y capturar validaciones.
from pydantic import BaseModel, Field, ValidationError

# Define un pago con restricciones simples.
class Pago(BaseModel):
    moneda: str = Field(pattern="^(ARS|USD)$")
    importe: float = Field(gt=0)

# Prepara intencionalmente dos valores inválidos.
datos = {"moneda": "EUR", "importe": -50}

try:
    # Intenta validar y muestra el resultado si fuera correcto.
    pago = Pago.model_validate(datos)
    print(pago.model_dump())
except ValidationError as error:
    # Recorre cada problema sin imprimir un traceback largo.
    for problema in error.errors():
        print({"campo": problema["loc"][0], "mensaje": problema["msg"]})

# Resumen final: este ejercicio transforma errores en mensajes controlados.
# Corrige primero moneda y observa que permanece únicamente el error de importe.
