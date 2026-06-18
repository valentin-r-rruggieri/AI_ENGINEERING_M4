"""
E05 — Golden cases visuales: evaluación reproducible
AEM4L1 | Visión e Imágenes

Objetivo pedagógico:
    "Parece funcionar" no es suficiente en producción.
    Los golden cases miden la calidad del pipeline de forma reproducible.
    Cada caso tiene: imagen PNG real + expected JSON + 4 métricas.

Flujo:
    Para cada imagen PNG:
        encode base64 → LangChain multimodal → BankApplicationWithConfidence
        comparar con expected JSON → calcular valid_schema, accuracy, completeness, human_review_correct

"""

import os
import json
import base64
import builtins
import subprocess
import sys
from pathlib import Path
from datetime import date
from typing import Optional, Literal, cast
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# Asegura salida UTF-8 para métricas y textos en español.
reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# Carga credenciales y modelo desde .env.
load_dotenv()

# Golden cases mide el modelo real; sin API key no hay resultado válido.
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

# --quiet oculta las trazas si se corre desde un pipeline de validación.
QUIET = "--quiet" in sys.argv


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    """Silencia prints pedagógicos: la consola solo muestra trazas reales."""
    return None


def trace(role: str, payload: str) -> None:
    # Todas las salidas observables pasan por roles para comparar casos.
    if not QUIET:
        builtins.print(f"{role}:")
        builtins.print(payload)
        builtins.print()

MODEL_NAME   = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DATA_DIR     = Path(__file__).parent / "data"
EXPECTED_DIR = DATA_DIR / "expected"


def ensure_data() -> None:
    # Los golden cases dependen de imágenes y JSON esperados generados localmente.
    missing = not (DATA_DIR / "formulario_bancario_limpio.png").exists()
    if missing:
        print("Imágenes no encontradas. Generando...")
        subprocess.run([sys.executable, str(DATA_DIR / "generate_images.py")], check=True)
        print()

ensure_data()


# ============================================================
# 1. CONTEXTO DEL CASO
# ============================================================

print("=" * 60)
print("AEM4L1 | E05 — Golden cases visuales")
print("=" * 60)
print("""
CASO:
  El extractor de formularios bancarios parece funcionar.
  Alguien pregunta: "¿Qué tan bien funciona realmente?"

  Sin métricas: "Probé 3 casos y parecía ok." — No sirve en producción.
  Con golden cases: medimos 4 métricas sobre 3 imágenes reales.

IMÁGENES DE ENTRADA:
  formulario_bancario_limpio.png   → formulario claro y completo
  formulario_bancario_cafe.png     → manchas de café cubren DNI y fecha
  formulario_bancario_borroso.png  → imagen borrosa de mala calidad
""")

for f in ["formulario_bancario_limpio.png", "formulario_bancario_cafe.png", "formulario_bancario_borroso.png"]:
    p = DATA_DIR / f
    if p.exists():
        print(f"  {f}: {p.stat().st_size // 1024} KB")


# ============================================================
# 2. VERSIÓN BÁSICA — evaluación a ojo
# ============================================================

print("\n=== VERSIÓN BÁSICA — Evaluación a ojo ===")
print()
print("  Revisé los 3 outputs... parecen estar bien.")
print("  Pero no sé:")
print("    - ¿Cuántos campos son correctos en cada caso?")
print("    - ¿El modelo marcó bien requires_human_review?")
print("    - ¿Cuánto mejoró si cambio el modelo de gpt-4o-mini a gpt-4o?")
print("    - ¿Cuál de los 3 casos es el más difícil?")
print()
print("  Sin métricas: imposible responder estas preguntas.")


# ============================================================
# 3. VERSIÓN MEJORADA — Schema + pipeline + 4 métricas
# ============================================================

print("\n=== VERSIÓN MEJORADA — Golden cases con 4 métricas ===")
print()


class BankApplicationWithConfidence(BaseModel):
    # Este schema replica el contrato de E04 para medir calidad con el mismo
    # formato que usaría el pipeline de producción.
    full_name: Optional[str] = None
    document_number: Optional[str] = None
    requested_amount: Optional[float] = Field(None, gt=0)
    birth_date: Optional[date] = None
    signature_present: Optional[bool] = None
    confidence: Literal["low", "medium", "high"]
    extraction_notes: str
    requires_human_review: bool


def encode_image_to_base64(path: Path) -> str:
    # Cada caso visual se envía al modelo como imagen base64 embebida.
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def load_expected(image_name: str) -> dict:
    """Carga el JSON de expected output para una imagen."""
    # Convención: formulario_bancario_limpio.png -> expected/formulario_bancario_limpio.json
    stem = image_name.replace(".png", "")
    path = EXPECTED_DIR / f"{stem}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def extract_from_image(image_path: Path) -> dict:
    """Extrae datos de una imagen con LangChain y OpenAI."""
    img_b64 = encode_image_to_base64(image_path)

    # El mismo extractor se ejecuta sobre todos los casos para que la comparación
    # sea justa y reproducible.
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

    # Structured output obliga a que todos los casos tengan la misma forma.
    structured_llm = llm.with_structured_output(BankApplicationWithConfidence)

    message = HumanMessage(content=[
        {
            "type": "text",
            "text": (
                "Analizá el formulario bancario. "
                "Devolvé null para campos no legibles. "
                "Indicá confidence y requires_human_review."
            ),
        },
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
    ])
    result = cast(BankApplicationWithConfidence, structured_llm.invoke([message]))
    return result.model_dump()
# ============================================================
# 4. LAS 4 MÉTRICAS
# ============================================================

def validate_schema(actual: dict) -> bool:
    """Métrica 1: ¿el output cumple el schema Pydantic?"""
    # Schema válido no significa dato correcto, pero sí significa que el backend
    # puede consumir la respuesta sin romperse.
    try:
        BankApplicationWithConfidence(**actual)
        return True
    except ValidationError:
        return False


def calculate_accuracy(expected: dict, actual: dict) -> float:
    """
    Métrica 2: ¿cuántos campos tienen el valor CORRECTO?
    Solo se comparan campos con expected no-None.
    """
    campos = [k for k, v in expected.items() if v is not None and k not in ("extraction_notes",)]
    if not campos:
        return 1.0
    correctos = sum(1 for c in campos if str(actual.get(c)) == str(expected[c]))
    return correctos / len(campos)


def calculate_completeness(expected: dict, actual: dict) -> float:
    """
    Métrica 3: ¿cuántos campos esperados (no-None) están presentes en el actual?
    Detecta cuando el modelo omite campos.
    """
    # Completeness detecta omisiones: campos que deberían venir pero quedaron None.
    campos = [k for k, v in expected.items() if v is not None and k not in ("extraction_notes",)]
    if not campos:
        return 1.0
    presentes = sum(1 for c in campos if actual.get(c) is not None)
    return presentes / len(campos)


def check_human_review_correct(expected: dict, actual: dict) -> bool:
    """
    Métrica 4: ¿el modelo marcó correctamente requires_human_review?
    Un falso negativo (debería ser True pero devolvió False) es peligroso.
    """
    # Esta métrica evalúa la decisión operativa, no solo los valores extraídos.
    return expected.get("requires_human_review") == actual.get("requires_human_review")


@dataclass
class CaseResult:
    # Contenedor liviano para imprimir y agregar métricas por caso.
    case_id: str
    image_name: str
    valid_schema: bool
    accuracy: float
    completeness: float
    human_review_correct: bool

    def summary_line(self) -> str:
        s = "✓" if self.valid_schema else "✗"
        h = "✓" if self.human_review_correct else "✗"
        return (
            f"  Schema: {s} | "
            f"Accuracy: {self.accuracy:.0%} | "
            f"Completeness: {self.completeness:.0%} | "
            f"HumanReview: {h}"
        )


# ============================================================
# 5. EVALUACIÓN / MEDICIÓN
# ============================================================

print("\n=== EVALUACIÓN DE LOS 3 CASOS ===")
print()

GOLDEN_CASES = [
    {"id": "case_001", "image": "formulario_bancario_limpio.png"},
    {"id": "case_002", "image": "formulario_bancario_cafe.png"},
    {"id": "case_003", "image": "formulario_bancario_borroso.png"},
]

results: list[CaseResult] = []

for case in GOLDEN_CASES:
    image_path = DATA_DIR / case["image"]
    expected   = load_expected(case["image"])
    actual     = extract_from_image(image_path)
    trace("USER", f"Analizá el formulario bancario `{case['image']}`. Devolvé campos estructurados, confidence y requires_human_review.")
    trace("EXTRACT", json.dumps(actual, ensure_ascii=False, indent=2, default=str))

    result = CaseResult(
        case_id=case["id"],
        image_name=case["image"],
        valid_schema=validate_schema(actual),
        accuracy=calculate_accuracy(expected, actual),
        completeness=calculate_completeness(expected, actual),
        human_review_correct=check_human_review_correct(expected, actual),
    )
    results.append(result)

    print(f"[{result.case_id}] {result.image_name}")
    print(result.summary_line())
    print()

# Reporte final
avg_acc  = sum(r.accuracy for r in results) / len(results)
avg_comp = sum(r.completeness for r in results) / len(results)
schemas  = sum(1 for r in results if r.valid_schema)
reviews  = sum(1 for r in results if r.human_review_correct)
trace("METRICS", json.dumps({
    "cases": [
        {
            "case_id": result.case_id,
            "image_name": result.image_name,
            "valid_schema": result.valid_schema,
            "accuracy": result.accuracy,
            "completeness": result.completeness,
            "human_review_correct": result.human_review_correct,
        }
        for result in results
    ],
    "summary": {
        "cases_evaluated": len(results),
        "valid_schemas": schemas,
        "human_review_correct": reviews,
        "average_accuracy": avg_acc,
        "average_completeness": avg_comp,
    },
}, ensure_ascii=False, indent=2))

print("─" * 55)
print("REPORTE FINAL:")
print(f"  Casos evaluados:            {len(results)}")
print(f"  Schemas válidos:            {schemas}/{len(results)}")
print(f"  Human review correcto:      {reviews}/{len(results)}")
print(f"  Accuracy promedio:          {avg_acc:.0%}")
print(f"  Completeness promedio:      {avg_comp:.0%}")


# ============================================================
# 6. ANTES VS DESPUÉS
# ============================================================

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (evaluación a ojo):
    "Probé 3 casos y parecía funcionar bien."
    Sin números, sin reproducibilidad, sin comparación posible.

  DESPUÉS (golden cases con 4 métricas):
    Schemas válidos:       {schemas}/{len(results)}
    Accuracy promedio:     {avg_acc:.0%}
    Completeness promedio: {avg_comp:.0%}
    Human review OK:       {reviews}/{len(results)}

    Detectamos que case_002 tuvo accuracy < 100% (el modelo inventó el DNI).
    Con esta tabla podemos comparar gpt-4o-mini vs gpt-4o en las mismas imágenes.
""")


# ============================================================
# 7. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print("""
  Agregá un cuarto golden case: una imagen rotada o invertida.
  Podés crearla modificando generate_images.py:

    def create_rotated_form(base):
        return base.rotate(5, expand=True, fillcolor='white')  # 5° de inclinación

  Añadí su expected JSON:
    {
      "full_name": null, "document_number": null, ...
      "confidence": "low",
      "requires_human_review": true,
      "extraction_notes": "Imagen rotada — difícil de leer"
    }

  Luego ejecutá el pipeline y respondé:
    - ¿El modelo detecta que la imagen está rotada?
    - ¿Cuánta accuracy logra con 5° de rotación vs 15°?
    - ¿A qué ángulo el modelo empieza a confabular?

  Ejecutalo con OPENAI_API_KEY para medir el comportamiento real del modelo.
""")

def main():
    pass


if __name__ == "__main__":
    main()
