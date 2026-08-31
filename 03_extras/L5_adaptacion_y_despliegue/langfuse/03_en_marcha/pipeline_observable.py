# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline corto con spans y resultado visible.

GUÍA DOCENTE
CUÁNDO USAR: para localizar latencia y errores entre etapas de un servicio de IA.
DIFERENCIA: observar no cambia el resultado; agrega evidencia sobre la ejecución.
EN CLASE: dibujar la jerarquía de spans antes de enviarla.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para decidir si se envían observaciones reales.
import os

# Importa el cliente actual de Langfuse.
from langfuse import get_client

# Define una entrada y dos transformaciones locales fáciles de comprobar.
entrada = "  Contrato de 18 meses  "
texto_limpio = entrada.strip().lower()
salida = {"texto": texto_limpio, "caracteres": len(texto_limpio)}

# Registra el pipeline y sus dos etapas como observaciones anidadas.
langfuse = get_client()
with langfuse.start_as_current_observation(as_type="span", name="pipeline", input=entrada) as raiz:
    with langfuse.start_as_current_observation(as_type="span", name="limpiar") as limpiar:
        limpiar.update(output=texto_limpio)
    with langfuse.start_as_current_observation(as_type="span", name="medir") as medir:
        medir.update(output=salida["caracteres"])
    raiz.update(output=salida)
langfuse.flush()
print("Trace enviado:", salida)

# Resumen final: este ejercicio integra pipeline, spans y resultado observable.
# Agrega una etapa validar y represéntala como un tercer span.
