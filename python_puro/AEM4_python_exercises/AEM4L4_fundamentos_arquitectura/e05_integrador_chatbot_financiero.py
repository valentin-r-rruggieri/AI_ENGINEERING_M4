"""
E05 - Integrador: chatbot financiero con arquitectura, tokens y LoRA
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Combinar self-attention, tokenizacion, budget de contexto, LoRA y ADR
    en una decision de arquitectura realista para un chatbot financiero.
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
CASE_PATH = DATA_DIR / "chatbot_financiero.json"
Adaptation = Literal["LoRA", "Full Fine-Tuning", "Prompting", "Hybrid"]


class FinancialArchitectureDecision(BaseModel):
    model_strategy: str
    tokenizer_strategy: str
    adaptation: Adaptation
    context_limit_tokens: int = Field(..., gt=0)
    latency_controls: list[str] = Field(..., min_length=1)
    risks: list[str] = Field(..., min_length=1)
    rationale: str = Field(..., min_length=40)


def title(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * 78)


def ensure_data() -> None:
    if CASE_PATH.exists():
        return
    subprocess.run([sys.executable, str(DATA_DIR / "generate_data.py")], check=True)


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Copia python_puro/AEM4_python_exercises/.env.example "
            "a .env y completa tu API key antes de ejecutar este ejercicio."
        )


def attention_pairs(tokens: int) -> int:
    return tokens * tokens


def estimate_tokens(text: str) -> int:
    return max(1, int(len(text.split()) * 1.35))


def decide_with_openai(case: dict, estimated_tokens: int) -> FinancialArchitectureDecision:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos arquitecto de IA. Disena una decision concreta para un chatbot financiero. "
                "Respeta el schema y justifica costo, latencia, tokenizacion y adaptacion.",
            ),
            ("user", "Caso: {case}\nTokens estimados del contexto inicial: {estimated_tokens}"),
        ]
    )
    chain = prompt | ChatOpenAI(model=model_name, temperature=0).with_structured_output(FinancialArchitectureDecision)
    return cast(FinancialArchitectureDecision, chain.invoke({"case": case, "estimated_tokens": estimated_tokens}))


def main() -> None:
    load_dotenv()
    ensure_data()
    require_openai_api_key()
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    context = "\n".join(case["sample_context"])
    estimated_tokens = estimate_tokens(context)

    title("AEM4L4 | E05 - Integrador chatbot financiero")

    section(1, "Contexto")
    print(json.dumps(case, ensure_ascii=False, indent=2))

    section(2, "Budget tecnico antes de llamar al modelo")
    print(f"Tokens estimados del contexto: {estimated_tokens}")
    print(f"Pares de attention aproximados: {attention_pairs(estimated_tokens)}")
    print(f"SLA: {case['latency_sla_ms']} ms")

    section(3, "Decision estructurada con OpenAI")
    decision = decide_with_openai(case, estimated_tokens)
    print(json.dumps(decision.model_dump(mode="json"), ensure_ascii=False, indent=2))

    section(4, "Checklist docente")
    print("1. Self-attention justifica usar Transformer para dependencias largas.")
    print("2. Tokenizacion robusta evita perder jerga regulatoria.")
    print("3. LoRA adapta dominio sin duplicar el modelo completo.")
    print("4. Control de contexto protege costo y latencia.")

    section(5, "Desafio")
    print("Cambia el SLA a 2000 ms y revisa que decision arquitectonica se vuelve posible.")


if __name__ == "__main__":
    main()
