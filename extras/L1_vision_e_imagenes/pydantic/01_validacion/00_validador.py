# Este archivo forma parte del recorrido práctico de Pydantic.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Regla de dominio mediante field_validator.

GUÍA DOCENTE
CUÁNDO USAR: cuando una regla no puede expresarse solo con el tipo del campo.
DIFERENCIA: Field aplica límites genéricos; un validador expresa lógica propia.
EN CLASE: explicar el valor de entrada y el valor devuelto por el validador.
"""

# Importa BaseModel y el decorador de validación de campos.
from pydantic import BaseModel, field_validator

# Define un contrato cuyo documento debe contener solo dígitos.
class Titular(BaseModel):
    nombre: str
    documento: str

    # Normaliza y valida el documento antes de conservarlo.
    @field_validator("documento")
    @classmethod
    def validar_documento(cls, valor: str) -> str:
        limpio = valor.replace(".", "").replace("-", "")
        if not limpio.isdigit():
            raise ValueError("el documento debe contener solo dígitos")
        return limpio

# Valida un dato con separadores habituales.
titular = Titular(nombre="Ana Pérez", documento="30.111.222")
print(titular.model_dump())

# Resumen final: este ejercicio normaliza una regla específica del dominio.
# Agrega una letra al documento y observa el mensaje del validador.
