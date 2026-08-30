# Este archivo forma parte del recorrido práctico de arquitecturas de serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Impacto del cold start en la latencia percibida.

GUÍA DOCENTE
CUÁNDO USAR: para estimar la primera respuesta de una instancia nueva.
DIFERENCIA: warm request reutiliza proceso; cold request carga entorno y modelo.
EN CLASE: sumar cada componente antes de comparar el SLA.
"""

# Expresa los componentes de latencia en milisegundos.
inicio_contenedor_ms = 350
carga_modelo_ms = 900
inferencia_ms = 120
red_ms = 40

# Calcula una solicitud fría y una caliente.
latencia_fria = inicio_contenedor_ms + carga_modelo_ms + inferencia_ms + red_ms
latencia_caliente = inferencia_ms + red_ms
sla_ms = 500

# Muestra el impacto contra el mismo SLA.
print({"fria_ms": latencia_fria, "cumple_sla": latencia_fria <= sla_ms})
print({"caliente_ms": latencia_caliente, "cumple_sla": latencia_caliente <= sla_ms})

# Resumen final: este ejercicio separa cold start de inferencia normal.
# Reduce carga_modelo_ms y calcula cuánto margen queda frente al SLA.
