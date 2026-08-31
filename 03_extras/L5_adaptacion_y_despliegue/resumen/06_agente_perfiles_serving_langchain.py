# Este archivo forma parte del resumen integrador de adaptación y despliegue.
# Ejecutalo para comparar tres perfiles de carga antes de elegir una arquitectura.

"""Agente LangChain que recomienda un despliegue para varios perfiles de serving.

GUÍA DOCENTE
CUÁNDO USAR: antes de elegir dónde publicar un modelo adaptado con LoRA.
DIFERENCIA: los datos de carga describen el problema; el agente justifica la decisión.
EN CLASE: comparar prototipo, API de equipo y servicio de alto tráfico.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa LangChain y Pydantic para obtener recomendaciones claras y consistentes.
from langchain.agents import create_agent
from pydantic import BaseModel, Field


# Define la decisión que un equipo de plataforma podría recibir del agente.
class DecisionDespliegue(BaseModel):
    perfil: str = ""
    destino: str
    replicas: int = Field(ge=1)
    observabilidad: str
    motivo: str


# Declara tres escenarios con tráfico y latencia que se pueden discutir en clase.
perfiles = [
    {"perfil": "prototipo local", "peticiones_por_minuto": 2, "latencia_objetivo_ms": 4000},
    {"perfil": "api de equipo", "peticiones_por_minuto": 40, "latencia_objetivo_ms": 1200},
    {"perfil": "servicio público", "peticiones_por_minuto": 300, "latencia_objetivo_ms": 500},
]

# Crea un agente que relaciona la carga con local, Docker o Kubernetes.
agente = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    response_format=DecisionDespliegue,
    system_prompt=(
        "Sos arquitecto de IA. Para un prototipo de poco tráfico recomendá local; "
        "para una API moderada recomendá Docker; para alto tráfico y baja latencia recomendá "
        "Kubernetes. Proponé réplicas coherentes y mencioná métricas o trazas observables."
    ),
)

# Pide la misma decisión estructurada para perfiles con necesidades crecientes.
for perfil in perfiles:
    pedido = f"Evaluá este perfil de serving para un modelo LoRA: {perfil}"
    respuesta = agente.invoke({"messages": [{"role": "user", "content": pedido}]})["structured_response"]
    decision = DecisionDespliegue.model_validate({**respuesta.model_dump(), "perfil": perfil["perfil"]})
    print(decision.model_dump())

# Resumen final: servir un modelo también requiere decidir capacidad y observabilidad.
# Cambiá las peticiones por minuto y defendé si la recomendación sigue siendo válida.
