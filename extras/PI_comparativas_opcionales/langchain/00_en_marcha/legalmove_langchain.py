# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""LegalMove con dos agentes LangChain y salida común.

GUÍA DOCENTE
CUÁNDO USAR: como referencia de la entrega multiagente del proyecto M4.
DIFERENCIA: cada agente conserva un rol y el resultado final es Pydantic.
EN CLASE: seguir contextualización, extracción y validación.
"""

# Importa os, agentes y Pydantic.
import os
from langchain.agents import create_agent
from pydantic import BaseModel, ConfigDict, Field

# Define el mismo contrato utilizado por los otros frameworks.
class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resumen_ejecutivo: str = Field(min_length=10)
    cambios_detectados: list[str] = Field(min_length=1)
    riesgos_legales: list[str]

# Usa textos breves para mantener visible el flujo de agentes.
original = "El contrato dura 12 meses y no se renueva automáticamente."
nuevo = "El contrato dura 18 meses y se renueva automáticamente por 12 meses."

if os.getenv("OPENAI_API_KEY"):
    # El primer agente construye contexto pero no extrae cambios.
    contextualizador = create_agent(
        "openai:gpt-4.1-mini",
        tools=[],
        system_prompt="Describe estructura, tema y relación entre cláusulas. No listes cambios.",
    )
    estado_1 = contextualizador.invoke({"messages": [{"role": "user", "content": f"Original: {original}\nNuevo: {nuevo}"}]})
    contexto = estado_1["messages"][-1].content

    # El segundo agente devuelve directamente el schema compartido.
    extractor = create_agent(
        "openai:gpt-4.1-mini",
        tools=[],
        system_prompt="Extrae cambios y riesgos sin inventar información.",
        response_format=ContractChangeOutput,
    )
    estado_2 = extractor.invoke({"messages": [{"role": "user", "content": f"Contexto: {contexto}\nOriginal: {original}\nNuevo: {nuevo}"}]})
    resultado = estado_2["structured_response"]
else:
    # Conserva una demostración local y validada sin usar la API.
    resultado = ContractChangeOutput(
        resumen_ejecutivo="Se amplía la vigencia y se incorpora renovación automática.",
        cambios_detectados=["El plazo aumenta de 12 a 18 meses.", "Se agrega renovación por 12 meses."],
        riesgos_legales=["La renovación automática puede requerir aviso previo."],
    )

print(resultado.model_dump_json(indent=2))

# Resumen final: este pipeline implementa dos roles y una salida estable.
# Cambia una cláusula y verifica que el schema no dependa del framework.
