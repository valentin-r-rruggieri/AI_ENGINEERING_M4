"""Modelos que definen el contrato de datos del pipeline LegalMove.

ContractChangeOutput contiene exactamente los tres campos exigidos por la rúbrica.
"""

# Importa dataclass para el resultado interno y Pydantic para el JSON evaluable.
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Define la única estructura JSON expuesta por la aplicación.
class ContractChangeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    sections_changed: list[str] = Field(
        min_length=1,
        description="Identificadores de las cláusulas o secciones modificadas.",
    )
    topics_touched: list[str] = Field(
        min_length=1,
        description="Categorías legales o comerciales afectadas por los cambios.",
    )
    summary_of_the_change: str = Field(
        min_length=20,
        description="Resumen detallado de adiciones, eliminaciones y modificaciones.",
    )

    # Limpia espacios, rechaza cadenas vacías y elimina duplicados sin alterar el orden.
    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def normalizar_listas(cls, valores: list[str]) -> list[str]:
        normalizados: list[str] = []
        vistos: set[str] = set()
        for valor in valores:
            limpio = valor.strip()
            if not limpio:
                raise ValueError("Las listas no pueden contener cadenas vacías.")
            clave = limpio.casefold()
            if clave not in vistos:
                normalizados.append(limpio)
                vistos.add(clave)
        return normalizados


# Conserva artefactos internos para auditoría sin agregarlos al JSON final.
@dataclass(frozen=True)
class PipelineResult:
    output: ContractChangeOutput
    original_text: str
    amendment_text: str
    context_map: str
