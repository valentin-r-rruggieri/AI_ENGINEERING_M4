"""E03 - Pipeline completo con trazabilidad local y Langfuse opcional.

Sin spans, un fallo dice poco. Con una traza por etapa podemos explicar si el
problema estuvo en vision, contextualizacion, extraccion o validacion.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from legalmove_core import (
    DATA_DIR,
    Trace,
    load_expected,
    parse_contract_image,
    print_json,
    print_section,
    print_title,
    run_pipeline,
    score_sections,
    validate_contract_change_output,
)


CONTRACT_IMG = DATA_DIR / "contrato_original.png"
AMENDMENT_IMG = DATA_DIR / "adenda_compleja.png"


def blind_pipeline() -> None:
    try:
        original = parse_contract_image(CONTRACT_IMG, "Contrato original")
        amendment = parse_contract_image(AMENDMENT_IMG, "Adenda compleja")
        _ = original, amendment
        validate_contract_change_output(
            {
                "sections_changed": ["payment_terms"],
                "topics_touched": ["monto mensual"],
                "summary_of_the_change": "corto",
            }
        )
        print("Pipeline OK")
    except Exception:
        print("fallo")


def traced_validation_error() -> Trace:
    trace = Trace(name="contract-analysis", contract_id="validation-error-demo")
    try:
        invalid_payload = trace.run_span(
            "extraction_agent",
            "context_map + texts",
            lambda: {
                "sections_changed": ["payment_terms"],
                "topics_touched": ["monto mensual"],
                "summary_of_the_change": "corto",
            },
            metadata={"agent": "ExtractionAgent", "demo": "payload incompleto"},
        )
        trace.run_span(
            "pydantic_validation",
            json.dumps(invalid_payload, ensure_ascii=False),
            lambda: validate_contract_change_output(invalid_payload),
            metadata={"schema": "ContractChangeOutput"},
        )
        trace.success = True
    except Exception:
        trace.success = False
    return trace


def run(use_real_api: bool = False, use_langfuse: bool = False) -> None:
    expected = load_expected("cambio_complejo")

    print_title("PIM4 | E03 - Pipeline completo con trazabilidad")

    print_section(1, "Contexto del caso")
    print("Caso complejo: el sistema debe leer imagenes, coordinar agentes y validar JSON.")
    print(f"Contrato: {CONTRACT_IMG}")
    print(f"Adenda  : {AMENDMENT_IMG}")

    print_section(2, "Version basica - sin logs")
    blind_pipeline()
    print("Con solo 'fallo' no sabemos que etapa produjo el problema.")

    print_section(3, "Version mejorada - trace por spans")
    result = run_pipeline(
        CONTRACT_IMG,
        AMENDMENT_IMG,
        use_real_api=use_real_api,
        use_langfuse=use_langfuse,
    )
    result.trace.print_tree()

    print_section(4, "Salida final validada")
    print_json("ContractChangeOutput", result.output)
    print(f"Score contra golden complejo: {score_sections(result.output, expected)}")

    print_section(5, "Fallo controlado con traza")
    bad_trace = traced_validation_error()
    bad_trace.print_tree()

    print_section(6, "Idea para explicar en clase")
    print("Langfuse o una traza local convierten una demo opaca en una demo auditable.")


def main() -> None:
    load_dotenv(Path(__file__).with_name(".env"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--real-api",
        action="store_true",
        default=os.getenv("PIM4_USE_REAL_API") == "1",
        help="Usa OpenAI real para vision/agentes. Por defecto usa mocks deterministas.",
    )
    parser.add_argument(
        "--langfuse",
        action="store_true",
        default=os.getenv("PIM4_USE_LANGFUSE") == "1",
        help="Envia la traza a Langfuse si hay credenciales configuradas.",
    )
    args = parser.parse_args()
    run(use_real_api=args.real_api, use_langfuse=args.langfuse)


if __name__ == "__main__":
    main()
