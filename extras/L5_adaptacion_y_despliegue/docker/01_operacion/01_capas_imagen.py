# Este archivo forma parte del recorrido práctico de Docker.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Orden de capas para aprovechar la caché de Docker.

GUÍA DOCENTE
CUÁNDO USAR: al escribir un Dockerfile que se reconstruye con frecuencia.
DIFERENCIA: dependencias cambian menos que el código de la aplicación.
EN CLASE: explicar por qué requirements se copia antes que los .py.
"""

# Representa las instrucciones principales del Dockerfile final.
capas = [
    "FROM python:3.12-slim",
    "COPY requirements.txt .",
    "RUN pip install -r requirements.txt",
    "COPY servicio_contenedor.py .",
    "CMD uvicorn servicio_contenedor:app",
]

# Muestra el orden y qué ocurre si cambia solo el código.
for posicion, capa in enumerate(capas, start=1):
    print(posicion, capa)

capas_reutilizables_si_cambia_python = 3
print("Capas iniciales reutilizables:", capas_reutilizables_si_cambia_python)

# Resumen final: este ejercicio hace visible la caché por capas.
# Mueve COPY del código antes de pip install y analiza el costo de reconstrucción.
