"""Parsing multimodal de imagenes de contratos con GPT-4o Vision.

Por que GPT-4o Vision y no OCR tradicional (Tesseract, Google Vision OCR)?
------------------------------------------------------------------------
OCR tradicional extrae caracteres sueltos pero pierde la estructura del
documento: no entiende que "Clausula 1" es un titulo, que "$1.000" es un
monto, ni que hay una jerarquia de secciones. El resultado es texto plano
ruidoso que requiere post-procesamiento complejo.

GPT-4o Vision entiende el documento como un todo: lee texto, comprende la
jerarquia de clausulas, identifica montos, fechas y condiciones, y los
preserva en el orden correcto. Esto produce un texto limpio y estructurado
listo para que los agentes lo analicen.

Como se usa
-----------
1. validate_image_path(): verifica que el archivo existe y es PNG/JPG/JPEG.
2. encode_image_to_base64(): convierte la imagen a base64 para enviarla por API.
3. parse_contract_image(): llama a GPT-4o Vision con un prompt especializado
   que instruye al modelo a extraer el texto fielmente, conservando numeracion
   de clausulas, titulos, montos y fechas.

La llamada usa LangChain (ChatOpenAI) en lugar de OpenAI directo porque:
- LangChain registra automaticamente tokens, latencia y costo en Langfuse
  mediante el CallbackHandler.
- Permite usar el mismo patron (ChatOpenAI + messages) que los agentes.
- Facilita cambiar de proveedor de modelo en el futuro.
"""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Extensiones de imagen permitidas. Limitamos el input para evitar que
# alguien pase un PDF, un .exe o un archivo corrupto que rompa la API.
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

# Directorio base del proyecto (proyecto_integrador/).
BASE_DIR = Path(__file__).resolve().parent.parent
# Directorio de datos de prueba (proyecto_integrador/data/).
DATA_DIR = BASE_DIR / "data"


def validate_image_path(image_path: str | Path) -> Path:
    """Valida que el archivo existe y tiene una extension de imagen permitida.

    Por que validar antes de llamar a la API?
    - Si el archivo no existe, la API fallaria con un error confuso.
    - Si la extension no es soportada (ej. .pdf, .gif), la codificacion
      base64 generaria un data URL invalido que GPT-4o rechazaria.
    Validar primero da mensajes de error claros y accionables.

    Args:
        image_path: ruta al archivo de imagen (string o Path).

    Returns:
        Path absoluta validada.

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
    """Codifica una imagen a base64 para enviarla por la API de OpenAI.

    La API de GPT-4o Vision acepta imagenes como data URLs:
        data:image/png;base64,iVBORw0KGgo...
    Esta funcion devuelve solo la parte base64 (sin el prefijo data:).
    El prefijo se arma en parse_contract_image() con el mime type correcto.

    Args:
        path: ruta al archivo de imagen.

    Returns:
        String base64 de la imagen.
    """
    validated = validate_image_path(path)
    return base64.b64encode(validated.read_bytes()).decode("utf-8")


def parse_contract_image(
    image_path: str | Path,
    document_label: str,
    use_real_api: bool = False,
    callbacks: list | None = None,
) -> str:
    """Extrae texto de una imagen de contrato usando GPT-4o Vision.

    Flujo:
    1. Valida el path y la extension de la imagen.
    2. Codifica la imagen a base64.
    3. Si use_real_api=True: llama a GPT-4o Vision con un prompt especializado.
       Si use_real_api=False: devuelve un texto mock deterministico (para clase
       sin credenciales ni red).

    El prompt de vision (VISION_PROMPT) instruye al modelo a:
    - Conservar la numeracion de clausulas.
    - Conservar titulos, subtitulos, montos, fechas, nombres y condiciones.
    - No resumir ni inventar texto.
    - Marcar partes ilegibles como [ILEGIBLE].
    - Devolver el texto organizado por secciones.

    Args:
        image_path: ruta al archivo PNG/JPG de la imagen del contrato.
        document_label: etiqueta descriptiva ("Contrato original", "Adenda").
        use_real_api: si True, llama a OpenAI. Si False, usa mock deterministico.
        callbacks: lista de CallbackHandlers de Langfuse para registrar tokens.

    Returns:
        Texto extraido de la imagen, organizado por secciones.
    """
    path = validate_image_path(image_path)
    image_b64 = encode_image_to_base64(path)

    if use_real_api:
        return _parse_with_openai_vision(path, image_b64, document_label, callbacks)

    return _mock_contract_text(path, document_label)


# Prompt especializado para el parser de vision.
# El rol del system prompt es anclar al modelo en el dominio legal para que
# no divague. Las reglas son explicitas para reducir alucinaciones:
# "no resumas", "no inventes", "marca como [ILEGIBLE]".
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


def _parse_with_openai_vision(
    path: Path,
    image_b64: str,
    document_label: str,
    callbacks: list | None = None,
) -> str:
    """Llama a GPT-4o Vision usando LangChain ChatOpenAI.

    Por que ChatOpenAI y no client.responses.create()?
    - ChatOpenAI acepta callbacks (Langfuse) automaticamente.
    - Usa el mismo patron de messages que los agentes.
    - Registra tokens, latencia y costo en Langfuse sin codigo extra.

    El content del HumanMessage es una lista con dos partes:
    1. {"type": "text", "text": ...} - el prompt de vision.
    2. {"type": "image_url", "image_url": {"url": "data:...;base64,..."}} - la imagen.
    """
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

    # El parametro config={"callbacks": [...]} inyecta el handler de Langfuse.
    # LangChain lo intercepta y registra la llamada como un span/generation.
    config = {"callbacks": callbacks} if callbacks else {}
    response = llm.invoke([message], config=config)
    return response.content


def _mock_contract_text(path: Path, document_label: str) -> str:
    """Devuelve texto simulado deterministico para clase sin API.

    Por que un mock?
    - En clase no siempre hay credenciales de OpenAI disponibles.
    - El mock permite ejecutar el pipeline completo y ver el flujo de agentes
      sin gastar tokens ni depender de la red.
    - Es deterministico: siempre devuelve el mismo texto, para que los
      golden cases (expected.json) sean comparables.

    El mock identifica la imagen por su nombre de archivo y devuelve el
    texto del contrato/adenda correspondiente. Si el nombre no coincide
    con ninguno conocido, devuelve un texto generico.
    """
    name = path.name.lower()

    # --- Par 1: Contrato de servicios (simple) ---
    if name == "contrato_original.png" and "pair1" in str(path).lower():
        return _TEXT_CONTRATO_SERVICIOS
    if name == "adenda_simple.png" and "pair1" in str(path).lower():
        return _TEXT_ADENDA_SIMPLE

    # --- Par 2: Contrato de confidencialidad (complejo) ---
    if name == "contrato_original.png" and "pair2" in str(path).lower():
        return _TEXT_CONTRATO_CONFIDENCIALIDAD
    if name == "adenda_compleja.png" and "pair2" in str(path).lower():
        return _TEXT_ADENDA_COMPLEJA

    # Fallback: texto generico para imagenes no catalogadas.
    return f"{document_label}: texto simulado no catalogado para {path.name}."


# ============================================================================
# Textos mock para cada documento de prueba.
# Estos textos reflejan exactamente lo que el generate_data.py dibuja en las
# imagenes PNG, para que el mock sea consistente con los golden cases.
# ============================================================================

_TEXT_CONTRATO_SERVICIOS = """\
CONTRATO COMERCIAL DE SERVICIOS
Version original - Enero 2024

Clausula 1 - Monto mensual de pago
El cliente abonara al proveedor la suma de pesos un mil ($1.000) mensuales,
pagaderos dentro de los primeros cinco dias habiles de cada mes.

Clausula 2 - Duracion del contrato
El presente contrato tendra una vigencia de doce (12) meses, contados a partir
de la fecha de firma del presente instrumento.

Clausula 3 - Territorio de operacion
El proveedor prestara los servicios objeto de este contrato exclusivamente en
el territorio de la Republica Argentina.

Clausula 4 - Confidencialidad
Las partes se comprometen a mantener confidencialidad sobre toda informacion
intercambiada durante la relacion contractual.
"""

_TEXT_ADENDA_SIMPLE = """\
ADENDA NRO 1
Modificacion simple - Marzo 2024

Clausula 2 modificada - Nueva duracion del contrato
Por acuerdo de partes, la vigencia del contrato se extiende a dieciocho (18)
meses, quedando sin efecto el plazo de doce meses estipulado en la clausula 2
original.
"""

_TEXT_CONTRATO_CONFIDENCIALIDAD = """\
CONTRATO DE CONFIDENCIALIDAD
Version original - Febrero 2024

Clausula 1 - Alcance territorial
Las partes acuerdan que la informacion confidencial cubierta por este contrato
no podra ser utilizada fuera del territorio de la Republica Argentina.

Clausula 2 - Restriccion de uso
El receptor de la informacion confidencial se compromete a no utilizar dicha
informacion para fines comerciales propios durante la vigencia del contrato ni
durante los doce (12) meses posteriores a su finalizacion.

Clausula 3 - Duracion del acuerdo
El presente acuerdo de confidencialidad tendra una vigencia de veinticuatro (24)
meses a partir de la fecha de firma.
"""

_TEXT_ADENDA_COMPLEJA = """\
ADENDA NRO 2
Modificacion compleja - Julio 2024

Clausula 1 modificada - Expansion del alcance territorial
Por acuerdo de partes, el alcance territorial se amplia a los territorios de
Argentina, Uruguay y Paraguay, quedando sin efecto la restriccion exclusiva
al territorio argentino estipulada en la clausula 1 original.

Clausula 2 eliminada - Restriccion de uso
Las partes acuerdan eliminar la clausula 2 del contrato original referida a la
restriccion de uso de la informacion confidencial. La informacion podra ser
utilizada por el receptor sin limitaciones temporales posteriores al contrato.

Clausula 4 agregada - Difusion controlada
Se incorpora la siguiente clausula nueva: el receptor podra difundir la
informacion confidencial a terceros subcontratistas, exclusivamente bajo
acuerdo de confidencialidad previo firmado con cada subcontratista.
"""
