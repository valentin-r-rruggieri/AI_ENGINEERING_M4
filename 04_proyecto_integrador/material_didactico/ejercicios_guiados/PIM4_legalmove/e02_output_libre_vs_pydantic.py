"""E02 - Output libre vs ContractChangeOutput con Pydantic.

Este ejercicio muestra por que un texto convincente no alcanza para produccion:
el resultado final debe cumplir un contrato de datos estable.
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from legalmove_core import (
    ContractChangeOutput,
    DATA_DIR,
    ExtractionAgent,
    load_expected,
    parse_contract_image,
    print_json,
    print_section,
    print_title,
    validate_contract_change_output,
)


CONTRACT_IMG = DATA_DIR / "contrato_original.png"
AMENDMENT_IMG = DATA_DIR / "adenda_compleja.png"


def agent_free_text_output() -> str:
    return (
        "Cambio el precio, tambien la duracion y el territorio. "
        "Sirve para leerlo, pero no para integrarlo a un sistema."
    )


def run_validation_cases(expected: dict) -> list[dict]:
    cases = [
        ("valido", expected),
        ("sections vacia", {**expected, "sections_changed": []}),
        ("summary corto", {**expected, "summary_of_the_change": "corto"}),
        ("sections string", {**expected, "sections_changed": "payment_terms"}),
        ("falta topics", {k: v for k, v in expected.items() if k != "topics_touched"}),
    ]
    results = []
    for name, payload in cases:
        try:
            obj = ContractChangeOutput.model_validate(payload)
            results.append({"case": name, "ok": True, "sections_changed": obj.sections_changed})
        except ValidationError as exc:
            results.append({"case": name, "ok": False, "error": str(exc).splitlines()[0]})
    return results


def run() -> None:
    expected = load_expected("cambio_complejo")

    print_title("PIM4 | E02 - Output libre vs Pydantic")

    print_section(1, "Contexto del caso")
    print("Caso complejo: una adenda modifica precio, duracion y territorio.")
    print(f"Contrato: {CONTRACT_IMG}")
    print(f"Adenda  : {AMENDMENT_IMG}")

    print_section(2, "Version basica - texto libre")
    free_text = agent_free_text_output()
    print(free_text)
    print("Problema: no hay tipos, campos obligatorios ni forma estable para downstream.")

    print_section(3, "Version mejorada - ContractChangeOutput")
    original_text = parse_contract_image(CONTRACT_IMG, "Contrato original")
    amendment_text = parse_contract_image(AMENDMENT_IMG, "Adenda compleja")
    result = ExtractionAgent().run(
        original_text=original_text,
        amendment_text=amendment_text,
        context_map="Mapa contextual: payment_terms, duration, service_territory.",
    )
    print_json("Output validado", result)

    print_section(4, "Casos de validacion")
    print_json("Resultados", run_validation_cases(expected))

    print_section(5, "Error controlado - JSON invalido para el schema")
    invalid_payload = {
        "sections_changed": "duration",
        "topics_touched": ["duracion contractual"],
        "summary_of_the_change": "Se extiende la duracion.",
    }
    try:
        validate_contract_change_output(invalid_payload)
    except ValueError as exc:
        print(str(exc).splitlines()[0])

    print_section(6, "Idea para explicar en clase")
    print("Pydantic valida forma, no verdad legal. Por eso se combina con golden cases.")


def main() -> None:
    load_dotenv(Path(__file__).with_name(".env"))
    run()


if __name__ == "__main__":
    main()
