"""
E02 - cProfile para encontrar cuellos de botella
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Separar CPU-bound de I/O-bound en un pipeline de texto + resumen LLM.
"""

from __future__ import annotations

import cProfile
import io
import os
import pstats
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import preview, read_text, require_openai_api_key, run_generator, trace_json, trace_text

load_dotenv()
require_openai_api_key()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
TEXT_PATH = DATA_DIR / "texto_largo.txt"
TERMS = ["contrato", "clausula", "monto", "plazo", "territorio", "rescicion", "auditoria"]


def title(text: str) -> None:
    print("=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print()
    print(f"=== {number}. {text} ===")


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", TEXT_PATH)


def summarize_llm(text: str) -> str:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Resumi el texto en una frase y menciona el tipo de documento."),
            ("user", "{texto}"),
        ]
    )
    chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()
    return chain.invoke({"texto": text[:3500]})


def count_terms_slow(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for term in TERMS:
        total = 0
        for _ in range(260):
            total += len(re.findall(term, text, flags=re.IGNORECASE))
        counts[term] = total
    return counts


def count_terms_optimized(text: str) -> dict[str, int]:
    patterns = {term: re.compile(term, flags=re.IGNORECASE) for term in TERMS}
    counts: dict[str, int] = {}
    for term, pattern in patterns.items():
        matches = len(pattern.findall(text))
        counts[term] = matches * 260
    return counts


def profile_call(label: str, func, text: str) -> tuple[dict[str, int], float, str]:
    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    result = func(text)
    profiler.disable()
    elapsed = time.perf_counter() - start

    stream = io.StringIO()
    pstats.Stats(profiler, stream=stream).sort_stats("cumtime").print_stats(8)
    report = stream.getvalue()

    print(f"\nPerfil {label}: {elapsed:.3f}s")
    print(report)
    return result, elapsed, report


def main() -> None:
    ensure_data()
    text = read_text(TEXT_PATH)

    title("AEM4L5 | E02 - cProfile y optimizacion")

    section(1, "CONTEXTO DEL CASO")
    print("Pipeline: texto largo -> conteo de terminos -> resumen LLM.")
    print(f"Modelo OpenAI: {MODEL_NAME}")
    print(f"Texto: {TEXT_PATH.name} | caracteres={len(text)} | preview={preview(text, 120)}")

    section(2, "VERSION BASICA - pipeline lento sin medir")
    start = time.perf_counter()
    baseline_counts = count_terms_slow(text)
    baseline_seconds = time.perf_counter() - start
    print(f"'Esta lento': {baseline_seconds:.3f}s, pero todavia no sabemos por que.")
    print(f"Conteos ejemplo: {dict(list(baseline_counts.items())[:3])}")

    section(3, "PROBLEMA DETECTADO")
    print("Sin profiling se optimiza a ciegas.")
    print("El conteo repetido de regex es CPU-bound; el resumen LLM es I/O-bound/red.")

    section(4, "VERSION MEJORADA - cProfile + regex compilada")
    slow_counts, slow_seconds, _ = profile_call("lento", count_terms_slow, text)
    fast_counts, fast_seconds, _ = profile_call("optimizado", count_terms_optimized, text)
    print("Lectura: ncalls=cantidad de llamadas, tottime=tiempo propio, cumtime=tiempo acumulado.")

    section(5, "LLM REAL COMO ETAPA I/O")
    llm_start = time.perf_counter()
    summary = summarize_llm(text)
    llm_seconds = time.perf_counter() - llm_start
    print(f"Resumen LLM ({llm_seconds:.2f}s): {summary}")

    section(6, "VALIDACION")
    print(f"Conteos iguales: {slow_counts == fast_counts}")
    print(f"Tiempo lento={slow_seconds:.3f}s | optimizado={fast_seconds:.3f}s | speedup={slow_seconds / fast_seconds:.2f}x")
    print("Conclusion: cProfile guia CPU-bound; async/batching guia I/O-bound.")

    section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega una funcion de serializacion JSON gigante y volve a perfilar.")
    print("2. Ordena por tottime y por cumtime: que cambia?")
    print("3. Explica por que compilar regex una vez reduce costo CPU.")

    trace_text("USER", "Profilea el pipeline lento y comparalo contra la version optimizada.")
    trace_json(
        "METRICS",
        {
            "slow_seconds": slow_seconds,
            "optimized_seconds": fast_seconds,
            "speedup": slow_seconds / fast_seconds,
            "llm_seconds": llm_seconds,
            "counts_equal": slow_counts == fast_counts,
            "classification": {
                "count_terms": "CPU-bound",
                "summarize_llm": "I/O-bound",
            },
        },
    )


if __name__ == "__main__":
    main()
