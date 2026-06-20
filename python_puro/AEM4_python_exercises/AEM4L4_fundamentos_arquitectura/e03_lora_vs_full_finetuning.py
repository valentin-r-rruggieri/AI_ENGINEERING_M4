"""
E03 - LoRA vs Full Fine-Tuning con ADR estructurado
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Comparar almacenamiento, costo operativo y riesgo entre full fine-tuning
    y LoRA; luego pedir a OpenAI un ADR validado con Pydantic.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field


DATA_DIR = Path(__file__).parent / "data"
PROFILES_PATH = DATA_DIR / "perfiles_uso.json"
Decision = Literal["LoRA", "Full Fine-Tuning", "Hybrid"]


class ArchitectureDecisionRecord(BaseModel):
    title: str
    context: str
    decision: Decision
    rationale: str = Field(..., min_length=30)
    consequences_positive: list[str] = Field(..., min_length=1)
    consequences_negative: list[str] = Field(..., min_length=1)


def title(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * 78)


def ensure_data() -> None:
    if PROFILES_PATH.exists():
        return
    subprocess.run([sys.executable, str(DATA_DIR / "generate_data.py")], check=True)


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Copia python_puro/AEM4_python_exercises/.env.example "
            "a .env y completa tu API key antes de ejecutar este ejercicio."
        )


def storage_full_ft(model_gb: float, clients: int) -> float:
    return model_gb * clients


def storage_lora(model_gb: float, adapter_gb: float, clients: int) -> float:
    return model_gb + adapter_gb * clients


def generate_adr(profile: dict) -> ArchitectureDecisionRecord:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos arquitecto ML. Genera un ADR breve en espanol para adaptar un LLM. "
                "La decision debe ser exactamente LoRA, Full Fine-Tuning o Hybrid.",
            ),
            ("user", "Perfil: {profile}"),
        ]
    )
    chain = prompt | ChatOpenAI(model=model_name, temperature=0).with_structured_output(ArchitectureDecisionRecord)
    return cast(ArchitectureDecisionRecord, chain.invoke({"profile": profile}))


def main() -> None:
    load_dotenv()
    ensure_data()
    require_openai_api_key()
    profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))

    title("AEM4L4 | E03 - LoRA vs Full Fine-Tuning")

    section(1, "Contexto")
    print("Una plataforma multi-cliente necesita adaptar un modelo a dominios diferentes.")
    print(f"Perfiles disponibles: {[profile['cliente'] for profile in profiles]}")

    section(2, "Costo de storage")
    model_gb = 14.0
    adapter_gb = 0.33
    clients = 50
    print(f"Full FT: {clients} x {model_gb} GB = {storage_full_ft(model_gb, clients):.1f} GB")
    print(f"LoRA   : base {model_gb} GB + {clients} x {adapter_gb} GB = {storage_lora(model_gb, adapter_gb, clients):.1f} GB")
    print("Diferencia:", f"{storage_full_ft(model_gb, clients) - storage_lora(model_gb, adapter_gb, clients):.1f} GB")

    section(3, "OpenAI genera ADRs")
    adrs = [generate_adr(profile) for profile in profiles]
    for profile, adr in zip(profiles, adrs):
        print(f"\nCliente: {profile['cliente']}")
        print(json.dumps(adr.model_dump(mode="json"), ensure_ascii=False, indent=2))

    section(4, "Interpretacion")
    print("Full fine-tuning modifica todos los parametros y puede ser razonable con mucho dato y presupuesto.")
    print("LoRA congela la base y entrena adapters chicos: ideal para dominios y clientes multiples.")

    section(5, "Desafio")
    print("Agrega costo_estimado_gpu_hours al ADR y defende cuando usarias Hybrid.")


if __name__ == "__main__":
    main()
