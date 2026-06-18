"""
E01 - Audio a transcripcion basica con Whisper real
AEM4L2 | Audio Pipelines

Objetivo pedagogico:
    Mostrar la primera pieza de cualquier pipeline de audio:
    un archivo WAV entra al ASR y vuelve texto crudo.

Flujo:
    archivo WAV real -> OpenAI audio.transcriptions -> texto ASR
"""

from __future__ import annotations

import builtins
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# En clases en español conviene fijar UTF-8 para que acentos y signos se vean bien.
reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# Cargamos la API key desde .env. No hay modo mock: la clase usa API real.
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

# --quiet permite validar/importar el archivo sin imprimir trazas.
QUIET = "--quiet" in sys.argv

# El modelo de audio queda configurable para poder comparar modelos sin tocar codigo.
AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")

# Rutas relativas al archivo para que funcione desde la raiz del repo o desde VS Code.
DATA_DIR = Path(__file__).parent / "data"
AUDIO_PATH = DATA_DIR / "llamada_soporte.wav"
REFERENCE_PATH = DATA_DIR / "transcripts" / "llamada_soporte_reference.txt"


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    # Evita salida pedagogica accidental: la consola queda solo con trazas reales.
    return None


def trace(role: str, payload: str) -> None:
    # Formato estilo agente: el usuario pide y el ASR responde.
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


def ensure_data() -> None:
    # Si el WAV no existe, generamos audios hablados con TTS local de macOS.
    if not AUDIO_PATH.exists():
        subprocess.run([sys.executable, str(DATA_DIR / "generate_audio.py")], check=True)


def transcribe_audio(audio_path: Path) -> str:
    # Import local para que el bloque donde ocurre la llamada real sea facil de señalar.
    from openai import OpenAI

    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=audio_file,
            language="es",
        )
    return result.text


def main() -> None:
    # E01 solo demuestra ASR: nada de resumen, nada de Pydantic todavia.
    ensure_data()
    reference = REFERENCE_PATH.read_text(encoding="utf-8").strip()
    transcript = transcribe_audio(AUDIO_PATH)
    trace("USER", f"Transcribi el audio `{AUDIO_PATH.name}` en español.")
    trace("REFERENCE", reference)
    trace("ASR", transcript)


if __name__ == "__main__":
    main()
