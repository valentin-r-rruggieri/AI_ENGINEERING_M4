"""Demo de consola (rich) — Profiling con cProfile: lento vs optimizado.

Sin API key. Ejecutar:  python demo_3_cprofile.py

Perfila dos versiones de una limpieza de texto, muestra los hotspots en una
tabla coloreada (ncalls / tottime / cumtime) y compara los tiempos con el
speedup obtenido. La idea pedagogica: optimizar SOLO despues de medir, y
volver a medir para demostrar la mejora con numeros.
"""

import cProfile
import os
import pstats
import re
import sys
import time

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

# Datos de prueba (texto ruidoso a limpiar).
TEXTS = ["Hola!!! Esto es una prueba 123..." * 200 for _ in range(2000)]


def clean_text_slow(text: str) -> str:
    # Version lenta: recorre caracter por caracter.
    return "".join(c.lower() for c in text if c.isalnum() or c.isspace())


def clean_text_fast(text: str) -> str:
    # Version optimizada: una regex compilada en C.
    return re.sub(r"[^A-Za-z0-9\s]+", "", text).lower()


def run_slow() -> list[str]:
    return [clean_text_slow(t) for t in TEXTS]


def run_fast() -> list[str]:
    return [clean_text_fast(t) for t in TEXTS]


def cronometrar(fn) -> float:
    inicio = time.perf_counter()
    fn()
    return time.perf_counter() - inicio


def tabla_hotspots(fn, titulo: str) -> Table:
    """Perfila fn() y devuelve una tabla con las funciones que más tiempo consumen."""
    profiler = cProfile.Profile()
    profiler.enable()
    fn()
    profiler.disable()
    stats = pstats.Stats(profiler)

    t = Table(title=titulo, box=box.SIMPLE, title_style="bold")
    t.add_column("función", style="cyan")
    t.add_column("ncalls", justify="right")
    t.add_column("tottime", justify="right")
    t.add_column("cumtime", justify="right", style="bold")
    # Ordenar por cumtime (indice 3 de la tupla de stats) y tomar el top 6.
    items = sorted(stats.stats.items(), key=lambda kv: kv[1][3], reverse=True)[:6]
    for (archivo, linea, func), (cc, nc, tt, ct, callers) in items:
        nombre = f"{func} ({os.path.basename(archivo)}:{linea})"
        t.add_row(nombre[:42], str(nc), f"{tt:.3f}", f"{ct:.3f}")
    return t


def main() -> None:
    console.print(
        Panel(
            "[bold]🔬 Profiling con cProfile — lento vs optimizado[/]\n"
            "[dim]Medir, optimizar y volver a medir[/]",
            border_style="cyan", box=box.DOUBLE,
        )
    )

    with console.status("[bold]Perfilando versión LENTA...", spinner="dots"):
        tabla_lenta = tabla_hotspots(run_slow, "🐢 Hotspots — versión LENTA (caracter por caracter)")
    console.print(tabla_lenta)

    with console.status("[bold]Perfilando versión OPTIMIZADA...", spinner="dots"):
        tabla_rapida = tabla_hotspots(run_fast, "⚡ Hotspots — versión OPTIMIZADA (regex)")
    console.print(tabla_rapida)

    # Tiempos sin profiler (mas representativos del speedup real).
    ts = cronometrar(run_slow)
    tf = cronometrar(run_fast)
    speedup = ts / tf if tf else 0.0

    comp = Table(title="Comparación de tiempos", box=box.ROUNDED, title_style="bold")
    comp.add_column("Versión", style="bold")
    comp.add_column("Tiempo", justify="right")
    comp.add_row("[red]Lenta[/]", f"{ts:.3f}s")
    comp.add_row("[green]Optimizada[/]", f"{tf:.3f}s")
    console.print(comp)

    console.print(
        Panel(
            f"[bold green]Speedup: {speedup:.1f}× más rápido[/]\n"
            "[dim]La mejora se demuestra con números comparables, no con intuición.[/]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
