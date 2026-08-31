# Este archivo forma parte del recorrido práctico de Hugging Face y LoRA.
# Ejecutalo para entrenar un adapter real, guardarlo y volver a cargarlo en CPU.
# pyright: reportPrivateImportUsage=false

"""Entrenamiento LoRA completo con un CSV local y BERT tiny.

GUÍA DOCENTE
CUÁNDO USAR: para demostrar una adaptación pequeña sin reentrenar todo el modelo.
DIFERENCIA: el modelo base se descarga una vez; LoRA guarda solo los pesos del adapter.
EN CLASE: seguir CSV -> tokens -> bucle PyTorch -> adapter guardado -> adapter recargado.
"""

# Importa CSV y Path para leer el dataset local sin depender de PyArrow.
import csv
from pathlib import Path
from typing import Any

# Importa PyTorch para el Dataset y la inferencia posterior al entrenamiento.
import torch
from torch.utils.data import Dataset

# Importa PEFT para insertar, guardar y recargar el adapter LoRA.
from peft import LoraConfig, PeftModel, TaskType, get_peft_model

# Importa el tokenizer y el clasificador BERT de Hugging Face.
from transformers import AutoModelForSequenceClassification, AutoTokenizer


# Define un Dataset mínimo que entrega tokens y la etiqueta esperada por el modelo.
class DatasetIntenciones(Dataset):
    def __init__(self, textos: list[str], etiquetas: list[int], tokenizer: Any) -> None:
        self.tokens = tokenizer(textos, truncation=True, padding=True, max_length=32)
        self.etiquetas = etiquetas

    def __len__(self) -> int:
        return len(self.etiquetas)

    def __getitem__(self, indice: int) -> dict[str, torch.Tensor]:
        item = {nombre: torch.tensor(valores[indice]) for nombre, valores in self.tokens.items()}
        item["labels"] = torch.tensor(self.etiquetas[indice])
        return item


# Fija una semilla para que la pequeña demo sea comparable entre ejecuciones.
torch.manual_seed(7)

# Ubica el CSV, la carpeta del adapter y el checkpoint liviano usado en clase.
base = Path(__file__).resolve().parents[1]
ruta_csv = base / "data/intenciones.csv"
carpeta_adapter = Path(__file__).resolve().parent / "adapter_entrenado_real"
nombre_modelo = "prajjwal1/bert-tiny"

# Lee ocho frases locales y separa texto de etiqueta: 1 cancelar, 0 consultar.
with ruta_csv.open(encoding="utf-8", newline="") as archivo_csv:
    filas = list(csv.DictReader(archivo_csv))
textos = [fila["texto"] for fila in filas]
etiquetas = [int(fila["label"]) for fila in filas]

# Descarga el tokenizer y el clasificador base una sola vez en la caché de Hugging Face.
tokenizer: Any = AutoTokenizer.from_pretrained(nombre_modelo)
modelo_base = AutoModelForSequenceClassification.from_pretrained(nombre_modelo, num_labels=2)
dataset = DatasetIntenciones(textos, etiquetas, tokenizer)

# Inserta LoRA solo en Query y Value para entrenar una fracción de los parámetros.
configuracion = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=4,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["query", "value"],
)
modelo_lora = get_peft_model(modelo_base, configuracion)
entrenables = sum(parametro.numel() for parametro in modelo_lora.parameters() if parametro.requires_grad)
totales = sum(parametro.numel() for parametro in modelo_lora.parameters())

# Entrena pocas épocas con un bucle explícito que solo actualiza los pesos LoRA.
modelo_lora.train()
optimizador = torch.optim.AdamW(
    [parametro for parametro in modelo_lora.parameters() if parametro.requires_grad],
    lr=0.005,
)
perdidas = []
for epoca in range(20):
    for indice in range(len(dataset)):
        lote = {nombre: tensor.unsqueeze(0) for nombre, tensor in dataset[indice].items()}
        salida = modelo_lora(**lote)
        salida.loss.backward()
        optimizador.step()
        optimizador.zero_grad()
        perdidas.append(round(float(salida.loss.item()), 4))

# Guarda solo el adapter LoRA entrenado, no una segunda copia completa de BERT tiny.
modelo_lora.save_pretrained(str(carpeta_adapter))

# Recarga un modelo base nuevo y conecta los pesos LoRA guardados en el paso anterior.
modelo_base_recargado = AutoModelForSequenceClassification.from_pretrained(nombre_modelo, num_labels=2)
modelo_recargado = PeftModel.from_pretrained(modelo_base_recargado, str(carpeta_adapter))
modelo_recargado.eval()

# Ejecuta inferencia con el adapter recargado para probar que el artefacto es reutilizable.
texto_prueba = "quiero cancelar el contrato hoy"
entrada = tokenizer(texto_prueba, return_tensors="pt")
with torch.no_grad():
    etiqueta_predicha = int(modelo_recargado(**entrada).logits.argmax(dim=-1).item())

# Muestra evidencia de entrenamiento, guardado, recarga e inferencia en una sola salida.
print({
    "modelo_base": nombre_modelo,
    "ejemplos_entrenamiento": len(dataset),
    "parametros_totales": totales,
    "parametros_entrenables_lora": entrenables,
    "porcentaje_entrenable": round(100 * entrenables / totales, 3),
    "perdida_inicial": perdidas[0],
    "perdida_final": perdidas[-1],
    "adapter_guardado": str(carpeta_adapter),
    "adapter_recargado": type(modelo_recargado).__name__,
    "texto_prueba": texto_prueba,
    "etiqueta_predicha": etiqueta_predicha,
})

# Resumen final: el adapter entrenado se guarda separado y se vuelve a conectar al modelo base.
# Agregá frases de cancelación y consulta al CSV antes de evaluar la calidad del clasificador.
