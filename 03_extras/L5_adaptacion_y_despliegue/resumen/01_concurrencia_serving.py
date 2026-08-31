# Este archivo resume L5 mediante un caso práctico de concurrencia.
# Lee cada bloque y modifica una variable por vez.

"""Caso 2: medir tareas concurrentes antes de elegir una arquitectura.

GUÍA DOCENTE
CUÁNDO USAR: cuando un servicio debe atender varias solicitudes a la vez.
DIFERENCIA: concurrencia mejora espera de I/O; no acelera mágicamente trabajo de CPU.
EN CLASE: comparar tiempo individual, total y cantidad de solicitudes.
"""

# Carga el .env para mantener el patrón uniforme de los resúmenes.
from dotenv import load_dotenv
load_dotenv()

# Importa asyncio, LangChain y tiempo para simular solicitudes que esperan una respuesta.
import asyncio
from time import perf_counter
from langchain_openai import ChatOpenAI

# Define una solicitud pequeña con una espera que representa I/O de un modelo remoto.
async def responder(numero: int) -> str:
    await asyncio.sleep(0.02)
    return f"respuesta-{numero}"

# Reúne las tareas dentro de una corrutina compatible con asyncio.run.
async def reunir_respuestas() -> list[str]:
    return await asyncio.gather(*(responder(numero) for numero in range(3)))

# Ejecuta tres solicitudes juntas y mide el tiempo del conjunto.
inicio = perf_counter()
respuestas = asyncio.run(reunir_respuestas())
latencia_ms = round((perf_counter() - inicio) * 1000, 1)

# Usa LangChain para interpretar la medición antes de elegir infraestructura.
conclusion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    f"Explica en una oración una latencia total de {latencia_ms} ms para {len(respuestas)} solicitudes concurrentes."
).content

# Muestra evidencia sencilla para discutir capacidad y concurrencia.
print({"respuestas": respuestas, "latencia_total_ms": latencia_ms, "concurrencia": len(respuestas), "conclusion": conclusion})

# Resumen final: medir precede a decidir replicas, contenedores o serverless.
# Cambiá el rango a seis y compará la latencia total.
