# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tokenización subword real con un tokenizer de Hugging Face.

GUÍA DOCENTE
CUÁNDO USAR: para representar palabras frecuentes completas y palabras nuevas en partes.
DIFERENCIA: combina cobertura de caracteres con secuencias más cortas que carácter por carácter.
EN CLASE: comparar la palabra larga con los dos ejercicios anteriores.
"""

# Importa AutoTokenizer para descargar o reutilizar un vocabulario subword entrenado.
from transformers import AutoTokenizer

# Carga un tokenizer multilingüe basado en WordPiece.
tokenizador = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# Usa una frase con una palabra de dominio y una posible palabra poco frecuente.
texto = "El paciente necesita una reprogramación clínica"

# Obtiene subtokens legibles y sus IDs reales del vocabulario del modelo.
subtokens = tokenizador.tokenize(texto)
ids = tokenizador.encode(texto, add_special_tokens=False)

# Muestra ambas representaciones para conectar texto, piezas e IDs.
print({"texto": texto, "subtokens": subtokens, "ids": ids, "cantidad_subtokens": len(subtokens)})

# Resumen final: subword equilibra palabras conocidas y cobertura ante palabras nuevas.
# Cambia hiperpersonalización por un término inventado y observa cómo se fragmenta.
