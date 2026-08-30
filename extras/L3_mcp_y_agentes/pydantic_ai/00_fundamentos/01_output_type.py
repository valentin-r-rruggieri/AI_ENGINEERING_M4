# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Salida estructurada mediante output_type.

GUÍA DOCENTE
CUÁNDO USAR: cuando el agente debe devolver datos validados y tipados.
DIFERENCIA: output_type integra la validación dentro del ciclo del agente.
EN CLASE: inspeccionar el modelo y el tipo real de resultado.output.
"""

# Importa credenciales, Agent y Pydantic.
import os
from pydantic_ai import Agent
from pydantic import BaseModel, Field

# Define el contrato que deberá generar el agente.
class Clasificacion(BaseModel):
    etiqueta: str
    confianza: float = Field(ge=0, le=1)

if os.getenv("OPENAI_API_KEY"):
    # Crea el agente tipado después de confirmar la credencial.
    agente = Agent(
        "openai:gpt-4.1-mini",
        output_type=Clasificacion,
        instructions="Clasifica el pedido como consulta o cancelacion.",
    )
    resultado = agente.run_sync("Quiero terminar mi contrato.")
    print(resultado.output.model_dump())
else:
    print("Falta OPENAI_API_KEY. Schema preparado:", Clasificacion.model_json_schema())

# Resumen final: este ejercicio integra generación y validación Pydantic.
# Restringe etiqueta con Literal y observa el schema resultante.
