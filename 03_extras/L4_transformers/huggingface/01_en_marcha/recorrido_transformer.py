# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Recorrido de texto, tokens e inferencia Transformer.

GUÍA DOCENTE
CUÁNDO USAR: para conectar la teoría de tokens y tensores con un modelo real.
DIFERENCIA: pipeline oculta estos pasos; aquí se muestran de forma explícita.
EN CLASE: anticipar tokens, dimensiones y etiqueta antes de ejecutar.
"""

# Importa torch para desactivar gradientes durante la inferencia.
import torch

# Importa tokenizer y modelo automático de clasificación.
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Carga un modelo pequeño ya ajustado para sentimiento.
nombre_modelo = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(nombre_modelo)
modelo = AutoModelForSequenceClassification.from_pretrained(nombre_modelo)

# Convierte un texto en tokens y tensores de entrada.
texto = "This contract is clear and fair."
entradas = tokenizer(texto, return_tensors="pt")
tokens = tokenizer.convert_ids_to_tokens(entradas["input_ids"][0])

# Ejecuta el Transformer sin calcular gradientes.
with torch.no_grad():
    salida = modelo(**entradas)

# Convierte logits en probabilidades y obtiene la etiqueta principal.
probabilidades = torch.softmax(salida.logits, dim=-1)[0]
indice = int(torch.argmax(probabilidades))
etiqueta = modelo.config.id2label[indice]

# Muestra cada etapa del recorrido.
print("Tokens:", tokens)
print("Dimensión de entrada:", tuple(entradas["input_ids"].shape))
print("Resultado:", {"etiqueta": etiqueta, "confianza": round(float(probabilidades[indice]), 3)})

# Resumen final: este ejercicio hace visible el recorrido interno de un Transformer.
# Cambia el adjetivo fair por unfair y compara tokens y probabilidades.
