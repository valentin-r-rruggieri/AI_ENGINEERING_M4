"""
E03 - Versionado de schemas MCP
AEM4L3 | Model Context Protocol

Objetivo pedagogico:
    Distinguir cambios aditivos de rupturistas y mostrar por que v1 y v2
    deben convivir durante una migracion.

Flujo:
    tool_schema_v1.json + tool_schema_v2.json
    -> payload viejo falla contra v2
    -> clasificador SemVer + adaptador v1 a v2

USE_REAL_API = False:
    Lee schemas reales y simula la eleccion de version.
USE_REAL_API = True:
    Usa LangChain bind_tools() con transferir_fondos_v1 y v2.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_json, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
SCHEMA_V1 = DATA_DIR / "tool_schema_v1.json"
SCHEMA_V2 = DATA_DIR / "tool_schema_v2.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", SCHEMA_V1)


class TransferV1(BaseModel):
    monto: str
    cuenta_destino: str


class TransferV2(BaseModel):
    monto: float
    cuenta_destino: str
    moneda: str


def classify_change(change: str, old_type: str | None, new_type: str | None, required: bool) -> tuple[Literal["aditivo", "rupturista"], str]:
    if change == "agregar_campo" and not required:
        return "aditivo", "MINOR"
    if change == "nuevo_endpoint":
        return "aditivo", "MINOR"
    if change in {"cambiar_tipo", "renombrar", "eliminar"}:
        return "rupturista", "MAJOR"
    if change == "agregar_campo" and required:
        return "rupturista", "MAJOR"
    return "aditivo", "PATCH"


def migrate_v1_to_v2(payload_v1: dict[str, Any]) -> TransferV2:
    old = TransferV1(**payload_v1)
    return TransferV2(monto=float(old.monto), cuenta_destino=old.cuenta_destino, moneda="ARS")


def choose_tool_version(query: str) -> dict[str, Any]:
    if USE_REAL_API:
        from langchain_core.tools import tool
        from langchain_openai import ChatOpenAI

        @tool
        def transferir_fondos_v1(monto: str, cuenta_destino: str) -> str:
            """Version legacy: monto como string."""
            return "ok"

        @tool
        def transferir_fondos_v2(monto: float, cuenta_destino: str, moneda: str) -> str:
            """Version nueva: monto numerico y moneda requerida."""
            return "ok"

        msg = ChatOpenAI(model=MODEL_NAME, temperature=0).bind_tools([transferir_fondos_v1, transferir_fondos_v2]).invoke(query)
        if not msg.tool_calls:
            return {"name": "sin_tool", "args": {}}
        return cast(dict[str, Any], msg.tool_calls[0])
    print("  [MOCK] Simulando eleccion de version por LangChain...")
    return {"name": "transferir_fondos_v2", "args": {"monto": 1000.0, "cuenta_destino": "CBU-123", "moneda": "ARS"}}


def main() -> None:
    ensure_data()
    schema_v1 = read_json(SCHEMA_V1)
    schema_v2 = read_json(SCHEMA_V2)

    print_title("AEM4L3 | E03 - Versionado de schemas")

    print_section(1, "CONTEXTO DEL CASO")
    print("La tool transferir_fondos cambia de v1 a v2. Los clientes viejos siguen enviando payloads v1.")
    print_file_evidence(SCHEMA_V1, "Schema v1")
    print_file_evidence(SCHEMA_V2, "Schema v2")
    print(f"v1: {schema_v1['input_schema']}")
    print(f"v2: {schema_v2['input_schema']}")

    print_section(2, "VERSION BASICA - cambiar el schema y listo")
    payload_viejo = {"monto": "1000", "cuenta_destino": "CBU-123"}
    print(f"Payload de cliente viejo: {payload_viejo}")
    try:
        TransferV2.model_validate(payload_viejo)
    except ValidationError as exc:
        print("Cliente roto al validar contra v2:")
        print(exc)

    print_section(3, "PROBLEMA DETECTADO")
    print("Cambiar tipo y agregar un campo requerido es rupturista. Sin versionado, integradores que funcionaban ayer fallan hoy.")

    print_section(4, "VERSION MEJORADA - SemVer + adaptador v1 a v2")
    cambios = [
        ("monto str->float", classify_change("cambiar_tipo", "string", "float", True)),
        ("+ moneda requerido", classify_change("agregar_campo", None, "string", True)),
        ("+ referencia opcional", classify_change("agregar_campo", None, "string", False)),
    ]
    for nombre, resultado in cambios:
        print(f"  {nombre}: {resultado[0]} -> bump {resultado[1]}")
    migrado = migrate_v1_to_v2(payload_viejo)
    print(f"Adaptador v1->v2 produce: {migrado}")
    print(f"Orquestador elige: {choose_tool_version('transferi 1000 pesos a CBU-123')}")

    print_section(5, "VALIDACION")
    assert isinstance(migrado, TransferV2)
    print("Adaptador produce TransferV2 valido.")
    bumps = [b for _, (_, b) in cambios]
    print(f"Bumps detectados: {bumps}. Si aparece MAJOR, version nueva debe convivir con la vieja.")

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: reemplazo directo de schema -> clientes rotos sin migracion.")
    print("DESPUES: v1 y v2 coexisten, SemVer comunica impacto y el adaptador permite migrar gradual.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega referencia: Optional[str] a v2 y comproba que es MINOR.")
    print("2. Escribi el changelog de v1.0.0 a v2.0.0.")
    print("3. Decide cuanto tiempo mantener v1 activa.")


if __name__ == "__main__":
    main()
