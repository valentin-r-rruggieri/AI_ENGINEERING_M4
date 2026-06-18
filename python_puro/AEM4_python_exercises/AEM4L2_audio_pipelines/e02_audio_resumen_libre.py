"""
E02 - Transcripcion a resumen libre con LangChain
AEM4L2 | Audio Pipelines

Objetivo pedagogico:
    Mostrar el segundo paso del pipeline: despues de transcribir,
    el LLM puede resumir, pero el resumen libre todavia no es backend-friendly.

Flujo:
    WAV real -> Whisper real -> transcript -> ChatOpenAI -> resumen libre
"""

from __future__ import annotations

import builtins
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# Siempre API real: Whisper para ASR y ChatOpenAI para el resumen.
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

QUIET = "--quiet" in sys.argv

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")
DATA_DIR = Path(__file__).parent / "data"
AUDIO_PATH = DATA_DIR / "llamada_soporte.wav"


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    # La salida visible debe ser la conversacion real, no explicaciones impresas.
    return None


def trace(role: str, payload: str) -> None:
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


def ensure_data() -> None:
    # Regenera el dataset de audio si todavia no existe.
    if not AUDIO_PATH.exists():
        subprocess.run([sys.executable, str(DATA_DIR / "generate_audio.py")], check=True)


def transcribe_audio(audio_path: Path) -> str:
    # Primera llamada real: audio -> texto.
    from openai import OpenAI

    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=audio_file,
            language="es",
        )
    return result.text


def summarize_free_text(transcript: str) -> str:
    # Segunda llamada real: texto -> resumen libre, sin schema.
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    messages = [
        SystemMessage(content="Sos un asistente que resume llamadas de soporte en español."),
        HumanMessage(content=f"Resumi esta transcripcion en 2 oraciones:\n\n{transcript}"),
    ]
    response = llm.invoke(messages)
    return response.content if isinstance(response.content, str) else str(response.content)


def main() -> None:
    # Este ejercicio muestra una mejora sobre E01, pero todavia sin contrato de salida.
    ensure_data()
    transcript = transcribe_audio(AUDIO_PATH)
    summary = summarize_free_text(transcript)
    trace("USER", f"Transcribi `{AUDIO_PATH.name}` y genera un resumen libre.")
    trace("ASR", transcript)
    trace("LLM", summary)


if __name__ == "__main__":
    main()
