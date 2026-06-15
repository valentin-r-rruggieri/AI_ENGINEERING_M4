"""
E02 - cProfile para encontrar cuellos de botella
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Separar CPU-bound de I/O-bound en un pipeline de texto + resumen LLM.

USE_REAL_API = False:
    Lee texto largo real y simula latencia de LLM.
USE_REAL_API = True:
    Usa LangChain para el resumen.
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
from common import print_file_evidence, print_section, print_title, read_text, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
TEXT_PATH = DATA_DIR / "texto_largo.txt"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", TEXT_PATH)


def summarize_llm(text: str) -> str:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Resumi el texto en una frase."),
            ("user", "{texto}"),
        ])
        return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()).invoke({"texto": text[:4000]})
    time.sleep(0.15)
    return "Resumen mock del texto procesado."


def regex_lento(text: str) -> dict[str, int]:
    terms = ["contrato", "clausula", "monto", "plazo", "territorio", "rescicion", "auditoria"]
    counts = {}
    for term in terms:
        total = 0
        for _ in range(250):
            total += len(re.findall(term, text, flags=re.IGNORECASE))
        counts[term] = total
    return counts


def regex_optimizado(text: str) -> dict[str, int]:
    patterns = {term: re.compile(term, flags=re.IGNORECASE) for term in ["contrato", "clausula", "monto", "plazo", "territorio", "rescicion", "auditoria"]}
    return {term: sum(len(pattern.findall(text)) for _ in range(250)) for term, pattern in patterns.items()}


def pipeline_lento(text: str) -> tuple[dict[str, int], str]:
    counts = regex_lento(text)
    summary = summarize_llm(text)
    return counts, summary


def pipeline_optimizado(text: str) -> tuple[dict[str, int], str]:
    counts = regex_optimizado(text)
    summary = summarize_llm(text)
    return counts, summary


def profile_call(label: str, func, text: str) -> float:
    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    func(text)
    profiler.disable()
    elapsed = time.perf_counter() - start
    stream = io.StringIO()
    pstats.Stats(profiler, stream=stream).sort_stats("cumtime").print_stats(8)
    print(f"\nPerfil {label} ({elapsed:.3f}s):")
    print(stream.getvalue())
    return elapsed


def main() -> None:
    ensure_data()
    text = read_text(TEXT_PATH)

    print_title("AEM4L5 | E02 - cProfile y optimizacion")

    print_section(1, "CONTEXTO DEL CASO")
    print("Pipeline: limpiar/buscar patrones en texto largo + llamar a una chain de resumen.")
    print_file_evidence(TEXT_PATH, "Texto largo")
    print(f"Caracteres: {len(text)}")

    print_section(2, "VERSION BASICA - pipeline lento sin medir")
    start = time.perf_counter()
    pipeline_lento(text)
    baseline = time.perf_counter() - start
    print(f"'Esta lento': {baseline:.3f}s, pero todavia no sabemos por que.")

    print_section(3, "PROBLEMA DETECTADO")
    print("Sin profiling se optimiza a ciegas: regex es CPU-bound, la llamada LLM es I/O-bound.")

    print_section(4, "VERSION MEJORADA - cProfile + regex compilada")
    slow = profile_call("lento", pipeline_lento, text)
    fast = profile_call("optimizado", pipeline_optimizado, text)
    print("Lectura de columnas: ncalls=cantidad de llamadas, tottime=tiempo propio, cumtime=tiempo acumulado.")

    print_section(5, "VALIDACION")
    print(f"Tiempo lento={slow:.3f}s | optimizado={fast:.3f}s | speedup={slow / fast:.2f}x")
    print("Clasificacion: regex=CPU-bound; summarize_llm=I/O-bound; async ayuda al I/O, no a la CPU.")

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: optimizar por intuicion.")
    print("DESPUES: cProfile ordenado por cumtime seniala donde trabajar primero.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega pasos con time.sleep y encontra el mayor cumtime.")
    print("2. Decide que pasos van con async y cuales con multiprocessing.")
    print("3. Explica por que compilar regex una vez mejora CPU-bound.")


if __name__ == "__main__":
    main()
