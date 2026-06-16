"""
E03 - Pipeline async con LangChain abatch/gather
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Mostrar que N llamadas I/O-bound al LLM no deberian ejecutarse en serie.

USE_REAL_API = False:
    Lee documentos reales y usa asyncio.sleep para simular latencia.
USE_REAL_API = True:
    Usa chain.abatch() de LangChain.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, preview, read_text, run_generator, trace_json, trace_text


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    return None

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
DOCS_DIR = DATA_DIR / "documentos"
FIRST_DOC = DOCS_DIR / "doc_01.txt"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", FIRST_DOC)


class AsyncSummary(BaseModel):
    doc_id: str
    summary: str = Field(..., min_length=12)


def summarize_sync(doc_id: str, text: str) -> AsyncSummary:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([("system", "Resumi breve."), ("user", "{texto}")])
        summary = (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()).invoke({"texto": text})
        return AsyncSummary(doc_id=doc_id, summary=summary)
    time.sleep(0.5)
    return AsyncSummary(doc_id=doc_id, summary=f"Resumen: {preview(text, 70)}")


async def summarize_async_mock(doc_id: str, text: str) -> AsyncSummary:
    await asyncio.sleep(0.5)
    return AsyncSummary(doc_id=doc_id, summary=f"Resumen async: {preview(text, 70)}")


async def summarize_async(docs: list[tuple[str, str]]) -> list[AsyncSummary]:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([("system", "Resumi breve."), ("user", "{texto}")])
        chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()
        raw = await chain.abatch([{"texto": text} for _, text in docs])
        return [AsyncSummary(doc_id=doc_id, summary=summary) for (doc_id, _), summary in zip(docs, raw)]
    return await asyncio.gather(*[summarize_async_mock(doc_id, text) for doc_id, text in docs])


def main() -> None:
    ensure_data()
    docs = [(p.name, read_text(p)) for p in sorted(DOCS_DIR.glob("doc_*.txt"))]

    print_title("AEM4L5 | E03 - Async pipeline")

    print_section(1, "CONTEXTO DEL CASO")
    print("Hay que resumir varios documentos. Cada llamada al LLM espera red: es I/O-bound.")
    print_file_evidence(FIRST_DOC, "Documento")
    print(f"Documentos: {len(docs)}")

    print_section(2, "VERSION BASICA - secuencial")
    start = time.perf_counter()
    seq = [summarize_sync(doc_id, text) for doc_id, text in docs]
    t_seq = time.perf_counter() - start
    print(f"Resumidos en serie: {len(seq)} docs en {t_seq:.2f}s")

    print_section(3, "PROBLEMA DETECTADO")
    print("Si cada request tarda 0.5s, 6 docs en serie tardan cerca de 3s. Con 50 docs escala mal.")

    print_section(4, "VERSION MEJORADA - async gather / LangChain abatch")
    start = time.perf_counter()
    async_results = asyncio.run(summarize_async(docs))
    t_async = time.perf_counter() - start
    for r in async_results:
        print(f"  {r.doc_id}: {r.summary}")
    print("Diagrama mental: secuencial = espera, espera, espera; async = dispara todas y espera el conjunto.")

    print_section(5, "VALIDACION")
    print(f"Secuencial={t_seq:.2f}s | Async={t_async:.2f}s | speedup={t_seq / t_async:.2f}x")
    print(f"Cantidad validada: {len(async_results)} == {len(docs)}")
    try:
        AsyncSummary(doc_id="x", summary="corto")
    except ValidationError as exc:
        print("Pydantic valida resumen minimo:")
        print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: N llamadas en serie = N x latencia.")
    print("DESPUES: abatch/gather para I/O-bound = cerca de 1 x latencia + overhead.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega una etapa CPU-bound de tokenizacion pesada.")
    print("2. Demostra que async no acelera CPU-bound.")
    print("3. Combina abatch para I/O y ProcessPoolExecutor para CPU.")

    trace_text("USER", "Resumí todos los documentos comparando ejecución secuencial vs async.")
    trace_json("RESULT", [result.model_dump(mode="json") for result in async_results])
    trace_json("METRICS", {
        "sequential_seconds": t_seq,
        "async_seconds": t_async,
        "speedup": t_seq / t_async,
        "documents": len(docs),
    })


if __name__ == "__main__":
    main()
