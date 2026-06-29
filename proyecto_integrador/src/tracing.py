"""Integracion con Langfuse v4 para trazabilidad del pipeline (PRODUCCION).

Por que Langfuse?
-----------------
Sin observabilidad, un fallo solo dice "se rompio". Con Langfuse vemos en que
span fallo, que input recibio, que output produjo, cuanto tardo y cuantos tokens
(= costo) consumo. Obligatorio en un dominio legal auditable.

Como funciona en Langfuse v4 (basado en OpenTelemetry)
------------------------------------------------------
- El cliente se obtiene con get_client(), que lee de las variables de entorno:
  LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST.
- El CallbackHandler() de LangChain NO recibe claves: se vincula al cliente global
  y, gracias al contexto de OpenTelemetry, anida sus llamadas bajo el span activo.
- En pipeline.py envolvemos todo el pipeline en
  client.start_as_current_observation(name="contract-analysis") para que las 5
  etapas queden como spans hijos de un unico trace raiz.
"""

from __future__ import annotations

from typing import Any


def get_langfuse_client() -> Any:
    """Devuelve el cliente Langfuse si hay credenciales validas, o None.

    Lee las credenciales del entorno (LANGFUSE_PUBLIC_KEY/SECRET_KEY/HOST) y
    valida con auth_check(). Si faltan claves o la autenticacion falla, devuelve
    None y el pipeline corre solo con la traza local (degradacion elegante).
    """
    try:
        from langfuse import get_client
    except ImportError:
        print("[tracing] Langfuse no esta instalado. Se usara solo traza local.")
        return None

    try:
        client = get_client()
        if not client.auth_check():
            print("[tracing] auth_check fallo: revisa LANGFUSE_PUBLIC_KEY/SECRET_KEY/HOST.")
            return None
        return client
    except Exception as exc:  # noqa: BLE001 - cualquier fallo => degradar a traza local
        print(f"[tracing] No se pudo inicializar Langfuse ({exc}). Se usara solo traza local.")
        return None


def get_langfuse_handler() -> Any:
    """Crea el CallbackHandler de LangChain para Langfuse.

    En v4 no recibe claves: usa el cliente global ya inicializado y se anida
    automaticamente bajo el span activo de OpenTelemetry.
    """
    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        return None
    return CallbackHandler()
