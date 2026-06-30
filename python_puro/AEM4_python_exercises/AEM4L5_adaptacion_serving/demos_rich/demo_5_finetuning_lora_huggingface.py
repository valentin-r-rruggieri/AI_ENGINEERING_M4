"""Demo de consola (rich) — Fine-tuning LoRA con Hugging Face + PEFT, EXPLICADO.

Ejecutar:  python demo_5_finetuning_lora_huggingface.py

⚠️  Este script NO entrena nada: MUESTRA y EXPLICA el código real de cómo se
hace fine-tuning con LoRA usando `transformers` + `peft`. El entrenamiento de
verdad necesita GPU y descargar el modelo (ideal: Google Colab con GPU), por eso
acá solo se ilustra paso a paso (como dice el material: no se entrena LoRA en vivo).

Por eso este script SOLO necesita `rich` (no requiere torch/transformers/peft).
"""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import box

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

console = Console()


def codigo(src: str) -> Syntax:
    """Devuelve el código con resaltado de sintaxis para mostrar en consola."""
    return Syntax(src.strip("\n"), "python", theme="monokai", line_numbers=True, word_wrap=True)


# ---------------------------------------------------------------------------
# Pasos del fine-tuning LoRA con Hugging Face (título, explicación, código real)
# ---------------------------------------------------------------------------
PASOS = [
    (
        "1) Instalar las librerías",
        "LoRA NO se entrena con LangChain. Se usa el stack de Hugging Face: "
        "`transformers` (modelos), `peft` (LoRA/adaptadores), `datasets` (datos), "
        "`accelerate` (entrenamiento) y, opcional, `bitsandbytes` para 4-bit (QLoRA).",
        """
# En una terminal con GPU (ej. Colab):
# pip install transformers peft accelerate datasets bitsandbytes
""",
    ),
    (
        "2) Cargar el modelo base + tokenizer",
        "El modelo base queda CONGELADO (no se modifican sus pesos). El tokenizer "
        "convierte texto en tokens que el modelo entiende.",
        """
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-3.2-1B"   # un modelo base preentrenado

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
""",
    ),
    (
        "3) Configurar LoRA con PEFT",
        "Acá está el corazón de LoRA: definimos adaptadores pequeños y entrenables "
        "que se insertan en ciertas capas (target_modules). El modelo base sigue congelado.",
        """
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    r=8,                       # rank: tamaño del adaptador (más alto = más capacidad)
    lora_alpha=16,            # escala del adaptador (suele ser 2x el rank)
    lora_dropout=0.05,        # regularización para evitar overfitting
    target_modules=["q_proj", "v_proj"],  # qué capas adaptar (atención)
    bias="none",
    task_type=TaskType.CAUSAL_LM,  # tarea: generación de texto
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()   # muestra cuántos params se entrenan
""",
    ),
    (
        "4) Preparar el dataset de dominio",
        "Los datos específicos de tu dominio (legal, salud, soporte...). Se tokenizan "
        "para que el modelo los pueda procesar.",
        """
from datasets import load_dataset

dataset = load_dataset("json", data_files="datos_dominio.jsonl")

def tokenizar(ejemplo):
    return tokenizer(ejemplo["text"], truncation=True, max_length=512)

tokenized = dataset.map(tokenizar, batched=True)
""",
    ),
    (
        "5) Entrenar (solo se actualiza el adaptador)",
        "El Trainer entrena ÚNICAMENTE los pocos parámetros del adaptador LoRA. "
        "El modelo base no cambia. Esto es lo que hace a LoRA barato y rápido.",
        """
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

args = TrainingArguments(
    output_dir="adapter_legal_v1",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=True,                 # media precisión: más rápido en GPU
    logging_steps=10,
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()
""",
    ),
    (
        "6) Guardar el adaptador (liviano)",
        "save_pretrained guarda SOLO el adaptador (unos pocos MB), no el modelo base "
        "entero. Por eso podés tener muchos adaptadores por cliente/dominio.",
        """
model.save_pretrained("adapter_legal_v1")
tokenizer.save_pretrained("adapter_legal_v1")
# -> carpeta de pocos MB con los pesos del adaptador
""",
    ),
    (
        "7) Cargar el adaptador para usarlo (inferencia)",
        "En producción cargás el modelo base + el adaptador entrenado. Ese modelo "
        "adaptado es el que después orquesta LangChain (ver Notebook N1).",
        """
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B", device_map="auto")
model = PeftModel.from_pretrained(base, "adapter_legal_v1")

# A partir de acá: model.generate(...) responde con el dominio adaptado.
# Y un endpoint que sirva este model puede integrarse en una chain de LangChain.
""",
    ),
]


def tabla_hiperparametros() -> Table:
    t = Table(title="Hiperparámetros clave de LoraConfig", box=box.ROUNDED, title_style="bold")
    t.add_column("Parámetro", style="bold cyan")
    t.add_column("Qué controla")
    t.add_column("Valor típico", justify="right", style="green")
    filas = [
        ("r (rank)", "Capacidad del adaptador (más alto = más expresivo, más params)", "8 – 64"),
        ("lora_alpha", "Escala del aporte del adaptador", "16 – 32"),
        ("lora_dropout", "Regularización (evita overfitting)", "0.05 – 0.1"),
        ("target_modules", "Qué capas se adaptan (atención: q_proj, v_proj...)", "q_proj, v_proj"),
        ("task_type", "Tipo de tarea", "CAUSAL_LM"),
    ]
    for f in filas:
        t.add_row(*f)
    return t


def estimar_trainable() -> Panel:
    """Estima params entrenables de LoRA vs el modelo base (fórmula simplificada)."""
    d_model = 2048      # dimensión del modelo (ejemplo, ~1B)
    n_layers = 16       # capas
    n_target = 2        # q_proj y v_proj
    r = 8               # rank
    all_params = 1_100_000_000

    # LoRA por capa adaptada agrega A (d_model x r) + B (r x d_model) = 2 * d_model * r
    trainable = n_layers * n_target * (2 * d_model * r)
    pct = trainable / all_params * 100
    return Panel(
        f"Modelo (ejemplo): d_model={d_model}, capas={n_layers}, target={n_target}, r={r}\n\n"
        f"Entrenables (LoRA) : [bold green]{trainable:,}[/]\n"
        f"Totales (base)     : {all_params:,}\n"
        f"[bold green]Se entrena solo el {pct:.3f}% del modelo[/]\n\n"
        "[dim]Eso es exactamente lo que imprime model.print_trainable_parameters().[/]",
        title="📊 ¿Cuánto se entrena realmente?", border_style="green",
    )


def main() -> None:
    console.print(
        Panel(
            "[bold]🤗 Fine-tuning LoRA con Hugging Face + PEFT[/]\n"
            "[dim]Cómo adaptar un modelo a tu dominio entrenando pocos parámetros[/]",
            border_style="cyan", box=box.DOUBLE,
        )
    )
    console.print(
        Panel(
            "[yellow]⚠️  Este script EXPLICA el código real; no entrena (eso necesita GPU "
            "y descargar el modelo). Corrélo para leer y mostrar el flujo en clase; para "
            "entrenar de verdad, usá Google Colab con GPU e instalá las librerías del Paso 1.[/]",
            border_style="yellow",
        )
    )

    for titulo, explicacion, src in PASOS:
        console.rule(f"[bold]{titulo}")
        console.print(explicacion)
        console.print(codigo(src))

    console.rule("[bold]Referencia rápida")
    console.print(tabla_hiperparametros())
    console.print(estimar_trainable())

    console.print(
        Panel(
            "[bold]Resumen del flujo:[/]\n"
            "modelo base (congelado) → LoraConfig → get_peft_model → train → "
            "save_pretrained (adaptador liviano) → cargar con PeftModel → servir.\n\n"
            "[bold]Conexión con la clase:[/] LangChain [bold]no[/] entrena el adaptador; "
            "[green]orquesta[/] el modelo ya adaptado (prompts, routing, chains). Ver Notebook N1.",
            title="✅ Cierre", border_style="green",
        )
    )


if __name__ == "__main__":
    main()
