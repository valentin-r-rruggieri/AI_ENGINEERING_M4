"""
E04 - Integrador: adaptacion, serving, profiling y async
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Combinar los temas de la clase en una decision de arquitectura completa.
"""

from __future__ import annotations

import asyncio
import cProfile
import io
import os
import pstats
import re
import sys
import time
from pathlib import Path
from typing import Literal, cast

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


AdaptationDecision = Literal["LoRA / PEFT", "Full fine-tuning", "Hybrid"]
ServingDecision = Literal["serverless", "servidor persistente", "hibrido"]


class ProductContext(BaseModel):
    product: str
    traffic: str
    budget: str
    personalization: str
    latency_problem: str
    team_constraint: str


class ArchitecturePlan(BaseModel):
    adaptation: AdaptationDecision
    serving: ServingDecision
    profiling_focus: list[str] = Field(..., min_length=1)
    async_targets: list[str] = Field(..., min_length=1)
    metrics: list[str] = Field(..., min_length=4)
    main_risks: list[str] = Field(..., min_length=2)
    rationale: str


def title(text: str) -> None:
    print("=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print()
    print(f"=== {number}. {text} ===")


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", FIRST_DOC)


def choose_adaptation(context: ProductContext) -> AdaptationDecision:
    if "cliente" in context.personalization.lower() and context.budget == "bajo":
        return "LoRA / PEFT"
    if context.budget == "alto" and "profunda" in context.personalization.lower():
        return "Full fine-tuning"
    return "Hybrid"


def choose_serving(context: ProductContext) -> ServingDecision:
    if "irregular" in context.traffic.lower() and context.budget == "bajo":
        return "serverless"
    if "24/7" in context.traffic.lower() or "tiempo real" in context.latency_problem.lower():
        return "servidor persistente"
    return "hibrido"


def generate_plan_with_llm(context: ProductContext) -> ArchitecturePlan:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos arquitecto de IA. Genera un plan breve, practico y estructurado "
                "para adaptar, servir y optimizar un sistema de resumen en produccion. "
                "Reglas del caso: si hay multiples clientes, presupuesto bajo y GPU compartida, "
                "usa LoRA / PEFT; si el trafico es irregular y el presupuesto es bajo, "
                "usa serverless como decision principal y menciona cold start como riesgo.",
            ),
            ("user", "Contexto del producto: {context}"),
        ]
    )
    chain = ChatOpenAI(model=MODEL_NAME, temperature=0).with_structured_output(ArchitecturePlan)
    return cast(ArchitecturePlan, (prompt | chain).invoke({"context": context.model_dump()}))


def expensive_normalize(text: str) -> int:
    total = 0
    for _ in range(160):
        cleaned = ""
        for char in text:
            if char.isalnum() or char.isspace():
                cleaned += char.lower()
        total += len(cleaned)
    return total


def optimized_normalize(text: str) -> int:
    noise = re.compile(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]+")
    cleaned = noise.sub("", text).lower()
    return len(cleaned) * 160


def profile_step(label: str, func, text: str) -> tuple[int, float]:
    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    result = func(text)
    profiler.disable()
    elapsed = time.perf_counter() - start

    stream = io.StringIO()
    pstats.Stats(profiler, stream=stream).sort_stats("cumtime").print_stats(6)
    print(f"\nPerfil {label}: {elapsed:.3f}s")
    print(stream.getvalue())
    return result, elapsed


async def read_and_write_result(doc_id: str, text: str) -> dict[str, str]:
    # Simula storage remoto: leer, procesar metadata y guardar resultado.
    await asyncio.sleep(0.25)
    await asyncio.sleep(0.25)
    return {"doc_id": doc_id, "status": "stored", "preview": preview(text, 60)}


async def process_io_batch(docs: list[tuple[str, str]]) -> list[dict[str, str]]:
    return await asyncio.gather(*[read_and_write_result(doc_id, text) for doc_id, text in docs])


def main() -> None:
    ensure_data()
    docs = [(path.name, read_text(path)) for path in sorted(DOCS_DIR.glob("doc_*.txt"))[:4]]
    long_text = "\n".join(text for _, text in docs) * 40

    title("AEM4L5 | E04 - Integrador adaptacion + serving")

    section(1, "CONTEXTO DEL PRODUCTO")
    context = ProductContext(
        product="resumen de documentos bajo demanda",
        traffic="muy irregular con picos por campañas",
        budget="bajo",
        personalization="tono y vocabulario por cliente",
        latency_problem="lectura de archivos y escritura de resultados lentas",
        team_constraint="una sola GPU compartida y equipo chico",
    )
    print(context.model_dump_json(indent=2))

    section(2, "DECISION LOCAL EXPLICABLE")
    local_adaptation = choose_adaptation(context)
    local_serving = choose_serving(context)
    print(f"Adaptacion recomendada: {local_adaptation}")
    print(f"Serving recomendado:    {local_serving}")
    print("Motivo: multiples clientes + presupuesto bajo + trafico irregular.")

    section(3, "PLAN ESTRUCTURADO CON OPENAI REAL")
    plan = generate_plan_with_llm(context)
    print(plan.model_dump_json(indent=2))

    section(4, "PROFILING CPU-BOUND")
    slow_result, slow_seconds = profile_step("normalizacion lenta", expensive_normalize, long_text)
    fast_result, fast_seconds = profile_step("normalizacion optimizada", optimized_normalize, long_text)
    print(f"Resultados equivalentes: {slow_result == fast_result}")
    print(f"Speedup CPU: {slow_seconds / fast_seconds:.2f}x")

    section(5, "ASYNC PARA I/O-BOUND")
    start = time.perf_counter()
    io_results = asyncio.run(process_io_batch(docs))
    async_seconds = time.perf_counter() - start
    for result in io_results:
        print(result)
    print(f"I/O batch async: {async_seconds:.2f}s para {len(docs)} documentos")

    section(6, "METRICAS FINALES")
    metrics = {
        "adaptation": local_adaptation,
        "serving": local_serving,
        "cpu_slow_seconds": slow_seconds,
        "cpu_fast_seconds": fast_seconds,
        "cpu_speedup": slow_seconds / fast_seconds,
        "io_async_seconds": async_seconds,
        "documents": len(docs),
        "llm_plan_metrics": plan.metrics,
    }
    print(metrics)

    section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Cambia el trafico a 24/7 y revisa la decision de serving.")
    print("2. Agrega un riesgo de cold start y una mitigacion.")
    print("3. Explica que parte resuelve LoRA, que parte serverless, que parte cProfile y que parte async.")

    trace_text("USER", "Disenia una arquitectura integral para resumen bajo demanda.")
    trace_json("PLAN", plan.model_dump(mode="json"))
    trace_json("METRICS", metrics)


if __name__ == "__main__":
    main()
