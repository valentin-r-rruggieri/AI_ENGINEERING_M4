# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servicio pequeño de clasificación con health check.

GUÍA DOCENTE
CUÁNDO USAR: como referencia mínima para servir un modelo persistente.
DIFERENCIA: el modelo se carga en lifespan y se reutiliza por solicitud.
EN CLASE: seguir inicio, validación, inferencia y respuesta.
"""

# Importa el lifespan, FastAPI y Pydantic.
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Conserva el clasificador cargado durante la vida del proceso.
recursos: dict[str, set[str]] = {}

@asynccontextmanager
async def lifespan(aplicacion: FastAPI):
    recursos["palabras_cancelacion"] = {"cancelar", "baja", "rescindir", "terminar"}
    print("Clasificador cargado")
    yield
    recursos.clear()

# Define entrada y salida explícitas.
class Solicitud(BaseModel):
    texto: str = Field(min_length=3)

class Prediccion(BaseModel):
    etiqueta: str
    confianza: float = Field(ge=0, le=1)

# Crea la API con sus endpoints operativos.
app = FastAPI(title="Clasificador AEM4", lifespan=lifespan)

@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}

@app.post("/predecir", response_model=Prediccion)
def predecir(solicitud: Solicitud) -> Prediccion:
    palabras = set(solicitud.texto.lower().split())
    coincide = bool(palabras & recursos["palabras_cancelacion"])
    return Prediccion(etiqueta="cancelacion" if coincide else "consulta", confianza=0.9 if coincide else 0.7)

print("Ejecutá: uvicorn servicio_inferencia:app --reload")

# Resumen final: este servicio carga, valida y responde una inferencia.
# Cambia una palabra del catálogo y prueba el resultado desde /docs.
