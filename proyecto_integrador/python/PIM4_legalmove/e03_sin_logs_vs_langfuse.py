"""
E03 - Pipeline completo con trace local y Langfuse opcional
PIM4 | LegalMove

Objetivo pedagogico:
    Mostrar que sin spans no se sabe donde fallo el pipeline, y que una traza
    por etapa localiza parsing, contextualizacion, extraccion o validacion.

USE_REAL_LANGFUSE = False:
    Mantiene trace local. Si se activa, se pueden pasar callbacks Langfuse.
"""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

# PIM vive fuera de python_puro para que el proyecto integrador quede separado,
# pero reutiliza las utilidades y el .env comun de los ejercicios Python.
REPO_DIR = Path(__file__).resolve().parents[3]
COMMON_DIR = REPO_DIR / "python_puro" / "AEM4_python_exercises"
sys.path.insert(0, str(COMMON_DIR))
from common import require_openai_api_key, image_to_base64, print_file_evidence, print_section, print_title, read_json, run_generator, trace_json, trace_text


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    return None

load_dotenv(COMMON_DIR / ".env")
require_openai_api_key()

USE_REAL_LANGFUSE = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
CONTRACT_IMG = DATA_DIR / "contrato_original.png"
AMENDMENT_IMG = DATA_DIR / "adenda_compleja.png"
EXPECTED_PATH = DATA_DIR / "expected" / "cambio_complejo.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", CONTRACT_IMG)


@dataclass
class Span:
    name: str
    input_preview: str
    output_preview: str = ""
    latency_ms: float = 0.0
    error: str | None = None


@dataclass
class Trace:
    contract_id: str
    spans: List[Span] = field(default_factory=list)
    success: bool = False

    def run_span(self, name: str, input_preview: str, fn: Callable[[], Any]) -> Any:
        span = Span(name=name, input_preview=input_preview)
        start = time.perf_counter()
        try:
            result = fn()
            span.output_preview = str(result)[:160]
            return result
        except Exception as exc:
            span.error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            span.latency_ms = (time.perf_counter() - start) * 1000
            self.spans.append(span)

    def print_tree(self) -> None:
        print(f"Trace contract_id={self.contract_id} success={self.success}")
        for i, span in enumerate(self.spans, start=1):
            icon = "OK" if span.error is None else "FAIL"
            print(f"  {i}. [{icon}] {span.name} ({span.latency_ms:.0f} ms)")
            print(f"     in : {span.input_preview}")
            print(f"     out: {span.output_preview}")
            if span.error:
                print(f"     err: {span.error}")

    def model_dump(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "success": self.success,
            "spans": [
                {
                    "name": span.name,
                    "input_preview": span.input_preview,
                    "output_preview": span.output_preview,
                    "latency_ms": span.latency_ms,
                    "error": span.error,
                }
                for span in self.spans
            ],
        }


class ContractChangeOutput(BaseModel):
    sections_changed: List[str]
    topics_touched: List[str]
    summary_of_the_change: str = Field(..., min_length=10)

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def non_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("La lista no puede estar vacia")
        return value


def parse_image(path: Path) -> str:
    img_b64 = image_to_base64(path)
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI

    msg = HumanMessage(content=[
        {"type": "text", "text": "Extrae texto de este documento legal."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
    ])
    content = ChatOpenAI(model=VISION_MODEL, temperature=0).invoke([msg]).content
    return content if isinstance(content, str) else str(content)
    if path.name == "contrato_original.png":
        return "Contrato original: payment_terms $1.000; duration 12 meses; service_territory Argentina."
    return "Adenda compleja: payment_terms $1.500; duration 24 meses; service_territory Argentina Uruguay Paraguay."


def contextualization_agent(original: str, amendment: str) -> str:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Mapea secciones; no extraigas cambios finales."),
        ("user", "{original}\n\n{amendment}"),
    ])
    return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()).invoke({"original": original, "amendment": amendment})
    return "Secciones detectadas: payment_terms, duration, service_territory. La adenda toca las tres."


def extraction_agent(original: str, amendment: str, context_map: str, broken: bool = False) -> dict[str, Any]:
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extrae cambios como JSON usando el mapa de contexto."),
        ("user", "Mapa:{context_map}\nOriginal:{original}\nAdenda:{amendment}"),
    ])
    return (prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | JsonOutputParser()).invoke({"context_map": context_map, "original": original, "amendment": amendment})
    if broken:
        return {"sections_changed": ["payment_terms"], "topics_touched": ["monto mensual"], "summary_of_the_change": "corto"}
    return read_json(EXPECTED_PATH)


def blind_pipeline() -> None:
    try:
        original = parse_image(CONTRACT_IMG)
        amendment = parse_image(AMENDMENT_IMG)
        ctx = contextualization_agent(original, amendment)
        raw = extraction_agent(original, amendment, ctx, broken=True)
        ContractChangeOutput(**raw)
        print("Pipeline OK")
    except Exception:
        print("fallo")


def traced_pipeline(contract_id: str, broken: bool = False) -> Trace:
    trace = Trace(contract_id=contract_id)
    try:
        original = trace.run_span("parse_contract_image", CONTRACT_IMG.name, lambda: parse_image(CONTRACT_IMG))
        amendment = trace.run_span("parse_amendment_image", AMENDMENT_IMG.name, lambda: parse_image(AMENDMENT_IMG))
        ctx = trace.run_span("contextualization_agent", "original+amendment", lambda: contextualization_agent(original, amendment))
        raw = trace.run_span("extraction_agent", "context_map+texts", lambda: extraction_agent(original, amendment, ctx, broken=broken))
        trace.run_span("pydantic_validation", "raw extraction", lambda: ContractChangeOutput(**raw))
        trace.success = True
    except Exception:
        trace.success = False
    return trace


def main() -> None:
    ensure_data()

    print_title("PIM4 | E03 - Pipeline completo con trace")

    print_section(1, "CONTEXTO DEL CASO")
    print("Un pipeline legal tiene varias etapas. Sin trazas, un 'fallo' no alcanza para diagnosticar.")
    print_file_evidence(CONTRACT_IMG, "Contrato")
    print_file_evidence(AMENDMENT_IMG, "Adenda")
    print_file_evidence(EXPECTED_PATH, "Golden")

    print_section(2, "VERSION BASICA - sin logs")
    blind_pipeline()

    print_section(3, "PROBLEMA DETECTADO")
    print("No sabemos si fallo vision, contextualizacion, extraccion o validacion. Tampoco vemos latencias por etapa.")

    print_section(4, "VERSION MEJORADA - trace de spans")
    ok_trace = traced_pipeline("contract-ok", broken=False)
    ok_trace.print_tree()
    print()
    bad_trace = traced_pipeline("contract-validation-error", broken=True)
    bad_trace.print_tree()
    if USE_REAL_LANGFUSE:
        print("Langfuse real activado: pasar callbacks en chain.invoke(config={'callbacks':[handler]}).")

    print_section(5, "VALIDACION")
    print(f"Caso OK success={ok_trace.success} spans={len(ok_trace.spans)}")
    print(f"Caso fallo success={bad_trace.success} ultimo_span={bad_trace.spans[-1].name} error={bad_trace.spans[-1].error}")

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: except -> 'fallo', sin diagnostico.")
    print("DESPUES: spans con input, output, latencia y error exacto por etapa.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega modelo, version, tokens y trace_id a Span.")
    print("2. Envia la traza a Langfuse con USE_REAL_LANGFUSE=True.")
    print("3. Agrega un golden diff cuando la validacion pasa pero el contenido no coincide.")

    trace_text("USER", "Procesá contrato y adenda compleja con trazabilidad por etapa.")
    trace_json("TRACE", {
        "ok": ok_trace.model_dump(),
        "validation_error": bad_trace.model_dump(),
    })
    trace_json("METRICS", {
        "ok_success": ok_trace.success,
        "ok_spans": len(ok_trace.spans),
        "bad_success": bad_trace.success,
        "bad_last_span": bad_trace.spans[-1].name,
        "bad_error": bad_trace.spans[-1].error,
    })


if __name__ == "__main__":
    main()
