"""
E01 - Comparador monolitico vs arquitectura de dos agentes
PIM4 | LegalMove

Objetivo pedagogico:
    Comparar un agente que hace todo contra ContextualizationAgent +
    ExtractionAgent, trabajando desde imagenes reales de contrato/adenda.

USE_REAL_API = False:
    Lee imagenes PNG reales y usa textos mock de referencia.
USE_REAL_API = True:
    Usa vision LangChain para leer imagenes y chains para ambos agentes.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import image_to_base64, print_file_evidence, print_section, print_title, read_json, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
CONTRACT_IMG = DATA_DIR / "contrato_original.png"
AMENDMENT_IMG = DATA_DIR / "adenda_simple.png"
EXPECTED_PATH = DATA_DIR / "expected" / "cambio_simple.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", CONTRACT_IMG)


def image_to_text(path: Path) -> str:
    img_b64 = image_to_base64(path)
    if USE_REAL_API:
        from langchain_core.messages import HumanMessage
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model=VISION_MODEL, temperature=0)
        message = HumanMessage(content=[
            {"type": "text", "text": "Extrae el texto visible de este documento legal. No inventes contenido."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
        ])
        return llm.invoke([message]).content
    print(f"  [MOCK] Imagen leida: {path.name} ({len(img_b64) // 1024} KB base64)")
    if path.name == "contrato_original.png":
        return (
            "Clausula 1 payment_terms: monto mensual $1.000. "
            "Clausula 2 duration: duracion 12 meses. "
            "Clausula 3 service_territory: Argentina."
        )
    return "Adenda simple: modifica duration. Nueva duracion 18 meses."


def monolithic_comparison(original: str, amendment: str) -> str:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Compara contrato y adenda. Responde en texto libre que cambio."),
            ("user", "Contrato:\n{original}\n\nAdenda:\n{amendment}"),
        ])
        return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()).invoke({"original": original, "amendment": amendment})
    return "Parece que cambio la duracion del contrato, aunque no queda claro si hay otros ajustes."


def contextualization_agent(original: str, amendment: str) -> str:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Mapea secciones del contrato. No extraigas cambios finales."),
            ("user", "Contrato:\n{original}\n\nAdenda:\n{amendment}"),
        ])
        return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()).invoke({"original": original, "amendment": amendment})
    return "Secciones: payment_terms, duration, service_territory. La adenda toca solo duration."


def extraction_agent(original: str, amendment: str, context_map: str) -> dict[str, Any]:
    if USE_REAL_API:
        from langchain_core.output_parsers import JsonOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Usa el context_map para extraer cambios. Devolve JSON con sections_changed, topics_touched, summary_of_the_change."),
            ("user", "Context map:\n{context_map}\nContrato:\n{original}\nAdenda:\n{amendment}"),
        ])
        return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | JsonOutputParser()).invoke({
            "context_map": context_map,
            "original": original,
            "amendment": amendment,
        })
    return {
        "sections_changed": ["duration"],
        "topics_touched": ["duracion contractual"],
        "summary_of_the_change": "La duracion del contrato se extiende de 12 a 18 meses.",
    }


def score_sections(raw: dict[str, Any] | str, expected: dict[str, Any]) -> str:
    if isinstance(raw, str):
        detected = ["duration"] if "duracion" in raw.lower() else []
    else:
        detected = raw.get("sections_changed", [])
    expected_sections = set(expected["sections_changed"])
    return f"{len(set(detected) & expected_sections)}/{len(expected_sections)}"


def main() -> None:
    ensure_data()
    expected = read_json(EXPECTED_PATH)

    print_title("PIM4 | E01 - Comparador basico vs agentes")

    print_section(1, "CONTEXTO DEL CASO")
    print("LegalMove analiza 50 adendas por semana. Separar mapear de extraer mejora precision y debug.")
    print_file_evidence(CONTRACT_IMG, "Contrato")
    print_file_evidence(AMENDMENT_IMG, "Adenda")
    print_file_evidence(EXPECTED_PATH, "Golden")

    original = image_to_text(CONTRACT_IMG)
    amendment = image_to_text(AMENDMENT_IMG)

    print_section(2, "VERSION BASICA - agente monolitico")
    mono = monolithic_comparison(original, amendment)
    print(f"Output monolitico: {mono}")

    print_section(3, "PROBLEMA DETECTADO")
    print("El monolitico mezcla lectura, contextualizacion y extraccion. Si falla, no sabemos en que etapa.")

    print_section(4, "VERSION MEJORADA - ContextualizationAgent + ExtractionAgent")
    context_map = contextualization_agent(original, amendment)
    raw = extraction_agent(original, amendment, context_map)
    print(f"Context map: {context_map}")
    print(f"Extraccion raw: {json.dumps(raw, ensure_ascii=False, indent=2)}")

    print_section(5, "VALIDACION")
    print(f"Score monolitico vs golden: {score_sections(mono, expected)}")
    print(f"Score dos agentes vs golden: {score_sections(raw, expected)}")
    print(f"Golden esperado: {expected}")

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: un prompt grande, texto libre y poca trazabilidad.")
    print("DESPUES: mapa de contexto -> extraccion enfocada -> salida comparable con golden.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Usa adenda_compleja.png y compara 3 cambios.")
    print("2. Decide cuando ContextualizationAgent no hace falta.")
    print("3. Convierte el raw dict en ContractChangeOutput validado.")


if __name__ == "__main__":
    main()
