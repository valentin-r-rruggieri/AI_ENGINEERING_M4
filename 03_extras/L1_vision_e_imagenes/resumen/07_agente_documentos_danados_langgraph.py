# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para ver un flujo LangGraph aplicado a cuatro calidades documentales.

"""Flujo LangGraph que prepara y revisa imágenes de formularios bancarios.

GUÍA DOCENTE
CUÁNDO USAR: cuando el análisis tiene pasos visibles que conviene conectar y auditar.
DIFERENCIA: LangGraph representa el estado y los nodos; LangChain realiza el análisis visual.
EN CLASE: explicar el recorrido imagen -> Base64 -> agente visual -> decisión Pydantic.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 y Path para leer la imagen antes de pasarla entre nodos.
import base64
from pathlib import Path
from typing import NotRequired, TypedDict, cast

# Importa el mensaje multimodal y el modelo visual orquestado por LangChain.
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Importa los elementos mínimos para dibujar el flujo de estados.
from langgraph.graph import END, START, StateGraph

# Importa Pydantic para validar la decisión final del agente.
from pydantic import BaseModel, Field


# Define la salida uniforme que recibirá cada documento al terminar el grafo.
class RevisionDocumento(BaseModel):
    archivo: str = ""
    datos_detectados: list[str] = Field(min_length=1)
    calidad: str
    accion: str
    confianza: float = Field(ge=0, le=1)
    motivo: str


# Define qué información existe al inicio y cuál aparece durante el recorrido.
class EstadoDocumento(TypedDict):
    archivo: str
    descripcion: str
    imagen_base64: NotRequired[str]
    revision: NotRequired[dict[str, object]]


# Define la actualización del nodo que prepara la imagen para el siguiente nodo.
class ActualizacionImagen(TypedDict):
    imagen_base64: str


# Define la actualización del nodo que guarda la respuesta validada.
class ActualizacionRevision(TypedDict):
    revision: dict[str, object]


# Ubica la carpeta compartida que contiene los cuatro documentos del ejercicio.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data"


# Lee el archivo del estado y lo convierte a Base64 sin ocultar este paso del flujo.
def preparar_imagen(state: EstadoDocumento) -> ActualizacionImagen:
    ruta_imagen = carpeta_datos / state["archivo"]
    imagen_base64 = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")
    return {"imagen_base64": imagen_base64}


# Usa LangChain dentro del nodo para analizar la imagen preparada por el nodo anterior.
def revisar_documento(state: EstadoDocumento) -> ActualizacionRevision:
    extractor = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(RevisionDocumento)
    mensaje = HumanMessage(content=[
        {
            "type": "text",
            "text": (
                "Sos un analista documental bancario. "
                f"Revisá este caso: {state['descripcion']}. Extraé solo datos visibles. "
                "Indicá calidad aceptable, baja o crítica y recomendá aceptar, revisión humana "
                "o solicitar nuevo documento. Nunca inventes datos tapados."
            ),
        },
        {"type": "image", "base64": state.get("imagen_base64", ""), "mime_type": "image/png"},
    ])
    respuesta_agente = RevisionDocumento.model_validate(extractor.invoke([mensaje]))
    respuesta = RevisionDocumento.model_validate({**respuesta_agente.model_dump(), "archivo": state["archivo"]})
    return {"revision": respuesta.model_dump()}


# Conecta dos nodos explícitos: preparar bytes primero y decidir después.
grafo = StateGraph(EstadoDocumento)
grafo.add_node("preparar_imagen", preparar_imagen)
grafo.add_node("revisar_documento", revisar_documento)
grafo.add_edge(START, "preparar_imagen")
grafo.add_edge("preparar_imagen", "revisar_documento")
grafo.add_edge("revisar_documento", END)
aplicacion = grafo.compile()

# Declara los mismos cuatro casos del ejercicio LangChain para comparar ambos enfoques.
casos = [
    ("formulario_bancario_limpio.png", "formulario normal y legible"),
    ("formulario_bancario_borroso.png", "formulario borroso"),
    ("formulario_bancario_roto.png", "formulario roto o incompleto"),
    ("formulario_bancario_cafe.png", "formulario manchado con café"),
]

# Ejecuta el grafo desde el mismo estado inicial para cada calidad del documento.
for nombre_archivo, descripcion in casos:
    entrada: EstadoDocumento = {"archivo": nombre_archivo, "descripcion": descripcion}
    resultado = cast(EstadoDocumento, aplicacion.invoke(entrada))
    print(resultado.get("revision", {}))

# Resumen final: LangGraph muestra cada paso del agente y mantiene una salida Pydantic.
# Agregá una quinta imagen al listado para ensayar una nueva regla de revisión.
