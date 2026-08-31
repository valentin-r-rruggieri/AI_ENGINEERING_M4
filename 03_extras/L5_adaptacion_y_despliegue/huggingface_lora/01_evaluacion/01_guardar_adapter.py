# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Guardado y recarga de un adapter LoRA.

GUÍA DOCENTE
CUÁNDO USAR: para distribuir la adaptación sin duplicar el modelo base.
DIFERENCIA: el adapter contiene pocos pesos y necesita el mismo modelo base.
EN CLASE: inspeccionar la carpeta guardada y distinguir base de adapter.
"""

# Importa rutas, PEFT y el modelo base.
from pathlib import Path
from peft import LoraConfig, PeftModel, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification

# Crea un adapter sin entrenar para observar el mecanismo de persistencia.
nombre_modelo = "prajjwal1/bert-tiny"
modelo_base = AutoModelForSequenceClassification.from_pretrained(nombre_modelo, num_labels=2)
configuracion = LoraConfig(task_type=TaskType.SEQ_CLS, r=4, lora_alpha=8, target_modules=["query", "value"])
modelo_lora = get_peft_model(modelo_base, configuracion)

# Guarda únicamente los archivos del adapter.
carpeta = Path(__file__).resolve().parent / "adapter_demo"
modelo_lora.save_pretrained(carpeta)

# Carga otra copia del modelo base y conecta el adapter guardado.
base_nueva = AutoModelForSequenceClassification.from_pretrained(nombre_modelo, num_labels=2)
modelo_recargado = PeftModel.from_pretrained(base_nueva, carpeta)
print("Adapter guardado:", carpeta)
print("Modelo recargado:", type(modelo_recargado).__name__)

# Resumen final: este ejercicio persiste y recarga una adaptación separada.
# Revisa el tamaño de adapter_model y compáralo con el modelo base en caché.
