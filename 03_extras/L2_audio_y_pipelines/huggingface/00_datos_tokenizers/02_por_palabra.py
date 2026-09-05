# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tokenización por palabra con un caso pequeño.

GUÍA DOCENTE
CUÁNDO USAR: para visualizar el enfoque más intuitivo de tokenización.
DIFERENCIA: cada palabra completa se vuelve una unidad del vocabulario.
EN CLASE: comparar una palabra conocida con una palabra nueva o mal escrita.
"""

# Define una frase breve similar a una transcripción de audio.
texto = "El paciente necesita una reprogramación clínica"

# Separa por espacios para representar el tokenizador por palabra más simple.
tokens = texto.lower().split()

# Crea un vocabulario mínimo como lo haría un dataset de entrenamiento pequeño.
vocabulario = {token: indice for indice, token in enumerate(sorted(set(tokens)), start=1)}

# Convierte cada palabra en su identificador numérico del vocabulario.
ids = [vocabulario[token] for token in tokens]

# Muestra todas las etapas para ver qué recibe un modelo después.
print({"texto": texto, "tokens": tokens, "vocabulario": vocabulario, "ids": ids})

# Resumen final: este enfoque es claro pero no maneja bien palabras nuevas.
# Cambia reprogramación por una palabra inventada y observa que exige un nuevo vocabulario.
