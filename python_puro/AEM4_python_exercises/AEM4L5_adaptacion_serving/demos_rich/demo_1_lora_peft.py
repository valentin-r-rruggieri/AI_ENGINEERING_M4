"""Demo de consola (rich) — LoRA / PEFT vs Full fine-tuning.

Sin API key. Ejecutar:  python demo_1_lora_peft.py

Muestra en consola, de forma visual:
- tabla comparativa full fine-tuning vs LoRA/PEFT;
- que fraccion de parametros se entrena con LoRA;
- cuanto storage se ahorra segun la cantidad de clientes/dominios.
"""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# Fuerza UTF-8 para que emojis/tildes se vean bien en cualquier consola Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

console = Console()


def tabla_comparativa() -> Table:
    t = Table(title="Full fine-tuning vs LoRA / PEFT", box=box.ROUNDED, title_style="bold")
    t.add_column("Aspecto", style="bold")
    t.add_column("Full fine-tuning", style="red")
    t.add_column("LoRA / PEFT", style="green")
    filas = [
        ("Parámetros entrenables", "Todos o casi todos", "Fracción pequeña"),
        ("Modelo base", "Se modifica", "Se congela"),
        ("Memoria de entrenamiento", "Alta", "Menor"),
        ("Storage por variante", "Alto", "Bajo"),
        ("Iteración", "Más lenta", "Más rápida"),
        ("Ideal para", "Cambios profundos", "Adaptación eficiente"),
    ]
    for f in filas:
        t.add_row(*f)
    return t


def tabla_storage() -> Table:
    t = Table(
        title="Storage según cantidad de clientes (modelo 14 GB · adapter 0.28 GB)",
        box=box.SIMPLE, title_style="bold",
    )
    t.add_column("Clientes", justify="right")
    t.add_column("Full (GB)", justify="right", style="red")
    t.add_column("LoRA (GB)", justify="right", style="green")
    t.add_column("Ahorro", justify="right", style="bold green")
    for n in (1, 5, 12, 50):
        full = 14.0 * n
        lora = 14.0 + 0.28 * n
        ahorro = 1 - lora / full
        t.add_row(str(n), f"{full:.1f}", f"{lora:.1f}", f"{ahorro:.0%}")
    return t


def main() -> None:
    console.print(
        Panel(
            "[bold]🧩 LoRA / PEFT vs Full fine-tuning[/]\n[dim]Adaptación eficiente de modelos[/]",
            border_style="cyan", box=box.DOUBLE,
        )
    )

    console.print(tabla_comparativa())

    base = 7_000_000_000
    adapter = 8_000_000
    pct = adapter / base * 100
    console.print(
        Panel(
            f"Modelo base    : [bold]{base:,}[/] parámetros\n"
            f"Adaptador LoRA : [bold]{adapter:,}[/] parámetros\n"
            f"[bold green]Entrenable     : {pct:.4f} %[/]",
            title="📊 ¿Cuánto se entrena con LoRA?", border_style="green",
        )
    )

    console.print(tabla_storage())

    console.print(
        Panel(
            "[bold]Conclusión:[/] LoRA brilla cuando hay [green]muchos clientes o dominios[/] "
            "y [green]recursos limitados[/]. Full fine-tuning conviene para cambios profundos "
            "con datos y presupuesto.",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    main()
