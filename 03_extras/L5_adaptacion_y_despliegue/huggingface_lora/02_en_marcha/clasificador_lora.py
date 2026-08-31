# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Clasificador tiny entrenado con LoRA en CPU.

GUÍA DOCENTE
CUÁNDO USAR: para recorrer dataset, tokenización, PEFT, Trainer e inferencia.
DIFERENCIA: el ejercicio enseña el mecanismo; ocho filas no producen calidad real.
EN CLASE: verificar qué parámetros se entrenan y qué artefacto se guarda.
"""

# Importa rutas, PyTorch, Datasets, PEFT y Transformers.
from pathlib import Path
import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

# Carga los datos y los componentes del modelo tiny.
base = Path(__file__).resolve().parents[1]
dataset = load_dataset("csv", data_files=str(base / "data/intenciones.csv"), split="train")
nombre_modelo = "prajjwal1/bert-tiny"
tokenizer = AutoTokenizer.from_pretrained(nombre_modelo)
modelo = AutoModelForSequenceClassification.from_pretrained(nombre_modelo, num_labels=2)

# Tokeniza y aplica LoRA sobre Query y Value.
dataset = dataset.map(lambda lote: tokenizer(lote["texto"], truncation=True, padding="max_length", max_length=32), batched=True)
configuracion = LoraConfig(task_type=TaskType.SEQ_CLS, r=4, lora_alpha=8, target_modules=["query", "value"])
modelo = get_peft_model(modelo, configuracion)

# Entrena una sola época con lotes pequeños.
salida = Path(__file__).resolve().parent / "adapter_intenciones"
argumentos = TrainingArguments(
    output_dir=str(salida),
    num_train_epochs=1,
    per_device_train_batch_size=2,
    report_to="none",
    save_strategy="no",
)
Trainer(model=modelo, args=argumentos, train_dataset=dataset).train()
modelo.save_pretrained(salida)

# Ejecuta una inferencia corta con el modelo recién adaptado.
entrada = tokenizer("quiero terminar el contrato", return_tensors="pt", truncation=True)
with torch.no_grad():
    etiqueta = int(modelo(**entrada).logits.argmax(dim=-1).item())
print({"texto": "quiero terminar el contrato", "etiqueta": etiqueta, "adapter": str(salida)})

# Resumen final: este pipeline entrena, guarda y usa un adapter LoRA.
# Agrega más casos reales antes de interpretar la predicción como evidencia de calidad.
