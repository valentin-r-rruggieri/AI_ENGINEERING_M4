"""Entry point CLI para el pipeline LegalMove (PRODUCCION).

Uso
---
    # Requiere OPENAI_API_KEY (y opcionalmente claves de Langfuse) en .env
    python src/main.py \
        data/test_contracts/pair1_simple/contrato_original.png \
        data/test_contracts/pair1_simple/adenda_simple.png

    # Sin enviar a Langfuse:
    python src/main.py contrato.png adenda.png --no-langfuse

Argumentos
----------
- original_path (posicional): ruta a la imagen del contrato original.
- amendment_path (posicional): ruta a la imagen de la adenda/enmienda.
- --no-langfuse: desactiva el envio de trazas a Langfuse (por defecto: activo).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from pipeline import run_pipeline


def main() -> None:
    """Entry point del CLI. Parsea argumentos y ejecuta el pipeline real."""
    # Carga OPENAI_API_KEY, LANGFUSE_* y demas variables desde .env.
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    parser = argparse.ArgumentParser(
        description="LegalMove PIM4 - Comparador de contratos con Vision y Agentes (produccion).",
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
        "--no-langfuse",
        action="store_true",
        help="Desactiva el envio de trazas a Langfuse (por defecto esta activo).",
    )
    args = parser.parse_args()

    print("=" * 78)
    print("LegalMove PIM4 - Pipeline de comparacion de contratos (PRODUCCION)")
    print("=" * 78)
    print(f"  Contrato original: {args.original_path}")
    print(f"  Adenda:            {args.amendment_path}")
    print(f"  Langfuse:          {'INACTIVO (--no-langfuse)' if args.no_langfuse else 'ACTIVO (si hay credenciales)'}")
    print()

    result = run_pipeline(
        original_path=args.original_path,
        amendment_path=args.amendment_path,
        use_langfuse=not args.no_langfuse,
    )

    print("=" * 78)
    print("TRAZA DE EJECUCION (local)")
    print("=" * 78)
    result.trace.print_tree()

    print()
    print("=" * 78)
    print("OUTPUT FINAL (ContractChangeOutput validado)")
    print("=" * 78)
    print(json.dumps(result.output.model_dump(mode="json"), ensure_ascii=False, indent=2))

    if result.trace_url:
        print()
        print(f"[Langfuse] Traza completa con tokens y latencia:\n           {result.trace_url}")


if __name__ == "__main__":
    main()
