# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Dependencias tipadas accesibles mediante RunContext.

GUÍA DOCENTE
CUÁNDO USAR: cuando una tool necesita datos o clientes creados por la aplicación.
DIFERENCIA: las dependencias se pasan por ejecución y no son variables globales.
EN CLASE: seguir deps_type, deps y ctx.deps.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa dataclass, os, Agent y RunContext.
from dataclasses import dataclass
import os
from pydantic_ai import Agent, RunContext

# Agrupa una política externa que puede variar por entorno.
@dataclass
class Politicas:
    umbral_revision: float

# Define la tool que consultará la dependencia de la ejecución.
def requiere_revision(ctx: RunContext[Politicas], confianza: float) -> bool:
    """Indica si la confianza está bajo el umbral configurado."""
    return confianza < ctx.deps.umbral_revision

politicas = Politicas(umbral_revision=0.85)

# Crea el agente y registra la tool luego de validar la clave.
agente = Agent("openai:gpt-4.1-mini", deps_type=Politicas)
agente.tool(requiere_revision)
resultado = agente.run_sync("¿Debo revisar una confianza de 0.80?", deps=politicas)
print(resultado.output)
# Resumen final: este ejercicio inyecta una política tipada por ejecución.
# Cambia el umbral y anticipa cómo debería responder la tool.
