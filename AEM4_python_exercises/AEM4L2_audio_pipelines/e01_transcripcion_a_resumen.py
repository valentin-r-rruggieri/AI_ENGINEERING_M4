"""
E01 — De audio WAV a resumen accionable con LangChain
AEM4L2 | Audio Pipelines

Objetivo pedagógico:
    Una transcripción plana no sirve para automatizar soporte.
    Necesitamos estructura: intención, urgencia y action items.
    LangChain + Pydantic garantizan que esa estructura siempre esté presente.

Flujo:
    archivo WAV real  →  Whisper (transcripción)
    →  LangChain chain (ChatPromptTemplate + structured_output)
    →  SupportCallSummary validado por Pydantic

"""

import os
import builtins
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

QUIET = "--quiet" in sys.argv


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    return None


def trace_text(role: str, payload: str) -> None:
    if not QUIET:
        builtins.print(f"{role}:")
        builtins.print(payload)
        builtins.print()


def trace_json(role: str, payload) -> None:  # type: ignore[no-untyped-def]
    trace_text(role, json.dumps(payload, ensure_ascii=False, indent=2, default=str))

MODEL_NAME    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AUDIO_MODEL   = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")
DATA_DIR      = Path(__file__).parent / "data"
AUDIO_PATH    = DATA_DIR / "llamada_soporte.wav"
TRANSCRIPT_PATH = DATA_DIR / "transcripts" / "llamada_soporte_reference.txt"


def ensure_data() -> None:
    if not AUDIO_PATH.exists():
        print("Archivos de audio no encontrados. Generando...")
        subprocess.run([sys.executable, str(DATA_DIR / "generate_audio.py")], check=True)
        print()

ensure_data()


# ============================================================
# 1. CONTEXTO DEL CASO
# ============================================================

print("=" * 60)
print("AEM4L2 | E01 — De audio a resumen accionable")
print("=" * 60)
print(f"""
CASO:
  Un sistema de soporte de ecommerce transcribe llamadas de clientes.
  El objetivo es que el resumen sea accionable: el agente sabe qué
  hacer sin escuchar la llamada completa.

Archivo de audio: {AUDIO_PATH.name}
  Tamaño: {AUDIO_PATH.stat().st_size // 1024} KB
  Transcripción de referencia: {TRANSCRIPT_PATH.name}
""")

# Leer la transcripción de referencia
REFERENCE_TRANSCRIPT = TRANSCRIPT_PATH.read_text(encoding="utf-8").strip()
print(f"Transcripción de referencia:\n  \"{REFERENCE_TRANSCRIPT}\"")


# ============================================================
# 2. VERSIÓN BÁSICA — devolver la transcripción cruda
# ============================================================

print("\n=== VERSIÓN BÁSICA — Solo transcripción cruda ===")
print()


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe un archivo WAV con Whisper real via OpenAI API."""
    from openai import OpenAI
    client = OpenAI()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=f,
            language="es",
        )
    return result.text
def basic_pipeline(audio_path: Path) -> str:
    """Versión básica: solo transcribir. Sin estructura."""
    transcript = transcribe_audio(audio_path)
    return transcript


resultado_basico = basic_pipeline(AUDIO_PATH)
print(f"Output básico (transcripción cruda):\n  \"{resultado_basico}\"")

print()
print("¿Qué NO hay en este output?")
print("  - Intención del cliente → imposible enrutar automáticamente")
print("  - Urgencia → imposible priorizar tickets")
print("  - Action items → el agente tiene que re-escuchar la llamada")


# ============================================================
# 3. PROBLEMA DETECTADO
# ============================================================

print("\n=== PROBLEMA DETECTADO ===")
print("""
Sin estructura, el sistema de soporte no puede:
  1. Priorizar tickets automáticamente por urgencia
  2. Asignar al agente correcto (logística vs. facturación)
  3. Mostrar los próximos pasos al agente sin escuchar la llamada
  4. Medir cuántos "delivery_claim" recibimos por día
  5. Detectar picos de ciertos tipos de reclamos en tiempo real
""")


# ============================================================
# 4. VERSIÓN MEJORADA — LangChain + SupportCallSummary
# ============================================================

print("\n=== VERSIÓN MEJORADA — LangChain + SupportCallSummary ===")
print()

print("""
Patrón:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(SupportCallSummary)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sos un analizador de llamadas de soporte..."),
        ("user", "Transcripción: {transcript}"),
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"transcript": transcript})
    # → instancia SupportCallSummary validada por Pydantic
""")


class SupportCallSummary(BaseModel):
    """
    Schema estructurado para el resumen de llamada de soporte.
    LangChain con structured_output fuerza al modelo a cumplir este schema.
    """
    transcript: str = Field(..., description="Transcripción original de la llamada")
    summary: str = Field(..., min_length=20, description="Resumen conciso (mín 20 chars)")
    customer_intent: Literal[
        "delivery_claim",    # reclamo por entrega no recibida
        "cancellation",      # cancelación de pedido
        "inquiry",           # consulta general
        "complaint",         # queja sin reclamo específico
        "refund_request",    # pedido de reembolso
    ] = Field(..., description="Intención principal del cliente")
    urgency: Literal["low", "medium", "high"] = Field(..., description="Nivel de urgencia")
    action_items: List[str] = Field(..., min_length=1, description="Pasos concretos para el agente")


def summarize_call(transcript: str) -> SupportCallSummary:
    """Resumir y clasificar la llamada con LangChain y OpenAI."""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    structured_llm = llm.with_structured_output(SupportCallSummary)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Sos un analizador experto de llamadas de soporte de ecommerce. "
            "Devolvé un resumen estructurado con la intención del cliente, "
            "nivel de urgencia y los pasos de acción para el agente."
        ),
        (
            "user",
            "Transcripción de la llamada:\n{transcript}"
        ),
    ])

    chain = prompt | structured_llm
    return cast(SupportCallSummary, chain.invoke({"transcript": transcript}))

# ============================================================
# 5. VALIDACIÓN
# ============================================================

print("\n=== VALIDACIÓN ===")
print()

resumen = summarize_call(resultado_basico)
print()
print("Output estructurado (SupportCallSummary validado):")
print(f"  Transcripción:  \"{resumen.transcript[:50]}...\"")
print(f"  Resumen:        \"{resumen.summary[:70]}...\"")
print(f"  Intención:      {resumen.customer_intent}")
print(f"  Urgencia:       {resumen.urgency}")
print(f"  Action items ({len(resumen.action_items)}):")
for i, item in enumerate(resumen.action_items, 1):
    print(f"    {i}. {item}")

# Demostrar que Pydantic rechaza intenciones inválidas
print()
print("Caso de error: intención fuera del Literal:")
try:
    SupportCallSummary(
        transcript="test",
        summary="Resumen de prueba para mostrar el error de validación con Pydantic.",
        customer_intent="quiero_hablar_con_un_humano",  # type: ignore
        urgency="high",
        action_items=["paso 1"],
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  Campo '{err['loc'][0]}': {err['msg']}")


# ============================================================
# 6. ANTES VS DESPUÉS
# ============================================================

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (transcripción cruda):
    Output: "{resultado_basico[:60]}..."
    - Sin intención detectada
    - Sin urgencia → no hay priorización
    - Sin action items → el agente re-escucha toda la llamada

  DESPUÉS (LangChain + SupportCallSummary):
    customer_intent: {resumen.customer_intent}
    urgency:         {resumen.urgency}
    action_items:    {len(resumen.action_items)} pasos concretos

    El sistema prioriza automáticamente los tickets de urgencia "high".
    El agente ve los action items en segundos, sin escuchar la llamada.
""")


# ============================================================
# 7. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print("""
  1. Abrí generate_audio.py y fijate cómo está definido el transcript
     de "llamada_soporte". Luego abrí data/transcripts/llamada_soporte_reference.txt.

  2. Adaptá el pipeline para una llamada bancaria:
     Transcript de ejemplo:
       "Vi un cobro de 3500 pesos que no reconozco en mi tarjeta del mes pasado."

     Cambios al schema:
       - Agregar intención: "unauthorized_charge"
       - Agregar campo:     order_or_case_number: Optional[str]
       - Agregar campo:     estimated_resolution_days: Optional[int]

  3. Con OPENAI_API_KEY configurada:
     - El script transcribe el WAV con Whisper
     - LangChain enviará la transcripción a GPT-4o-mini
     - Recibirás el SupportCallSummary generado por el modelo real
""")

trace_text("USER", "Transcribí esta llamada de soporte y generá un resumen accionable.")
trace_text("ASR", resultado_basico)
trace_json("EXTRACT", resumen.model_dump(mode="json"))


def main():
    pass


if __name__ == "__main__":
    main()
