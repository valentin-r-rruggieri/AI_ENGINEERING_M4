"""
E02 — Formulario manchado con café: confianza y revisión humana
AEM4L1 | Visión e Imágenes

Objetivo pedagógico:
    Si la imagen está dañada, el modelo puede INVENTAR datos.
    La solución: campos opcionales + confidence + requires_human_review.
    LangChain con structured_output fuerza al modelo a reportar su incertidumbre.

Flujo:
    imagen PNG con mancha  →  encode base64  →  LangChain multimodal
    →  structured_output(BankApplicationWithConfidence)
    →  model_validator verifica coherencia de requires_human_review

USE_REAL_API = False → lee la imagen real + mock honesto (reporta None en campos tapados)
USE_REAL_API = True  → envía la imagen manchada a GPT-4o-mini → respuesta real
"""

import os
import base64
import subprocess
import sys
from pathlib import Path
from datetime import date
from typing import Optional, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, model_validator

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

USE_REAL_API   = False
MODEL_NAME     = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DATA_DIR       = Path(__file__).parent / "data"
IMAGE_CAFE     = DATA_DIR / "formulario_bancario_cafe.png"
IMAGE_LIMPIO   = DATA_DIR / "formulario_bancario_limpio.png"


def ensure_data() -> None:
    if not IMAGE_CAFE.exists():
        print("Imágenes no encontradas. Generando...")
        subprocess.run([sys.executable, str(DATA_DIR / "generate_images.py")], check=True)
        print()

ensure_data()


# ============================================================
# 1. CONTEXTO DEL CASO
# ============================================================

print("=" * 60)
print("AEM4L1 | E02 — Formulario manchado con café")
print("=" * 60)
print(f"""
CASO:
  El mismo formulario del E01, pero llegó con manchas de café.
  Las manchas cubren el campo DNI y la fecha de nacimiento.

  Imagen de entrada: {IMAGE_CAFE.name}
  El modelo de visión sigue extrayendo... ¿pero qué hace con los campos tapados?
""")


# ============================================================
# 2. VERSIÓN BÁSICA — el modelo inventa datos (peligroso)
# ============================================================

print("\n=== VERSIÓN BÁSICA — El modelo inventa datos ===")
print()


def encode_image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def bad_extraction_confabulates(image_path: Path) -> dict:
    """
    El modelo recibe la imagen manchada pero devuelve todos los campos completos.
    Problema: cuando no puede leer un campo, INVENTA un valor con total confianza.
    """
    img_b64 = encode_image_to_base64(image_path)

    if USE_REAL_API:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        from langchain_core.output_parsers import JsonOutputParser

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        # Sin instrucciones de incertidumbre → el modelo rellena todo
        message = HumanMessage(content=[
            {
                "type": "text",
                "text": "Extraé TODOS los datos del formulario bancario. Devolvé JSON con: full_name, document_number, requested_amount, birth_date, signature_present."
            },
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
        ])
        parser = JsonOutputParser()
        chain = llm | parser
        return chain.invoke([message])
    else:
        print(f"  [MOCK] Leyendo {image_path.name} ({image_path.stat().st_size // 1024} KB)...")
        # El modelo CONFABULA: rellena campos que no podía leer
        return {
            "full_name": "Juan Pérez",
            "document_number": "40111222",   # ← campo cubierto por café → INVENTADO
            "requested_amount": 50000.0,
            "birth_date": "1994-05-12",      # ← campo cubierto por café → INVENTADO
            "signature_present": True,
        }


resultado_malo = bad_extraction_confabulates(IMAGE_CAFE)
print("Output (modelo que confabula):")
for k, v in resultado_malo.items():
    print(f"  {k}: {v}")

print()
print("  PELIGRO: document_number y birth_date están INVENTADOS.")
print("  El modelo NO puede leer esos campos pero no lo dice.")
print("  En producción: crédito procesado con DNI y fecha incorrectos.")


# ============================================================
# 3. PROBLEMA DETECTADO
# ============================================================

print("\n=== PROBLEMA DETECTADO ===")
print("""
¿Qué está MAL con el modelo que siempre rellena?

  El modelo no vio el DNI (está tapado por café) pero devolvió "40111222".
  El modelo no vio la fecha (también tapada) pero devolvió "1994-05-12".
  Esto se llama "confabulación" o "alucinación" → el modelo inventa.

  En el dominio bancario esto implica:
    - Aprobar créditos para personas con DNI equivocado
    - Calcular edad incorrectamente (puede afectar elegibilidad)
    - Fraudes no detectados
    - Responsabilidad legal del banco

  La solución: instruir al modelo a reportar su incertidumbre.
""")


# ============================================================
# 4. VERSIÓN MEJORADA — schema con confianza + revisión humana
# ============================================================

print("\n=== VERSIÓN MEJORADA — Campos opcionales + confidence ===")
print()

print("""
Patrón:
    structured_llm = llm.with_structured_output(BankApplicationWithConfidence)
    El prompt instruye: "Si un campo no es legible, devolvé null."
    → El modelo reporta None + un nivel de confianza bajo
    → model_validator fuerza que requires_human_review = True en esos casos
""")


class BankApplicationWithConfidence(BaseModel):
    """
    Schema mejorado: captura la incertidumbre del modelo.

    Campos opcionales → el modelo reporta None si no puede leerlo.
    confidence → el modelo declara qué tan seguro está del output completo.
    requires_human_review → calculado automáticamente por el model_validator.
    """
    full_name: Optional[str] = None
    document_number: Optional[str] = None
    requested_amount: Optional[float] = Field(None, gt=0)
    birth_date: Optional[date] = None
    signature_present: Optional[bool] = None

    confidence: Literal["low", "medium", "high"] = Field(
        ..., description="Confianza del modelo en la extracción completa"
    )
    extraction_notes: str = Field(
        ..., description="Notas sobre campos no legibles o dudosos"
    )
    requires_human_review: bool = Field(
        ..., description="Debe ser True si algún campo crítico es None o confidence es low/medium"
    )

    @model_validator(mode="after")
    def validate_human_review_consistency(self):
        """
        Regla de negocio: si algún campo crítico es None O la confianza es baja/media,
        requires_human_review DEBE ser True.
        Esto previene que el modelo omita la bandera de revisión.
        """
        campos_criticos_nulos = any([
            self.full_name is None,
            self.document_number is None,
            self.requested_amount is None,
        ])
        confianza_insuficiente = self.confidence in ("low", "medium")

        if (campos_criticos_nulos or confianza_insuficiente) and not self.requires_human_review:
            raise ValueError(
                "requires_human_review debe ser True cuando confidence es low/medium "
                "o algún campo crítico (full_name, document_number, requested_amount) es None."
            )
        return self


def safe_extraction_honest(image_path: Path) -> BankApplicationWithConfidence:
    """
    Versión segura: el modelo reporta incertidumbre en lugar de inventar.
    """
    img_b64 = encode_image_to_base64(image_path)

    if USE_REAL_API:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        structured_llm = llm.with_structured_output(BankApplicationWithConfidence)

        message = HumanMessage(content=[
            {
                "type": "text",
                "text": (
                    "Analizá este formulario bancario. "
                    "Si algún campo está cubierto, borroso o no es legible, devolvé null para ese campo. "
                    "Indicá tu nivel de confianza ('low'/'medium'/'high') sobre la extracción completa. "
                    "En extraction_notes describí qué campos no pudiste leer y por qué. "
                    "Si confidence es 'low' o 'medium', o algún campo crítico es null, "
                    "requires_human_review debe ser true."
                ),
            },
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
        ])
        return structured_llm.invoke([message])

    else:
        print(f"  [MOCK] Leyendo {image_path.name} ({image_path.stat().st_size // 1024} KB)...")
        print("  [MOCK] Simulando respuesta honesta de GPT-4o-mini...")
        # El modelo ahora reporta honestamente lo que no puede leer
        return BankApplicationWithConfidence(
            full_name="Juan Pérez",
            document_number=None,       # ← campo tapado → None
            requested_amount=50000.0,
            birth_date=None,            # ← campo tapado → None
            signature_present=True,
            confidence="medium",
            extraction_notes=(
                "El campo 'número de documento' está cubierto por una mancha de café. "
                "El campo 'fecha de nacimiento' también está parcialmente cubierto. "
                "No es posible leerlos con certeza."
            ),
            requires_human_review=True,
        )


print()
app_segura = safe_extraction_honest(IMAGE_CAFE)
print()
print("Output honesto (campos tapados → None):")
print(f"  full_name:             {app_segura.full_name}")
print(f"  document_number:       {app_segura.document_number}  ← None: campo no legible")
print(f"  requested_amount:      {app_segura.requested_amount}")
print(f"  birth_date:            {app_segura.birth_date}  ← None: campo no legible")
print(f"  confidence:            {app_segura.confidence}")
print(f"  extraction_notes:      {app_segura.extraction_notes[:70]}...")
print(f"  requires_human_review: {app_segura.requires_human_review}")


# ============================================================
# 5. VALIDACIÓN — routing automático
# ============================================================

print("\n=== VALIDACIÓN — Routing automático ===")
print()

CRITICAL_FIELDS = ["full_name", "document_number", "requested_amount"]


def route_application(app: BankApplicationWithConfidence) -> tuple[str, str]:
    """Decide si la solicitud va a procesamiento automático o revisión humana."""
    if app.requires_human_review:
        missing = [f for f in CRITICAL_FIELDS if getattr(app, f) is None]
        reason = f"Confianza: {app.confidence}"
        if missing:
            reason += f" | Campos faltantes: {missing}"
        return "human_review", reason
    return "auto_process", "OK — todos los campos críticos presentes y confidence=high"


destino, motivo = route_application(app_segura)
print(f"Resultado del routing: {destino}")
print(f"Motivo: {motivo}")

# Caso imagen limpia (del E01) — debería ir a auto_process
print()
print("Comparación con imagen limpia:")
app_limpia = BankApplicationWithConfidence(
    full_name="Juan Pérez",
    document_number="40111222",
    requested_amount=50000.0,
    birth_date=date(1994, 5, 12),
    signature_present=True,
    confidence="high",
    extraction_notes="Imagen clara. Todos los campos son legibles.",
    requires_human_review=False,
)
destino2, motivo2 = route_application(app_limpia)
print(f"  Resultado: {destino2}")
print(f"  Motivo:    {motivo2}")

# Demostrar que el model_validator atrapa inconsistencias
print()
print("Caso de error — modelo dice requires_human_review=False con campos None:")
try:
    BankApplicationWithConfidence(
        full_name="Ana López",
        document_number=None,         # crítico faltante
        requested_amount=None,        # crítico faltante
        signature_present=True,
        confidence="medium",
        extraction_notes="Imagen dudosa.",
        requires_human_review=False,  # ← inconsistente → model_validator lo rechaza
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  model_validator: {err['msg'][:90]}...")


# ============================================================
# 6. ANTES VS DESPUÉS
# ============================================================

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (modelo que confabula):
    document_number: "40111222"   ← INVENTADO (campo cubierto)
    birth_date: "1994-05-12"      ← INVENTADO (campo cubierto)
    Sin confidence, sin requires_human_review

  DESPUÉS (LangChain + Pydantic + model_validator):
    document_number:       None   ← honesto: "no pudo leerlo"
    birth_date:            None   ← honesto: "no pudo leerlo"
    confidence:            medium
    requires_human_review: True   ← obligado por model_validator
    Routing:               → cola de revisión humana

  El banco nunca procesa un crédito con datos inventados.
""")


# ============================================================
# 7. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print("""
  Agregá un campo image_quality al schema:
    image_quality: Literal["good", "damaged", "unreadable"]

  Regla adicional en el model_validator:
    - "damaged"    → requires_human_review = True siempre
    - "unreadable" → requires_human_review = True + imprimir alerta
    - "good"       → solo si confidence = "high" puede ir a auto_process

  Probá con image_quality = "damaged" y confidence = "high".
  ¿El model_validator la rechaza si requires_human_review = False?

  Luego abrí formulario_bancario_cafe.png y formulario_bancario_borroso.png
  y observá la diferencia visual → ¿cuál sería "damaged" y cuál "unreadable"?
""")


def main():
    pass


if __name__ == "__main__":
    main()
