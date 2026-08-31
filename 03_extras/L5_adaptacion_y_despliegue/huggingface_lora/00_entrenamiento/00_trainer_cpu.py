# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Entrenamiento breve con Trainer en CPU.

GUÍA DOCENTE
CUÁNDO USAR: para adaptar todas las capas de un modelo a una clasificación.
DIFERENCIA: este baseline entrena el modelo completo; LoRA entrenará pocos parámetros.
EN CLASE: revisar dataset, tokenización y argumentos antes de entrenar.
"""

# Importa rutas, datasets y componentes de Transformers.
from pathlib import Path
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

# Carga el dataset local y el modelo BERT tiny.
ruta = Path(__file__).resolve().parents[1] / "data/intenciones.csv"
dataset = load_dataset("csv", data_files=str(ruta), split="train")
tokenizer = AutoTokenizer.from_pretrained("prajjwal1/bert-tiny")
modelo = AutoModelForSequenceClassification.from_pretrained("prajjwal1/bert-tiny", num_labels=2)

# Tokeniza todos los ejemplos y divide seis para entrenamiento y dos para prueba.
dataset = dataset.map(lambda lote: tokenizer(lote["texto"], truncation=True, padding="max_length", max_length=32), batched=True)
partes = dataset.train_test_split(test_size=0.25, seed=7)

# Configura una época pequeña sin servicios externos.
argumentos = TrainingArguments(
    output_dir=str(Path(__file__).resolve().parent / "salida_trainer"),
    num_train_epochs=1,
    per_device_train_batch_size=2,
    report_to="none",
    save_strategy="no",
)
entrenador = Trainer(model=modelo, args=argumentos, train_dataset=partes["train"])
entrenador.train()
print("Ejemplos entrenados:", len(partes["train"]))

# Resumen final: este ejercicio muestra el baseline de fine-tuning completo.
# Cambia la época a 2 y compara tiempo; no interpretes este dataset como benchmark.
