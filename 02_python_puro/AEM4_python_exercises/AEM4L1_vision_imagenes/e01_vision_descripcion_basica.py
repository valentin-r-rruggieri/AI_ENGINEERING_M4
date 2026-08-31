"""
E01 - Vision descripcion basica con LangChain
AEM4L1 | Vision e Imagenes

Objetivo pedagogico:
    Hacer la primera llamada multimodal minima: una imagen real entra al
    modelo y vuelve una descripcion en texto libre.

Flujo:
    imagen PNG real -> base64 -> ChatOpenAI multimodal -> texto libre
"""

from __future__ import annotations

import base64
import builtins
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# En macOS/VS Code a veces stdout no viene configurado como UTF-8.
# Reconfigurarlo evita caracteres rotos cuando el modelo responde en español.
reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding="utf-8", errors="replace")

# Carga variables desde .env para no hardcodear credenciales en el código.
load_dotenv()

# Este ejercicio siempre usa la API real. Fallar temprano evita que el alumno
# piense que el problema está en LangChain cuando en realidad falta la key.
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu API key de OpenAI.")

# --quiet permite ocultar trazas si se usa el script dentro de otra prueba.
QUIET = "--quiet" in sys.argv

# El modelo queda configurable por entorno para poder comparar modelos sin editar el archivo.
MODEL_NAME = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")

# Las rutas se calculan desde la ubicación del archivo para que funcione aunque
# el alumno ejecute el script desde otra carpeta.
DATA_DIR = Path(__file__).parent / "data"
IMAGE_PATH = DATA_DIR / "formulario_bancario_limpio.png"


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    # Silenciamos prints pedagógicos: la consola solo debe mostrar USER/LLM.
    return None


def trace(role: str, payload: str) -> None:
    # Todas las salidas visibles pasan por trace para imitar un flujo user-agent.
    if QUIET:
        return
    builtins.print(f"{role}:")
    builtins.print(payload)
    builtins.print()


def ensure_data() -> None:
    # El ejercicio depende de una imagen real. Si falta, la generamos para que
    # la clase sea reproducible en una máquina nueva.
    if not IMAGE_PATH.exists():
        subprocess.run([sys.executable, str(DATA_DIR / "generate_images.py")], check=True)


def encode_image_to_base64(path: Path) -> str:
    # OpenAI recibe la imagen embebida como data URL; por eso el PNG primero se
    # lee como bytes y luego se transforma a texto base64.
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def describe_image(image_path: Path) -> str:
    # Importamos LangChain dentro de la función para que el bloque donde ocurre
    # la llamada real quede visible y fácil de explicar en clase.
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI

    image_b64 = encode_image_to_base64(image_path)

    # Primer prompt deliberadamente simple: todavía no pedimos JSON ni schema,
    # solo queremos demostrar que la imagen llega al modelo y vuelve texto.
    user_prompt = (
        "Describi brevemente que ves en esta imagen. "
        "No extraigas JSON todavia; responde como texto natural."
    )

    # HumanMessage puede mezclar partes de texto y partes de imagen.
    # Esta es la estructura mínima de un mensaje multimodal.
    message = HumanMessage(content=[
        {"type": "text", "text": user_prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
    ])

    # temperature=0 reduce variabilidad: útil para ejercicios de extracción.
    response = ChatOpenAI(model=MODEL_NAME, temperature=0).invoke([message])

    # LangChain puede devolver content como string o como una estructura más rica;
    # normalizamos a string para que el primer ejercicio sea fácil de leer.
    return response.content if isinstance(response.content, str) else str(response.content)


def main() -> None:
    # main solo orquesta: prepara datos, ejecuta la llamada y muestra trazas limpias.
    ensure_data()
    user_prompt = (
        "Describi brevemente que ves en esta imagen. "
        "No extraigas JSON todavia; responde como texto natural."
    )
    result = describe_image(IMAGE_PATH)
    trace("USER", user_prompt)
    trace("LLM", result)


if __name__ == "__main__":
    main()
