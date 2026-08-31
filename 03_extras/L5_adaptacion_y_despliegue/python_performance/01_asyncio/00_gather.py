# Este archivo forma parte del recorrido práctico de rendimiento en Python.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Ejecución concurrente de esperas con asyncio.gather.

GUÍA DOCENTE
CUÁNDO USAR: cuando varias operaciones I/O independientes pueden solaparse.
DIFERENCIA: gather reduce espera total; no acelera cálculos de CPU.
EN CLASE: comparar tres esperas secuenciales con la duración concurrente.
"""

# Importa asyncio para tareas y time para medir la duración.
import asyncio
import time

# Simula una consulta remota sin bloquear el event loop.
async def consultar(nombre: str, demora: float) -> str:
    await asyncio.sleep(demora)
    return f"{nombre}: ok"

# Agrupa tres consultas independientes.
async def ejecutar_consultas() -> list[str]:
    return await asyncio.gather(
        consultar("contratos", 0.2),
        consultar("clientes", 0.2),
        consultar("políticas", 0.2),
    )

# Mide la ejecución concurrente completa.
inicio = time.perf_counter()
resultados = asyncio.run(ejecutar_consultas())
duracion = time.perf_counter() - inicio
print(resultados)
print("Duración segundos:", round(duracion, 3))

# Resumen final: este ejercicio solapa tres esperas I/O-bound.
# Reemplaza gather por tres await consecutivos y compara el tiempo.
