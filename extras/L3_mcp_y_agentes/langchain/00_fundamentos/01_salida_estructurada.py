# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Salida Pydantic mediante with_structured_output.

GUÍA DOCENTE
CUÁNDO USAR: cuando el resultado debe consumirse como datos tipados.
DIFERENCIA: el modelo estructurado devuelve una instancia, no texto libre.
EN CLASE: leer el schema y luego observar el tipo del resultado.
"""

# Importa credenciales, ChatOpenAI y Pydantic.
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define el formato esperado para una cláusula.
class Analisis(BaseModel):
    tema: str
    riesgo: str
    confianza: float = Field(ge=0, le=1)

# Prepara un fragmento contractual breve.
clausula = "El acuerdo se renovará automáticamente por otros doce meses."

if os.getenv("OPENAI_API_KEY"):
    # Activa structured output nativo y ejecuta la extracción.
    modelo = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    modelo_estructurado = modelo.with_structured_output(Analisis, method="json_schema")
    resultado = modelo_estructurado.invoke(f"Analiza esta cláusula: {clausula}")
    print(resultado.model_dump())
else:
    print("Falta OPENAI_API_KEY. Schema preparado:", Analisis.model_json_schema())

# Resumen final: este ejercicio recibe una instancia Pydantic desde el modelo.
# Agrega un campo recomendacion y vuelve a ejecutar.
