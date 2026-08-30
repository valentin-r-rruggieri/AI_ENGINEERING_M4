"""Instrumentación obligatoria del workflow mediante Langfuse v4.

La clase ofrece spans jerárquicos y callbacks para las llamadas realizadas por LangChain.
"""

# Importa contextmanager para actualizar automáticamente spans fallidos.
from contextlib import contextmanager
from typing import Any, Iterator

# Importa el cliente v4 y su integración oficial con LangChain.
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

# Importa configuración y error de dominio.
from .config import Settings
from .errors import ObservabilityError


class LangfuseObservability:
    """Administra una única conexión de Langfuse durante todo el pipeline."""

    # Inicializa el cliente con las credenciales ya validadas.
    def __init__(self, settings: Settings) -> None:
        self.public_key = settings.langfuse_public_key
        try:
            self.client = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                base_url=settings.langfuse_host,
                timeout=int(settings.openai_timeout_seconds),
            )
        except Exception as exc:
            raise ObservabilityError(f"No se pudo inicializar Langfuse: {exc}") from exc

    # Crea un span o agente hijo dentro del contexto activo.
    @contextmanager
    def observation(
        self,
        *,
        name: str,
        as_type: str = "span",
        input: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[Any]:
        try:
            with self.client.start_as_current_observation(
                name=name,
                as_type=as_type,
                input=input,
                metadata=metadata,
            ) as observacion:
                try:
                    yield observacion
                except Exception as exc:
                    observacion.update(
                        level="ERROR",
                        status_message=f"{type(exc).__name__}: {exc}",
                    )
                    raise
        except Exception:
            raise

    # Entrega el callback que registra automáticamente generaciones y tokens de LangChain.
    def callback_handler(self) -> Any:
        return CallbackHandler(public_key=self.public_key)

    # Fuerza el envío antes de que el proceso de línea de comandos termine.
    def flush(self) -> None:
        try:
            self.client.flush()
        except Exception as exc:
            raise ObservabilityError(f"No se pudo enviar la traza a Langfuse: {exc}") from exc
