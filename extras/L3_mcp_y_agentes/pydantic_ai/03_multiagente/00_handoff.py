# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Handoff programático entre dos Agents.

GUÍA DOCENTE
CUÁNDO USAR: cuando los roles deben ejecutarse en una secuencia auditable.
DIFERENCIA: el código, no el modelo, decide quién recibe el siguiente turno.
EN CLASE: verificar que cada instructions define una responsabilidad distinta.
"""

# Importa os y Agent.
import os
from pydantic_ai import Agent

# Prepara la entrada común a los dos roles.
original = "Vigencia de 12 meses."
nuevo = "Vigencia de 18 meses con renovación automática."

if os.getenv("OPENAI_API_KEY"):
    # Crea los dos agentes con responsabilidades no superpuestas.
    contextualizador = Agent(
        "openai:gpt-4.1-mini",
        name="contextualizador",
        instructions="Describe estructura y tema. No extraigas cambios.",
    )
    extractor = Agent(
        "openai:gpt-4.1-mini",
        name="extractor",
        instructions="Usa el contexto recibido para listar cambios y riesgos.",
    )

    # Ejecuta el primer rol y entrega su output al segundo.
    contexto = contextualizador.run_sync(f"Original: {original}\nNuevo: {nuevo}")
    cambios = extractor.run_sync(f"Contexto: {contexto.output}\nOriginal: {original}\nNuevo: {nuevo}")
    print(cambios.output)
else:
    print("Falta OPENAI_API_KEY. Flujo preparado: contextualizador -> extractor")

# Resumen final: este ejercicio implementa un handoff controlado por Python.
# Invierte el orden y explica por qué se mezclan las responsabilidades.
