# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Delegación de un agente hacia otro mediante una tool.

GUÍA DOCENTE
CUÁNDO USAR: cuando un agente coordinador decide si necesita un especialista.
DIFERENCIA: en delegación el control vuelve al coordinador después de la tool.
EN CLASE: comparar este flujo con el handoff programático fijo.
"""

# Importa os, Agent y RunContext para compartir el uso de la ejecución.
import os
from pydantic_ai import Agent, RunContext

if os.getenv("OPENAI_API_KEY"):
    # Define el especialista y el coordinador después de validar la clave.
    especialista = Agent(
        "openai:gpt-4.1-mini",
        name="especialista_legal",
        instructions="Identifica un único riesgo legal concreto.",
    )
    coordinador = Agent(
        "openai:gpt-4.1-mini",
        name="coordinador",
        instructions="Consulta al especialista y entrega una recomendación breve.",
    )

    # Expone el especialista como una tool del coordinador.
    @coordinador.tool
    async def consultar_especialista(ctx: RunContext, clausula: str) -> str:
        """Solicita una revisión al especialista legal."""
        resultado = await especialista.run(clausula, usage=ctx.usage)
        return resultado.output

    resultado = coordinador.run_sync("Revisa: el contrato se renueva automáticamente.")
    print(resultado.output)
else:
    print("Falta OPENAI_API_KEY. Delegación preparada: coordinador -> especialista")

# Resumen final: este ejercicio permite al coordinador delegar y retomar control.
# Limita la pregunta a un caso sin riesgo y observa si delega igualmente.
