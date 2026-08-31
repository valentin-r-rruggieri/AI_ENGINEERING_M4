# Este archivo forma parte del recorrido práctico de arquitecturas de serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Capacidad aproximada con trabajadores concurrentes.

GUÍA DOCENTE
CUÁNDO USAR: para estimar si una configuración soporta el tráfico esperado.
DIFERENCIA: concurrencia I/O puede compartir espera; CPU compite por núcleos.
EN CLASE: tratar la fórmula como aproximación para iniciar una prueba de carga.
"""

# Define trabajadores, duración y tráfico esperado.
trabajadores = 4
latencia_segundos = 0.5
utilizacion_objetivo = 0.7
solicitudes_esperadas_por_segundo = 5

# Estima capacidad sostenible con un margen operativo.
capacidad_teorica = trabajadores / latencia_segundos
capacidad_objetivo = capacidad_teorica * utilizacion_objetivo
alcanza = capacidad_objetivo >= solicitudes_esperadas_por_segundo

# Muestra capacidad y decisión.
print({
    "capacidad_teorica_rps": capacidad_teorica,
    "capacidad_objetivo_rps": capacidad_objetivo,
    "alcanza": alcanza,
})

# Resumen final: este ejercicio traduce latencia y workers en capacidad aproximada.
# Duplica la latencia y calcula cuántos workers necesitarías.
