# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Inferencia con un pipeline de clasificación.

GUÍA DOCENTE
CUÁNDO USAR: para probar rápidamente un modelo preparado para una tarea.
DIFERENCIA: pipeline agrupa tokenizer, modelo y postprocesamiento.
EN CLASE: reconocer label y score como salida de inferencia.
"""

# Importa pipeline para construir una inferencia de alto nivel.
from transformers import pipeline

# Carga un modelo pequeño ya ajustado para sentimiento en inglés.
clasificador = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1,
)

# Clasifica dos textos para comparar puntajes.
textos = ["This agreement is clear and fair.", "This clause creates a serious risk."]
resultados = clasificador(textos)

# Muestra cada texto junto con su predicción.
for texto, resultado in zip(textos, resultados):
    print(texto, "->", resultado)

# Resumen final: este ejercicio usa una tarea completa con pipeline.
# Cambia un adjetivo del segundo texto y observa el score.
