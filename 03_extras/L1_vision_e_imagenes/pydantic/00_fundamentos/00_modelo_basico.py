# Este archivo forma parte del recorrido práctico de Pydantic.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Modelo de datos mínimo con tipos declarados.

GUÍA DOCENTE
CUÁNDO USAR: cuando un pipeline debe intercambiar datos con una forma conocida.
DIFERENCIA: un diccionario acepta cualquier contenido; un modelo aplica un contrato.
EN CLASE: identificar campos, tipos y conversión a diccionario.
"""

# Importa BaseModel para declarar un contrato de datos.
from pydantic import BaseModel

# Define los dos campos requeridos para una persona.
class Persona(BaseModel):
    nombre: str
    edad: int

# Valida un diccionario y crea una instancia tipada.
datos = {"nombre": "Ana", "edad": 34}
persona = Persona.model_validate(datos)

# Muestra el objeto y su representación serializable.
print(persona)
print(persona.model_dump())

# Resumen final: este ejercicio convierte un diccionario en datos validados.
# Elimina edad del diccionario y observa el error generado.
