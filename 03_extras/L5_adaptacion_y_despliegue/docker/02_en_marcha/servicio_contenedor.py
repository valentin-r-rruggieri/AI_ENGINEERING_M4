# Este archivo forma parte del recorrido práctico de Docker.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servicio FastAPI listo para ejecutar dentro de Docker.

GUÍA DOCENTE
CUÁNDO USAR: como proceso único de una imagen de serving.
DIFERENCIA: Uvicorn escucha 0.0.0.0 para ser accesible fuera del contenedor.
EN CLASE: probar salud, configuración y predicción después de construir.
"""

# Importa os, FastAPI y Pydantic.
import os
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Define la entrada del clasificador didáctico.
class Solicitud(BaseModel):
    texto: str = Field(min_length=3)

# Crea la aplicación e identifica el entorno.
app = FastAPI(title="AEM4 en Docker")
entorno = os.getenv("APP_ENV", "desarrollo")

# Publica un health check utilizado también por Dockerfile.
@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok", "entorno": entorno}

# Publica una inferencia pequeña para verificar el contenedor.
@app.post("/predecir")
def predecir(solicitud: Solicitud) -> dict[str, str]:
    texto = solicitud.texto.lower()
    etiqueta = "cancelacion" if "cancel" in texto or "baja" in texto else "consulta"
    return {"etiqueta": etiqueta}

print("Servicio preparado para Uvicorn en el contenedor")

# Resumen final: este servicio aporta salud, configuración e inferencia.
# Ejecuta el contenedor con APP_ENV=produccion y consulta /salud.
