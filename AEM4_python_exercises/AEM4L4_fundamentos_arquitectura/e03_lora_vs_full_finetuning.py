"""
E03 - LoRA vs Full Fine-Tuning con ADR estructurado
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Comparar storage/costo entre full fine-tuning y LoRA, y convertir la
    decision en un Architecture Decision Record validado.

USE_REAL_API = False:
    Lee perfiles reales y devuelve ADRs mock calibrados.
USE_REAL_API = True:
    Usa LangChain structured output para generar ADRs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_json, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
PROFILES_PATH = DATA_DIR / "perfiles_uso.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", PROFILES_PATH)


class ArchitectureDecisionRecord(BaseModel):
    title: str
    context: str
    decision: Literal["LoRA", "Full Fine-Tuning", "Hybrid"]
    rationale: str = Field(..., min_length=30)
    consequences_positive: list[str] = Field(..., min_length=1)
    consequences_negative: list[str] = Field(..., min_length=1)


def storage_full_ft(model_gb: float, clients: int) -> float:
    return model_gb * clients


def storage_lora(model_gb: float, adapter_gb: float, clients: int) -> float:
    return model_gb + adapter_gb * clients


def decide_profile(profile: dict) -> str:
    if len(profile["dominios"]) == 1 and profile["presupuesto"] == "alto" and profile["trafico"] == "estable_alto":
        return "Full Fine-Tuning"
    if profile["trafico"] == "picos" and profile["presupuesto"] == "alto":
        return "Hybrid"
    return "LoRA"


def generate_adr(profile: dict) -> ArchitectureDecisionRecord:
    if USE_REAL_API:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Sos arquitecto ML. Genera un ADR breve y estructurado para adaptar un LLM."),
            ("user", "Perfil: {profile}"),
        ])
        chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0).with_structured_output(ArchitectureDecisionRecord)
        return chain.invoke({"profile": profile})
    decision = decide_profile(profile)
    return ArchitectureDecisionRecord(
        title=f"Adaptacion de modelo para {profile['cliente']}",
        context=f"Dominios={profile['dominios']}, presupuesto={profile['presupuesto']}, trafico={profile['trafico']}.",
        decision=decision,
        rationale=f"Se elige {decision} porque balancea costo, aislamiento por cliente y velocidad de iteracion para este perfil concreto.",
        consequences_positive=["Decision explicita y reproducible", "Costo estimable antes de entrenar"],
        consequences_negative=["Puede requerir reevaluacion si cambia el trafico", "La calidad debe medirse con dataset propio"],
    )


def main() -> None:
    ensure_data()
    profiles = read_json(PROFILES_PATH)

    print_title("AEM4L4 | E03 - LoRA vs Full Fine-Tuning")

    print_section(1, "CONTEXTO DEL CASO")
    print("Una plataforma necesita adaptar un modelo para varios clientes y dominios.")
    print_file_evidence(PROFILES_PATH, "Perfiles")

    print_section(2, "VERSION BASICA - elegir Full FT para todos")
    model_gb = 14.0
    adapter_gb = 0.33
    clients = 50
    print(f"Full FT: {clients} clientes x {model_gb} GB = {storage_full_ft(model_gb, clients):.1f} GB")
    print("La decision parece simple, pero duplica el modelo completo por cliente.")

    print_section(3, "PROBLEMA DETECTADO")
    print("Full FT entrena todos los parametros, requiere mas GPU, mas storage y aumenta riesgo de catastrophic forgetting.")
    print("Para muchos clientes, el costo operativo escala linealmente con copias completas.")

    print_section(4, "VERSION MEJORADA - LoRA + ADR")
    print(f"LoRA: modelo base {model_gb} GB + {clients} adapters x {adapter_gb} GB = {storage_lora(model_gb, adapter_gb, clients):.1f} GB")
    print("Tabla de decision: un dominio + alto presupuesto -> Full FT; multi-cliente o bajo presupuesto -> LoRA; picos + calidad -> Hybrid.")
    for profile in profiles:
        adr = generate_adr(profile)
        print(f"\nADR - {profile['cliente']}")
        print(f"  Decision: {adr.decision}")
        print(f"  Contexto: {adr.context}")
        print(f"  Rationale: {adr.rationale}")

    print_section(5, "VALIDACION")
    try:
        ArchitectureDecisionRecord(
            title="ADR malo",
            context="sin contexto",
            decision="Prompting",
            rationale="corto",
            consequences_positive=[],
            consequences_negative=[],
        )
    except ValidationError as exc:
        print("Pydantic rechaza decision fuera de Literal y rationale corto:")
        print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: decision a dedo, storage alto y trade-offs invisibles.")
    print("DESPUES: calculo LoRA vs Full FT + ADR con contexto, decision y consecuencias.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega un perfil hibrido con picos de trafico y varios dominios.")
    print("2. Agrega costo_estimado_gpu_hours al schema.")
    print("3. Defende cuando Full FT sigue siendo razonable.")


if __name__ == "__main__":
    main()
