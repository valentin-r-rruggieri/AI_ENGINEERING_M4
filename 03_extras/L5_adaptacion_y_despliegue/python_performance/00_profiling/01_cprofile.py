# Este archivo forma parte del recorrido práctico de rendimiento en Python.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Perfil de CPU con cProfile y pstats.

GUÍA DOCENTE
CUÁNDO USAR: para localizar funciones que acumulan mayor tiempo de CPU.
DIFERENCIA: tiempo total dice cuánto; cProfile ayuda a explicar dónde.
EN CLASE: leer ncalls, tottime y cumtime de la tabla.
"""

# Importa las herramientas estándar de profiling y una salida en memoria.
import cProfile
import io
import pstats

# Define dos etapas para que el perfil pueda distinguirlas.
def normalizar(textos: list[str]) -> list[str]:
    return [texto.strip().lower() for texto in textos]

def contar(textos: list[str]) -> int:
    return sum(len(texto.split()) for texto in textos)

# Ejecuta las etapas dentro del profiler.
textos = [" Contrato de doce meses "] * 20_000
perfil = cProfile.Profile()
perfil.enable()
limpios = normalizar(textos)
palabras = contar(limpios)
perfil.disable()

# Ordena la salida por tiempo acumulado y muestra pocas filas.
salida = io.StringIO()
pstats.Stats(perfil, stream=salida).sort_stats("cumulative").print_stats(8)
print("Palabras:", palabras)
print(salida.getvalue())

# Resumen final: este ejercicio localiza tiempo por función.
# Cambia el orden a tottime y compara qué función aparece primero.
