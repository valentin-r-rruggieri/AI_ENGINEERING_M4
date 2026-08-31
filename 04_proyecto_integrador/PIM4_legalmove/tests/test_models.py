"""Pruebas del contrato Pydantic que se devuelve por stdout."""

# Importa JSON, rutas, pytest y el único modelo JSON público.
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.models import ContractChangeOutput


# Comprueba limpieza de espacios y eliminación de duplicados.
def test_normaliza_listas_y_rechaza_campos_extra() -> None:
    salida = ContractChangeOutput.model_validate(
        {
            "sections_changed": [" Cláusula 2 ", "cláusula 2", "Cláusula 3"],
            "topics_touched": ["precio", "PRECIO", "vigencia"],
            "summary_of_the_change": "MODIFICACIÓN: se ajusta el precio y se extiende la vigencia del contrato.",
        }
    )
    assert salida.sections_changed == ["Cláusula 2", "Cláusula 3"]
    assert salida.topics_touched == ["precio", "vigencia"]

    with pytest.raises(ValidationError):
        ContractChangeOutput.model_validate({**salida.model_dump(), "extra": "no permitido"})


# Comprueba los límites mínimos exigidos por la rúbrica.
def test_rechaza_listas_vacias_y_resumen_corto() -> None:
    with pytest.raises(ValidationError):
        ContractChangeOutput.model_validate(
            {
                "sections_changed": [],
                "topics_touched": ["precio"],
                "summary_of_the_change": "Demasiado corto",
            }
        )


# Comprueba que los dos resultados esperados usan exactamente el contrato evaluable.
@pytest.mark.parametrize("caso", ["caso_simple", "caso_complejo"])
def test_expected_json_es_un_contract_change_output(caso: str) -> None:
    raiz = Path(__file__).resolve().parents[1] / "data" / "test_contracts"
    payload = json.loads((raiz / caso / "expected.json").read_text(encoding="utf-8"))
    salida = ContractChangeOutput.model_validate(payload)
    assert set(salida.model_dump()) == {
        "sections_changed",
        "topics_touched",
        "summary_of_the_change",
    }
