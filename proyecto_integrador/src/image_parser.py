"""Parsing multimodal de imagenes de contratos con GPT-4o Vision (PRODUCCION).

Convierte la imagen de un contrato en texto estructurado usando GPT-4o Vision via
LangChain. No hay modo mock: este modulo siempre llama a la API real de OpenAI.

Por que GPT-4o Vision y no OCR tradicional?
------------------------------------------
OCR tradicional extrae caracteres sueltos y pierde la estructura del documento.
GPT-4o Vision entiende el documento como un todo: lee texto, comprende la jerarquia
de clausulas, identifica montos, fechas y condiciones, y los preserva en orden.

Por que LangChain (ChatOpenAI) y no el cliente OpenAI directo?
-------------------------------------------------------------
- El CallbackHandler de Langfuse se inyecta en cada invoke (config={"callbacks": [...]})
  y registra automaticamente tokens, latencia y costo.
- Mismo patron de messages que los agentes.
"""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Extensiones de imagen permitidas. Limitamos el input para evitar PDFs,
# archivos corruptos o formatos no soportados que romperian la API de Vision.
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def validate_image_path(image_path: str | Path) -> Path:
    """Valida que el archivo existe y tiene una extension de imagen permitida.

    Raises:
        FileNotFoundError: si el archivo no existe.
        ValueError: si la extension no esta en ALLOWED_EXTENSIONS.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Formato invalido: {path.suffix}. Formatos soportados: {ALLOWED_EXTENSIONS}."
        )
    return path


def encode_image_to_base64(path: str | Path) -> str:
    """Codifica una imagen a base64 para enviarla como data URL a la API de OpenAI."""
    validated = validate_image_path(path)
    return base64.b64encode(validated.read_bytes()).decode("utf-8")


# Prompt especializado para el parser de vision. Ancla al modelo en el dominio
# legal y le pone reglas explicitas para reducir alucinaciones.
VISION_PROMPT = """\
Sos un analista legal especializado en lectura de contratos escaneados.

Documento: {document_label}

Tarea:
Extrae el texto del documento de la forma mas fiel posible.

Reglas:
- Conserva numeracion de clausulas.
- Conserva titulos, subtitulos, montos, fechas, nombres y condiciones.
- No resumas.
- No inventes texto.
- Si una parte es ilegible, marcala como [ILEGIBLE].
- Devolve solo el texto extraido, organizado por secciones.
"""


def parse_contract_image(
    image_path: str | Path,
    document_label: str,
    callbacks: list | None = None,
) -> str:
    """Extrae texto de una imagen de contrato usando GPT-4o Vision.

    Flujo:
    1. Valida el path y la extension de la imagen.
    2. Codifica la imagen a base64 y arma un data URL.
    3. Llama a GPT-4o Vision con el prompt especializado.

    Args:
        image_path: ruta al archivo PNG/JPG de la imagen del contrato.
        document_label: etiqueta descriptiva ("Contrato original", "Adenda").
        callbacks: lista de CallbackHandlers de Langfuse para registrar tokens.

    Returns:
        Texto extraido de la imagen, organizado por secciones.
    """
    path = validate_image_path(image_path)
    image_b64 = encode_image_to_base64(path)

    model = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")
    llm = ChatOpenAI(model=model, max_tokens=2000)

    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "image/png"

    prompt_text = VISION_PROMPT.format(document_label=document_label)
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{image_b64}"},
            },
        ]
    )

    # config={"callbacks": [...]} inyecta el handler de Langfuse: LangChain lo
    # intercepta y registra la llamada como una generation con tokens y latencia.
    config = {"callbacks": callbacks} if callbacks else {}
    response = llm.invoke([message], config=config)
    return response.content
