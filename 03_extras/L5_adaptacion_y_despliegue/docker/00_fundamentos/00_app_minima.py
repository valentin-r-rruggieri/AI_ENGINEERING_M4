# Este archivo forma parte del recorrido práctico de Docker.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Aplicación mínima que luego entrará en un contenedor.

GUÍA DOCENTE
CUÁNDO USAR: para probar localmente la aplicación antes de construir la imagen.
DIFERENCIA: Docker empaqueta el proceso; no corrige una aplicación defectuosa.
EN CLASE: ejecutar primero Uvicorn fuera del contenedor.
"""

# Importa FastAPI para crear el servicio HTTP.
from fastapi import FastAPI

# Crea una aplicación pequeña y sin estado.
app = FastAPI(title="Docker Demo")

# Publica una ruta que demuestra que el proceso responde.
@app.get("/")
def inicio() -> dict[str, str]:
    """Devuelve un mensaje identificable."""
    return {"mensaje": "servicio AEM4 activo"}

# Indica cómo probar la app antes de usar Docker.
print("Ejecutá: uvicorn 00_app_minima:app --reload")

# Resumen final: este ejercicio separa aplicación y empaquetado.
# Cambia el mensaje y verifica primero la ejecución local.
