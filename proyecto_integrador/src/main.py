"""Entry point CLI para el pipeline LegalMove (PRODUCCION).

Formas de ejecutar
------------------
1. Sin argumentos (usa los archivos definidos abajo en "ARCHIVOS A COMPARAR"):
       python src/main.py
   o en VS Code: Run -> Run Without Debugging (Ctrl+F5).

2. Pasando tus propias imagenes:
       python src/main.py ruta/contrato.png ruta/adenda.png

3. Sin enviar a Langfuse:  agregar  --no-langfuse

Requiere OPENAI_API_KEY en el archivo .env (Langfuse es opcional).
La salida usa `rich` (colores, paneles, spinners) para diferenciar cada etapa.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from pipeline import run_pipeline

# Fuerza UTF-8 para tildes/ñ y emojis en cualquier terminal de Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Rich para una salida visual y diferenciada (ideal para dar la clase).
# Si no esta instalado, caemos a texto plano (no rompe). Para verlo lindo:
#     pip install rich        (o:  pip install -r requirements.txt)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box

    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    HAS_RICH = False
    print("[aviso] 'rich' no esta instalado: se usara salida de texto plano.")
    print("        Para la version visual:  pip install rich\n")

# Raiz del proyecto (proyecto_integrador/). Resuelve el .env y las rutas por
# defecto SIN depender del directorio desde el que se ejecute.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
#  ✏️  ARCHIVOS A COMPARAR  (editá acá para cambiar los documentos)
#  Estas rutas se usan cuando ejecutás main.py SIN pasar argumentos.
# ============================================================================
ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair1_simple/contrato_original.png"
ARCHIVO_ADENDA            = "data/test_contracts/pair1_simple/adenda_simple.png"
# Otros casos — descomentá el par que quieras probar:
# Par 2 (complejo):
# ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair2_complex/contrato_original.png"
# ARCHIVO_ADENDA            = "data/test_contracts/pair2_complex/adenda_compleja.png"
# Par 3 (manchado con café):
# ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair3_alquiler_cafe/contrato_original.png"
# ARCHIVO_ADENDA            = "data/test_contracts/pair3_alquiler_cafe/adenda.png"
# Par 4 (borroso):
# ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair4_laboral_borroso/contrato_original.png"
# ARCHIVO_ADENDA            = "data/test_contracts/pair4_laboral_borroso/adenda.png"
# Par 5 (roto/rasgado):
# ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair5_compraventa_roto/contrato_original.png"
# ARCHIVO_ADENDA            = "data/test_contracts/pair5_compraventa_roto/adenda.png"
# Par 6 (extremo: café + blur + ruido + rotación):
# ARCHIVO_CONTRATO_ORIGINAL = "data/test_contracts/pair6_extremo/contrato_original.png"
# ARCHIVO_ADENDA            = "data/test_contracts/pair6_extremo/adenda.png"
# ============================================================================

_DEFAULT_ORIGINAL = str(BASE_DIR / ARCHIVO_CONTRATO_ORIGINAL)
_DEFAULT_AMENDMENT = str(BASE_DIR / ARCHIVO_ADENDA)


def _panel_encabezado(args) -> None:
    """Imprime el encabezado y los parametros de la corrida."""
    langfuse_txt = "desactivado" if args.no_langfuse else "activo (si hay credenciales)"
    if not HAS_RICH:
        print("=" * 70)
        print("  LegalMove · Comparador de contratos (PRODUCCION)")
        print("=" * 70)
        print(f"  Contrato original : {Path(args.original_path).name}")
        print(f"  Adenda            : {Path(args.amendment_path).name}")
        print(f"  Langfuse          : {langfuse_txt}")
        return
    console.print(
        Panel(
            "[bold]⚖️  LegalMove[/] · Comparador de contratos con Vision + Agentes\n"
            "[dim]Modo PRODUCCIÓN (API real de OpenAI)[/]",
            border_style="cyan",
            box=box.DOUBLE,
        )
    )
    info = Table.grid(padding=(0, 2))
    info.add_column(style="bold")
    info.add_column()
    info.add_row("📄 Contrato original", Path(args.original_path).name)
    info.add_row("📝 Adenda", Path(args.amendment_path).name)
    info.add_row("📊 Langfuse", "[red]desactivado[/]" if args.no_langfuse else "[green]activo[/] (si hay credenciales)")
    console.print(info)


def _panel_resultado(output) -> None:
    """Muestra el ContractChangeOutput en una tabla dentro de un panel verde."""
    if not HAS_RICH:
        print("\n" + "=" * 70)
        print("  RESULTADO — Cambios detectados en la adenda")
        print("=" * 70)
        print("  Secciones : " + ", ".join(output.sections_changed))
        print("  Temas     : " + ", ".join(output.topics_touched))
        print("  Resumen   : " + output.summary_of_the_change)
        return
    tabla = Table(show_header=False, box=box.SIMPLE, expand=True)
    tabla.add_column(style="bold cyan", no_wrap=True, ratio=1)
    tabla.add_column(ratio=4)
    tabla.add_row("📑 Secciones", "\n".join(f"• {s}" for s in output.sections_changed))
    tabla.add_row("🏷️  Temas", "\n".join(f"• {t}" for t in output.topics_touched))
    tabla.add_row("📝 Resumen", output.summary_of_the_change)
    console.print(
        Panel(tabla, title="[bold]📦 Cambios detectados en la adenda", border_style="green")
    )


def main() -> None:
    """Entry point del CLI. Parsea argumentos y ejecuta el pipeline real."""
    load_dotenv(BASE_DIR / ".env")

    parser = argparse.ArgumentParser(
        description="LegalMove PIM4 - Comparador de contratos con Vision y Agentes (produccion).",
    )
    parser.add_argument(
        "original_path", type=str, nargs="?", default=_DEFAULT_ORIGINAL,
        help="Ruta a la imagen del contrato original (PNG/JPG/JPEG). Default: definido en el codigo.",
    )
    parser.add_argument(
        "amendment_path", type=str, nargs="?", default=_DEFAULT_AMENDMENT,
        help="Ruta a la imagen de la adenda (PNG/JPG/JPEG). Default: definido en el codigo.",
    )
    parser.add_argument(
        "--no-langfuse", action="store_true",
        help="Desactiva el envio de trazas a Langfuse (por defecto esta activo).",
    )
    args = parser.parse_args()

    _panel_encabezado(args)
    if HAS_RICH:
        console.rule("[bold]🚀 Pipeline: Vision → Agente 1 → Agente 2 → Validación")
    else:
        print("\n--- Ejecutando pipeline: Vision -> Agente 1 -> Agente 2 -> Validacion ---")

    inicio = time.perf_counter()
    try:
        result = run_pipeline(
            original_path=args.original_path,
            amendment_path=args.amendment_path,
            use_langfuse=not args.no_langfuse,
        )
    except Exception as exc:
        # Fallo controlado: p. ej. un documento demasiado degradado/ilegible hace
        # que el modelo no extraiga cambios válidos y Pydantic lo rechace.
        detalle = (
            f"{type(exc).__name__}: {exc}\n\n"
            "Causa probable: el documento estaba demasiado degradado o ilegible y el "
            "modelo no pudo extraer cambios válidos. La validación evitó devolver un "
            "resultado inventado. Probá con una imagen más legible."
        )
        if HAS_RICH:
            console.print(Panel(detalle, title="[bold red]❌ El pipeline no pudo completar", border_style="red"))
        else:
            print("\nERROR — el pipeline no pudo completar:\n" + detalle)
        sys.exit(1)
    total = time.perf_counter() - inicio

    _panel_resultado(result.output)

    if HAS_RICH:
        estado = "[bold green]✅ OK[/]" if result.trace.success else "[bold red]❌ FALLÓ[/]"
        console.print(f"\n⏱️  [bold]Tiempo total:[/] {total:.1f}s   ·   Estado: {estado}")
        if result.trace_url:
            console.print(f"🔗 [bold]Langfuse:[/] [link={result.trace_url}]{result.trace_url}[/link]")
    else:
        estado = "OK" if result.trace.success else "FALLO"
        print(f"\nTiempo total: {total:.1f}s   ·   Estado: {estado}")
        if result.trace_url:
            print(f"Langfuse: {result.trace_url}")


if __name__ == "__main__":
    main()
