# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente LangChain capaz de elegir una tool.

GUÍA DOCENTE
CUÁNDO USAR: cuando el modelo debe decidir si necesita ejecutar una capacidad.
DIFERENCIA: create_agent administra el ciclo modelo, tool y respuesta.
EN CLASE: observar el mensaje de tool antes de leer la respuesta final.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os, create_agent y el decorador de tools.
import os
from langchain.agents import create_agent
from langchain.tools import tool

# Define una capacidad determinista.
@tool
def consultar_estado(contrato: str) -> str:
    """Consulta el estado de un contrato de demostración."""
    return f"El contrato {contrato} está vigente."

# Crea el agente con una instrucción y la tool disponible.
agente = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[consultar_estado],
    system_prompt="Usa la tool para responder estados contractuales.",
)
resultado = agente.invoke({"messages": [{"role": "user", "content": "¿Cuál es el estado de C-100?"}]})
print(resultado["messages"][-1].content)
# Resumen final: este ejercicio permite al agente llamar una tool.
# Pregunta algo ajeno al estado y observa si la tool sigue siendo necesaria.
