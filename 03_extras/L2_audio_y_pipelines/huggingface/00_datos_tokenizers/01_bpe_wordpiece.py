# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Comparación visible entre BPE y WordPiece.

GUÍA DOCENTE
CUÁNDO USAR: para entender cómo el vocabulario divide palabras desconocidas.
DIFERENCIA: GPT-2 usa BPE; BERT marca continuaciones WordPiece con ##.
EN CLASE: comparar la misma palabra poco frecuente en ambos tokenizers.
"""

# Importa AutoTokenizer para cargar tokenizadores desde Hub.
from transformers import AutoTokenizer

# Carga un tokenizer BPE y otro WordPiece.
tokenizer_bpe = AutoTokenizer.from_pretrained("gpt2")
tokenizer_wordpiece = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# Usa una palabra de dominio que puede dividirse en subwords.
texto = "hiperpersonalización contractual"
tokens_bpe = tokenizer_bpe.tokenize(texto)
tokens_wordpiece = tokenizer_wordpiece.tokenize(texto)

# Muestra las dos segmentaciones lado a lado.
print("BPE:", tokens_bpe)
print("WordPiece:", tokens_wordpiece)

# Resumen final: este ejercicio muestra dos estrategias de subwords.
# Cambia el texto por un apellido raro y compara la cantidad de tokens.
