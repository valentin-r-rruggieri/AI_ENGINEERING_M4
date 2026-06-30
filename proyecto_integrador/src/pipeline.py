"""Orquestacion del pipeline LegalMove (PRODUCCION).

Une todos los componentes en 5 etapas:
    parse(original) -> parse(adenda) -> ContextualizationAgent
    -> ExtractionAgent -> validacion Pydantic

Trazabilidad
------------
Se mantienen DOS trazas en paralelo:
1. Traza local (Trace/Span): se imprime en consola, util sin abrir el dashboard.
2. Traza Langfuse: si hay credenciales, se envuelve todo el pipeline en
   client.start_as_current_observation(name="contract-analysis") para que las
   llamadas al LLM (via CallbackHandler) queden anidadas como spans hijos de un
   unico trace raiz, con tokens, latencia y costo.

Jerarquia esperada en Langfuse
------------------------------
    contract-analysis (trace raiz)
    |-- ChatOpenAI (parse contrato original)   <- generation con tokens
    |-- ChatOpenAI (parse adenda)              <- generation con tokens
    |-- ChatOpenAI (contextualization)         <- generation con tokens
    |-- ChatOpenAI (extraction)                <- generation con tokens
"""

from __future__ import annotations

import json
import time
from contextlib import nullcontext
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from models import ContractChangeOutput, validate_contract_change_output
from image_parser import parse_contract_image
from agents.contextualization_agent import ContextualizationAgent
from agents.extraction_agent import ExtractionAgent
from tracing import get_langfuse_client, get_langfuse_handler

# Rich da colores, spinners y paneles para diferenciar las salidas en clase.
# Si no esta instalado, el pipeline cae a print() plano (degradacion elegante).
try:
    from rich.console import Console

    _console: Console | None = Console()
except ImportError:
    _console = None


def _start_status(verbose: bool, paso: str, display: str):
    """Devuelve un context manager para la etapa (spinner rich o texto plano)."""
    if not verbose:
        return nullcontext()
    if _console is not None:
        return _console.status(f"[bold cyan]Paso {paso}[/] · {display}", spinner="dots")
    print(f"\n  ▶  Paso {paso} · {display}", flush=True)
    return nullcontext()


def _report_ok(verbose: bool, paso: str, display: str, dur: float, result: Any) -> None:
    """Informa que una etapa terminó bien (con color si hay rich)."""
    if not verbose:
        return
    detalle = f" · {len(result)} caracteres" if isinstance(result, str) else ""
    if _console is not None:
        _console.print(
            f"  [bold green]✅ Paso {paso}[/] · {display} "
            f"[dim]({dur:.1f}s{detalle})[/]"
        )
    else:
        print(f"     ✅ Listo en {dur:.1f}s{detalle}", flush=True)


def _report_fail(verbose: bool, paso: str, display: str, err: str) -> None:
    """Informa que una etapa falló (en rojo si hay rich)."""
    if not verbose:
        return
    if _console is not None:
        _console.print(f"  [bold red]❌ Paso {paso}[/] · {display} — {err}")
    else:
        print(f"     ❌ Falló: {err}", flush=True)


@dataclass
class Span:
    """Una etapa del pipeline en la traza local."""

    name: str
    input_preview: str
    output_preview: str = ""
    latency_ms: float = 0.0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trace:
    """Traza local raiz: agrupa todos los spans de una ejecucion."""

    name: str
    contract_id: str
    spans: list[Span] = field(default_factory=list)
    success: bool = False
    verbose: bool = False          # si True, imprime logs en vivo por etapa
    total_steps: int = 0           # total de pasos (para mostrar "Paso x/N")
    step_count: int = 0            # contador interno de pasos ya iniciados

    def run_span(
        self,
        name: str,
        input_preview: str,
        fn: Callable[[], Any],
        metadata: dict[str, Any] | None = None,
        label: str | None = None,
    ) -> Any:
        """Ejecuta fn() dentro de un span que mide latencia y captura errores.

        Si verbose=True, imprime en vivo el inicio y el fin de cada etapa con
        su duracion, para que se vea puntualmente que sucede en cada parte.
        """
        self.step_count += 1
        display = label or name
        paso = f"{self.step_count}/{self.total_steps}" if self.total_steps else f"{self.step_count}"

        span = Span(
            name=name,
            input_preview=_preview(input_preview),
            metadata=metadata or {},
        )
        start = time.perf_counter()
        try:
            # El spinner (rich) anima mientras corre la etapa; al terminar se
            # imprime la linea de OK con la duracion.
            with _start_status(self.verbose, paso, display):
                result = fn()
            span.output_preview = _preview(_dump_for_preview(result))
            _report_ok(self.verbose, paso, display, time.perf_counter() - start, result)
            return result
        except Exception as exc:
            span.error = f"{type(exc).__name__}: {exc}"
            _report_fail(self.verbose, paso, display, span.error)
            raise
        finally:
            span.latency_ms = (time.perf_counter() - start) * 1000
            self.spans.append(span)

    def print_tree(self) -> None:
        """Imprime la traza local como arbol jerarquico en consola."""
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
        """Serializa la traza local a dict."""
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
    """Resultado completo: output + traza local + textos intermedios + URL de Langfuse."""

    output: ContractChangeOutput
    trace: Trace
    original_text: str
    amendment_text: str
    context_map: str
    trace_url: str | None = None


def _preview(value: str, max_chars: int = 180) -> str:
    """Trunca un string a max_chars, colapsando espacios para legibilidad."""
    clean = " ".join(value.split())
    return clean if len(clean) <= max_chars else clean[: max_chars - 3] + "..."


def _dump_for_preview(value: Any) -> str:
    """Convierte cualquier valor a string para preview."""
    if isinstance(value, ContractChangeOutput):
        return json.dumps(value.model_dump(mode="json"), ensure_ascii=False)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def run_pipeline(
    original_path: str | Path,
    amendment_path: str | Path,
    use_langfuse: bool = True,
    verbose: bool = True,
) -> PipelineResult:
    """Ejecuta el pipeline completo de comparacion de contratos (API real).

    Args:
        original_path: ruta a la imagen del contrato original.
        amendment_path: ruta a la imagen de la adenda/enmienda.
        use_langfuse: si True (default), envia la traza a Langfuse si hay credenciales.

    Returns:
        PipelineResult con el output validado, la traza local, los textos
        intermedios y la URL de la traza en Langfuse (si aplica).
    """
    # Cliente y handler de Langfuse (None si no hay credenciales validas).
    client = get_langfuse_client() if use_langfuse else None
    handler = get_langfuse_handler() if client else None
    callbacks = [handler] if handler else None

    trace = Trace(
        name="contract-analysis",
        contract_id=Path(amendment_path).stem,
        verbose=verbose,
        total_steps=5,
    )
    trace_url: str | None = None

    # Span raiz de Langfuse: hace que todas las llamadas al LLM queden anidadas
    # bajo un unico trace. Si no hay cliente, nullcontext() no hace nada.
    root_ctx = (
        client.start_as_current_observation(name="contract-analysis", as_type="span")
        if client
        else nullcontext()
    )

    try:
        with root_ctx:
            # --- Etapa 1: Parsing del contrato original ---
            original_text = trace.run_span(
                "parse_original_contract",
                str(original_path),
                lambda: parse_contract_image(
                    original_path, "Contrato original", callbacks=callbacks
                ),
                metadata={"document_label": "Contrato original"},
                label="👁️  Leyendo el contrato original con GPT-4o Vision",
            )

            # --- Etapa 2: Parsing de la adenda ---
            amendment_text = trace.run_span(
                "parse_amendment_contract",
                str(amendment_path),
                lambda: parse_contract_image(
                    amendment_path, "Adenda o enmienda", callbacks=callbacks
                ),
                metadata={"document_label": "Adenda o enmienda"},
                label="👁️  Leyendo la adenda con GPT-4o Vision",
            )

            # --- Etapa 3: Contextualizacion (Agente 1) ---
            contextualizer = ContextualizationAgent()
            context_map = trace.run_span(
                "contextualization_agent",
                "original_text + amendment_text",
                lambda: contextualizer.run(original_text, amendment_text, callbacks=callbacks),
                metadata={"agent": "ContextualizationAgent", "model": contextualizer.model},
                label="🧭 Agente 1 · Contextualización (mapa de secciones)",
            )

            # --- Etapa 4: Extraccion (Agente 2) ---
            extractor = ExtractionAgent()
            output = trace.run_span(
                "extraction_agent",
                "context_map + original_text + amendment_text",
                lambda: extractor.run(original_text, amendment_text, context_map, callbacks=callbacks),
                metadata={"agent": "ExtractionAgent", "model": extractor.model},
                label="🔍 Agente 2 · Extracción de cambios (adiciones/eliminaciones/modificaciones)",
            )

            # --- Etapa 5: Validacion Pydantic (frontera final de produccion) ---
            output = trace.run_span(
                "pydantic_validation",
                "ContractChangeOutput",
                lambda: validate_contract_change_output(output.model_dump(mode="json")),
                metadata={"schema": "ContractChangeOutput"},
                label="✅ Validación final con Pydantic",
            )

            trace.success = True

            # URL de la traza en Langfuse (dentro del span activo).
            if client:
                try:
                    trace_url = client.get_trace_url()
                except Exception:  # noqa: BLE001 - la URL es informativa, no critica
                    trace_url = None

        return PipelineResult(
            output, trace, original_text, amendment_text, context_map, trace_url
        )

    except Exception:
        trace.success = False
        raise

    finally:
        # Asegura que los eventos pendientes se envien a Langfuse antes de salir.
        if client:
            client.flush()
