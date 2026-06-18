"""
E02 - Vision a JSON minimo con LangChain y Pydantic
AEM4L1 | Vision e Imagenes

Objetivo pedagogico:
    Dar el primer salto desde texto libre hacia una salida minima que un
    backend puede consumir.

Flujo:
    imagen PNG real -> base64 -> ChatOpenAI.with_structured_output()
    -> MinimalApplicationExtract validado por Pydantic
"""

from __future__ import annotations

import base64
import builtins
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Mantiene la salida en UTF-8 para que los ejemplos en español se lean bien.
reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# Cargamos .env para obtener OPENAI_API_KEY y, opcionalmente, OPENAI_VISION_MODEL.
load_dotenv()

# Este starter ya usa API real: si falta la key, detenemos el script antes de
# construir prompts para que el error sea claro.
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

# --quiet sirve cuando queremos correr validaciones sin imprimir trazas.
QUIET = "--quiet" in sys.argv

# Modelo configurable para comparar gpt-4o-mini, gpt-4o u otro modelo de visión.
MODEL_NAME = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")

# Usamos rutas relativas al archivo para que el ejercicio sea portable.
DATA_DIR = Path(__file__).parent / "data"
IMAGE_PATH = DATA_DIR / "formulario_bancario_limpio.png"


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    # Evita prints decorativos: la salida real queda concentrada en trace().
    return None


def trace(role: str, payload: str) -> None:
    # Mantiene una consola estilo agente: USER entra, EXTRACT sale.
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


class MinimalApplicationExtract(BaseModel):
    # Schema mínimo para introducir Pydantic sin abrumar al alumno.
    # Cada Field le da al modelo una descripción y a Pydantic una regla.
    full_name: str = Field(..., description="Nombre completo visible en el formulario")
    requested_amount: float = Field(..., gt=0, description="Monto solicitado en pesos")
    signature_present: bool = Field(..., description="True si se ve una firma en el formulario")


def ensure_data() -> None:
    # Si el PNG no existe, regeneramos los datos de la clase automáticamente.
    if not IMAGE_PATH.exists():
        subprocess.run([sys.executable, str(DATA_DIR / "generate_images.py")], check=True)


def encode_image_to_base64(path: Path) -> str:
    # El modelo no recibe el archivo por ruta local; recibe los bytes codificados
    # dentro de una data URL.
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def extract_minimal_json(image_path: Path) -> MinimalApplicationExtract:
    # Imports cerca de la llamada real para que el alumno vea qué piezas de
    # LangChain intervienen: mensaje multimodal + wrapper de OpenAI.
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI

    image_b64 = encode_image_to_base64(image_path)

    # Prompt acotado: pedimos solo tres campos para separar el concepto de
    # structured output del caso bancario completo que viene en E03.
    user_prompt = (
        "Extrae solamente estos tres datos del formulario: nombre completo, "
        "monto solicitado y si hay firma visible."
    )

    # Igual que en E01, el mensaje contiene texto + imagen.
    message = HumanMessage(content=[
        {"type": "text", "text": user_prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
    ])

    # with_structured_output pide al LLM una respuesta compatible con el schema.
    # Pydantic valida el resultado y lo convierte en un objeto Python usable.
    structured_llm = ChatOpenAI(model=MODEL_NAME, temperature=0).with_structured_output(MinimalApplicationExtract)
    return cast(MinimalApplicationExtract, structured_llm.invoke([message]))


def main() -> None:
    # main conserva la historia del ejercicio: input del usuario y extracción final.
    ensure_data()
    user_prompt = (
        "Extrae solamente estos tres datos del formulario: nombre completo, "
        "monto solicitado y si hay firma visible."
    )
    result = extract_minimal_json(IMAGE_PATH)
    trace("USER", user_prompt)
    trace("EXTRACT", result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
