"""
E01 — Formulario bancario limpio: texto libre vs Pydantic + LangChain
AEM4L1 | Visión e Imágenes

Objetivo pedagógico:
    Un modelo multimodal puede devolver texto libre, pero eso no sirve
    para un backend. LangChain + Pydantic resuelve el problema:
    fuerza un esquema, tipos y validaciones desde el modelo.

Flujo:
    imagen PNG real  →  encode base64  →  LangChain ChatOpenAI (multimodal)
    →  structured_output(BankApplication)  →  Pydantic validado

USE_REAL_API = False:
    Lee la imagen real del disco → simula la respuesta del modelo con mock.
USE_REAL_API = True:
    Lee la imagen real → la envía a GPT-4o-mini → parsea con Pydantic.
"""

import os
import base64
import subprocess
import sys
from pathlib import Path
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

# ── Configuración ──────────────────────────────────────────────
USE_REAL_API   = False
MODEL_NAME     = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DATA_DIR       = Path(__file__).parent / "data"
IMAGE_PATH     = DATA_DIR / "formulario_bancario_limpio.png"


# ── Generar imágenes si no existen ────────────────────────────
def ensure_data() -> None:
    if not IMAGE_PATH.exists():
        print("Imágenes no encontradas. Generando...")
        subprocess.run(
            [sys.executable, str(DATA_DIR / "generate_images.py")],
            check=True
        )
        print()

ensure_data()


# ============================================================
# 1. CONTEXTO DEL CASO
# ============================================================

print("=" * 60)
print("AEM4L1 | E01 — Formulario bancario limpio")
print("=" * 60)
print(f"""
CASO:
  Un banco escanea formularios de solicitud de crédito como PNG.
  Un modelo multimodal (GPT-4o-mini) extrae la información.
  El backend necesita esos datos tipados y validados.

Imagen de entrada: {IMAGE_PATH.name}
  Tamaño: {IMAGE_PATH.stat().st_size // 1024} KB
""")


# ============================================================
# 2. VERSIÓN BÁSICA — texto libre (problema)
# ============================================================

print("\n=== VERSIÓN BÁSICA — El modelo devuelve texto libre ===")
print()


def encode_image_to_base64(path: Path) -> str:
    """Codifica una imagen PNG a base64 para enviarla al modelo multimodal."""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def basic_extraction_free_text(image_path: Path) -> str:
    """
    Versión básica: el modelo recibe la imagen y devuelve texto libre.
    Sin instrucciones de formato → el backend no puede parsear el output.
    """
    img_b64 = encode_image_to_base64(image_path)
    print(f"  Imagen codificada: {len(img_b64) // 1024} KB base64")

    if USE_REAL_API:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        message = HumanMessage(content=[
            {"type": "text", "text": "Describí qué ves en este formulario bancario."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
        ])
        response = llm.invoke([message])
        return response.content
    else:
        # MOCK — simula lo que devolvería el modelo sin instrucciones de formato
        return (
            "El solicitante parece ser Juan Pérez. "
            "Pidió 50000 pesos aproximadamente. "
            "El DNI es 40111222 y firmó abajo."
        )


texto_libre = basic_extraction_free_text(IMAGE_PATH)
print(f"Output texto libre:\n  '{texto_libre}'")

print()
print("Intento de parsear el monto a float:")
try:
    palabras = texto_libre.replace("$", "").split()
    monto = None
    for p in palabras:
        clean = p.replace(".", "").replace(",", "")
        if clean.isdigit():
            monto = float(clean)
            break
    print(f"  Resultado: {monto}  ← ¿Y si el modelo escribe '$50.000' o 'cincuenta mil'?")
except Exception as e:
    print(f"  Error: {e}")


# ============================================================
# 3. PROBLEMA DETECTADO
# ============================================================

print("\n=== PROBLEMA DETECTADO ===")
print("""
¿Qué está MAL con el texto libre?

  1. Sin campos garantizados → el parser depende del vocabulario del modelo
  2. Monto como string → no se puede usar para calcular intereses
  3. "firmó abajo" ≠ booleano → no puedo hacer: if application.signature_present
  4. Si el modelo cambia el estilo → mi regex parser se rompe
  5. Sin validación de rangos → ¿qué pasa si extrae monto negativo?

  Con texto libre, el backend no puede confiar en el output del modelo.
""")


# ============================================================
# 4. VERSIÓN MEJORADA — LangChain + Pydantic structured output
# ============================================================

print("\n=== VERSIÓN MEJORADA — LangChain + Pydantic structured output ===")
print()

print("""
Patrón clave:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(BankApplication)
    result = structured_llm.invoke([HumanMessage(content=[image, text])])

    → El modelo devuelve directamente una instancia de BankApplication validada.
    → No hace falta parsear JSON manualmente.
""")


class BankApplication(BaseModel):
    """
    Schema de validación para la solicitud bancaria.
    LangChain con .with_structured_output() obliga al modelo a cumplir este schema.
    """
    full_name: str = Field(..., description="Nombre completo del solicitante")
    document_number: str = Field(..., description="Número de DNI sin puntos")
    requested_amount: float = Field(..., gt=0, description="Monto solicitado en pesos (positivo)")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento YYYY-MM-DD")
    signature_present: bool = Field(..., description="True si hay firma visible en el formulario")


def structured_extraction(image_path: Path) -> BankApplication:
    """
    Versión mejorada: LangChain envía la imagen y fuerza el schema Pydantic.

    USE_REAL_API = True  → llamada real a GPT-4o-mini
    USE_REAL_API = False → lee la imagen real + simula la respuesta del modelo
    """
    img_b64 = encode_image_to_base64(image_path)

    if USE_REAL_API:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        structured_llm = llm.with_structured_output(BankApplication)

        message = HumanMessage(content=[
            {
                "type": "text",
                "text": (
                    "Analizá esta imagen de un formulario bancario y extraé los datos solicitados. "
                    "Si un campo no es legible, devolvé null. "
                    "El document_number debe ser solo los dígitos, sin puntos ni espacios."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_b64}"},
            },
        ])

        # LangChain hace la llamada y valida el output contra BankApplication
        return structured_llm.invoke([message])

    else:
        # MOCK: imagen leída, respuesta simulada
        print(f"  [MOCK] Imagen leída: {image_path.name} ({len(img_b64) // 1024} KB)")
        print("  [MOCK] Simulando respuesta de GPT-4o-mini...")
        return BankApplication(
            full_name="Juan Pérez",
            document_number="40111222",
            requested_amount=50000.0,
            birth_date=date(1994, 5, 12),
            signature_present=True,
        )


application = structured_extraction(IMAGE_PATH)
print()
print("Output estructurado (BankApplication validada por Pydantic):")
print(f"  full_name:         {application.full_name}")
print(f"  document_number:   {application.document_number}")
print(f"  requested_amount:  ${application.requested_amount:,.2f}")
print(f"  birth_date:        {application.birth_date}")
print(f"  signature_present: {application.signature_present}")


# ============================================================
# 5. VALIDACIÓN — Pydantic detecta outputs incorrectos del modelo
# ============================================================

print("\n=== VALIDACIÓN — Pydantic detecta errores del modelo ===")
print()

print("Caso 1: el modelo extrae monto negativo (alucinación):")
try:
    BankApplication(
        full_name="Test User",
        document_number="12345678",
        requested_amount=-5000.0,  # ← el modelo inventó un número negativo
        signature_present=True,
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  Campo '{err['loc'][0]}': {err['msg']}")

print()
print("Caso 2: el modelo devuelve el monto como string:")
try:
    BankApplication(
        full_name="Test User",
        document_number="12345678",
        requested_amount="cincuenta mil",  # type: ignore
        signature_present=True,
    )
except ValidationError as e:
    for err in e.errors():
        print(f"  Campo '{err['loc'][0]}': {err['msg']}")


# ============================================================
# 6. ANTES VS DESPUÉS
# ============================================================

print("\n=== ANTES VS DESPUÉS ===")
print(f"""
  ANTES (texto libre):
    Output: "{texto_libre}"
    - Sin campos garantizados
    - Monto como string
    - Parser frágil con regex

  DESPUÉS (LangChain + Pydantic):
    full_name:         {application.full_name!r}
    document_number:   {application.document_number!r}
    requested_amount:  {application.requested_amount}  (float validado > 0)
    signature_present: {application.signature_present}  (bool garantizado)

    LangChain obliga al modelo a respetar el schema.
    Pydantic valida tipos y rangos.
    ValidationError explícito si el modelo falla.
""")


# ============================================================
# 7. DESAFÍO PARA EL ALUMNO
# ============================================================

print("=== DESAFÍO PARA EL ALUMNO ===")
print("""
  1. Extendé BankApplication con:
       from typing import Literal
       employment_status: Literal["empleado", "autonomo", "desempleado"]

  2. En el mock (o con API real), incluí ese campo en la respuesta.

  3. Probá que Pydantic rechaza employment_status = "jubilado".

  4. (Si tenés API key) Cambiá USE_REAL_API = True,
     copiá .env.example a .env, completá OPENAI_API_KEY y ejecutá.
     ¿El modelo lee correctamente el formulario PNG generado?
""")


def main():
    pass


if __name__ == "__main__":
    main()
