"""Agentes especializados que colaboran mediante un handoff explícito."""

# Expone las dos clases evaluadas para facilitar su importación desde el pipeline.
from .contextualization_agent import ContextualizationAgent
from .extraction_agent import ExtractionAgent

__all__ = ["ContextualizationAgent", "ExtractionAgent"]
