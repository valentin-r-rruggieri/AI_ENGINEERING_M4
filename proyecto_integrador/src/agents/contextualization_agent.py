"""Agente 1: ContextualizationAgent (PRODUCCION).

Mapea la estructura del contrato y la adenda. NO extrae cambios: produce un
"mapa contextual" en texto que el ExtractionAgent usa como guia.

Por que dos agentes?
--------------------
Un enfoque monolitico (un solo prompt que lee, entiende, compara y extrae) es
fragil y alucina mas. Separar en "mapear estructura" (Agente 1) y "extraer
cambios" (Agente 2) le da a cada uno una sola responsabilidad y mas precision.

Por que el output es texto y no JSON?
-------------------------------------
El mapa contextual es una descripcion narrativa que puede expresar ambiguedades
y correspondencias parciales que un JSON rigido no capturaria.
"""

from __future__ import annotations

import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# System prompt: ancla al modelo en el rol de "Analista Senior de Contratos" para
# que su output tenga profundidad. La instruccion "NO extraigas cambios / NO JSON"
# preserva la separacion de responsabilidades con el ExtractionAgent.
CONTEXTUALIZATION_SYSTEM_PROMPT = """\
Sos un Analista Senior de Contratos con 15 anos de experiencia en \
comparacion de documentos legales comerciales.

Tu tarea es analizar el contrato original y su adenda, y construir \
un MAPA CONTEXTUAL que servira de guia para un agente extractor.

Debes identificar:
1. Que secciones o clausulas existen en cada documento.
2. Como se corresponden entre si (directas, modificadas, nuevas, eliminadas).
3. Cual es el proposito general de cada bloque.

Reglas estrictas:
- NO extraigas los cambios finales. Eso es tarea del agente extractor.
- NO generes JSON.
- Devolve un texto estructurado y claro, organizado por secciones.
- Si hay ambiguedades o correspondencias parciales, mencionelas.
"""


class ContextualizationAgent:
    """Agente 1: mapea la estructura del contrato y la adenda (texto, no JSON).

    Attributes:
        model: nombre del modelo (default: OPENAI_MODEL del env, o gpt-4o-mini).
        llm: instancia de ChatOpenAI.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=self.model)

    def run(
        self,
        original_text: str,
        amendment_text: str,
        callbacks: list | None = None,
    ) -> str:
        """Ejecuta el agente de contextualizacion.

        Args:
            original_text: texto extraido del contrato original.
            amendment_text: texto extraido de la adenda/enmienda.
            callbacks: handlers de Langfuse para registrar la llamada.

        Returns:
            Mapa contextual como texto estructurado (no JSON).
        """
        messages = [
            SystemMessage(content=CONTEXTUALIZATION_SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"CONTRATO ORIGINAL:\n{original_text}\n\n"
                    f"ADENDA:\n{amendment_text}"
                )
            ),
        ]
        config = {"callbacks": callbacks} if callbacks else {}
        response = self.llm.invoke(messages, config=config)
        return response.content
