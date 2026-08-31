# Este archivo forma parte del recorrido práctico de rendimiento en Python.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Límite de concurrencia y timeout.

GUÍA DOCENTE
CUÁNDO USAR: para proteger una API externa de demasiadas solicitudes simultáneas.
DIFERENCIA: Semaphore limita concurrencia; timeout limita duración individual.
EN CLASE: observar qué tareas terminan y cuáles expiran.
"""

# Importa asyncio para semáforos, tareas y timeouts.
import asyncio

# Permite como máximo dos consultas activas.
semaforo = asyncio.Semaphore(2)

# Simula una llamada protegida y con duración variable.
async def consultar(numero: int, demora: float) -> str:
    async with semaforo:
        await asyncio.sleep(demora)
        return f"consulta-{numero}: ok"

# Ejecuta cuatro tareas con un timeout común.
async def ejecutar_lote() -> None:
    tareas = [consultar(1, 0.1), consultar(2, 0.1), consultar(3, 0.4), consultar(4, 0.1)]
    try:
        resultados = await asyncio.wait_for(asyncio.gather(*tareas), timeout=0.45)
        print(resultados)
    except TimeoutError:
        print("El lote superó el timeout de 0.45 segundos.")

# Ejecuta el lote directamente.
asyncio.run(ejecutar_lote())

# Resumen final: este ejercicio controla presión y duración de un lote.
# Aumenta el semáforo a 4 y observa si el timeout deja de activarse.
