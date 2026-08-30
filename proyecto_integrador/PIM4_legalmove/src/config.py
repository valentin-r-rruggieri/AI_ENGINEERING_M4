"""Carga y valida la configuración obligatoria de LegalMove.

La aplicación solo usa variables de entorno para evitar claves hardcodeadas.
"""

# Importa os para leer las variables configuradas en el archivo .env.
import os
from dataclasses import dataclass

# Importa el error específico utilizado ante credenciales faltantes.
from .errors import ConfigurationError


# Centraliza todos los valores que utilizan el parser, los agentes y Langfuse.
@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_vision_model: str
    openai_agent_model: str
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str
    openai_timeout_seconds: float
    openai_max_retries: int
    max_image_bytes: int = 20 * 1024 * 1024

    # Construye la configuración y falla temprano si una variable obligatoria falta.
    @classmethod
    def from_env(cls) -> "Settings":
        variables_requeridas = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "").strip(),
            "LANGFUSE_PUBLIC_KEY": os.getenv("LANGFUSE_PUBLIC_KEY", "").strip(),
            "LANGFUSE_SECRET_KEY": os.getenv("LANGFUSE_SECRET_KEY", "").strip(),
        }
        faltantes = [nombre for nombre, valor in variables_requeridas.items() if not valor]
        if faltantes:
            nombres = ", ".join(faltantes)
            raise ConfigurationError(
                f"Faltan variables obligatorias: {nombres}. Copiá .env.example a .env."
            )

        # Convierte timeout y reintentos con mensajes claros ante valores inválidos.
        try:
            timeout = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"))
            reintentos = int(os.getenv("OPENAI_MAX_RETRIES", "2"))
        except ValueError as exc:
            raise ConfigurationError(
                "OPENAI_TIMEOUT_SECONDS y OPENAI_MAX_RETRIES deben ser numéricos."
            ) from exc

        if timeout <= 0 or reintentos < 0:
            raise ConfigurationError(
                "El timeout debe ser mayor que cero y los reintentos no pueden ser negativos."
            )

        # Devuelve una configuración inmutable para toda la ejecución.
        return cls(
            openai_api_key=variables_requeridas["OPENAI_API_KEY"],
            openai_vision_model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o").strip() or "gpt-4o",
            openai_agent_model=os.getenv("OPENAI_AGENT_MODEL", "gpt-4o").strip() or "gpt-4o",
            langfuse_public_key=variables_requeridas["LANGFUSE_PUBLIC_KEY"],
            langfuse_secret_key=variables_requeridas["LANGFUSE_SECRET_KEY"],
            langfuse_host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com").strip(),
            openai_timeout_seconds=timeout,
            openai_max_retries=reintentos,
        )
