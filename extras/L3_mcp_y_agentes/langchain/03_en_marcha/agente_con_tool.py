# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente corto con una tool determinista.

GUÍA DOCENTE
CUÁNDO USAR: cuando el modelo debe decidir si consulta una capacidad externa.
DIFERENCIA: la tool calcula; el agente decide cuándo llamarla y cómo responder.
EN CLASE: ejecutar primero la función local y después observar al agente.
"""

# Importa os para comprobar la credencial antes de crear el agente.
import os

# Importa el constructor de agentes y el decorador de tools.
from langchain.agents import create_agent
from langchain.tools import tool

# Define una operación pequeña cuyo resultado puede verificarse a mano.
@tool
def calcular_cambio_plazo(original: int, nuevo: int) -> int:
    """Calcula cuántos meses cambia un plazo contractual."""
    return nuevo - original

if os.getenv("OPENAI_API_KEY"):
    # Entrega la tool al agente y formula una consulta concreta.
    agente = create_agent(
        model="openai:gpt-4.1-mini",
        tools=[calcular_cambio_plazo],
        system_prompt="Usa la tool para calcular cambios de plazos.",
    )
    resultado = agente.invoke({
        "messages": [{"role": "user", "content": "El plazo pasa de 12 a 18 meses. ¿Cuánto cambia?"}]
    })
    print(resultado["messages"][-1].content)
else:
    # Ejecuta exactamente la misma capacidad sin consumir una API.
    cambio = calcular_cambio_plazo.invoke({"original": 12, "nuevo": 18})
    print("Falta OPENAI_API_KEY. Resultado local:", cambio, "meses")

# Resumen final: este ejercicio integra agente, decisión y tool verificable.
# Cambia el nuevo plazo a 24 meses y anticipa el resultado antes de ejecutar.
