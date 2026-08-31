# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Nivel de error y métricas en una observación.

GUÍA DOCENTE
CUÁNDO USAR: cuando una ejecución termina pero necesita atención operativa.
DIFERENCIA: level destaca el problema; metadata conserva mediciones del caso.
EN CLASE: distinguir excepción técnica de resultado de baja calidad.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os y el cliente Langfuse.
import os
from langfuse import get_client

# Simula las métricas obtenidas después de una extracción.
metricas = {"latencia_ms": 420, "confianza": 0.62, "tokens": 380}
requiere_revision = metricas["confianza"] < 0.8

# Registra el caso con WARNING sin convertirlo en una excepción falsa.
langfuse = get_client()
with langfuse.start_as_current_observation(
    as_type="span",
    name="validar_calidad",
    input=metricas,
) as span:
    span.update(
        output={"requiere_revision": requiere_revision},
        level="WARNING" if requiere_revision else "DEFAULT",
        status_message="Confianza bajo el umbral" if requiere_revision else None,
        metadata=metricas,
    )
langfuse.flush()

print({"metricas": metricas, "requiere_revision": requiere_revision})

# Resumen final: este ejercicio diferencia baja calidad de fallo técnico.
# Sube confianza a 0.90 y observa el nivel normal.
