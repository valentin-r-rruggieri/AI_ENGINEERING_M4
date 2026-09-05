# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tokenización por carácter con una frase de audio.

GUÍA DOCENTE
CUÁNDO USAR: para explicar cómo representar palabras no vistas sin token desconocido.
DIFERENCIA: cada letra, espacio o símbolo se vuelve una unidad.
EN CLASE: observar que cubre cualquier palabra pero alarga la secuencia.
"""

# Define una frase con una palabra larga que puede ser desconocida para un vocabulario.
texto = "El paciente necesita una reprogramación clínica"

# Convierte cada carácter, incluidos espacios y acentos, en un token individual.
tokens = list(texto.lower())

# Crea un vocabulario pequeño de caracteres observados en esta frase.
vocabulario = {caracter: indice for indice, caracter in enumerate(sorted(set(tokens)), start=1)}

# Reemplaza cada carácter por su identificador numérico correspondiente.
ids = [vocabulario[caracter] for caracter in tokens]

# Muestra longitud, caracteres e IDs para contrastar con tokenización por palabra.
print({"cantidad_tokens": len(tokens), "tokens": tokens, "ids": ids})

# Resumen final: los caracteres cubren palabras nuevas a costa de secuencias largas.
# Prueba un nombre propio y compara su longitud con una separación por palabras.
