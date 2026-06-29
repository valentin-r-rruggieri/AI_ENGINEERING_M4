"""Entry point CLI para el pipeline LegalMove.

Como se usa
-----------
Desde la linea de comandos, ejecutar:

    # Modo mock (sin API, para clase):
    python src/main.py \
        data/test_contracts/pair1_simple/contrato_original.png \
        data/test_contracts/pair1_simple/adenda_simple.png

    # Modo real (con OpenAI Vision + Langfuse):
    python src/main.py \
        data/test_contracts/pair2_complex/contrato_original.png \
        data/test_contracts/pair2_complex/adenda_compleja.png \
        --real-api --langfuse

Por que un main.py?
-------------------
La rubrica del PIM4 pide explicitamente un entry point que acepte dos
paths de imagenes como argumentos. main.py cumple ese requisito: acepta
los paths posicionales y opcionalmente flags para activar API real y Langfuse.

Argumentos
----------
- original_path (posicional): ruta a la imagen del contrato original.
- amendment_path (posicional): ruta a la imagen de la adenda/enmienda.
- --real-api: activa llamadas reales a OpenAI (default: mock deterministico).
- --langfuse: envia la traza a Langfuse (default: solo traza local).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from pipeline import run_pipeline


def main() -> None:
    """Entry point del CLI. Parsea argumentos y ejecuta el pipeline."""
    # Carga variables de entorno desde .env (si existe).
    # Esto permite usar OPENAI_API_KEY, LANGFUSE_* keys, etc.
    # sin hardcodearlas en el codigo.
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    parser = argparse.ArgumentParser(
        description="LegalMove PIM4 - Comparador de contratos con Vision y Agentes.",
    )
    parser.add_argument(
        "original_path",
        type=str,
        help="Ruta a la imagen del contrato original (PNG/JPG/JPEG).",
    )
    parser.add_argument(
        "amendment_path",
        type=str,
        help="Ruta a la imagen de la adenda o enmienda (PNG/JPG/JPEG).",
    )
    parser.add_argument(
        "--real-api",
        action="store_true",
        default=os.getenv("PIM4_USE_REAL_API") == "1",
        help="Usa OpenAI Vision/LLM real. Por defecto corre con mocks deterministicos.",
    )
    parser.add_argument(
        "--langfuse",
        action="store_true",
        default=os.getenv("PIM4_USE_LANGFUSE") == "1",
        help="Envia la traza a Langfuse si hay credenciales configuradas.",
    )
    args = parser.parse_args()

    print("=" * 78)
    print("LegalMove PIM4 - Pipeline de comparacion de contratos")
    print("=" * 78)
    print(f"  Contrato original: {args.original_path}")
    print(f"  Adenda:            {args.amendment_path}")
    print(f"  Modo API:          {'REAL (OpenAI)' if args.real_api else 'MOCK (deterministico)'}")
    print(f"  Langfuse:          {'ACTIVO' if args.langfuse else 'INACTIVO (solo traza local)'}")
    print()

    # Ejecutar el pipeline completo.
    result = run_pipeline(
        original_path=args.original_path,
        amendment_path=args.amendment_path,
        use_real_api=args.real_api,
        use_langfuse=args.langfuse,
    )

    # Imprimir la traza jerarquica (spans con latencia y estado).
    print("=" * 78)
    print("TRAZA DE EJECUCION")
    print("=" * 78)
    result.trace.print_tree()

    # Imprimir el output final validado por Pydantic.
    print()
    print("=" * 78)
    print("OUTPUT FINAL (ContractChangeOutput validado)")
    print("=" * 78)
    print(json.dumps(result.output.model_dump(mode="json"), ensure_ascii=False, indent=2))

    # Mostrar URL de Langfuse si esta activo.
    if args.langfuse:
        print()
        print("[Langfuse] Revisa el dashboard en https://cloud.langfuse.com")
        print("           para ver la traza completa con tokens y latencia.")


if __name__ == "__main__":
    main()
