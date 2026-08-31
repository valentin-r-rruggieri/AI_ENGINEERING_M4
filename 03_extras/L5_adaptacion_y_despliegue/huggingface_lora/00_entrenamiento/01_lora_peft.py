# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Aplicación de LoRA a BERT tiny.

GUÍA DOCENTE
CUÁNDO USAR: para adaptar un modelo entrenando una fracción de sus parámetros.
DIFERENCIA: el modelo base se conserva y se agregan matrices de bajo rango.
EN CLASE: comparar parámetros totales y entrenables antes de entrenar.
"""

# Importa PEFT y Transformers para preparar el modelo.
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification

# Carga un clasificador BERT pequeño.
modelo_base = AutoModelForSequenceClassification.from_pretrained(
    "prajjwal1/bert-tiny",
    num_labels=2,
)

# Indica rango, dropout y módulos de atención que recibirá LoRA.
configuracion = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=4,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["query", "value"],
)
modelo_lora = get_peft_model(modelo_base, configuracion)

# Cuenta solamente los parámetros que actualizará el optimizador.
totales = sum(parametro.numel() for parametro in modelo_lora.parameters())
entrenables = sum(parametro.numel() for parametro in modelo_lora.parameters() if parametro.requires_grad)
print({"totales": totales, "entrenables": entrenables})
print("Porcentaje entrenable:", round(100 * entrenables / totales, 3))

# Resumen final: este ejercicio inyecta adapters LoRA en atención.
# Cambia r de 4 a 8 y observa cómo aumenta la cantidad entrenable.
