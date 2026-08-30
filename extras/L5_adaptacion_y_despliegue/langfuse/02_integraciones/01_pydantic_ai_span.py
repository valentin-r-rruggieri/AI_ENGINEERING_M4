# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente PydanticAI dentro de un span Langfuse.

GUÍA DOCENTE
CUÁNDO USAR: para agrupar una ejecución tipada dentro de un workflow mayor.
DIFERENCIA: el span manual fija la jerarquía aunque el agente sea otro framework.
EN CLASE: observar input, output y nombre del agente.
"""

# Importa os, Langfuse, PydanticAI y Pydantic.
import os
from langfuse import get_client
from pydantic_ai import Agent
from pydantic import BaseModel

# Define una salida tipada para la demostración.
class Resultado(BaseModel):
    cambio: str
    riesgo: str

configurado = all(os.getenv(nombre) for nombre in [
    "OPENAI_API_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
])

if configurado:
    # Ejecuta el agente dentro de un span con entrada y salida explícitas.
    langfuse = get_client()
    agente = Agent("openai:gpt-4.1-mini", output_type=Resultado)
    with langfuse.start_as_current_observation(as_type="span", name="agente_pydantic_ai", input="cambio de plazo") as span:
        resultado = agente.run_sync("Analiza el cambio de 12 a 18 meses.")
        span.update(output=resultado.output.model_dump())
        print(resultado.output.model_dump())
    langfuse.flush()
else:
    print("Configurá OpenAI y Langfuse para ejecutar la integración.")

# Resumen final: este ejercicio agrupa un Agent dentro de una observación.
# Añade un span padre llamado legalmove y revisa la nueva jerarquía.
