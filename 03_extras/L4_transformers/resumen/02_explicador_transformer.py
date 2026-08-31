# Este archivo resume L4 mediante una explicación tipada de una inferencia.
# Lee cada bloque y modifica una variable por vez.

"""Caso 3: traducir métricas de un Transformer a lenguaje claro.

GUÍA DOCENTE
CUÁNDO USAR: para comunicar una inferencia técnica a una persona usuaria.
DIFERENCIA: LangChain explica los resultados; PyTorch hace el cálculo.
EN CLASE: evitar decir que el LLM reemplaza al Transformer.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa la clave, LangChain y Pydantic para la explicación final.
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# Define el contrato para explicar las métricas sin cambiar el cálculo técnico.
class ExplicacionTransformer(BaseModel):
    tokens: int
    forma_atencion: str
    explicacion: str

# Reutiliza métricas que podrían salir de los dos casos anteriores.
metricas = {"tokens": 4, "forma_atencion": "(1, 4, 4)"}

# Usa LangChain para redactar una explicación breve y validada por Pydantic.
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ExplicacionTransformer)
resultado = extractor.invoke(
    "Explica en lenguaje claro estas métricas de Transformer y conserva sus valores: " + str(metricas)
)
# Muestra una salida útil para una interfaz o una explicación docente.
print(resultado.model_dump())

# Resumen final: LangChain comunica la inferencia, no calcula la atención.
# Cambia la cantidad de tokens y actualizá la forma esperada.
