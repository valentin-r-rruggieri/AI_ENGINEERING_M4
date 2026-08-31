"""Utilidades compartidas para los ejercicios Python de AEM4."""

from __future__ import annotations

import base64
import builtins
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


QUIET = "--quiet" in sys.argv


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    """Silencia prints pedagógicos importados desde common."""
    return None


def trace_text(role: str, payload: str) -> None:
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


def trace_json(role: str, payload: Any) -> None:
    trace_text(role, json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def require_openai_api_key() -> None:
    """Falla temprano si el ejercicio requiere OpenAI y no hay API key."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI."
        )


def run_generator(data_dir: Path, script_name: str, required_path: Path) -> None:
    """Ejecuta un generador de data si falta el archivo requerido."""
    if required_path.exists():
        return
    print(f"Data no encontrada: {required_path.name}. Generando dataset...")
    subprocess.run([sys.executable, str(data_dir / script_name)], check=True)
    print()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def print_title(title: str) -> None:
    print("=" * 72)
    print(title)
    print("=" * 72)


def print_section(number: int, title: str) -> None:
    print()
    print(f"=== {number}. {title} ===")
    print()


def preview(text: str, max_chars: int = 180) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= max_chars else clean[: max_chars - 3] + "..."


def print_file_evidence(path: Path, label: str = "Archivo") -> None:
    size = path.stat().st_size
    print(f"{label}: {path.name} ({size} bytes)")
