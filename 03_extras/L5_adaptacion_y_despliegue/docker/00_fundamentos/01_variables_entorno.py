# Este archivo forma parte del recorrido práctico de Docker.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Configuración del contenedor mediante variables de entorno.

GUÍA DOCENTE
CUÁNDO USAR: para cambiar entorno y modelo sin reconstruir la imagen.
DIFERENCIA: imagen contiene código; variables aportan configuración de ejecución.
EN CLASE: nunca copiar una API key dentro del Dockerfile.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para leer configuración del proceso.
import os

# Obtiene valores con defaults seguros para desarrollo.
entorno = os.getenv("APP_ENV", "desarrollo")
modelo = os.getenv("MODEL_NAME", "clasificador-tiny")
api_key_disponible = bool(os.getenv("OPENAI_API_KEY"))

# Muestra configuración no sensible.
print({
    "entorno": entorno,
    "modelo": modelo,
    "api_key_disponible": api_key_disponible,
})

# Resume un comando de ejecución sin incluir secretos reales.
print("Ejemplo: docker run -e APP_ENV=produccion -e OPENAI_API_KEY=... imagen")

# Resumen final: este ejercicio separa configuración y artefacto.
# Define APP_ENV en PowerShell y vuelve a ejecutar el archivo.
