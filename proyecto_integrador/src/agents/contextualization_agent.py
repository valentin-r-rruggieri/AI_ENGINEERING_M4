"""Agente 1: ContextualizationAgent.

Por que existe este agente?
---------------------------
Un enfoque monolitico (un solo prompt que lee el contrato y extrae cambios)
es fragil: el LLM tiene que hacer demasiadas cosas a la vez (leer, entender
estructura, comparar, extraer) y comete mas alucinaciones.

La separacion en dos agentes sigue el principio de "dividir para conquistar":
- El Agente 1 (ContextualizationAgent) SOLO mapea la estructura: que
  secciones existen, como se corresponden y cual es el proposito de cada una.
  NO extrae cambios. Esto reduce el contexto que el Agente 2 tiene que
  procesar y le da un "mapa" claro para trabajar.
- El Agente 2 (ExtractionAgent) usa ese mapa para focalizarse en extraer
  los cambios con precision.

El handoff entre agentes
------------------------
El output del ContextualizationAgent es texto estructurado (no JSON), que
funciona como "mapa contextual" para el ExtractionAgent:

    ContextualizationAgent
        input:  texto_original + texto_adenda
        output: mapa contextual (texto estructurado)
                    |
                    v
    ExtractionAgent
        input:  mapa contextual + texto_original + texto_adenda
        output: ContractChangeOutput (JSON validado)

Por que el output es texto y no JSON?
- El mapa contextual es una descripcion narrativa, no un dato estructurado.
- Un texto permite al LLM expresar ambiguedades y correspondencias
  parciales que un JSON rigido no capturaria.

Como se usa LangChain
---------------------
- ChatOpenAI: cliente del LLM (gpt-4o-mini por defecto).
- SystemMessage: ancla el rol ("Analista Senior de Contratos").
- HumanMessage: pasa los textos del contrato y la adenda.
- config={"callbacks": [handler]}: Langfuse registra tokens automaticamente.
"""

from __future__ import annotations

import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# System prompt especializado para el Agente de Contextualizacion.
#
# El rol del system prompt es anclar al modelo en un rol especifico
# ("Analista Senior de Contratos") para que su output tenga la profundidad
# y el rigor esperados. Sin un system prompt, el LLM tiende a dar respuestas
# genericas.
#
# La instruccion clave es "No generes el JSON final" porque este agente
# SOLO mapea contexto. Si extrajera cambios, estaria pisando la
# responsabilidad del ExtractionAgent y violaria la separacion de roles.
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
    """Agente 1: mapea la estructura del contrato y la adenda.

    No extrae cambios. Su output es un mapa contextual en texto plano
    que el ExtractionAgent usara como guia.

    Attributes:
        use_real_api: si True, llama a OpenAI. Si False, usa mock deterministico.
        model: nombre del modelo a usar (default: gpt-4o-mini desde env).
        llm: instancia de ChatOpenAI (se crea en __init__).
    """

    def __init__(self, use_real_api: bool = False, model: str | None = None) -> None:
        self.use_real_api = use_real_api
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        # ChatOpenAI solo se instancia si vamos a llamar a la API real.
        # En modo mock no necesitamos credenciales.
        self.llm: ChatOpenAI | None = ChatOpenAI(model=self.model) if use_real_api else None

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
        if self.use_real_api and self.llm is not None:
            return self._run_with_langchain(original_text, amendment_text, callbacks)
        return self._run_mock(original_text, amendment_text)

    def _run_with_langchain(
        self,
        original_text: str,
        amendment_text: str,
        callbacks: list | None = None,
    ) -> str:
        """Llama al LLM usando LangChain ChatOpenAI.

        El HumanMessage contiene ambos textos (original + adenda) para que
        el modelo pueda compararlos y mapear correspondencias.
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

    def _run_mock(self, original_text: str, amendment_text: str) -> str:
        """Mock deterministico para clase sin API.

        El mock detecta secciones del texto de la adenda usando palabras clave
        y construye un mapa contextual basico. Es deterministico para que los
        golden cases sean comparables entre ejecuciones.
        """
        sections = _detect_sections(amendment_text)
        rows = []
        for section in sections:
            purpose = _SECTION_PURPOSES.get(section, "tema no catalogado")
            rows.append(
                f"- {section}: correspondencia directa; "
                f"proposito: {purpose}; "
                f"el agente extractor debe analizar el cambio final."
            )
        return "Mapa contextual comparado:\n" + "\n".join(rows)


# Proposito de cada tipo de seccion (usado por el mock).
_SECTION_PURPOSES = {
    "payment_terms": "monto mensual de pago",
    "duration": "duracion contractual",
    "service_territory": "territorio de operacion",
    "use_restriction": "restriccion de uso de informacion",
    "controlled_disclosure": "difusion controlada a terceros",
}


def _detect_sections(text: str) -> list[str]:
    """Detecta que secciones estan presentes en un texto usando palabras clave.

    Esta funcion es usada por el mock del ContextualizationAgent y del
    ExtractionAgent. No es un NLP sofisticado: simplemente busca keywords
    que aparecen en los documentos de prueba.

    Args:
        text: texto del contrato o adenda.

    Returns:
        Lista de identificadores de secciones detectadas.
    """
    lower = text.lower()
    sections: list[str] = []
    # Nota: evitamos keywords genericas como "clausula 1"/"clausula 2" porque
    # una adenda puede referenciar esas clausulas por numero al modificar OTRO
    # tema (ej: "clausula 2 eliminada - Restriccion de uso"), generando falsos
    # positivos. Usamos keywords semanticas propias de cada tema.
    if any(kw in lower for kw in ("quinientos", "$1.500", "monto mensual", "monto de pago")):
        sections.append("payment_terms")
    if any(kw in lower for kw in ("dieciocho", "veinticuatro", "duracion", "vigencia")):
        sections.append("duration")
    if any(kw in lower for kw in ("uruguay", "paraguay", "territorio", "alcance territorial", "clausula 1 modificada")):
        sections.append("service_territory")
    if any(kw in lower for kw in ("restriccion de uso", "clausula 2 eliminada")):
        sections.append("use_restriction")
    if any(kw in lower for kw in ("difusion", "subcontratistas", "clausula 4")):
        sections.append("controlled_disclosure")
    return sections
