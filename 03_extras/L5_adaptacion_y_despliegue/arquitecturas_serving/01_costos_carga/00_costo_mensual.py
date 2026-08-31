# Este archivo forma parte del recorrido práctico de arquitecturas de serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Estimación didáctica de costos por patrón.

GUÍA DOCENTE
CUÁNDO USAR: para comparar órdenes de magnitud antes de elegir infraestructura.
DIFERENCIA: servidor cobra horas disponibles; serverless cobra uso efectivo.
EN CLASE: aclarar que los valores son supuestos, no precios de proveedor.
"""

# Define supuestos simples y explícitos.
horas_mes = 730
costo_servidor_hora = 0.08
solicitudes_mes = 12_000
duracion_promedio_seg = 1.5
costo_serverless_segundo = 0.00002

# Calcula los dos órdenes de costo.
costo_servidor = horas_mes * costo_servidor_hora
costo_serverless = solicitudes_mes * duracion_promedio_seg * costo_serverless_segundo

# Muestra valores redondeados y la opción menor.
print({"servidor_usd": round(costo_servidor, 2), "serverless_usd": round(costo_serverless, 2)})
print("Menor costo simulado:", "serverless" if costo_serverless < costo_servidor else "servidor")

# Resumen final: este ejercicio compara disponibilidad contra uso efectivo.
# Multiplica las solicitudes por cien y revisa dónde cambia la decisión.
