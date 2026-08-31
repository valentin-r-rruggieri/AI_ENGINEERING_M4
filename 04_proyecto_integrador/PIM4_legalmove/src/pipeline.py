"""Orquesta visión, handoff de agentes, validación y observabilidad.

El orden de las cinco etapas coincide exactamente con la arquitectura de la rúbrica.
"""

# Importa hashing y rutas para metadata de auditoría reproducible.
import hashlib
from pathlib import Path
from typing import Any, Callable

# Importa el cliente OpenAI directo; la generación Vision se registra manualmente.
from openai import OpenAI

# Importa Pydantic para diferenciar errores del contrato final.
from pydantic import ValidationError

# Importa los dos agentes y el resto de componentes del pipeline.
from .agents import ContextualizationAgent, ExtractionAgent
from .config import Settings
from .errors import ObservabilityError, OutputValidationError
from .image_parser import parse_contract_image
from .models import ContractChangeOutput, PipelineResult
from .observability import LangfuseObservability


# Produce metadata estable sin registrar la imagen completa en Langfuse.
def _file_metadata(path: str | Path) -> dict[str, Any]:
    ruta = Path(path).expanduser().resolve()
    contenido = ruta.read_bytes()
    return {
        "file_name": ruta.name,
        "file_size_bytes": len(contenido),
        "sha256": hashlib.sha256(contenido).hexdigest(),
    }


# Ejecuta el workflow completo y devuelve el JSON junto con artefactos auditables.
def analyze_contracts(
    original_path: str | Path,
    amendment_path: str | Path,
    *,
    settings: Settings | None = None,
    image_parser: Callable[..., str] = parse_contract_image,
    contextualization_agent: Any | None = None,
    extraction_agent: Any | None = None,
    observability: Any | None = None,
    openai_client: Any | None = None,
) -> PipelineResult:
    configuracion = settings or Settings.from_env()
    trazabilidad = observability or LangfuseObservability(configuracion)
    hubo_error = False

    # El parser actualiza el span de generación con tokens normalizados de Responses API.
    cliente_openai = openai_client or OpenAI(
        api_key=configuracion.openai_api_key,
        timeout=configuracion.openai_timeout_seconds,
        max_retries=configuracion.openai_max_retries,
    )
    agente_contexto = contextualization_agent or ContextualizationAgent(configuracion)
    agente_extractor = extraction_agent or ExtractionAgent(configuracion)
    callbacks = [trazabilidad.callback_handler()]

    try:
        # El span raíz contiene las cinco etapas evaluadas y el JSON final.
        with trazabilidad.observation(
            name="contract-analysis",
            as_type="span",
            input={"original_path": str(original_path), "amendment_path": str(amendment_path)},
            metadata={
                "vision_model": configuracion.openai_vision_model,
                "agent_model": configuracion.openai_agent_model,
            },
        ) as raiz:
            # Etapa 1: extrae fielmente el contrato original.
            with trazabilidad.observation(
                name="parse_original_contract",
                as_type="generation",
                input={"path": str(original_path), "document_label": "Contrato original"},
                metadata={"model": configuracion.openai_vision_model},
            ) as span_original:
                texto_original = image_parser(
                    original_path,
                    "Contrato original",
                    settings=configuracion,
                    client=cliente_openai,
                    observation=span_original,
                )
                span_original.update(
                    output={"extracted_text": texto_original},
                    metadata=_file_metadata(original_path),
                )

            # Etapa 2: extrae fielmente la adenda o enmienda.
            with trazabilidad.observation(
                name="parse_amendment_contract",
                as_type="generation",
                input={"path": str(amendment_path), "document_label": "Adenda"},
                metadata={"model": configuracion.openai_vision_model},
            ) as span_adenda:
                texto_adenda = image_parser(
                    amendment_path,
                    "Adenda o enmienda",
                    settings=configuracion,
                    client=cliente_openai,
                    observation=span_adenda,
                )
                span_adenda.update(
                    output={"extracted_text": texto_adenda},
                    metadata=_file_metadata(amendment_path),
                )

            # Etapa 3: el primer agente construye el mapa sin extraer cambios.
            with trazabilidad.observation(
                name="contextualization_agent",
                as_type="agent",
                input={"original_text": texto_original, "amendment_text": texto_adenda},
                metadata={"model": configuracion.openai_agent_model},
            ) as span_contexto:
                mapa_contextual = agente_contexto.run(
                    texto_original,
                    texto_adenda,
                    callbacks=callbacks,
                )
                span_contexto.update(output={"context_map": mapa_contextual})

            # Etapa 4: el segundo agente usa el handoff y produce structured output.
            with trazabilidad.observation(
                name="extraction_agent",
                as_type="agent",
                input={
                    "context_map": mapa_contextual,
                    "original_text": texto_original,
                    "amendment_text": texto_adenda,
                },
                metadata={"model": configuracion.openai_agent_model},
            ) as span_extractor:
                salida_agente = agente_extractor.run(
                    texto_original,
                    texto_adenda,
                    mapa_contextual,
                    callbacks=callbacks,
                )
                span_extractor.update(output=salida_agente.model_dump(mode="json"))

            # Etapa 5: valida explícitamente el payload antes de exponerlo al sistema.
            with trazabilidad.observation(
                name="pydantic_validation",
                input=salida_agente.model_dump(mode="json"),
                metadata={"schema": "ContractChangeOutput", "extra_fields": "forbid"},
            ) as span_validacion:
                try:
                    salida_validada = ContractChangeOutput.model_validate(
                        salida_agente.model_dump(mode="json")
                    )
                except ValidationError as exc:
                    raise OutputValidationError(
                        f"La salida final no cumple ContractChangeOutput: {exc}"
                    ) from exc
                span_validacion.update(output=salida_validada.model_dump(mode="json"))

            raiz.update(output=salida_validada.model_dump(mode="json"))
            return PipelineResult(
                output=salida_validada,
                original_text=texto_original,
                amendment_text=texto_adenda,
                context_map=mapa_contextual,
            )
    except Exception:
        hubo_error = True
        raise
    finally:
        # Intenta enviar siempre la traza; un fallo previo conserva prioridad sobre flush.
        try:
            trazabilidad.flush()
        except ObservabilityError:
            if not hubo_error:
                raise
