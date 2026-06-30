"""Demo de consola (rich) — Async vs Secuencial en tareas I/O-bound.

Sin API key. Ejecutar:  python demo_4_async_vs_secuencial.py

Simula 5 "descargas" de 0.5s cada una. Secuencial tarda ~2.5s; async con
asyncio.gather tarda ~0.5s porque las esperas se solapan. Solo funciona porque
el cuello de botella es ESPERA (I/O), no calculo (CPU).
"""

import asyncio
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

# Fuerza UTF-8 para que emojis/tildes se vean bien en cualquier consola Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

console = Console()

N = 5
DELAY = 0.5  # segundos por "descarga"


def descargar(i: int) -> str:
    time.sleep(DELAY)  # simula espera de red/IO (bloqueante)
    return f"doc-{i}"


async def descargar_async(i: int) -> str:
    await asyncio.sleep(DELAY)  # simula espera de red/IO (no bloqueante)
    return f"doc-{i}"


def _progress() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    )


def correr_secuencial() -> float:
    inicio = time.perf_counter()
    with _progress() as p:
        tarea = p.add_task("[red]Secuencial", total=N)
        for i in range(N):
            descargar(i)
            p.advance(tarea)
    return time.perf_counter() - inicio


async def correr_async() -> float:
    inicio = time.perf_counter()
    with _progress() as p:
        tarea = p.add_task("[green]Async (gather)", total=N)

        async def una(i: int) -> None:
            await descargar_async(i)
            p.advance(tarea)

        await asyncio.gather(*[una(i) for i in range(N)])
    return time.perf_counter() - inicio


def main() -> None:
    console.print(
        Panel(
            "[bold]⚡ Async vs Secuencial (tareas I/O-bound)[/]\n"
            f"[dim]{N} descargas de {DELAY}s cada una[/]",
            border_style="cyan", box=box.DOUBLE,
        )
    )

    console.print("\n[bold]1) Ejecución secuencial[/]")
    ts = correr_secuencial()

    console.print("\n[bold]2) Ejecución asíncrona[/]")
    ta = asyncio.run(correr_async())

    t = Table(title="Comparación de tiempos", box=box.ROUNDED, title_style="bold")
    t.add_column("Modo", style="bold")
    t.add_column("Tiempo", justify="right")
    t.add_row("[red]Secuencial[/]", f"{ts:.2f}s")
    t.add_row("[green]Async (gather)[/]", f"{ta:.2f}s")
    console.print(t)

    speedup = ts / ta if ta else 0.0
    console.print(
        Panel(
            f"[bold green]{speedup:.1f}× más rápido[/] — y solo porque el cuello de botella "
            "es [bold]espera (I/O)[/], no cálculo. Para CPU-bound, async NO ayuda.",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
