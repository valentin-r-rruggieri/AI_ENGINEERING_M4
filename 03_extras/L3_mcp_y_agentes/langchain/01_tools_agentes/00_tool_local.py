# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tool local con schema inferido desde Python.

GUÍA DOCENTE
CUÁNDO USAR: cuando un agente necesita consultar o ejecutar una capacidad.
DIFERENCIA: la tool puede probarse sin modelo antes de entregarla al agente.
EN CLASE: inspeccionar nombre, descripción y argumentos.
"""

# Importa el decorador tool de LangChain.
from langchain.tools import tool

# Convierte una función determinista en una tool.
@tool
def calcular_diferencia_plazo(original: int, nuevo: int) -> int:
    """Calcula la diferencia entre dos plazos expresados en meses."""
    return nuevo - original

# Ejecuta la tool directamente para probar su lógica.
resultado = calcular_diferencia_plazo.invoke({"original": 12, "nuevo": 18})

# Muestra metadata y resultado.
print("Nombre:", calcular_diferencia_plazo.name)
print("Descripción:", calcular_diferencia_plazo.description)
print("Resultado:", resultado)

# Resumen final: este ejercicio crea y prueba una tool sin LLM.
# Agrega validación para impedir plazos negativos.
