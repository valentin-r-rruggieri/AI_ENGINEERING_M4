# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""LegalMove multimodal con dos agentes PydanticAI.

GUÍA DOCENTE
CUÁNDO USAR: como referencia tipada del proyecto integrador M4.
DIFERENCIA: BinaryContent lleva imágenes y output_type garantiza el contrato final.
EN CLASE: seguir imágenes, contextualizador, extractor y salida validada.
"""

# Importa os, rutas, agentes, contenido binario y Pydantic.
import os
from pathlib import Path
from pydantic_ai import Agent, BinaryContent
from pydantic import BaseModel, ConfigDict, Field

# Define el contrato idéntico al de LangChain y LangGraph.
class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resumen_ejecutivo: str = Field(min_length=10)
    cambios_detectados: list[str] = Field(min_length=1)
    riesgos_legales: list[str]

# Localiza las imágenes del proyecto integrador.
raiz = Path(__file__).resolve().parents[4]
original = raiz / "proyecto_integrador/PIM4_legalmove/data/test_contracts/caso_simple/contrato_original.png"
adenda = raiz / "proyecto_integrador/PIM4_legalmove/data/test_contracts/caso_simple/adenda.png"

if os.getenv("OPENAI_API_KEY"):
    # Crea los dos roles especializados después de validar la clave.
    contextualizador = Agent(
        "openai:gpt-4.1-mini",
        name="contextualizador",
        instructions="Transcribe y mapea estructura y tema. No listes cambios.",
    )
    extractor = Agent(
        "openai:gpt-4.1-mini",
        name="extractor",
        output_type=ContractChangeOutput,
        instructions="Usa el mapa para extraer cambios y riesgos sin inventar.",
    )

    # El primer agente observa ambas imágenes y construye un mapa textual.
    contexto = contextualizador.run_sync([
        "Compara la estructura de contrato original y adenda.",
        BinaryContent(data=original.read_bytes(), media_type="image/png"),
        BinaryContent(data=adenda.read_bytes(), media_type="image/png"),
    ])

    # El segundo agente convierte el mapa en la salida común.
    resultado = extractor.run_sync(f"Mapa del contextualizador:\n{contexto.output}")
    salida = resultado.output
else:
    # Mantiene una demostración local del contrato de salida.
    salida = ContractChangeOutput(
        resumen_ejecutivo="La adenda amplía el plazo e incorpora una nueva penalidad.",
        cambios_detectados=["El plazo aumenta de 12 a 18 meses."],
        riesgos_legales=["La penalidad se aplica sin período de gracia."],
    )

print(salida.model_dump_json(indent=2))

# Resumen final: este pipeline combina imágenes, dos agentes y validación estricta.
# Cambia adenda_simple por adenda_compleja y compara los riesgos detectados.
