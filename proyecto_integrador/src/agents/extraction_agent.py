"""Agente 2: ExtractionAgent (PRODUCCION).

Toma el mapa contextual (Agente 1) + ambos textos y extrae los cambios,
distinguiendo adiciones, eliminaciones y modificaciones. Devuelve un
ContractChangeOutput ya validado.

Por que with_structured_output()?
---------------------------------
LangChain ofrece llm.with_structured_output(ModeloPydantic), que usa el feature
"structured outputs" / function calling de OpenAI. El modelo es forzado a producir
una salida que cumple el esquema Pydantic, eliminando el parseo manual de JSON
(no mas json.loads ni problemas con markdown ```json```). Aun asi, el pipeline
re-valida con Pydantic como frontera final de produccion.
"""

from __future__ import annotations

import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from models import ContractChangeOutput

# System prompt: rol "Auditor Legal" (mas riguroso que el Analista) porque produce
# el output final. Explica los 3 tipos de cambio que debe distinguir.
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

Completa los campos:
- sections_changed: identificadores cortos de las secciones modificadas
  (ej: payment_terms, duration, service_territory, use_restriction).
- topics_touched: temas legales/comerciales afectados (ej: duracion contractual).
- summary_of_the_change: resumen detallado, distinguiendo adiciones,
  eliminaciones y modificaciones (minimo 10 caracteres).
"""


class ExtractionAgent:
    """Agente 2: extrae cambios y devuelve un ContractChangeOutput validado.

    Attributes:
        model: nombre del modelo (default: OPENAI_MODEL del env, o gpt-4o-mini).
        llm: ChatOpenAI envuelto con with_structured_output(ContractChangeOutput).
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        # with_structured_output fuerza al modelo a devolver una instancia
        # de ContractChangeOutput (no texto crudo que haya que parsear).
        self.llm = ChatOpenAI(model=self.model).with_structured_output(ContractChangeOutput)

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
            Instancia de ContractChangeOutput (validada por structured output).
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
        # invoke devuelve directamente un ContractChangeOutput gracias a
        # with_structured_output. El pipeline lo re-valida como frontera final.
        return self.llm.invoke(messages, config=config)
