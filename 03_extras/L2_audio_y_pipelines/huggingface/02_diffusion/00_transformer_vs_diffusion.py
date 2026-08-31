# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Selección entre Transformer y difusión en audio.

GUÍA DOCENTE
CUÁNDO USAR: para elegir arquitectura según la tarea de audio.
DIFERENCIA: Transformers interpretan secuencias; difusión genera o restaura iterativamente.
EN CLASE: justificar la decisión con tarea, latencia y recursos.
"""

# Describe tres tareas y la familia normalmente más adecuada.
tareas = {
    "transcribir una llamada": "Transformer",
    "clasificar una intención": "Transformer",
    "generar un efecto de sonido": "Difusión",
    "restaurar audio degradado": "Difusión",
}

# Muestra las decisiones como una tabla textual pequeña.
for tarea, arquitectura in tareas.items():
    print(f"{tarea:30} -> {arquitectura}")

# Selecciona una tarea para discutir la latencia esperada.
tarea_elegida = "generar un efecto de sonido"
print("Selección:", tareas[tarea_elegida])

# Resumen final: este ejercicio relaciona arquitectura y caso de uso.
# Agrega text-to-speech y justifica dónde lo ubicarías.
