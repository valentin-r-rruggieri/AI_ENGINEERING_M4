# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Body HTTP validado automáticamente con Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando un cliente envía datos estructurados a la API.
DIFERENCIA: FastAPI genera JSON Schema y errores 422 desde el modelo.
EN CLASE: probar un body válido y otro con confianza fuera de rango.
"""

# Importa FastAPI y componentes Pydantic para la entrada.
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Define el contrato del body recibido.
class Prediccion(BaseModel):
    texto: str = Field(min_length=3)
    confianza: float = Field(ge=0, le=1)

# Crea la aplicación y una ruta POST.
app = FastAPI(title="Validación")

@app.post("/predicciones")
def registrar_prediccion(prediccion: Prediccion) -> dict[str, object]:
    """Valida y devuelve una predicción de demostración."""
    return {"aceptada": prediccion.confianza >= 0.8, "datos": prediccion.model_dump()}

# Indica cómo abrir la documentación interactiva.
print("Ejecutá Uvicorn y abrí http://127.0.0.1:8000/docs")

# Resumen final: este ejercicio usa Pydantic como contrato HTTP.
# Envía confianza 1.5 desde /docs y observa el error 422.
