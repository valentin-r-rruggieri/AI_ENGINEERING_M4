"""Pruebas de responsabilidades separadas y handoff entre agentes."""

# Importa objetos de prueba y los dos agentes LangChain envueltos.
from types import SimpleNamespace

import pytest

from src.agents.contextualization_agent import ContextualizationAgent
from src.agents.extraction_agent import ExtractionAgent
from src.config import Settings
from src.errors import OutputValidationError
from src.models import ContractChangeOutput


# Entrega una configuración ficticia porque los agentes simulados no usan red.
def configuracion() -> Settings:
    return Settings("key", "gpt-4o", "gpt-4o", "pk", "sk", "https://host", 10, 0)


# Registra entradas y devuelve el resultado indicado por cada prueba.
class AgenteFalso:
    def __init__(self, respuesta: dict) -> None:
        self.respuesta = respuesta
        self.entrada = None

    def invoke(self, entrada, config=None):
        self.entrada = entrada
        return self.respuesta


# Confirma que el primer agente recibe ambos textos y entrega solo el mapa.
def test_contextualization_agent_construye_handoff() -> None:
    falso = AgenteFalso({"messages": [SimpleNamespace(content="Mapa: cláusula 2 corresponde a cláusula 2")]})
    agente = ContextualizationAgent(configuracion(), agent=falso)
    mapa = agente.run("Original A", "Adenda B")
    assert mapa.startswith("Mapa")
    contenido = falso.entrada["messages"][0]["content"]
    assert "Original A" in contenido and "Adenda B" in contenido


# Confirma que el segundo agente recibe el handoff y valida el schema final.
def test_extraction_agent_usa_handoff_y_valida_salida() -> None:
    salida = ContractChangeOutput(
        sections_changed=["Cláusula 2"],
        topics_touched=["precio"],
        summary_of_the_change="MODIFICACIÓN: el precio se actualiza según la adenda recibida.",
    )
    falso = AgenteFalso({"structured_response": salida})
    agente = ExtractionAgent(configuracion(), agent=falso)
    resultado = agente.run("Original", "Adenda", "Mapa obligatorio")
    assert resultado == salida
    assert "Mapa obligatorio" in falso.entrada["messages"][0]["content"]

    invalido = AgenteFalso({"structured_response": {"sections_changed": [], "topics_touched": [], "summary_of_the_change": "corto"}})
    with pytest.raises(OutputValidationError):
        ExtractionAgent(configuracion(), agent=invalido).run("A", "B", "Mapa")
