# Este archivo forma parte del recorrido práctico de Kubernetes.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Estimación simple de capacidad por réplicas.

GUÍA DOCENTE
CUÁNDO USAR: para iniciar una conversación sobre escalado horizontal.
DIFERENCIA: más réplicas aumentan capacidad, pero también costo y memoria total.
EN CLASE: validar la estimación con una prueba de carga real.
"""

# Define capacidad medida por Pod y tráfico esperado.
replicas = 2
capacidad_por_pod_rps = 3.5
trafico_esperado_rps = 5.0
margen_objetivo = 0.75

# Calcula capacidad total y capacidad operativa con margen.
capacidad_total = replicas * capacidad_por_pod_rps
capacidad_operativa = capacidad_total * margen_objetivo
alcanza = capacidad_operativa >= trafico_esperado_rps

# Muestra la estimación y la decisión.
print({
    "replicas": replicas,
    "capacidad_operativa_rps": capacidad_operativa,
    "trafico_rps": trafico_esperado_rps,
    "alcanza": alcanza,
})

# Resumen final: este ejercicio relaciona réplicas y capacidad.
# Sube tráfico a 8 RPS y calcula cuántas réplicas serían necesarias.
