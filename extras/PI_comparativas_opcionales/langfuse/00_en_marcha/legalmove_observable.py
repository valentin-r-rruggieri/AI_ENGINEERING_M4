# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""LegalMove observable con tres etapas y métricas.

GUÍA DOCENTE
CUÁNDO USAR: para auditar contexto, extracción y validación de una ejecución.
DIFERENCIA: los spans explican dónde ocurrió cada resultado y cuánto tardó.
EN CLASE: relacionar la jerarquía con los criterios de la rúbrica.
"""

# Importa os, time y el cliente Langfuse v4.
import os
import time
from langfuse import get_client

# Prepara datos deterministas para concentrar el ejercicio en observabilidad.
entrada = {"original": "12 meses", "nuevo": "18 meses con renovación"}
contexto = {"tema": "vigencia", "estructura": "cláusula temporal"}
resultado = {
    "resumen_ejecutivo": "Se amplía el plazo y se agrega renovación.",
    "cambios_detectados": ["12 meses pasa a 18 meses"],
    "riesgos_legales": ["renovación automática"],
}

if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
    # Crea la traza raíz y un span por etapa del pipeline.
    langfuse = get_client()
    with langfuse.start_as_current_observation(as_type="span", name="legalmove", input=entrada) as raiz:
        inicio = time.perf_counter()
        with langfuse.start_as_current_observation(as_type="span", name="contextualizacion") as span:
            span.update(output=contexto)
        with langfuse.start_as_current_observation(as_type="span", name="extraccion") as span:
            span.update(output=resultado, metadata={"tokens": 240})
        with langfuse.start_as_current_observation(as_type="span", name="validacion") as span:
            span.update(output={"schema_valido": True})
        latencia_ms = round((time.perf_counter() - inicio) * 1000, 2)
        raiz.update(output=resultado, metadata={"latencia_ms": latencia_ms})
    langfuse.flush()
    print("Traza enviada con latencia_ms:", latencia_ms)
else:
    print("Flujo local:", entrada, "->", contexto, "->", resultado)

# Resumen final: este pipeline deja una etapa observable por responsabilidad.
# Marca validación como error y agrega un status_message útil.
