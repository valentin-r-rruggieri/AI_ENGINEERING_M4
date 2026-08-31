# Caso adicional LangChain de L4: tutor para interpretar atención.
"""Salida Pydantic que explica una métrica de self-attention."""
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class ExplicacionAtencion(BaseModel):
    concepto: str
    ejemplo: str
    advertencia: str

forma_atencion = "(1, 3, 3)"
extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ExplicacionAtencion)
resultado = extractor.invoke("Explica self-attention con una matriz de forma " + forma_atencion + " para un estudiante de ingeniería.")
print(resultado.model_dump())
