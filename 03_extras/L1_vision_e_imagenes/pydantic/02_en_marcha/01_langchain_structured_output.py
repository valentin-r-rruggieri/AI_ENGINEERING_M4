# Este archivo forma parte del recorrido práctico de Pydantic con LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Salida estructurada: LangChain invoca el modelo y Pydantic valida el resultado.

GUÍA DOCENTE
CUÁNDO USAR: cuando la respuesta de un LLM será consumida por otra parte del sistema.
DIFERENCIA: texto libre puede variar; un schema Pydantic mantiene campos y tipos.
EN CLASE: explicar el modelo Pydantic antes de llamar a with_structured_output.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar que la clave de OpenAI esté configurada.
import os

# Importa el wrapper LangChain y el contrato de datos Pydantic.
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Define la estructura mínima que debe producir el modelo.
class ResumenContrato(BaseModel):
    tema: str
    riesgo: str
    confianza: float = Field(ge=0, le=1)


# Prepara un texto pequeño y fácil de discutir durante la clase.
texto = "La adenda aumenta el monto mensual de USD 1.000 a USD 1.500."

# Envuelve ChatOpenAI con el schema para recibir un objeto Pydantic validado.
modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)
extractor = modelo.with_structured_output(ResumenContrato, method="json_schema")
resultado = extractor.invoke(f"Analizá este texto contractual: {texto}")
print(resultado.model_dump())
# Resumen final: LangChain entrega la respuesta y Pydantic protege su estructura.
# Agregá un campo obligatorio y observá cómo cambia el contrato del modelo.
