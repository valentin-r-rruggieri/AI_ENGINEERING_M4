"""Orquestacion del pipeline LegalMove.

El pipeline une todos los componentes:
    parse_contract_image (x2) -> ContextualizationAgent -> ExtractionAgent -> Pydantic

Por que un pipeline y no llamadas sueltas?
-----------------------------------------
Un pipeline orquestado garantiza:
1. Orden correcto: no se puede extraer antes de contextualizar.
2. Trazabilidad: cada etapa se registra en un span con input, output y latencia.
3. Manejo de errores: si una etapa falla, el span registra el error y el
   pipeline falla controladamente, no silenciosamente.
4. Reproducibilidad: el mismo input produce el mismo flujo de ejecucion.

Estructura de la traza
----------------------
La traza tiene un span raiz (contract-analysis) y spans hijos por etapa:

    contract-analysis (trace raiz)
    |-- parse_original_contract   (span: vision, latencia, tokens)
    |-- parse_amendment_contract  (span: vision, latencia, tokens)
    |-- contextualization_agent   (span: LLM, latencia, tokens)
    |-- extraction_agent          (span: LLM, latencia, tokens)
    |-- pydantic_validation       (span: validacion, latencia)

En modo real (use_real_api=True), Langfuse registra estos spans
automaticamente via CallbackHandler. En modo mock, la traza local
(Span/Trace dataclasses) replica la misma estructura para debugging.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from models import ContractChangeOutput, validate_contract_change_output
from image_parser import parse_contract_image
from agents.contextualization_agent import ContextualizationAgent
from agents.extraction_agent import ExtractionAgent
from tracing import get_langfuse_handler


@dataclass
class Span:
    """Un span representa una etapa del pipeline.

    Attributes:
        name: nombre de la etapa (ej: "parse_original_contract").
        input_preview: preview del input (truncado para legibilidad).
        output_preview: preview del output.
        latency_ms: tiempo de ejecucion en milisegundos.
        error: mensaje de error si la etapa fallo, None si exito.
        metadata: metadata adicional (tokens, modelo, etc.).
    """

    name: str
    input_preview: str
    output_preview: str = ""
    latency_ms: float = 0.0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trace:
    """Traza raiz del pipeline. Agrupa todos los spans de una ejecucion.

    Attributes:
        name: nombre de la traza (ej: "contract-analysis").
        contract_id: identificador del contrato (ej: nombre del archivo).
        spans: lista de spans hijos.
        success: True si el pipeline completo sin errores.
    """

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
        """Ejecuta una funcion dentro de un span y registra su resultado.

        Este metodo es el corazon de la trazabilidad: envuelve cualquier
        funcion en un span que mide latencia, captura el output y registra
        errores. Si la funcion falla, el span registra el error y lo
        re-lanza para que el pipeline lo maneje.

        Args:
            name: nombre del span.
            input_preview: descripcion del input (para el log).
            fn: funcion a ejecutar.
            metadata: metadata adicional para el span.

        Returns:
            El resultado de fn().
        """
        span = Span(
            name=name,
            input_preview=_preview(input_preview),
            metadata=metadata or {},
        )
        start = time.perf_counter()
        try:
            result = fn()
            span.output_preview = _preview(_dump_for_preview(result))
            return result
        except Exception as exc:
            span.error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            span.latency_ms = (time.perf_counter() - start) * 1000
            self.spans.append(span)

    def print_tree(self) -> None:
        """Imprime la traza como arbol jerarquico en la consola.

        Formato:
            Trace contract-analysis contract_id=adenda_simple success=True
              1. [OK] parse_original_contract (12 ms)
                 in : contrato_original.png
                 out: CONTRATO COMERCIAL DE SERVICIOS...
              2. [OK] contextualization_agent (45 ms)
                 ...
        """
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
        """Serializa la traza a dict (para exportar o enviar a Langfuse)."""
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
    """Resultado completo del pipeline: output + traza + textos intermedios.

    Conservar los textos intermedios (original_text, amendment_text,
    context_map) permite auditar el flujo completo: si el output final
    es incorrecto, podemos revisar cada etapa para encontrar donde fallo.
    """

    output: ContractChangeOutput
    trace: Trace
    original_text: str
    amendment_text: str
    context_map: str


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
    use_real_api: bool = False,
    use_langfuse: bool = False,
) -> PipelineResult:
    """Ejecuta el pipeline completo de comparacion de contratos.

    Flujo:
    1. parse_original_contract: extrae texto del contrato original (Vision).
    2. parse_amendment_contract: extrae texto de la adenda (Vision).
    3. contextualization_agent: mapea secciones (NO extrae cambios).
    4. extraction_agent: extrae cambios y devuelve ContractChangeOutput.
    5. pydantic_validation: valida el output final contra el esquema.

    Si use_langfuse=True, se inyecta el CallbackHandler de Langfuse en cada
    llamada a ChatOpenAI. Langfuse registra automaticamente tokens, latencia
    y costo de cada llamada al LLM, ademas de la traza local.

    Args:
        original_path: ruta a la imagen del contrato original.
        amendment_path: ruta a la imagen de la adenda/enmienda.
        use_real_api: si True, usa OpenAI. Si False, usa mocks deterministicos.
        use_langfuse: si True, envia la traza a Langfuse.

    Returns:
        PipelineResult con el output validado, la traza y los textos intermedios.

    Raises:
        Exception: si cualquier etapa falla (el span registra el error).
    """
    # El handler de Langfuse se inyecta en cada llamada a ChatOpenAI.
    # Si no hay credenciales o Langfuse no esta instalado, es None y se
    # usa solo la traza local.
    langfuse_handler = get_langfuse_handler() if use_langfuse else None
    callbacks = [langfuse_handler] if langfuse_handler else None

    # La traza local replica la jerarquia de Langfuse para debugging sin dashboard.
    trace = Trace(name="contract-analysis", contract_id=Path(amendment_path).stem)

    try:
        # --- Etapa 1: Parsing del contrato original ---
        original_text = trace.run_span(
            "parse_original_contract",
            str(original_path),
            lambda: parse_contract_image(
                original_path, "Contrato original",
                use_real_api=use_real_api, callbacks=callbacks,
            ),
            metadata={"document_label": "Contrato original", "real_api": use_real_api},
        )

        # --- Etapa 2: Parsing de la adenda ---
        amendment_text = trace.run_span(
            "parse_amendment_contract",
            str(amendment_path),
            lambda: parse_contract_image(
                amendment_path, "Adenda o enmienda",
                use_real_api=use_real_api, callbacks=callbacks,
            ),
            metadata={"document_label": "Adenda o enmienda", "real_api": use_real_api},
        )

        # --- Etapa 3: Contextualizacion (Agente 1) ---
        contextualizer = ContextualizationAgent(use_real_api=use_real_api)
        context_map = trace.run_span(
            "contextualization_agent",
            "original_text + amendment_text",
            lambda: contextualizer.run(
                original_text, amendment_text, callbacks=callbacks,
            ),
            metadata={"agent": "ContextualizationAgent", "model": contextualizer.model},
        )

        # --- Etapa 4: Extraccion (Agente 2) ---
        extractor = ExtractionAgent(use_real_api=use_real_api)
        output = trace.run_span(
            "extraction_agent",
            "context_map + original_text + amendment_text",
            lambda: extractor.run(
                original_text, amendment_text, context_map, callbacks=callbacks,
            ),
            metadata={"agent": "ExtractionAgent", "model": extractor.model},
        )

        # --- Etapa 5: Validacion Pydantic (frontera de produccion) ---
        # Aunque el ExtractionAgent ya valida internamente, este span asegura
        # que el output que llega al usuario final cumple el esquema.
        output = trace.run_span(
            "pydantic_validation",
            "raw ContractChangeOutput",
            lambda: validate_contract_change_output(output.model_dump(mode="json")),
            metadata={"schema": "ContractChangeOutput"},
        )

        trace.success = True
        return PipelineResult(output, trace, original_text, amendment_text, context_map)

    except Exception:
        # Si cualquier etapa falla, marcamos la traza como fallida.
        # El span especifico ya registro el error en trace.print_tree().
        trace.success = False
        raise
