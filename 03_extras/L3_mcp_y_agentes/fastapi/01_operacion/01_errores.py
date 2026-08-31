# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Error HTTP explícito y comprensible.

GUÍA DOCENTE
CUÁNDO USAR: cuando una condición de negocio impide completar la solicitud.
DIFERENCIA: HTTPException controla status y detalle sin traceback al cliente.
EN CLASE: distinguir errores de validación, negocio y servidor.
"""

# Importa FastAPI y HTTPException para respuestas controladas.
from fastapi import FastAPI, HTTPException

# Crea una API con un catálogo local pequeño.
app = FastAPI(title="Errores controlados")
contratos = {"C-100": "vigente", "C-200": "vencido"}

# Busca un contrato o responde 404 si no existe.
@app.get("/contratos/{identificador}")
def obtener_contrato(identificador: str) -> dict[str, str]:
    """Consulta un contrato del catálogo de demostración."""
    if identificador not in contratos:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return {"identificador": identificador, "estado": contratos[identificador]}

# Muestra cómo iniciar la API.
print("Probá C-100 y C-999 desde /docs")

# Resumen final: este ejercicio traduce una condición de negocio a HTTP 404.
# Cambia el status a 400 y discute cuál representa mejor el caso.
