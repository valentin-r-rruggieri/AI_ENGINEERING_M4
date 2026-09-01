# Este archivo forma parte del recorrido práctico de visión local.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Visión local con LM Studio, LangChain y Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando una imagen no debe salir de la computadora.
DIFERENCIA: GPT-4o usa una API remota; LM Studio expone un modelo local compatible con OpenAI.
EN CLASE: mostrar que Pydantic valida igual aunque cambie el proveedor.
"""

# Importa utilidades para localizar la imagen, leer la configuración y codificar Base64.
import base64
import os
from pathlib import Path

# Importa el mensaje multimodal, el wrapper LangChain y el contrato de salida.
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define qué datos debe encontrar el modelo local en el formulario bancario ficticio.
class LecturaFormularioLocal(BaseModel):
    nombre: str = Field(description="Nombre completo visible en el formulario.")
    dni: str = Field(description="DNI o documento, sin inventar dígitos.")
    monto_solicitado: float = Field(description="Monto numérico solicitado.")
    requiere_revision: bool = Field(description="True si algún dato está borroso, roto o ilegible.")

# Localiza una imagen didáctica que ya forma parte de la lecture.
ruta_raiz = Path(__file__).resolve().parents[3]
ruta_imagen = ruta_raiz / "02_python_puro" / "AEM4_python_exercises" / "AEM4L1_vision_imagenes" / "data" / "formulario_bancario_limpio.png"

# Convierte los bytes a Base64 para incluir la imagen en el formato OpenAI-compatible.
imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")

# Lee la dirección y el identificador exacto del modelo cargado en LM Studio.
direccion_lmstudio = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
nombre_modelo = os.getenv("LMSTUDIO_MODEL", "qwen2.5-vl-3b-instruct")

try:
    # Conecta LangChain al servidor local de LM Studio; la clave es solo un valor local de compatibilidad.
    modelo_local = ChatOpenAI(
        base_url=direccion_lmstudio,
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
        model=nombre_modelo,
        temperature=0,
    ).with_structured_output(LecturaFormularioLocal, method="json_schema")

    # Envía la imagen al modelo de visión que está cargado localmente en LM Studio.
    mensaje = HumanMessage(content=[
        {"type": "text", "text": "Lee el formulario. No inventes datos: marca requiere_revision si un campo no es legible."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{imagen_base64}"}},
    ])
    lectura = modelo_local.invoke([mensaje])

    # Muestra la instancia ya validada por Pydantic.
    print(lectura.model_dump())
except Exception as error:
    # Explica la preparación local sin mostrar un traceback confuso durante la clase.
    print("No se pudo conectar con LM Studio:", error)
    print("En LM Studio cargá un modelo con visión, iniciá Developer > Start Server y revisá LMSTUDIO_MODEL.")

# Resumen final: LangChain usa el servidor OpenAI-compatible y Pydantic conserva el contrato.
# Probá cambiar la imagen por formulario_bancario_cafe.png y analizá la decisión de revisión.

