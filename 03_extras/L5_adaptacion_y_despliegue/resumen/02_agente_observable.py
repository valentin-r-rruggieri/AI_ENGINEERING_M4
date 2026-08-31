# Este archivo resume L5 mediante un caso práctico observable de serving.
# Lee cada bloque y modifica una variable por vez.

"""Caso 3: responder, medir y recomendar un despliegue.

GUÍA DOCENTE
CUÁNDO USAR: antes de publicar un agente que debe ser observable y escalable.
DIFERENCIA: LangChain genera la respuesta; Langfuse registra evidencia de ejecución.
EN CLASE: conectar latencia, trazas y la elección de Docker o Kubernetes.
"""

# Carga las variables del archivo .env de la raíz del proyecto.
from dotenv import load_dotenv
load_dotenv()

# Importa dependencias para el agente, medición y salida tipada.
from time import perf_counter
from langfuse import get_client
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define el resultado que usaría un servicio de IA antes de desplegarse.
class ResultadoServing(BaseModel):
    respuesta: str
    latencia_ms: float = Field(ge=0)
    destino: str
    observabilidad: str

# Prepara una consulta pequeña que un agente puede responder de forma económica.
consulta = "Explica LoRA en una oración."
inicio = perf_counter()

# Usa el wrapper LangChain para obtener una respuesta de producción.
respuesta = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(consulta).content
# Calcula la latencia y selecciona una primera estrategia de despliegue.
latencia_ms = round((perf_counter() - inicio) * 1000, 1)
destino = "Kubernetes" if latencia_ms > 500 else "Docker"
resultado = ResultadoServing(
    respuesta=str(respuesta),
    latencia_ms=latencia_ms,
    destino=destino,
    observabilidad="Langfuse",
)

# Envía una traza corta con input, output y metadata del despliegue sugerido.
langfuse = get_client()
with langfuse.start_as_current_observation(as_type="span", name="resumen-l5", input=consulta) as span:
    span.update(output=resultado.model_dump(), metadata={"destino": destino, "latencia_ms": latencia_ms})
langfuse.flush()

# Muestra la salida que podría entregar un endpoint FastAPI o un contenedor.
print(resultado.model_dump())

# Resumen final: servir un agente exige respuesta, medición, trazas y capacidad.
# Cambiá el umbral de 500 ms y justificá una estrategia distinta.
