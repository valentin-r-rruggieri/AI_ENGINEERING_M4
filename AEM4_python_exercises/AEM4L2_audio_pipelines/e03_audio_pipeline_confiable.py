"""
E03 — Pipeline de audio confiable con gate de calidad
AEM4L2 | Audio Pipelines

Objetivo pedagógico:
    Un resumen basado en mala transcripción es peor que no tener resumen.
    WER actúa como "reliability gate": si la calidad no alcanza el umbral,
    el pipeline para y envía a revisión humana.
    LangChain solo procesa los audios que superaron el gate.

Flujo:
    3 archivos WAV → transcribir (Whisper o mock) → calcular WER
    → gate: WER <= 0.20 → LangChain summarize → ReliableSummary
    → gate: WER > 0.20  → marcar como no confiable → revisión humana

USE_REAL_API = False → lee los 3 WAV reales + transcripts de referencia + mock
USE_REAL_API = True  → Whisper + LangChain reales
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

load_dotenv()

USE_REAL_API  = False
MODEL_NAME    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AUDIO_MODEL   = os.getenv("OPENAI_AUDIO_MODEL", "whisper-1")
DATA_DIR      = Path(__file__).parent / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

WER_THRESHOLD = 0.20  # gate de calidad


def ensure_data() -> None:
    if not (DATA_DIR / "llamada_soporte.wav").exists():
        print("Archivos de audio no encontrados. Generando...")
        subprocess.run([sys.executable, str(DATA_DIR / "generate_audio.py")], check=True)
        print()

ensure_data()


# ============================================================
# 1. CONTEXTO DEL CASO
# ============================================================

print("=" * 60)
print("AEM4L2 | E03 — Pipeline de audio confiable")
print("=" * 60)
print(f"""
CASO:
  El sistema de soporte recibe grabaciones con distinta calidad.
  ¿Qué hacemos con el resumen cuando la transcripción es mala?

WER como reliability gate:
  WER <= {WER_THRESHOLD:.0%} → confiable → generar resumen con LangChain
  WER >  {WER_THRESHOLD:.0%} → no confiable → enviar a revisión humana

Archivos de audio:
""")

for f in ["llamada_soporte.wav", "indicacion_medica.wav", "reunion_equipo.wav"]:
    p = DATA_DIR / f
    if p.exists():
        print(f"  {f}: {p.stat().st_size // 1024} KB")


# ============================================================
# 2. VERSIÓN BÁSICA — siempre genera el resumen
# ============================================================

print("\n=== VERSIÓN BÁSICA — Siempre resume, sin importar la calidad ===")
print()

def basic_pipeline(transcript: str) -> str:
    return f"Resumen generado de: '{transcript[:40]}...'"

# Simular 3 casos de calidad distinta
casos_basico = [
    "Hola llamo porque el pedido cuatro cinco dos uno no llegó.",
    "Hola yamo prq el pddo 4521 no lyegó.",          # ASR con mucho ruido
    "aaa bbb ccc ddd 4521 eee fff ggg.",              # ASR inutilizable
]
for t in casos_basico:
    r = basic_pipeline(t)
    print(f"  Entrada: '{t[:45]}'")
    print(f"  Resumen: '{r}'")
    print()

print("  Problema: el tercer resumen es basura pero el agente no lo sabe.")


# ============================================================
# 3. WER reutilizado del E02
# ============================================================

def tokenize(text: str) -> List[str]:
    return text.lower().split()


def calculate_wer(reference: str, hypothesis: str) -> float:
    ref_words = tokenize(reference)
    hyp_words = tokenize(hypothesis)
    n = len(ref_words)
    if n == 0:
        return 0.0
    m = len(hyp_words)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp[n][m] / n


# ============================================================
# 4. SCHEMA PYDANTIC
# ============================================================

class ReliableSummary(BaseModel):
    """
    Schema que incluye el resumen + la evaluación de confiabilidad.
    Si is_reliable = False, el resumen no debe usarse para tomar decisiones.
    """
    case_id: str
    audio_file: str
    reference_transcript: str
    asr_transcript: str
    wer: float = Field(..., ge=0.0)
    summary: str = Field(..., description="Resumen o mensaje de no-confiable")
    is_reliable: bool
    reason: str
    human_review_required: bool
    risk_level: str


# ============================================================
# 5. VERSIÓN MEJORADA — pipeline con gate
# ============================================================

print("\n=== VERSIÓN MEJORADA — Pipeline con reliability gate ===")
print()

print("""
Arquitectura:

    WAV → transcribir (Whisper) → WER vs referencia
                                    │
                   ┌────────────────┴────────────────┐
                   ▼ WER <= 20%                       ▼ WER > 20%
         LangChain summarize               [RESUMEN NO GENERADO]
         → ReliableSummary                → revisión humana
           is_reliable = True               is_reliable = False
""")


def transcribe_audio(audio_path: Path, reference_path: Path) -> str:
    """Transcribe el audio. Si USE_REAL_API=False, usa el transcript de referencia."""
    if USE_REAL_API:
        from openai import OpenAI
        client = OpenAI()
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=AUDIO_MODEL, file=f, language="es"
            )
        return result.text
    else:
        return reference_path.read_text(encoding="utf-8").strip()


def summarize_with_langchain(transcript: str) -> str:
    """
    Resumen con LangChain. Solo se llama cuando WER supera el gate.
    """
    if USE_REAL_API:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Sos un sistema de resumen de llamadas de soporte. "
                "Generá un resumen conciso en 2-3 oraciones indicando el problema y la urgencia."
            ),
            ("user", "Transcripción:\n{transcript}"),
        ])
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"transcript": transcript})
    else:
        # MOCK — simula el resumen del LLM
        words = transcript.split()[:6]
        return (
            f"El cliente contactó soporte con una consulta sobre: '{' '.join(words)}...' "
            f"Se requiere atención del equipo de logística."
        )


def process_audio_with_gate(
    case_id: str,
    audio_path: Path,
    reference_path: Path,
    wer_threshold: float = WER_THRESHOLD,
) -> ReliableSummary:
    """
    Pipeline completo: transcribir → WER gate → resumir con LangChain si pasa.
    """
    print(f"  Procesando {audio_path.name}...")
    reference = reference_path.read_text(encoding="utf-8").strip()
    hypothesis = transcribe_audio(audio_path, reference_path)
    wer = calculate_wer(reference, hypothesis)

    if wer <= wer_threshold:
        summary = summarize_with_langchain(hypothesis)
        return ReliableSummary(
            case_id=case_id,
            audio_file=audio_path.name,
            reference_transcript=reference,
            asr_transcript=hypothesis,
            wer=wer,
            summary=summary,
            is_reliable=True,
            human_review_required=False,
            reason=f"WER {wer:.2%} dentro del umbral ({wer_threshold:.0%}). Resumen generado.",
            risk_level="low" if wer <= 0.05 else "medium",
        )
    else:
        return ReliableSummary(
            case_id=case_id,
            audio_file=audio_path.name,
            reference_transcript=reference,
            asr_transcript=hypothesis,
            wer=wer,
            summary=f"[NO GENERADO — WER {wer:.2%} supera el umbral {wer_threshold:.0%}]",
            is_reliable=False,
            human_review_required=True,
            reason=f"WER {wer:.2%} supera el umbral ({wer_threshold:.0%}). Revisión humana requerida.",
            risk_level="high",
        )


# ============================================================
# 6. VALIDACIÓN — los 3 casos reales
# ============================================================

print("\n=== VALIDACIÓN — Los 3 archivos WAV ===")
print()

# Para simular distintas calidades de ASR, construimos hypothesis con distintos WER
CASOS_HIPOTESIS = {
    "llamada_soporte": lambda ref: ref,  # ASR perfecto (WER=0)
    "indicacion_medica": lambda ref: ref.replace("ocho", "dos", 1),  # 1 error (WER~5%)
    "reunion_equipo": lambda ref: " ".join(ref.split()[::2]),  # 50% palabras omitidas (WER~50%)
}

resultados: list[ReliableSummary] = []

for name, mutate_fn in CASOS_HIPOTESIS.items():
    audio_path = DATA_DIR / f"{name}.wav"
    ref_path   = TRANSCRIPTS_DIR / f"{name}_reference.txt"
    if not audio_path.exists() or not ref_path.exists():
        continue

    # Sobreescribir transcribe_audio para el mock de calidad variable
    original_transcribe = transcribe_audio

    def transcribe_with_quality(audio_path=audio_path, ref_path=ref_path, name=name):
        ref = ref_path.read_text(encoding="utf-8").strip()
        if USE_REAL_API:
            return original_transcribe(audio_path, ref_path)
        return CASOS_HIPOTESIS[name](ref)

    reference = ref_path.read_text(encoding="utf-8").strip()
    hypothesis = CASOS_HIPOTESIS[name](reference)
    wer = calculate_wer(reference, hypothesis)

    if wer <= WER_THRESHOLD:
        summary = summarize_with_langchain(hypothesis)
        result = ReliableSummary(
            case_id=f"call_{name}",
            audio_file=audio_path.name,
            reference_transcript=reference,
            asr_transcript=hypothesis,
            wer=wer,
            summary=summary,
            is_reliable=True,
            human_review_required=False,
            reason=f"WER {wer:.2%} dentro del umbral. Resumen generado con LangChain.",
            risk_level="low" if wer <= 0.05 else "medium",
        )
    else:
        result = ReliableSummary(
            case_id=f"call_{name}",
            audio_file=audio_path.name,
            reference_transcript=reference,
            asr_transcript=hypothesis,
            wer=wer,
            summary=f"[NO GENERADO — WER {wer:.2%} supera el umbral {WER_THRESHOLD:.0%}]",
            is_reliable=False,
            human_review_required=True,
            reason=f"WER {wer:.2%} supera el umbral. Revisión humana.",
            risk_level="high",
        )

    resultados.append(result)
    icon = "✓" if result.is_reliable else "✗"
    print(f"[{result.case_id}] {result.audio_file}")
    print(f"  WER:             {result.wer:.2%}")
    print(f"  Confiable:       {icon} {result.is_reliable}")
    print(f"  Revisión humana: {result.human_review_required}")
    print(f"  Riesgo:          {result.risk_level}")
    print(f"  Resumen:         {result.summary[:70]}...")
    print()


# ============================================================
# 7. ANTES VS DESPUÉS
# ============================================================

confiables = sum(1 for r in resultados if r.is_reliable)
revisiones = sum(1 for r in resultados if r.human_review_required)

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (sin gate de calidad):
    Los {len(resultados)} casos generan resumen incluyendo el de WER alto.
    El agente no sabe que el tercer resumen es basura.

  DESPUÉS (con reliability gate):
    Confiables:      {confiables}/{len(resultados)}  → LangChain generó resumen
    Revisión humana: {revisiones}/{len(resultados)}  → no se generó resumen

    El pipeline para cuando la calidad no alcanza el umbral.
    LangChain solo procesa los audios confiables.
""")


# ============================================================
# 8. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print(f"""
  Ajustá el pipeline para soportar umbrales distintos por dominio:

    THRESHOLDS = {{
        "ecommerce": 0.20,  # el umbral actual
        "medical":   0.05,  # muy estricto — errores pueden ser peligrosos
        "legal":     0.03,  # ultra estricto — documentos vinculantes
        "informal":  0.40,  # relajado — notas personales
    }}

  Modificá process_audio_with_gate() para recibir domain: str
  y buscar el umbral en el diccionario.

  Probá la indicación médica (WER ~5%) con domain="medical" vs domain="ecommerce".
  ¿En cuál pasa el gate? ¿Cuál es el correcto para el dominio médico?

  (Con API key real: USE_REAL_API = True para transcribir los WAV reales con Whisper)
""")


def main():
    pass


if __name__ == "__main__":
    main()
