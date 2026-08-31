# Este archivo resume L5 mediante un caso práctico de adaptación con LoRA.
# Lee cada bloque y modifica una variable por vez.

"""Caso 1: decidir si LoRA es adecuado para una adaptación pequeña.

GUÍA DOCENTE
CUÁNDO USAR: cuando se quiere adaptar un modelo sin entrenar todos sus pesos.
DIFERENCIA: LoRA aprende adapters; fine-tuning completo modifica el modelo entero.
EN CLASE: relacionar cantidad de parámetros, costo y tiempo de entrenamiento.
"""

# Carga el .env para mantener el patrón uniforme de los resúmenes.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain y Pydantic para dejar la decisión explícita y validada.
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Describe una recomendación de adaptación pequeña y comprensible.
class DecisionAdaptacion(BaseModel):
    tecnica: str
    parametros_entrenables: int = Field(ge=1)
    recomendacion: str

# Representa un adapter de rango bajo frente a un modelo de gran tamaño.
parametros_adapter = 120_000
resultado = DecisionAdaptacion(
    tecnica="LoRA",
    parametros_entrenables=parametros_adapter,
    recomendacion="Usar LoRA para probar una adaptación económica en CPU antes de escalar.",
)

# Usa LangChain para justificar la decisión con lenguaje de producto.
justificacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    "Explica en una oración por qué LoRA puede ser más económico que fine-tuning completo."
).content

# Muestra la decisión que guiaría el ejercicio de entrenamiento posterior.
print({**resultado.model_dump(), "justificacion_langchain": justificacion})

# Resumen final: LoRA reduce lo que se entrena, no elimina la evaluación.
# Duplicá los parámetros y discutí si todavía entra en el presupuesto.
