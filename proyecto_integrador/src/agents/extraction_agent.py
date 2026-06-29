"""Agente 2: ExtractionAgent.

Por que existe este agente?
---------------------------
Mientras el ContextualizationAgent mapea la estructura, el ExtractionAgent se
focaliza en una sola tarea: identificar, aislar y describir cada cambio
introducido por la adenda. Al tener el mapa contextual del Agente 1, no tiene
que "descubrir" la estructura del documento; solo debe comparar y extraer.

Que hace el ExtractionAgent?
----------------------------
1. Recibe el mapa contextual (output del Agente 1).
2. Recibe el texto del contrato original y de la adenda.
3. Identifica cambios distinguiendo 3 tipos:
   - Adiciones (clausulas nuevas que no estaban en el original).
   - Eliminaciones (clausulas del original que la adenda quita).
   - Modificaciones (clausulas que cambian de contenido).
4. Devuelve un dict con los 3 campos de ContractChangeOutput.
5. El dict se valida con Pydantic en el pipeline.

Por que with_structured_output()?
---------------------------------
LangChain ofrece with_structured_output(PydanticModel) que usa el feature
"structured outputs" / "function calling" de OpenAI. Esto le dice al modelo
que su output DEBE cumplir el esquema Pydantic, reduciendo errores de
formato. Aun asi, validamos con model_validate() despues porque:
- El modelo puede equivocarse en restricciones semanticas (ej: lista vacia).
- Pydantic es la frontera final de produccion.
"""

from __future__ import annotations

import json
import os
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from models import ContractChangeOutput, validate_contract_change_output

# Importamos la deteccion de secciones del agente de contextualizacion
# porque el mock del ExtractionAgent la reutiliza.
from agents.contextualization_agent import _detect_sections, _SECTION_PURPOSES

# System prompt especializado para el Agente de Extraccion.
#
# El rol es "Auditor Legal" (mas riguroso que "Analista Senior") porque
# este agente produce el output final que un sistema de produccion usara.
#
# La instruccion clave: "Devolve solo JSON valido" asegura que el output
# sea parseable. La distincion entre adiciones/eliminaciones/modificaciones
# enriquece el resumen para que un humano pueda auditarlo.
EXTRACTION_SYSTEM_PROMPT = """\
Sos un Auditor Legal con especializacion en comparacion de contratos \
y deteccion de cambios normativos.

Tu tarea es identificar, aislar y describir cada cambio introducido por \
la adenda respecto al contrato original, usando el mapa contextual \
proporcionado por el agente de contextualizacion.

Debes distinguir entre:
- ADICIONES: clausulas nuevas que no existian en el contrato original.
- ELIMINACIONES: clausulas del original que la adenda remueve.
- MODIFICACIONES: clausulas que cambian de contenido.

Reglas de salida:
- Devolve SOLO un JSON valido con exactamente 3 campos:
  - sections_changed: lista de identificadores de secciones modificadas.
  - topics_touched: lista de temas legales/comerciales afectados.
  - summary_of_the_change: resumen detallado de los cambios (minimo 10 caracteres).
- No incluyas markdown, explicaciones ni texto fuera del JSON.
"""


class ExtractionAgent:
    """Agente 2: extrae cambios validados con ContractChangeOutput.

    Attributes:
        use_real_api: si True, llama a OpenAI. Si False, usa mock deterministico.
        model: nombre del modelo a usar (default: gpt-4o-mini desde env).
        llm: instancia de ChatOpenAI (se crea en __init__).
    """

    def __init__(self, use_real_api: bool = False, model: str | None = None) -> None:
        self.use_real_api = use_real_api
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm: ChatOpenAI | None = ChatOpenAI(model=self.model) if use_real_api else None

    def run(
        self,
        original_text: str,
        amendment_text: str,
        context_map: str,
        callbacks: list | None = None,
    ) -> ContractChangeOutput:
        """Ejecuta el agente de extraccion.

        Args:
            original_text: texto extraido del contrato original.
            amendment_text: texto extraido de la adenda/enmienda.
            context_map: mapa contextual (output del ContextualizationAgent).
            callbacks: handlers de Langfuse para registrar la llamada.

        Returns:
            Instancia validada de ContractChangeOutput.
        """
        if self.use_real_api and self.llm is not None:
            raw = self._run_with_langchain(original_text, amendment_text, context_map, callbacks)
        else:
            raw = self._run_mock(amendment_text)
        # La validacion con Pydantic es la frontera de produccion.
        # Si el LLM devolvio un JSON con tipos incorrectos o campos faltantes,
        # validate_contract_change_output levanta un ValueError accionable.
        return validate_contract_change_output(raw)

    def _run_with_langchain(
        self,
        original_text: str,
        amendment_text: str,
        context_map: str,
        callbacks: list | None = None,
    ) -> dict[str, Any]:
        """Llama al LLM usando LangChain ChatOpenAI.

        El HumanMessage contiene los 3 inputs del agente:
        1. El mapa contextual (guia del Agente 1).
        2. El texto del contrato original (para comparar).
        3. El texto de la adenda (donde estan los cambios).

        El modelo devuelve texto plano (que deberia ser JSON). Lo parseamos
        con json.loads. Si el JSON es invalido, json.loads levanta un error
        que se captura en el pipeline como un fallo controlado.
        """
        messages = [
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"MAPA CONTEXTUAL:\n{context_map}\n\n"
                    f"CONTRATO ORIGINAL:\n{original_text}\n\n"
                    f"ADENDA:\n{amendment_text}"
                )
            ),
        ]
        config = {"callbacks": callbacks} if callbacks else {}
        response = self.llm.invoke(messages, config=config)
        return json.loads(response.content)

    def _run_mock(self, amendment_text: str) -> dict[str, Any]:
        """Mock deterministico para clase sin API.

        El mock detecta secciones en el texto de la adenda y construye
        un payload que cumple ContractChangeOutput. Usa los golden cases
        cuando reconoce el patron de cambios (simple o complejo).
        """
        sections = _detect_sections(amendment_text)

        # Caso simple: solo cambia la duracion.
        if sections == ["duration"]:
            return {
                "sections_changed": ["duration"],
                "topics_touched": ["duracion contractual"],
                "summary_of_the_change": "La duracion del contrato se extiende de 12 a 18 meses.",
            }

        # Caso complejo: precio + duracion + territorio.
        if set(sections) == {"payment_terms", "duration", "service_territory"}:
            return {
                "sections_changed": ["payment_terms", "duration", "service_territory"],
                "topics_touched": [
                    "monto mensual",
                    "duracion contractual",
                    "territorio de operacion",
                ],
                "summary_of_the_change": (
                    "El monto mensual sube de $1.000 a $1.500. "
                    "La duracion se extiende de 12 a 24 meses. "
                    "El territorio se amplia de Argentina a Argentina, Uruguay y Paraguay."
                ),
            }

        # Caso complejo de confidencialidad: territorio + eliminacion + adicion.
        if set(sections) == {"service_territory", "use_restriction", "controlled_disclosure"}:
            return {
                "sections_changed": [
                    "service_territory",
                    "use_restriction",
                    "controlled_disclosure",
                ],
                "topics_touched": [
                    "alcance territorial",
                    "restriccion de uso",
                    "difusion controlada a terceros",
                ],
                "summary_of_the_change": (
                    "Modificacion: el alcance territorial se amplia de Argentina a Argentina, "
                    "Uruguay y Paraguay. Eliminacion: se remueve la clausula de restriccion "
                    "de uso, permitiendo uso sin limite temporal. Adicion: se incorpora una "
                    "clausula nueva de difusion controlada a subcontratistas bajo acuerdo previo."
                ),
            }

        # Fallback: cambio generico no catalogado.
        return {
            "sections_changed": sections or ["unknown"],
            "topics_touched": [
                _SECTION_PURPOSES.get(s, "tema no catalogado") for s in sections
            ] or ["tema no catalogado"],
            "summary_of_the_change": "Se detecto una modificacion contractual que requiere revision humana.",
        }
