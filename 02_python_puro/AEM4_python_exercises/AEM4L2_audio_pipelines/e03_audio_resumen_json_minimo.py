"""
E03 - Transcripcion a JSON minimo validado
AEM4L2 | Audio Pipelines

Objetivo pedagogico:
    Dar el salto desde resumen libre hacia una estructura minima que
    un backend pueda leer: summary, urgency y action_items.

Flujo:
    WAV real -> Whisper real -> transcript -> with_structured_output()
    -> MinimalAudioSummary validado por Pydantic
"""

from __future__ import annotations

import builtins
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field

reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# La clase usa API real de OpenAI para ASR y para el LLM.
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

QUIET = "--quiet" in sys.argv

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")
DATA_DIR = Path(__file__).parent / "data"
AUDIO_PATH = DATA_DIR / "llamada_soporte.wav"


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    # Solo mostramos USER, ASR y EXTRACT.
    return None


def trace_text(role: str, payload: str) -> None:
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


def trace_json(role: str, payload) -> None:  # type: ignore[no-untyped-def]
    trace_text(role, json.dumps(payload, ensure_ascii=False, indent=2, default=str))


class MinimalAudioSummary(BaseModel):
    # Schema chico para que el alumno vea structured output antes del caso completo.
    summary: str = Field(..., min_length=20, description="Resumen breve de la llamada")
    urgency: Literal["low", "medium", "high"] = Field(..., description="Urgencia operativa del caso")
    action_items: list[str] = Field(..., min_length=1, description="Acciones concretas para el agente")


def ensure_data() -> None:
    if not AUDIO_PATH.exists():
        subprocess.run([sys.executable, str(DATA_DIR / "generate_audio.py")], check=True)


def transcribe_audio(audio_path: Path) -> str:
    # Whisper real convierte el WAV en texto antes de llamar al LLM.
    from openai import OpenAI

    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=audio_file,
            language="es",
        )
    return result.text


def extract_minimal_summary(transcript: str) -> MinimalAudioSummary:
    # LangChain transforma el transcript en un objeto validado por Pydantic.
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    structured_llm = llm.with_structured_output(MinimalAudioSummary)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Sos un analizador de llamadas de soporte. "
            "Devolve solo datos operables para un agente."
        ),
        ("user", "Transcripcion:\n{transcript}"),
    ])
    chain = prompt | structured_llm
    return cast(MinimalAudioSummary, chain.invoke({"transcript": transcript}))


def main() -> None:
    # E03 instala el patron: transcript -> schema minimo -> JSON usable.
    ensure_data()
    transcript = transcribe_audio(AUDIO_PATH)
    result = extract_minimal_summary(transcript)
    trace_text("USER", f"Transcribi `{AUDIO_PATH.name}` y extrae summary, urgency y action_items.")
    trace_text("ASR", transcript)
    trace_json("EXTRACT", result.model_dump(mode="json"))


if __name__ == "__main__":
    main()
