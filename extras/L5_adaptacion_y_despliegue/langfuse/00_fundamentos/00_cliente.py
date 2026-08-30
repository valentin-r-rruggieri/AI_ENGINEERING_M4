# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Cliente Langfuse configurado por variables de entorno.

GUÍA DOCENTE
CUÁNDO USAR: antes de crear observaciones o integrar un framework.
DIFERENCIA: get_client reutiliza el cliente configurado del proceso.
EN CLASE: distinguir public key, secret key y base URL.
"""

# Importa os para comprobar credenciales y get_client para obtener el singleton.
import os
from langfuse import get_client

# Verifica las dos credenciales necesarias sin mostrar sus valores.
configurado = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))

if configurado:
    # Obtiene el cliente que utilizarán spans e integraciones.
    langfuse = get_client()
    print("Cliente Langfuse creado:", type(langfuse).__name__)
    print("Host:", os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"))
else:
    print("Configurá LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY.")

# Resumen final: este ejercicio prepara observabilidad sin incluir secretos en código.
# Cambia LANGFUSE_BASE_URL si utilizás una instalación self-hosted.
