"""
E01 - Serverless vs servidor persistente con servicio de resumen
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Medir cold start vs warm requests y decidir infraestructura con evidencia.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import preview, read_text, require_openai_api_key, run_generator, trace_json, trace_text

load_dotenv()
require_openai_api_key()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
DOCS_DIR = DATA_DIR / "documentos"
FIRST_DOC = DOCS_DIR / "doc_01.txt"
COLD_START_S = 0.7
_MODEL_LOADED = False


class SummaryResponse(BaseModel):
    doc_id: str
    summary: str = Field(..., min_length=15)
    cold_start: bool
    latency_ms: float = Field(..., ge=0)


def title(text: str) -> None:
    print("=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print()
    print(f"=== {number}. {text} ===")


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", FIRST_DOC)


def summarize_text(text: str) -> str:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Resumi el documento en una o dos oraciones accionables. "
                "Menciona el problema y la prioridad si aparece.",
            ),
            ("user", "{texto}"),
        ]
    )
    chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()
    return chain.invoke({"texto": text[:1200]})


def summarize_service(doc_id: str, text: str) -> SummaryResponse:
    global _MODEL_LOADED
    cold = not _MODEL_LOADED
    start = time.perf_counter()
    if cold:
        # Simula carga de runtime, dependencias, modelo base y adapter.
        time.sleep(COLD_START_S)
        _MODEL_LOADED = True
    summary = summarize_text(text)
    latency_ms = (time.perf_counter() - start) * 1000
    return SummaryResponse(doc_id=doc_id, summary=summary, cold_start=cold, latency_ms=latency_ms)


def choose_deployment(requests_per_day: int, latency_sla_ms: int, irregular: bool, model_large: bool) -> str:
    if latency_sla_ms <= 150 or (requests_per_day > 20_000 and not irregular):
        return "servidor persistente"
    if irregular and model_large:
        return "hibrido: minimo caliente + escala bajo demanda"
    if irregular:
        return "serverless"
    return "contenedor/servidor simple segun costo"


def main() -> None:
    ensure_data()
    docs = sorted(DOCS_DIR.glob("doc_*.txt"))[:4]

    title("AEM4L5 | E01 - Serverless vs servidor persistente")

    section(1, "CONTEXTO DEL CASO")
    print("Un servicio de resumen atiende documentos con trafico irregular.")
    print(f"Modelo OpenAI: {MODEL_NAME}")
    print(f"Documento ejemplo: {FIRST_DOC.name} | {preview(read_text(FIRST_DOC), 100)}")
    print(f"Documentos usados en la demo: {len(docs)}")

    section(2, "VERSION BASICA - asumir latencia plana")
    flat_latency_ms = 350
    for doc in docs:
        print(f"{doc.name}: latencia asumida {flat_latency_ms} ms")

    section(3, "PROBLEMA DETECTADO")
    print("El promedio plano oculta el cold start.")
    print("En serverless, la primera llamada puede cargar runtime, dependencias, modelo y adapter.")

    section(4, "VERSION MEJORADA - medir cold/warm")
    responses = [summarize_service(doc.name, read_text(doc)) for doc in docs]
    for response in responses:
        state = "cold" if response.cold_start else "warm"
        print(f"{response.doc_id:10} {state:5} {response.latency_ms:8.0f} ms | {response.summary}")

    section(5, "DECISION DE ARQUITECTURA")
    scenarios = [
        ("batch ocasional", 40, 2500, True, False),
        ("chatbot realtime", 80_000, 100, False, True),
        ("picos impredecibles", 12_000, 1800, True, False),
        ("modelo grande con picos", 6_000, 900, True, True),
    ]
    for name, requests, sla, irregular, large in scenarios:
        decision = choose_deployment(requests, sla, irregular, large)
        print(f"{name:22} -> {decision}")

    section(6, "VALIDACION")
    cold_ms = responses[0].latency_ms
    warm_min_ms = min(response.latency_ms for response in responses[1:])
    print(f"Cold={cold_ms:.0f} ms | warm minimo={warm_min_ms:.0f} ms | cold>warm={cold_ms > warm_min_ms}")
    print("Regla docente: serverless sirve si el costo ocioso importa mas que el cold start.")

    section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Cambia COLD_START_S y revisa la decision.")
    print("2. Agrega un escenario con SLA menor a 100 ms.")
    print("3. Explica cuando conviene una arquitectura hibrida.")

    trace_text("USER", "Resumi documentos y medi latencia cold/warm del servicio.")
    trace_json("RESULT", [response.model_dump(mode="json") for response in responses])
    trace_json(
        "METRICS",
        {
            "cold_ms": cold_ms,
            "warm_min_ms": warm_min_ms,
            "cold_gt_warm": cold_ms > warm_min_ms,
        },
    )


if __name__ == "__main__":
    main()
