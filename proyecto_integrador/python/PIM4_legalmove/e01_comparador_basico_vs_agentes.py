"""E01 - Comparador monolitico vs arquitectura de dos agentes.

La clase arranca con una idea simple: comparar texto original contra adenda.
Despues separa responsabilidades en ContextualizationAgent y ExtractionAgent,
que es exactamente lo que pide la rubrica del PIM4.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from legalmove_core import (
    DATA_DIR,
    ContextualizationAgent,
    ExtractionAgent,
    load_expected,
    parse_contract_image,
    print_json,
    print_section,
    print_title,
    score_sections,
)


CONTRACT_IMG = DATA_DIR / "contrato_original.png"
AMENDMENT_IMG = DATA_DIR / "adenda_simple.png"


def monolithic_comparison(original_text: str, amendment_text: str) -> str:
    """Version fragil: un solo paso mezcla lectura, contexto y extraccion."""
    _ = original_text
    _ = amendment_text
    return (
        "Parece que cambio la duracion del contrato. "
        "La respuesta es util para una persona, pero no es un dato validado."
    )


def run(use_real_api: bool = False) -> None:
    expected = load_expected("cambio_simple")

    print_title("PIM4 | E01 - Comparador basico vs dos agentes")

    print_section(1, "Contexto del caso")
    print("Caso simple: contrato original + adenda que modifica la duracion.")
    print(f"Contrato: {CONTRACT_IMG}")
    print(f"Adenda  : {AMENDMENT_IMG}")

    original_text = parse_contract_image(CONTRACT_IMG, "Contrato original", use_real_api=use_real_api)
    amendment_text = parse_contract_image(AMENDMENT_IMG, "Adenda simple", use_real_api=use_real_api)

    print_section(2, "Version basica - prompt monolitico")
    monolithic = monolithic_comparison(original_text, amendment_text)
    print(monolithic)
    print(f"Score contra golden: {score_sections(monolithic, expected)}")

    print_section(3, "Problema detectado")
    print("El output monolitico no deja claro que etapa fallo si el resultado es incorrecto.")
    print("Tampoco produce un JSON que un backend pueda procesar directamente.")

    print_section(4, "Version mejorada - dos agentes")
    context_map = ContextualizationAgent(use_real_api=use_real_api).run(original_text, amendment_text)
    result = ExtractionAgent(use_real_api=use_real_api).run(original_text, amendment_text, context_map)
    print(context_map)
    print_json("ContractChangeOutput validado", result)
    print(f"Score contra golden: {score_sections(result, expected)}")

    print_section(5, "Idea para explicar en clase")
    print("Primero leemos, despues ordenamos contexto y recien al final extraemos cambios.")
    print("Separar esos pasos baja alucinaciones y vuelve auditable el pipeline.")


def main() -> None:
    load_dotenv(Path(__file__).with_name(".env"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--real-api",
        action="store_true",
        default=os.getenv("PIM4_USE_REAL_API") == "1",
        help="Usa OpenAI Vision/LLM real. Por defecto corre con mocks deterministas.",
    )
    args = parser.parse_args()
    run(use_real_api=args.real_api)


if __name__ == "__main__":
    main()
