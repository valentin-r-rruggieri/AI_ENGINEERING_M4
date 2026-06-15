"""
E01 - Serverless vs servidor persistente con servicio de resumen
AEM4L5 | Arquitecturas avanzadas de adaptacion y serving

Objetivo pedagogico:
    Medir cold start vs warm requests y decidir infraestructura con evidencia.

USE_REAL_API = False:
    Lee documentos reales y mockea el resumen.
USE_REAL_API = True:
    Resume con LangChain ChatOpenAI.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, preview, read_text, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
DOCS_DIR = DATA_DIR / "documentos"
FIRST_DOC = DOCS_DIR / "doc_01.txt"
COLD_START_S = 0.7
_MODEL_LOADED = False


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", FIRST_DOC)


class SummaryResponse(BaseModel):
    doc_id: str
    summary: str = Field(..., min_length=15)
    cold_start: bool
    latency_ms: float = Field(..., ge=0)


def summarize_text(text: str) -> str:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Resumi el documento en una o dos oraciones accionables."),
            ("user", "{texto}"),
        ])
        chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()
        return chain.invoke({"texto": text})
    time.sleep(0.12)
    return f"Resumen: {preview(text, 90)}"


def summarize_service(doc_id: str, text: str) -> SummaryResponse:
    global _MODEL_LOADED
    cold = not _MODEL_LOADED
    start = time.perf_counter()
    if cold:
        print("  [MOCK] Cold start: cargando modelo/chain...")
        time.sleep(COLD_START_S)
        _MODEL_LOADED = True
    summary = summarize_text(text)
    latency_ms = (time.perf_counter() - start) * 1000
    return SummaryResponse(doc_id=doc_id, summary=summary, cold_start=cold, latency_ms=latency_ms)


def main() -> None:
    ensure_data()
    docs = sorted(DOCS_DIR.glob("doc_*.txt"))

    print_title("AEM4L5 | E01 - Serverless vs servidor persistente")

    print_section(1, "CONTEXTO DEL CASO")
    print("Un servicio de resumen procesa documentos. La primera llamada puede pagar cold start.")
    print_file_evidence(FIRST_DOC, "Documento")
    print(f"Documentos disponibles: {len(docs)}")

    print_section(2, "VERSION BASICA - asumir latencia plana")
    flat_latency_ms = 120
    for doc in docs[:3]:
        print(f"  {doc.name}: latencia asumida {flat_latency_ms} ms")

    print_section(3, "PROBLEMA DETECTADO")
    print("Si el primer request tarda mucho mas, el SLA de serverless no se entiende mirando solo promedios planos.")
    print("Cold start puede cargar runtime, dependencias y modelo antes de responder.")

    print_section(4, "VERSION MEJORADA - medir cold/warm")
    responses = []
    for doc in docs:
        responses.append(summarize_service(doc.name, read_text(doc)))
    for r in responses:
        print(f"  {r.doc_id}: cold={r.cold_start} latency={r.latency_ms:.0f} ms summary={r.summary}")
    print("Decision: trafico bajo o batch -> serverless; trafico alto estable/modelo grande en RAM -> persistente; mixto -> hibrido.")

    print_section(5, "VALIDACION")
    cold = responses[0].latency_ms
    warm = min(r.latency_ms for r in responses[1:])
    print(f"Cold={cold:.0f} ms | Warm minimo={warm:.0f} ms | cold>warm={cold > warm}")
    try:
        SummaryResponse(doc_id="x", summary="corto", cold_start=False, latency_ms=-1)
    except ValidationError as exc:
        print("Pydantic valida summary minimo y latencia positiva:")
        print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: latencia plana asumida y decision de infra basada en costumbre.")
    print("DESPUES: cold/warm medido + tabla de decision por trafico, costo y RAM.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Evalua 4 perfiles: bajo, estable alto, batch y picos impredecibles.")
    print("2. Decide serverless, persistente o hibrido.")
    print("3. Agrega modelo 7B en RAM y revisa la decision.")


if __name__ == "__main__":
    main()
