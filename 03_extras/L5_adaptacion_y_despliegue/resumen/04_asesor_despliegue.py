# Caso adicional LangChain de L5: recomendación tipada de despliegue.
"""Cadena que recomienda una arquitectura según carga y latencia."""
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class PlanDespliegue(BaseModel):
    plataforma: str
    replicas_iniciales: int
    motivo: str

escenario = "300 solicitudes por minuto, latencia objetivo de 300 ms y carga variable"
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(PlanDespliegue)
resultado = extractor.invoke("Recomendá Docker o Kubernetes para este escenario: " + escenario)
print(resultado.model_dump())
