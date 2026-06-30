"""Demo de consola (rich) — Serverless vs Servidor persistente.

Sin API key. Ejecutar:  python demo_2_serverless_vs_server.py

Simula la latencia de 6 requests en cada patron para mostrar el efecto del
cold start (serverless) vs la latencia estable (servidor), y aplica una
funcion de decision sobre varios casos.
"""

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

# Factor para acelerar la demo en clase (los tiempos reales serian mayores).
ACELERAR = 0.3


def latencia_simulada(modo: str, indice: int) -> float:
    """Latencia (en segundos) de una request segun el patron de despliegue."""
    if modo == "serverless":
        return 1.2 if indice == 0 else 0.15  # 1ra request: cold start
    return 0.2  # servidor persistente: siempre caliente


def simular(modo: str, n: int = 6) -> list[float]:
    lat: list[float] = []
    console.print(f"\n[bold]Simulando {n} requests — {modo}[/]")
    for i in range(n):
        d = latencia_simulada(modo, i)
        time.sleep(d * ACELERAR)
        etiqueta = " [yellow](cold start)[/]" if (modo == "serverless" and i == 0) else ""
        color = "yellow" if etiqueta else ("green" if modo == "servidor" else "cyan")
        console.print(f"   req {i + 1}: [{color}]{d:.2f}s[/]{etiqueta}")
        lat.append(d)
    return lat


def elegir_arquitectura(trafico, latencia_estricta, presupuesto_bajo, modelo_grande) -> str:
    if latencia_estricta and trafico == "constante":
        return "Servidor persistente"
    if modelo_grande and latencia_estricta:
        return "Servidor persistente"
    if presupuesto_bajo and trafico == "irregular":
        return "Serverless"
    if trafico == "picos":
        return "Serverless o híbrido"
    return "Depende: analizar costo, latencia, operación y crecimiento"


def main() -> None:
    console.print(
        Panel(
            "[bold]☁️  Serverless vs 🖥️  Servidor persistente[/]\n"
            "[dim]Patrones de despliegue para sistemas de IA[/]",
            border_style="cyan", box=box.DOUBLE,
        )
    )

    lat_sl = simular("serverless")
    lat_sv = simular("servidor")

    resumen = Table(title="Resumen de latencias", box=box.ROUNDED, title_style="bold")
    resumen.add_column("Métrica", style="bold")
    resumen.add_column("Serverless", justify="right", style="cyan")
    resumen.add_column("Servidor", justify="right", style="green")
    resumen.add_row("1ra request", f"{lat_sl[0]:.2f}s", f"{lat_sv[0]:.2f}s")
    resumen.add_row("Promedio", f"{sum(lat_sl)/len(lat_sl):.2f}s", f"{sum(lat_sv)/len(lat_sv):.2f}s")
    resumen.add_row("Costo sin tráfico", "Bajo", "Alto")
    resumen.add_row("Riesgo principal", "Cold start", "Costo ocioso")
    console.print(resumen)

    casos = [
        ("App interna usada 10 veces/día", "irregular", False, True, False),
        ("Asistente de voz en tiempo real", "constante", True, False, True),
        ("Análisis legal con picos mensuales", "picos", False, True, False),
        ("API usada 24/7", "constante", False, False, False),
    ]
    dec = Table(title="Decisión de arquitectura", box=box.SIMPLE, title_style="bold")
    dec.add_column("Caso", style="bold")
    dec.add_column("Recomendación")
    for nombre, traf, lat, pres, grande in casos:
        r = elegir_arquitectura(traf, lat, pres, grande)
        color = "green" if "Servidor" in r else "cyan"
        dec.add_row(nombre, f"[{color}]{r}[/]")
    console.print(dec)

    console.print(
        Panel(
            "[bold]Conclusión:[/] no hay patrón “mejor”. Serverless gana con tráfico "
            "[cyan]irregular[/] y presupuesto bajo; servidor gana con tráfico [green]constante[/] "
            "y latencia estricta.",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    main()
