# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente tipado con una tool local.

GUÍA DOCENTE
CUÁNDO USAR: cuando se necesita una operación verificable y una salida validada.
DIFERENCIA: Pydantic valida el resultado final además de describir la tool.
EN CLASE: revisar la función y el schema antes de permitir la llamada al modelo.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la clave y Pydantic para el contrato.
import os
from pydantic import BaseModel, Field

# Importa Agent para combinar modelo, tool y output tipado.
from pydantic_ai import Agent

# Define la estructura mínima del resultado.
class CambioPlazo(BaseModel):
    diferencia_meses: int
    confianza: float = Field(ge=0, le=1)

# Define una capacidad local que también puede probarse sin agente.
def calcular_diferencia(original: int, nuevo: int) -> int:
    """Calcula la diferencia entre dos plazos en meses."""
    return nuevo - original

# Crea el agente solo después de confirmar la credencial.
agente = Agent(
    "openai:gpt-4.1-mini",
    output_type=CambioPlazo,
    instructions="Usa la tool y devuelve diferencia_meses y confianza.",
)
agente.tool_plain(calcular_diferencia)
resultado = agente.run_sync("El plazo cambia de 12 a 18 meses.")
print(resultado.output.model_dump())
# Resumen final: este ejercicio integra tool, agente y contrato Pydantic.
# Cambia el plazo nuevo y agrega una restricción para impedir valores negativos.
