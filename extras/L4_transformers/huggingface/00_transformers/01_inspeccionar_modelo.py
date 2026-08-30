# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Inspección de parámetros de un Transformer pequeño.

GUÍA DOCENTE
CUÁNDO USAR: antes de decidir entre full fine-tuning y PEFT.
DIFERENCIA: parámetros totales y entrenables coinciden antes de congelar capas.
EN CLASE: relacionar tamaño del modelo con memoria de entrenamiento.
"""

# Importa el modelo automático de clasificación.
from transformers import AutoModelForSequenceClassification

# Carga BERT tiny con una cabeza para dos etiquetas.
modelo = AutoModelForSequenceClassification.from_pretrained(
    "prajjwal1/bert-tiny",
    num_labels=2,
)

# Cuenta parámetros totales y actualmente entrenables.
parametros_totales = sum(parametro.numel() for parametro in modelo.parameters())
parametros_entrenables = sum(
    parametro.numel() for parametro in modelo.parameters() if parametro.requires_grad
)

# Muestra la escala antes de aplicar LoRA.
print({"totales": parametros_totales, "entrenables": parametros_entrenables})
print("Porcentaje entrenable:", round(100 * parametros_entrenables / parametros_totales, 2))

# Resumen final: este ejercicio cuantifica el costo del modelo completo.
# Congela la primera capa y vuelve a calcular el porcentaje entrenable.
