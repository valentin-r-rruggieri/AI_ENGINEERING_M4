"""Integracion con Langfuse para trazabilidad del pipeline.

Por que Langfuse?
-----------------
Sin observabilidad, un fallo en el pipeline solo dice "se rompio". Con Langfuse,
podemos ver exactamente en que span fallo, que input recibio, que output produjo,
cuanto tardo y cuantos tokens consumo. Esto es obligatorio para un entorno de
produccion legal donde cada decision debe ser auditable.

Como funciona la integracion con LangChain
------------------------------------------
Langfuse provee un CallbackHandler que se inyecta en cada llamada a ChatOpenAI
mediante el parametro config={"callbacks": [handler]}. Cuando LangChain ejecuta
el modelo, el handler registra automaticamente:
- Input (messages)
- Output (response)
- Latencia
- Token usage (prompt_tokens, completion_tokens, total_tokens)
- Costo estimado

Estructura de jerarquia de spans esperada en el dashboard de Langfuse
---------------------------------------------------------------------
    contract-analysis (trace raiz)
    |-- parse_original_contract (span)
    |-- parse_amendment_contract (span)
    |-- contextualization_agent (span)
    |-- extraction_agent (span)
    |-- pydantic_validation (span)

Cada span tiene su input, output, latencia y metadata.
"""

from __future__ import annotations

import os
from typing import Any


def get_langfuse_handler(trace_name: str = "contract-analysis") -> Any:
    """Crea un CallbackHandler de Langfuse para tracear el pipeline.

    Lee las credenciales de las variables de entorno:
    - LANGFUSE_PUBLIC_KEY
    - LANGFUSE_SECRET_KEY
    - LANGFUSE_HOST (opcional, default: cloud.langfuse.com)

    Si Langfuse no esta instalado o faltan credenciales, devuelve None.
    En ese caso, el pipeline sigue funcionando con una traza local (Trace/Span)
    definida en pipeline.py, para no bloquear el desarrollo sin observabilidad.

    Args:
        trace_name: nombre de la traza raiz en el dashboard de Langfuse.

    Returns:
        CallbackHandler de langfuse.langchain, o None si no hay configuracion.
    """
    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        print("[tracing] Langfuse no esta instalado. Se usara traza local.")
        return None

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if not public_key or not secret_key:
        print("[tracing] Faltan credenciales LANGFUSE_PUBLIC_KEY/SECRET_KEY. Se usara traza local.")
        return None

    handler = CallbackHandler(public_key=public_key)
    return handler
