# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente PydanticAI mínimo.

GUÍA DOCENTE
CUÁNDO USAR: para encapsular modelo, instrucciones, tools y tipo de salida.
DIFERENCIA: el Agent es reutilizable entre múltiples ejecuciones.
EN CLASE: identificar modelo, name, instructions y resultado.output.
"""

# Importa os para la clave y Agent como interfaz principal.
import os
from pydantic_ai import Agent

if os.getenv("OPENAI_API_KEY"):
    # Define el agente solo después de confirmar la credencial.
    agente = Agent(
        "openai:gpt-4.1-mini",
        name="docente_aem4",
        instructions="Responde en una oración clara para estudiantes de AI Engineering.",
    )

    # Ejecuta el agente en modo síncrono y lee su output.
    resultado = agente.run_sync("¿Qué problema resuelve MCP?")
    print(resultado.output)
else:
    print("Falta OPENAI_API_KEY. Agente previsto: docente_aem4")

# Resumen final: este ejercicio crea y ejecuta un Agent reutilizable.
# Cambia las instrucciones para una audiencia experta y compara la respuesta.
