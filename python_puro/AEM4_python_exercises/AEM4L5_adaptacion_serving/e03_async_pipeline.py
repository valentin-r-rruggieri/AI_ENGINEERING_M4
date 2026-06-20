"""
E03 - Pipeline async con LangChain abatch
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Mostrar que N llamadas I/O-bound al LLM no deberian ejecutarse en serie.
"""

from __future__ import annotations

import asyncio
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


class AsyncSummary(BaseModel):
    doc_id: str
    summary: str = Field(..., min_length=12)


def title(text: str) -> None:
    print("=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print()
    print(f"=== {number}. {text} ===")


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", FIRST_DOC)


def build_chain():
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Resumi breve en una frase accionable."),
            ("user", "{texto}"),
        ]
    )
    return prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()


def summarize_sequential(docs: list[tuple[str, str]]) -> list[AsyncSummary]:
    chain = build_chain()
    results: list[AsyncSummary] = []
    for doc_id, text in docs:
        summary = chain.invoke({"texto": text})
        results.append(AsyncSummary(doc_id=doc_id, summary=summary))
    return results


async def summarize_async(docs: list[tuple[str, str]]) -> list[AsyncSummary]:
    chain = build_chain()
    raw_results = await chain.abatch([{"texto": text} for _, text in docs])
    return [
        AsyncSummary(doc_id=doc_id, summary=summary)
        for (doc_id, _), summary in zip(docs, raw_results)
    ]


def classify_stage(stage_name: str, waits_external_resource: bool, heavy_local_compute: bool) -> str:
    if heavy_local_compute:
        return f"{stage_name}: CPU/GPU-bound -> perfilar, optimizar, vectorizar o paralelizar"
    if waits_external_resource:
        return f"{stage_name}: I/O-bound -> async, batching y limites de concurrencia"
    return f"{stage_name}: revisar con medicion real"


def main() -> None:
    ensure_data()
    docs = [(path.name, read_text(path)) for path in sorted(DOCS_DIR.glob("doc_*.txt"))[:4]]

    title("AEM4L5 | E03 - Async pipeline con OpenAI real")

    section(1, "CONTEXTO DEL CASO")
    print("Hay que resumir varios documentos. Cada llamada al LLM espera red: es I/O-bound.")
    print(f"Modelo OpenAI: {MODEL_NAME}")
    print(f"Documento ejemplo: {FIRST_DOC.name} | {preview(read_text(FIRST_DOC), 100)}")
    print(f"Documentos usados: {len(docs)}")

    section(2, "VERSION BASICA - secuencial")
    start = time.perf_counter()
    sequential_results = summarize_sequential(docs)
    sequential_seconds = time.perf_counter() - start
    for result in sequential_results:
        print(f"{result.doc_id}: {result.summary}")
    print(f"Tiempo secuencial: {sequential_seconds:.2f}s")

    section(3, "PROBLEMA DETECTADO")
    print("Si cada request espera red, N documentos en serie acumulan N esperas.")
    print("Async no hace mas rapido al modelo, pero evita esperar una llamada antes de iniciar la siguiente.")

    section(4, "VERSION MEJORADA - abatch async")
    start = time.perf_counter()
    async_results = asyncio.run(summarize_async(docs))
    async_seconds = time.perf_counter() - start
    for result in async_results:
        print(f"{result.doc_id}: {result.summary}")
    print(f"Tiempo async: {async_seconds:.2f}s")

    section(5, "VALIDACION")
    print(f"Cantidad validada: {len(async_results)} == {len(docs)}")
    print(f"Speedup medido: {sequential_seconds / async_seconds:.2f}x")
    print("Nota: el speedup real depende de red, rate limits y latencia del proveedor.")

    section(6, "CLASIFICACION DE ETAPAS")
    print(classify_stage("leer documento desde storage", waits_external_resource=True, heavy_local_compute=False))
    print(classify_stage("normalizar texto con loops grandes", waits_external_resource=False, heavy_local_compute=True))
    print(classify_stage("llamar al LLM remoto", waits_external_resource=True, heavy_local_compute=False))
    print(classify_stage("serializar JSON gigante", waits_external_resource=False, heavy_local_compute=True))

    section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega un limite de concurrencia con asyncio.Semaphore.")
    print("2. Simula un error en un documento y captura excepciones por tarea.")
    print("3. Explica por que async no acelera una funcion CPU-bound pura.")

    trace_text("USER", "Resumi todos los documentos comparando ejecucion secuencial vs async.")
    trace_json("RESULT", [result.model_dump(mode="json") for result in async_results])
    trace_json(
        "METRICS",
        {
            "sequential_seconds": sequential_seconds,
            "async_seconds": async_seconds,
            "speedup": sequential_seconds / async_seconds,
            "documents": len(docs),
        },
    )


if __name__ == "__main__":
    main()
