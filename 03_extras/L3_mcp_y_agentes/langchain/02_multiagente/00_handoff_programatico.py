# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Handoff programático entre dos agentes especializados.

GUÍA DOCENTE
CUÁNDO USAR: cuando las responsabilidades tienen un orden fijo y auditable.
DIFERENCIA: el segundo agente recibe el mapa producido por el primero.
EN CLASE: explicar por qué los prompts no deben solaparse.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os y create_agent para construir dos roles.
import os
from langchain.agents import create_agent

# Prepara dos fragmentos que compartirán ambos agentes.
original = "Vigencia de 12 meses."
nuevo = "Vigencia de 18 meses con renovación automática."

# Crea un agente que solo contextualiza la estructura.
contextualizador = create_agent(
    "openai:gpt-4.1-mini",
    tools=[],
    system_prompt="Describe contexto y estructura. No extraigas cambios.",
)
mapa = contextualizador.invoke({"messages": [{"role": "user", "content": f"Original: {original}\nNuevo: {nuevo}"}]})
contexto = mapa["messages"][-1].content

# Crea un segundo agente que usa el mapa para extraer diferencias.
extractor = create_agent(
    "openai:gpt-4.1-mini",
    tools=[],
    system_prompt="Extrae únicamente cambios y riesgos usando el contexto recibido.",
)
cambios = extractor.invoke({"messages": [{"role": "user", "content": f"Contexto: {contexto}\nOriginal: {original}\nNuevo: {nuevo}"}]})
print(cambios["messages"][-1].content)
# Resumen final: este ejercicio encadena dos agentes con responsabilidades distintas.
# Quita el contexto del segundo y compara la calidad de la extracción.
