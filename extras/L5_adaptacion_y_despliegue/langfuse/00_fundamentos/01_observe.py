# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Traza automática de una función con observe.

GUÍA DOCENTE
CUÁNDO USAR: para instrumentar una función completa con muy poco código.
DIFERENCIA: observe registra entrada, salida, duración y errores automáticamente.
EN CLASE: ejecutar la función y localizar su observación en el dashboard.
"""

# Importa os para las credenciales y observe/get_client para instrumentar.
import os
from langfuse import get_client, observe

# Decora una transformación que representa una etapa del pipeline.
@observe(name="normalizar_contrato")
def normalizar(texto: str) -> str:
    return " ".join(texto.lower().split())

# Ejecuta la función aunque Langfuse no esté configurado.
resultado = normalizar("  Vigencia de 18 MESES  ")
print(resultado)

if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
    # Fuerza el envío antes de terminar el script corto.
    get_client().flush()
    print("Observación enviada a Langfuse.")
else:
    print("Sin credenciales: se mostró solamente el resultado local.")

# Resumen final: este ejercicio instrumenta una función con un decorador.
# Provoca un error dentro de la función y observa cómo queda registrado.
