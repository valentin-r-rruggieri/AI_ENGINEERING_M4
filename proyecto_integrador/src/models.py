"""Modelos Pydantic para LegalMove PIM4.

Por que Pydantic y no un dict plano?
-----------------------------------
En produccion, un sistema legal no puede recibir "cualquier JSON" del LLM.
El LLM puede alucinar campos, devolver tipos incorrectos (un string donde
esperabamos una lista) u omitir campos obligatorios.

Pydantic actua como una "frontera de produccion": si el output del LLM no
cumple el schema, se levanta un ValidationError accionable antes de que el
dato llegue a un backend, una base de datos o un reporte legal.

Como se usa
-----------
1. El ExtractionAgent devuelve un dict crudo (respuesta del LLM).
2. Se valida con ContractChangeOutput.model_validate(payload).
3. Si pasa, tenemos un objeto tipado con las 3 garantias:
   - sections_changed y topics_touched son listas no vacias.
   - summary_of_the_change tiene al menos 10 caracteres.
4. Si falla, capturamos ValidationError y devolvemos un mensaje claro.

Los 3 campos requeridos por la rubrica del PIM4
------------------------------------------------
| Campo                    | Tipo        | Restriccion          |
|--------------------------|-------------|----------------------|
| sections_changed         | List[str]   | lista no vacia       |
| topics_touched           | List[str]   | lista no vacia       |
| summary_of_the_change    | str         | min_length=10        |
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ContractChangeOutput(BaseModel):
    """Esquema de salida final del pipeline LegalMove.

    Este modelo representa el contrato de datos que el sistema garantiza
    a cualquier sistema downstream (API, base de datos, reporte legal).
    Si un payload no cumple este esquema, no se considera un resultado valido.
    """

    sections_changed: list[str] = Field(
        description=(
            "Identificadores de clausulas o secciones modificadas por la adenda. "
            "Ejemplos: ['payment_terms', 'duration', 'service_territory']."
        )
    )

    topics_touched: list[str] = Field(
        description=(
            "Temas legales o comerciales afectados por los cambios. "
            "Ejemplos: ['monto mensual', 'duracion contractual']."
        )
    )

    summary_of_the_change: str = Field(
        min_length=10,
        description=(
            "Resumen claro y detallado de los cambios introducidos por la adenda, "
            "distinguiendo adiciones, eliminaciones y modificaciones."
        ),
    )

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def non_empty_list(cls, value: list[str]) -> list[str]:
        """Valida que las listas no esten vacias y que ningun item sea un string vacio.

        Por que es necesario?
        - Un LLM podria devolver sections_changed: [] (lista vacia), lo cual
          no tiene sentido: si hay una adenda, al menos una seccion cambio.
        - Tambien podria devolver [''] (un item que es un string vacio),
          lo cual pasaria la validacion de tipo pero no aporta informacion.
        Este validator rechaza ambos casos con un mensaje accionable.
        """
        if not value:
            raise ValueError("La lista no puede estar vacia; la adenda debe afectar al menos una seccion.")
        if any(not item.strip() for item in value):
            raise ValueError("Los valores de la lista no pueden ser strings vacios.")
        return value


def validate_contract_change_output(payload: dict) -> ContractChangeOutput:
    """Valida un dict crudo contra ContractChangeOutput.

    Envuelve model_validate para convertir ValidationError (excepcion de Pydantic,
    con mensajes tecnicos) en un ValueError con un mensaje claro y accionable.
    Esto permite que el pipeline capture el error y lo registre en Langfuse
    como un fallo controlado, sin exponer detalles internos de Pydantic.

    Args:
        payload: dict crudo devuelto por el ExtractionAgent.

    Returns:
        Instancia validada de ContractChangeOutput.

    Raises:
        ValueError: si el payload no cumple el esquema, con el primer error.
    """
    from pydantic import ValidationError

    try:
        return ContractChangeOutput.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"El output no cumple ContractChangeOutput: {exc}") from exc
