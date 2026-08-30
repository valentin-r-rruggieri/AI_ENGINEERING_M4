"""Errores de dominio con mensajes comprensibles para la defensa en vivo.

Cada excepción identifica la etapa que falló sin mostrar secretos ni trazas internas.
"""


# Agrupa todos los errores esperados de la aplicación.
class LegalMoveError(Exception):
    """Error controlado que puede mostrarse directamente al usuario."""


# Señala variables de entorno faltantes o valores de configuración inválidos.
class ConfigurationError(LegalMoveError):
    """La aplicación no puede iniciar con la configuración recibida."""


# Señala imágenes ausentes, corruptas o incompatibles.
class ImageValidationError(LegalMoveError):
    """Una imagen de entrada no cumple los requisitos del parser."""


# Señala errores producidos durante el parsing con GPT-4o Vision.
class VisionParsingError(LegalMoveError):
    """GPT-4o Vision no pudo producir una extracción utilizable."""


# Señala errores en cualquiera de los dos agentes LangChain.
class AgentExecutionError(LegalMoveError):
    """Un agente no pudo completar su responsabilidad especializada."""


# Señala una salida final que no respeta ContractChangeOutput.
class OutputValidationError(LegalMoveError):
    """El resultado del extractor no cumple el contrato Pydantic."""


# Señala que la traza obligatoria no pudo enviarse correctamente.
class ObservabilityError(LegalMoveError):
    """Langfuse no pudo registrar o enviar la ejecución."""
