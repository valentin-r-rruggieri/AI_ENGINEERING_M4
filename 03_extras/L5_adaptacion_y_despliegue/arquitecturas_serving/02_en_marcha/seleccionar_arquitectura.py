# Este archivo forma parte del recorrido práctico de arquitecturas de serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Selector pequeño de arquitectura de serving.

GUÍA DOCENTE
CUÁNDO USAR: para ordenar criterios antes de diseñar un despliegue real.
DIFERENCIA: la regla explica una recomendación; no reemplaza pruebas de carga.
EN CLASE: modificar un criterio por vez y discutir el resultado.
"""

# Define las características del caso a evaluar.
caso = {
    "solicitudes_por_hora": 20,
    "latencia_maxima_ms": 3000,
    "carga_modelo_ms": 900,
    "trafico_predecible": False,
    "puede_escalar_a_cero": True,
}

# Calcula si el cold start todavía entra en el presupuesto.
inferencia_ms = 150
cold_start_estimado = caso["carga_modelo_ms"] + inferencia_ms
tolera_cold_start = cold_start_estimado <= caso["latencia_maxima_ms"]
uso_esporadico = caso["solicitudes_por_hora"] < 100

# Recomienda serverless solo cuando coinciden los criterios principales.
if uso_esporadico and tolera_cold_start and caso["puede_escalar_a_cero"]:
    arquitectura = "serverless"
    motivo = "uso esporádico y cold start dentro del presupuesto"
else:
    arquitectura = "servidor persistente"
    motivo = "prioridad en disponibilidad o carga frecuente"

# Muestra decisión y señales que la explican.
print({"arquitectura": arquitectura, "motivo": motivo})
print({"cold_start_ms": cold_start_estimado, "uso_esporadico": uso_esporadico})

# Resumen final: este ejercicio produce una recomendación explicable.
# Reduce latencia_maxima_ms a 500 y observa qué criterio cambia.
