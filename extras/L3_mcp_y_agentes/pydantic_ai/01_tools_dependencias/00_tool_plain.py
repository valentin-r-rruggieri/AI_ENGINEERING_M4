# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tool sin dependencias mediante tool_plain.

GUÍA DOCENTE
CUÁNDO USAR: cuando una capacidad depende solo de sus argumentos.
DIFERENCIA: tool_plain no recibe RunContext; tool sí puede usar dependencias.
EN CLASE: observar cómo firma y docstring forman el schema.
"""

# Importa os y Agent para registrar la tool.
import os
from pydantic_ai import Agent

# Define una función determinista que puede probarse sin un modelo.
def diferencia_plazo(original: int, nuevo: int) -> int:
    """Calcula la diferencia entre dos plazos en meses."""
    return nuevo - original

if os.getenv("OPENAI_API_KEY"):
    # Crea el agente y registra la función como tool_plain.
    agente = Agent(
        "openai:gpt-4.1-mini",
        instructions="Usa la tool para calcular diferencias de plazos.",
    )
    agente.tool_plain(diferencia_plazo)
    resultado = agente.run_sync("¿Cuánto cambia un plazo de 12 a 18 meses?")
    print(resultado.output)
else:
    print("Falta OPENAI_API_KEY. Tool local devuelve:", diferencia_plazo(12, 18))

# Resumen final: este ejercicio entrega una función local al agente.
# Agrega una validación para rechazar valores negativos.
