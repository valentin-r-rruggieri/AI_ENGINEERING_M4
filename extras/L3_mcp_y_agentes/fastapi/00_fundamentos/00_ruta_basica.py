# Este archivo forma parte del recorrido práctico de FastAPI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Primera ruta GET con FastAPI.

GUÍA DOCENTE
CUÁNDO USAR: para exponer un estado o dato sin modificar recursos.
DIFERENCIA: la función Python se convierte en endpoint HTTP mediante el decorador.
EN CLASE: ubicar método, path y respuesta JSON.
"""

# Importa FastAPI para crear la aplicación web.
from fastapi import FastAPI

# Crea la aplicación que cargará Uvicorn.
app = FastAPI(title="AEM4 API")

# Publica un endpoint de salud sencillo.
@app.get("/salud")
def salud() -> dict[str, str]:
    """Confirma que el proceso está disponible."""
    return {"estado": "ok"}

# Muestra la instrucción de ejecución sin arrancar otro proceso.
print("Ejecutá: uvicorn 00_ruta_basica:app --reload")

# Resumen final: este ejercicio convierte una función en una ruta GET.
# Cambia el path a /health y revisa la documentación en /docs.
