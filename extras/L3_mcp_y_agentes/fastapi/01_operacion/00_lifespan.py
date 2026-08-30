# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Carga de un recurso durante el lifespan.

GUÍA DOCENTE
CUÁNDO USAR: para cargar una vez un modelo que atenderá muchas solicitudes.
DIFERENCIA: cargar dentro del endpoint repetiría el costo por cada request.
EN CLASE: observar los mensajes de inicio y cierre de Uvicorn.
"""

# Importa el gestor asíncrono y FastAPI.
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Simula el almacén donde vivirá un modelo cargado.
recursos: dict[str, str] = {}

# Define qué ocurre al iniciar y al detener la aplicación.
@asynccontextmanager
async def lifespan(aplicacion: FastAPI):
    recursos["modelo"] = "clasificador-tiny-cargado"
    print("Recurso cargado")
    yield
    recursos.clear()
    print("Recurso liberado")

# Conecta el lifespan y expone el nombre del recurso.
app = FastAPI(lifespan=lifespan)

@app.get("/modelo")
def modelo_activo() -> dict[str, str]:
    """Informa qué modelo está listo para inferencia."""
    return {"modelo": recursos["modelo"]}

print("Ejecutá: uvicorn 00_lifespan:app --reload")

# Resumen final: este ejercicio carga una dependencia una vez por proceso.
# Mueve la asignación al endpoint y explica por qué empeora la latencia.
