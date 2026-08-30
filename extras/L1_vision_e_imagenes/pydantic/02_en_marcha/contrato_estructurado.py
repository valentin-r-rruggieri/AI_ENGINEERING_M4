# Este archivo forma parte del recorrido práctico de Pydantic.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Contrato de salida utilizado por LegalMove.

GUÍA DOCENTE
CUÁNDO USAR: para garantizar que distintos agentes entreguen el mismo formato.
DIFERENCIA: el framework puede cambiar; el contrato de salida permanece estable.
EN CLASE: relacionar cada campo con un criterio de la rúbrica del proyecto.
"""

# Importa BaseModel, Field y ConfigDict para un contrato estricto.
from pydantic import BaseModel, ConfigDict, Field

# Define la salida común a LangChain, LangGraph y PydanticAI.
class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resumen_ejecutivo: str = Field(min_length=10)
    cambios_detectados: list[str] = Field(min_length=1)
    riesgos_legales: list[str]

# Simula el resultado entregado por un agente de extracción.
salida_agente = {
    "resumen_ejecutivo": "La adenda modifica el plazo y la penalidad del contrato.",
    "cambios_detectados": ["El plazo aumenta de 12 a 18 meses."],
    "riesgos_legales": ["La penalidad se aplica sin período de gracia."],
}

# Valida el resultado antes de enviarlo a otra capa.
resultado = ContractChangeOutput.model_validate(salida_agente)
print(resultado.model_dump_json(indent=2))

# Resumen final: este ejercicio fija un contrato independiente del framework.
# Agrega un campo inesperado y observa cómo extra="forbid" lo rechaza.
