# Este archivo forma parte del recorrido práctico de rendimiento en Python.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Medición de latencia con perf_counter.

GUÍA DOCENTE
CUÁNDO USAR: para comparar el tiempo total de dos implementaciones.
DIFERENCIA: perf_counter mide duración; cProfile descompone por función.
EN CLASE: repetir varias veces antes de concluir que algo es más rápido.
"""

# Importa time para usar un reloj de alta resolución.
import time

# Simula una etapa CPU-bound mediante una suma conocida.
cantidad = 500_000
inicio = time.perf_counter()
resultado = sum(numero * numero for numero in range(cantidad))
duracion_ms = (time.perf_counter() - inicio) * 1000

# Muestra resultado y tiempo para evitar optimizaciones invisibles.
print("Resultado:", resultado)
print("Duración ms:", round(duracion_ms, 2))

# Deriva una comparación simple contra un presupuesto.
presupuesto_ms = 100
print("Dentro del presupuesto:", duracion_ms <= presupuesto_ms)

# Resumen final: este ejercicio mide latencia de extremo a extremo.
# Duplica cantidad y observa si el tiempo crece aproximadamente al doble.
