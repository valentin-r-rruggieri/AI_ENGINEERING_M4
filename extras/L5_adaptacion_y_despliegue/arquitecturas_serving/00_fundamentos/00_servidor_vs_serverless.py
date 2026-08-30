# Este archivo forma parte del recorrido práctico de arquitecturas de serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Comparación explícita entre servidor y serverless.

GUÍA DOCENTE
CUÁNDO USAR: al decidir cómo mantener disponible un modelo.
DIFERENCIA: servidor prioriza disponibilidad; serverless reduce costo ocioso.
EN CLASE: relacionar frecuencia, latencia y costo con el patrón elegido.
"""

# Describe los trade-offs principales de ambos patrones.
patrones = {
    "servidor": {
        "modelo_en_memoria": True,
        "cold_start": "bajo",
        "costo_ocioso": "alto",
        "ideal": "tráfico continuo",
    },
    "serverless": {
        "modelo_en_memoria": False,
        "cold_start": "alto",
        "costo_ocioso": "bajo",
        "ideal": "tráfico esporádico",
    },
}

# Muestra los dos perfiles lado a lado.
for nombre, propiedades in patrones.items():
    print(nombre, "->", propiedades)

# Selecciona un patrón para una carga frecuente.
trafico_continuo = True
seleccion = "servidor" if trafico_continuo else "serverless"
print("Selección:", seleccion)

# Resumen final: este ejercicio convierte trade-offs en una decisión inicial.
# Cambia tráfico_continuo a False y justifica la nueva selección.
