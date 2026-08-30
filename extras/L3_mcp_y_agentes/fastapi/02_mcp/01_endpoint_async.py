# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Endpoint asíncrono para operaciones I/O-bound.

GUÍA DOCENTE
CUÁNDO USAR: cuando el endpoint espera una API, base o archivo remoto.
DIFERENCIA: async libera el event loop durante await; no acelera CPU intensiva.
EN CLASE: comparar tres esperas secuenciales con gather.
"""

# Importa asyncio para simular I/O y FastAPI para la ruta.
import asyncio
from fastapi import FastAPI

# Crea una aplicación de demostración.
app = FastAPI(title="Async")

# Ejecuta tres esperas en forma concurrente.
@app.get("/consultas")
async def consultar_fuentes() -> dict[str, list[str]]:
    """Simula tres consultas remotas concurrentes."""

    async def consultar(nombre: str) -> str:
        await asyncio.sleep(0.1)
        return f"{nombre}: ok"

    resultados = await asyncio.gather(
        consultar("contratos"),
        consultar("clientes"),
        consultar("políticas"),
    )
    return {"resultados": resultados}

print("Ejecutá Uvicorn y llama GET /consultas")

# Resumen final: este ejercicio solapa tres esperas de I/O.
# Cambia una espera a un segundo y observa la latencia total.
