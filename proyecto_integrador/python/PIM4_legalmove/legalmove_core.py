"""Nucleo compartido para los ejercicios Python del PIM4 LegalMove.

El modo por defecto es deterministico para poder dar clase sin credenciales ni
red. Si se activa ``use_real_api=True``, el parser visual usa OpenAI Vision.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, Field, ValidationError, field_validator


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


class ContractChangeOutput(BaseModel):
    sections_changed: list[str] = Field(
        description="Identificadores de clausulas o secciones modificadas por la adenda."
    )
    topics_touched: list[str] = Field(
        description="Temas legales o comerciales afectados por los cambios."
    )
    summary_of_the_change: str = Field(
        min_length=10,
        description="Resumen claro y detallado de los cambios introducidos.",
    )

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def non_empty_list(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("La lista no puede estar vacia.")
        if any(not item.strip() for item in value):
            raise ValueError("Los valores de la lista no pueden estar vacios.")
        return value


@dataclass
class Span:
    name: str
    input_preview: str
    output_preview: str = ""
    latency_ms: float = 0.0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trace:
    name: str
    contract_id: str
    spans: list[Span] = field(default_factory=list)
    success: bool = False

    def run_span(
        self,
        name: str,
        input_preview: str,
        fn: Callable[[], Any],
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        span = Span(name=name, input_preview=preview(input_preview), metadata=metadata or {})
        start = time.perf_counter()
        try:
            result = fn()
            span.output_preview = preview(dump_for_preview(result))
            return result
        except Exception as exc:
            span.error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            span.latency_ms = (time.perf_counter() - start) * 1000
            self.spans.append(span)

    def print_tree(self) -> None:
        print(f"Trace {self.name} contract_id={self.contract_id} success={self.success}")
        for index, span in enumerate(self.spans, start=1):
            status = "OK" if span.error is None else "FAIL"
            print(f"  {index}. [{status}] {span.name} ({span.latency_ms:.0f} ms)")
            print(f"     in : {span.input_preview}")
            print(f"     out: {span.output_preview}")
            if span.metadata:
                print(f"     meta: {json.dumps(span.metadata, ensure_ascii=False)}")
            if span.error:
                print(f"     err: {span.error}")

    def model_dump(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "contract_id": self.contract_id,
            "success": self.success,
            "spans": [
                {
                    "name": span.name,
                    "input_preview": span.input_preview,
                    "output_preview": span.output_preview,
                    "latency_ms": round(span.latency_ms, 2),
                    "error": span.error,
                    "metadata": span.metadata,
                }
                for span in self.spans
            ],
        }


@dataclass
class PipelineResult:
    output: ContractChangeOutput
    trace: Trace
    original_text: str
    amendment_text: str
    context_map: str


def preview(value: str, max_chars: int = 180) -> str:
    clean = " ".join(value.split())
    return clean if len(clean) <= max_chars else clean[: max_chars - 3] + "..."


def dump_for_preview(value: Any) -> str:
    if isinstance(value, BaseModel):
        return json.dumps(value.model_dump(mode="json"), ensure_ascii=False)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_expected(name: str) -> dict[str, Any]:
    return read_json(DATA_DIR / "expected" / f"{name}.json")


def validate_image_path(image_path: str | Path) -> Path:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Formato invalido: {path.suffix}. Usar PNG, JPG o JPEG.")
    return path


def encode_image_to_base64(path: str | Path) -> str:
    validated = validate_image_path(path)
    return base64.b64encode(validated.read_bytes()).decode("utf-8")


def parse_contract_image(
    image_path: str | Path,
    document_label: str,
    use_real_api: bool = False,
) -> str:
    path = validate_image_path(image_path)
    image_b64 = encode_image_to_base64(path)

    if use_real_api:
        return _parse_contract_image_with_openai(path, image_b64, document_label)

    return _mock_contract_text(path, document_label)


def _parse_contract_image_with_openai(path: Path, image_b64: str, document_label: str) -> str:
    from openai import OpenAI

    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "image/png"
    model = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")
    client = OpenAI()
    prompt = f"""
Sos un analista legal especializado en lectura de contratos escaneados.

Documento: {document_label}

Tarea:
Extrae el texto del documento de la forma mas fiel posible.

Reglas:
- Conserva numeracion de clausulas.
- Conserva titulos, subtitulos, montos, fechas, nombres y condiciones.
- No resumas.
- No inventes texto.
- Si una parte es ilegible, marcala como [ILEGIBLE].
- Devolve solo el texto extraido, organizado por secciones.
"""
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{image_b64}",
                    },
                ],
            }
        ],
    )
    return response.output_text


def _mock_contract_text(path: Path, document_label: str) -> str:
    name = path.name.lower()
    if name == "contrato_original.png":
        return """
CONTRATO COMERCIAL DE SERVICIOS
Version original - Enero 2024

Clausula 1 - Monto mensual de pago
El cliente abonara al proveedor la suma de pesos un mil ($1.000) mensuales,
pagaderos dentro de los primeros cinco dias habiles de cada mes.

Clausula 2 - Duracion del contrato
El presente contrato tendra una vigencia de doce (12) meses, contados a partir
de la fecha de firma del presente instrumento.

Clausula 3 - Territorio de operacion
El proveedor prestara los servicios objeto de este contrato exclusivamente en
el territorio de la Republica Argentina.

Clausula 4 - Confidencialidad
Las partes se comprometen a mantener confidencialidad sobre toda informacion
intercambiada durante la relacion contractual.
""".strip()
    if name == "adenda_simple.png":
        return """
ADENDA NRO 1
Modificacion simple - Marzo 2024

Clausula 2 modificada - Nueva duracion del contrato
Por acuerdo de partes, la vigencia del contrato se extiende a dieciocho (18)
meses, quedando sin efecto el plazo de doce meses estipulado en la clausula 2
original.
""".strip()
    if name == "adenda_compleja.png":
        return """
ADENDA NRO 2
Modificacion compleja - Julio 2024

Clausula 1 modificada - Nuevo monto mensual de pago
Por acuerdo de partes, el monto mensual se incrementa a pesos un mil quinientos
($1.500), quedando sin efecto el monto de la clausula 1 original.

Clausula 2 modificada - Nueva duracion del contrato
La vigencia del contrato se extiende a veinticuatro (24) meses, quedando sin
efecto el plazo original de doce meses.

Clausula 3 modificada - Expansion del territorio de operacion
El proveedor amplia la prestacion de servicios a los territorios de Argentina,
Uruguay y Paraguay.
""".strip()
    return f"{document_label}: texto simulado no catalogado para {path.name}."


class ContextualizationAgent:
    def __init__(self, use_real_api: bool = False, model: str | None = None) -> None:
        self.use_real_api = use_real_api
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def run(self, original_text: str, amendment_text: str) -> str:
        if self.use_real_api:
            return self._run_with_openai(original_text, amendment_text)
        return self._run_mock(original_text, amendment_text)

    def _run_mock(self, original_text: str, amendment_text: str) -> str:
        sections = detect_sections(amendment_text)
        rows = []
        for section in sections:
            purpose = SECTION_PURPOSES[section]
            rows.append(
                f"- {section}: correspondencia directa; proposito: {purpose}; "
                "el agente extractor debe analizar el cambio final."
            )
        return "Mapa contextual comparado:\n" + "\n".join(rows)

    def _run_with_openai(self, original_text: str, amendment_text: str) -> str:
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Sos un Analista Senior de Contratos. Mapea secciones, "
                        "correspondencias y ambiguedades. No generes el JSON final."
                    ),
                },
                {
                    "role": "user",
                    "content": f"CONTRATO ORIGINAL:\n{original_text}\n\nADENDA:\n{amendment_text}",
                },
            ],
        )
        return response.output_text


class ExtractionAgent:
    def __init__(self, use_real_api: bool = False, model: str | None = None) -> None:
        self.use_real_api = use_real_api
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def run(
        self,
        original_text: str,
        amendment_text: str,
        context_map: str,
    ) -> ContractChangeOutput:
        if self.use_real_api:
            raw = self._run_with_openai(original_text, amendment_text, context_map)
        else:
            raw = self._run_mock(amendment_text)
        return validate_contract_change_output(raw)

    def _run_mock(self, amendment_text: str) -> dict[str, Any]:
        sections = detect_sections(amendment_text)
        if sections == ["duration"]:
            return load_expected("cambio_simple")
        if set(sections) == {"payment_terms", "duration", "service_territory"}:
            return load_expected("cambio_complejo")
        return {
            "sections_changed": sections or ["unknown"],
            "topics_touched": [SECTION_PURPOSES.get(section, "tema no catalogado") for section in sections]
            or ["tema no catalogado"],
            "summary_of_the_change": "Se detecto una modificacion contractual que requiere revision humana.",
        }

    def _run_with_openai(
        self,
        original_text: str,
        amendment_text: str,
        context_map: str,
    ) -> dict[str, Any]:
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Sos un Auditor Legal. Devolve solo JSON valido con "
                        "sections_changed, topics_touched y summary_of_the_change. "
                        "Distingui adiciones, eliminaciones y modificaciones en el resumen."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"MAPA CONTEXTUAL:\n{context_map}\n\n"
                        f"CONTRATO ORIGINAL:\n{original_text}\n\nADENDA:\n{amendment_text}"
                    ),
                },
            ],
        )
        return json.loads(response.output_text)


SECTION_PURPOSES = {
    "payment_terms": "monto mensual de pago",
    "duration": "duracion contractual",
    "service_territory": "territorio de operacion",
}


def detect_sections(text: str) -> list[str]:
    lower = text.lower()
    sections: list[str] = []
    if any(marker in lower for marker in ("quinientos", "$1.500", "monto mensual", "clausula 1")):
        sections.append("payment_terms")
    if any(marker in lower for marker in ("dieciocho", "veinticuatro", "duracion", "clausula 2")):
        sections.append("duration")
    if any(marker in lower for marker in ("uruguay", "paraguay", "territorio", "clausula 3")):
        sections.append("service_territory")
    return sections


def validate_contract_change_output(payload: Any) -> ContractChangeOutput:
    try:
        return ContractChangeOutput.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"El output no cumple ContractChangeOutput: {exc}") from exc


def score_sections(actual: ContractChangeOutput | dict[str, Any] | str, expected: dict[str, Any]) -> str:
    if isinstance(actual, ContractChangeOutput):
        detected = actual.sections_changed
    elif isinstance(actual, dict):
        detected = actual.get("sections_changed", [])
    else:
        detected = detect_sections(actual)
    expected_sections = set(expected["sections_changed"])
    hits = len(set(detected) & expected_sections)
    return f"{hits}/{len(expected_sections)}"


def run_pipeline(
    original_path: str | Path,
    amendment_path: str | Path,
    use_real_api: bool = False,
    use_langfuse: bool = False,
) -> PipelineResult:
    trace = Trace(name="contract-analysis", contract_id=Path(amendment_path).stem)
    try:
        original_text = trace.run_span(
            "parse_original_contract",
            str(original_path),
            lambda: parse_contract_image(original_path, "Contrato original", use_real_api=use_real_api),
            metadata={"document_label": "Contrato original", "real_api": use_real_api},
        )
        amendment_text = trace.run_span(
            "parse_amendment_contract",
            str(amendment_path),
            lambda: parse_contract_image(amendment_path, "Adenda o enmienda", use_real_api=use_real_api),
            metadata={"document_label": "Adenda o enmienda", "real_api": use_real_api},
        )
        contextualizer = ContextualizationAgent(use_real_api=use_real_api)
        context_map = trace.run_span(
            "contextualization_agent",
            "original_text + amendment_text",
            lambda: contextualizer.run(original_text, amendment_text),
            metadata={"agent": "ContextualizationAgent"},
        )
        extractor = ExtractionAgent(use_real_api=use_real_api)
        output = trace.run_span(
            "extraction_agent",
            "context_map + original_text + amendment_text",
            lambda: extractor.run(original_text, amendment_text, context_map),
            metadata={"agent": "ExtractionAgent"},
        )
        output = trace.run_span(
            "pydantic_validation",
            "raw ContractChangeOutput",
            lambda: validate_contract_change_output(output.model_dump(mode="json")),
            metadata={"schema": "ContractChangeOutput"},
        )
        trace.success = True
        result = PipelineResult(output, trace, original_text, amendment_text, context_map)
        if use_langfuse:
            send_trace_to_langfuse(trace)
        return result
    except Exception:
        trace.success = False
        if use_langfuse:
            send_trace_to_langfuse(trace)
        raise


def send_trace_to_langfuse(trace: Trace) -> None:
    try:
        from langfuse import Langfuse
    except ImportError:
        print("Langfuse no esta instalado. Se conserva solo la traza local.")
        return

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if not public_key or not secret_key:
        print("Faltan credenciales Langfuse. Se conserva solo la traza local.")
        return

    client = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )
    langfuse_trace = client.trace(
        name=trace.name,
        id=f"{trace.contract_id}-{int(time.time())}",
        metadata={"success": trace.success, "contract_id": trace.contract_id},
    )
    for span in trace.spans:
        langfuse_trace.span(
            name=span.name,
            input=span.input_preview,
            output=span.output_preview,
            metadata={**span.metadata, "latency_ms": span.latency_ms, "error": span.error},
        )
    client.flush()


def print_title(title: str) -> None:
    print("=" * 78)
    print(title)
    print("=" * 78)


def print_section(number: int, title: str) -> None:
    print()
    print(f"=== {number}. {title} ===")


def print_json(label: str, payload: Any) -> None:
    print(f"{label}:")
    if isinstance(payload, BaseModel):
        payload = payload.model_dump(mode="json")
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
