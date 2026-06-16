"""
E02 — WER y error crítico en ASR médico
AEM4L2 | Audio Pipelines

Objetivo pedagógico:
    WER puede ser bajo (1 palabra de 10) pero fatal en dominios críticos.
    Calculamos WER con Levenshtein + detectamos errores en términos sensibles.
    LangChain genera el informe de evaluación estructurado.

Flujo:
    archivo WAV (indicacion_medica.wav) → Whisper real
    → comparar contra transcript de referencia → calcular WER
    → LangChain chain → ASREvaluation estructurado

"""

import os
import builtins
import json
import subprocess
import sys
from pathlib import Path
from typing import List, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field

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
AUDIO_PATH    = DATA_DIR / "indicacion_medica.wav"
TRANSCRIPT_PATH = DATA_DIR / "transcripts" / "indicacion_medica_reference.txt"


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
print("AEM4L2 | E02 — WER y error crítico en ASR médico")
print("=" * 60)

# Leer transcripción de referencia
REFERENCE = TRANSCRIPT_PATH.read_text(encoding="utf-8").strip()

from openai import OpenAI

with open(AUDIO_PATH, "rb") as audio_file:
    HYPOTHESIS = OpenAI().audio.transcriptions.create(
        model=AUDIO_MODEL,
        file=audio_file,
        language="es",
    ).text

print(f"""
CASO:
  Un sistema hospitalario transcribe prescripciones médicas dictadas por voz.
  El ASR cometió UN solo error de palabra.
  ¿Es grave ese error?

Audio: {AUDIO_PATH.name} ({AUDIO_PATH.stat().st_size // 1024} KB)
Referencia (lo que dijo el médico):
  "{REFERENCE}"
Transcripción ASR real (hypothesis):
  "{HYPOTHESIS}"
Diferencia: se calcula automáticamente contra la referencia.
""")


# ============================================================
# 2. VERSIÓN BÁSICA — comparación visual
# ============================================================

print("\n=== VERSIÓN BÁSICA — Comparación visual ===")
print()

def basic_comparison(reference: str, hypothesis: str) -> None:
    if reference == hypothesis:
        print("  Los textos son idénticos. OK.")
    else:
        print("  Los textos son diferentes.")
        print("  ¿Cuánto? ¿Es grave? ¿Qué palabra cambió? — No lo sabemos.")

basic_comparison(REFERENCE, HYPOTHESIS)


# ============================================================
# 3. ALGORITMO WER — Levenshtein por palabras
# ============================================================

print("\n=== VERSIÓN MEJORADA — WER con Levenshtein ===")
print()


def tokenize(text: str) -> List[str]:
    return text.lower().split()


def levenshtein_distance(ref_words: List[str], hyp_words: List[str]) -> tuple[int, int, int]:
    """
    Distancia de edición entre dos listas de palabras (DP).
    Devuelve: (sustituciones, deleciones, inserciones)
    """
    n = len(ref_words)
    m = len(hyp_words)

    # Tabla DP: dp[i][j] = costo mínimo para transformar ref[:i] en hyp[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i  # i deleciones
    for j in range(m + 1):
        dp[0][j] = j  # j inserciones

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # sustitución
                    dp[i - 1][j],      # deleción
                    dp[i][j - 1],      # inserción
                )

    # Backtrace para contar por tipo
    substitutions = deletions = insertions = 0
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_words[i - 1] == hyp_words[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            substitutions += 1
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            deletions += 1
            i -= 1
        else:
            insertions += 1
            j -= 1

    return substitutions, deletions, insertions


def calculate_wer(reference: str, hypothesis: str) -> tuple[float, int, int, int]:
    """WER = (S + D + I) / N  donde N = palabras en la referencia."""
    ref_words = tokenize(reference)
    hyp_words = tokenize(hypothesis)
    s, d, ins = levenshtein_distance(ref_words, hyp_words)
    n = len(ref_words)
    wer = (s + d + ins) / n if n > 0 else 0.0
    return wer, s, d, ins


wer, subs, dels, ins = calculate_wer(REFERENCE, HYPOTHESIS)
n_ref = len(tokenize(REFERENCE))

print(f"Referencia ({n_ref} palabras):")
print(f"  \"{REFERENCE[:60]}...\"")
print()
print(f"Hypothesis:")
print(f"  \"{HYPOTHESIS[:60]}...\"")
print()
print(f"  Sustituciones (S): {subs}  ← 'ocho' → 'dos'")
print(f"  Deleciones    (D): {dels}")
print(f"  Inserciones   (I): {ins}")
print(f"  N (ref words):     {n_ref}")
print()
print(f"  WER = ({subs} + {dels} + {ins}) / {n_ref} = {wer:.4f} = {wer:.2%}")


# ============================================================
# 4. DETECCIÓN DE ERROR CRÍTICO
# ============================================================

CRITICAL_MEDICAL_TERMS = {
    "ocho", "dos", "tres", "cuatro", "seis", "doce", "veinticuatro",
    "miligramos", "microgramos", "mililitros",
    "diario", "semanal", "mensual",
    "no", "sin",
}


def detect_critical_error(reference: str, hypothesis: str) -> tuple[bool, str]:
    """Detecta si alguna sustitución toca términos críticos del dominio."""
    ref_set = set(tokenize(reference))
    hyp_set = set(tokenize(hypothesis))
    missing = ref_set - hyp_set
    extra   = hyp_set - ref_set
    crit_missing = missing & CRITICAL_MEDICAL_TERMS
    crit_extra   = extra   & CRITICAL_MEDICAL_TERMS

    if crit_missing or crit_extra:
        return True, (
            f"ERROR CRÍTICO: términos médicos afectados. "
            f"Eliminados de referencia: {crit_missing or '∅'}. "
            f"Aparecidos en hypothesis: {crit_extra or '∅'}. "
            f"Puede cambiar dosis o frecuencia del tratamiento."
        )
    return False, "Sin errores críticos detectados."


is_critical, explanation = detect_critical_error(REFERENCE, HYPOTHESIS)


# ============================================================
# 5. SCHEMA + LANGCHAIN REPORT
# ============================================================

class ASREvaluation(BaseModel):
    reference: str = Field(..., description="Texto de referencia (ground truth)")
    hypothesis: str = Field(..., description="Texto del ASR")
    wer: float = Field(..., ge=0.0, description="Word Error Rate")
    substitutions: int = Field(..., ge=0)
    deletions: int = Field(..., ge=0)
    insertions: int = Field(..., ge=0)
    critical_error: bool = Field(..., description="True si el error afecta términos críticos del dominio")
    explanation: str = Field(..., description="Explicación del error crítico si aplica")
    domain_risk: str = Field(..., description="Nivel de riesgo en el dominio: low / medium / high / critical")


def build_evaluation_report(
    reference: str,
    hypothesis: str,
    wer_val: float,
    s: int, d: int, i: int,
    is_crit: bool,
    expl: str,
) -> ASREvaluation:
    """
    Construye el informe de evaluación.
    Usa LangChain para generar el análisis narrativo.
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    structured_llm = llm.with_structured_output(ASREvaluation)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Sos un auditor de calidad de sistemas ASR médicos. "
            "Evaluá la transcripción e identificá si hay errores críticos."
        ),
        (
            "user",
            "Referencia: {reference}\n"
            "Hypothesis: {hypothesis}\n"
            "WER calculado: {wer:.2%}\n"
            "Sustituciones: {s}, Deleciones: {d}, Inserciones: {ins}\n"
            "Error crítico detectado: {is_crit}\n"
            "Explicación: {expl}\n\n"
            "Generá el informe completo de evaluación."
        ),
    ])
    chain = prompt | structured_llm
    return cast(ASREvaluation, chain.invoke({
        "reference": reference,
        "hypothesis": hypothesis,
        "wer": wer_val,
        "s": s, "d": d, "ins": i,
        "is_crit": is_crit,
        "expl": expl,
    }))
evaluation = build_evaluation_report(
    REFERENCE, HYPOTHESIS, wer, subs, dels, ins, is_critical, explanation
)

print()
print("=== INFORME DE EVALUACIÓN ===")
print(f"  WER:             {evaluation.wer:.2%}")
print(f"  Sustituciones:   {evaluation.substitutions}")
print(f"  Error crítico:   {evaluation.critical_error}")
print(f"  Riesgo dominio:  {evaluation.domain_risk}")
print(f"  Explicación:     {evaluation.explanation[:90]}...")

# Tabla de interpretación WER
print()
print("Interpretación del WER en dominio médico:")
wer_table = [
    (0.03, "Excelente — apto para prescripciones"),
    (0.08, "Bueno — revisión ocasional recomendada"),
    (0.15, "Aceptable — SOLO para notas no críticas"),
    (float("inf"), "INACEPTABLE — no usar en contexto médico"),
]
for threshold, label in wer_table:
    if evaluation.wer <= threshold:
        print(f"  WER {evaluation.wer:.2%} → {label}")
        break


# ============================================================
# 6. ANTES VS DESPUÉS
# ============================================================

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (comparación visual):
    "Los textos son diferentes." — fin del análisis.
    No sabemos si el error es grave o no.

  DESPUÉS (WER + ASREvaluation):
    WER:             {evaluation.wer:.2%}  (solo 1 palabra de {n_ref} está mal)
    Error crítico:   {evaluation.critical_error}
    Riesgo dominio:  {evaluation.domain_risk}
    Motivo:          'ocho' → 'dos' en dosis médica → 3x la frecuencia

    Conclusión: WER bajo NO significa error aceptable en dominios críticos.
""")


# ============================================================
# 7. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print("""
  1. Lee el archivo data/transcripts/indicacion_medica_reference.txt
     y cambiá "miligramos" → "gramos" (10x la dosis).
     ¿Cuánto sube el WER? ¿Es un error crítico?

  2. Extendé la detección para el dominio financiero:
     CRITICAL_FINANCIAL_TERMS = {
         "mil", "millón", "billón",
         "comprar", "vender", "transferir",
         "dólares", "pesos", "euros",
     }
     Transcript financiero:
       reference  = "transferir un millón de pesos a la cuenta cuatro cinco dos uno"
       hypothesis = "transferir un mil de pesos a la cuenta cuatro cinco dos uno"
     ¿Cuál es el WER? ¿Es un error crítico financiero?

  3. Con OPENAI_API_KEY configurada, Whisper transcribe el WAV real y el modelo evalúa la calidad.
""")

trace_text("REFERENCE", REFERENCE)
trace_text("ASR", HYPOTHESIS)
trace_json("METRICS", {
    "wer": evaluation.wer,
    "substitutions": evaluation.substitutions,
    "deletions": evaluation.deletions,
    "insertions": evaluation.insertions,
    "critical_error": evaluation.critical_error,
    "domain_risk": evaluation.domain_risk,
    "explanation": evaluation.explanation,
})


def main():
    pass


if __name__ == "__main__":
    main()
