# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Construcción controlada de prompts para imágenes de evaluación.

GUÍA DOCENTE
CUÁNDO USAR: para producir variaciones comparables de un mismo documento.
DIFERENCIA: un prompt estructurado permite cambiar una condición por vez.
EN CLASE: separar contenido, calidad y dificultad visual.
"""

# Define las dimensiones que controlan el caso sintético.
tipo_documento = "formulario de apertura de cuenta"
calidad = "fotocopia con contraste medio"
dificultad = "un sello parcialmente superpuesto al número de documento"
privacidad = "todos los nombres y números deben ser ficticios"

# Combina las dimensiones en una instrucción reproducible.
prompt = (
    f"Genera un {tipo_documento}. "
    f"Calidad visual: {calidad}. "
    f"Dificultad: {dificultad}. "
    f"Privacidad: {privacidad}."
)

# Muestra el prompt antes de utilizarlo en una API con costo.
print(prompt)

# Resumen final: este ejercicio controla las variables de un caso sintético.
# Cambia solo calidad y conserva las demás condiciones para comparar resultados.
