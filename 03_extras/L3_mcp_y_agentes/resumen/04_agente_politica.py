# Caso adicional LangChain de L3: agente que consulta una política mediante una tool.
"""Agente con herramienta local que representa una política publicada por MCP."""
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool

@tool
def consultar_politica(tema: str) -> str:
    """Devuelve una política contractual vigente."""
    return {"baja": "Las bajas requieren revisión humana.", "plazo": "Los cambios de plazo requieren adenda."}.get(tema, "Política no encontrada.")

agente = create_agent(model="openai:gpt-4.1-mini", tools=[consultar_politica],
                      system_prompt="Consultá la tool antes de explicar una política contractual.")
resultado = agente.invoke({"messages": [{"role": "user", "content": "¿Qué política aplica a una baja?"}]})
print(resultado["messages"][-1].content)
