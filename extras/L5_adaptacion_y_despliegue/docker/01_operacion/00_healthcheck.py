# Este archivo forma parte del recorrido práctico de Docker.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Comprobación de salud desde Python.

GUÍA DOCENTE
CUÁNDO USAR: para que Docker determine si el proceso responde correctamente.
DIFERENCIA: proceso en ejecución no implica servicio saludable.
EN CLASE: iniciar el contenedor y luego ejecutar este cliente.
"""

# Importa json y urllib desde la biblioteca estándar.
import json
from urllib.error import URLError
from urllib.request import urlopen

# Define el endpoint publicado por el servicio final.
url = "http://127.0.0.1:8000/salud"

try:
    # Consulta el endpoint con un timeout corto.
    with urlopen(url, timeout=2) as respuesta:
        datos = json.loads(respuesta.read().decode("utf-8"))
        print({"status_http": respuesta.status, "body": datos})
except URLError:
    print("Iniciá primero el servicio o contenedor en el puerto 8000.")

# Resumen final: este ejercicio comprueba disponibilidad desde afuera del proceso.
# Cambia el path por uno inexistente y observa el tipo de error.
