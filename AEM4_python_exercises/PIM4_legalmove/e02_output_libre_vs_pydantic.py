"""
E02 - Output libre vs ContractChangeOutput con Pydantic
PIM4 | LegalMove

Objetivo pedagogico:
    Mostrar que el ExtractionAgent puede devolver formatos inconsistentes y
    que ContractChangeOutput es la ultima linea de defensa.

USE_REAL_API = False:
    Lee golden JSON real y devuelve mock valido.
USE_REAL_API = True:
    Usa LangChain with_structured_output(ContractChangeOutput).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_json, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
CONTRACT_IMG = DATA_DIR / "contrato_original.png"
EXPECTED_PATH = DATA_DIR / "expected" / "cambio_complejo.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", CONTRACT_IMG)


class ContractChangeOutput(BaseModel):
    sections_changed: List[str]
    topics_touched: List[str]
    summary_of_the_change: str = Field(..., min_length=10)

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def non_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("La lista no puede estar vacia")
        return value


def agent_free_text_output() -> str:
    return "Cambio el precio, tambien la duracion y creo que el territorio, pero no se en que campos guardarlo."


def structured_extraction(expected: dict) -> ContractChangeOutput:
    if USE_REAL_API:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Extrae cambios contractuales con el schema indicado."),
            ("user", "Caso complejo LegalMove. Devolve los tres campos requeridos."),
        ])
        chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0).with_structured_output(ContractChangeOutput)
        return cast(ContractChangeOutput, chain.invoke({}))
    print("  [MOCK] Simulando structured output de LangChain...")
    return ContractChangeOutput(**expected)


def main() -> None:
    ensure_data()
    expected = read_json(EXPECTED_PATH)

    print_title("PIM4 | E02 - Output libre vs Pydantic")

    print_section(1, "CONTEXTO DEL CASO")
    print("El backend legal necesita tres campos confiables: secciones, temas y resumen.")
    print_file_evidence(EXPECTED_PATH, "Golden complejo")

    print_section(2, "VERSION BASICA - output libre")
    free = agent_free_text_output()
    print(f"Texto libre: {free}")
    print("No se sabe cuantas secciones son, ni si los nombres coinciden con el sistema.")

    print_section(3, "PROBLEMA DETECTADO")
    print("El LLM puede devolver string en vez de lista, summary vacio o campos faltantes.")

    print_section(4, "VERSION MEJORADA - ContractChangeOutput + structured output")
    structured = structured_extraction(expected)
    print(structured)

    print_section(5, "VALIDACION")
    cases = [
        ("valido", expected),
        ("sections vacia", {**expected, "sections_changed": []}),
        ("summary corto", {**expected, "summary_of_the_change": "corto"}),
        ("sections string", {**expected, "sections_changed": "payment_terms"}),
    ]
    for name, payload in cases:
        try:
            obj = ContractChangeOutput(**payload)
            print(f"  {name}: OK -> {obj.sections_changed}")
        except ValidationError as exc:
            print(f"  {name}: ValidationError")
            print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: texto libre no indexable y formatos variables.")
    print("DESPUES: tres campos tipados, validaciones de negocio y errores accionables.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Rechaza el caso complejo si falta alguna de las tres secciones esperadas.")
    print("2. Normaliza 'duracion' a 'duration'.")
    print("3. Agrega severity por cada cambio.")


if __name__ == "__main__":
    main()
