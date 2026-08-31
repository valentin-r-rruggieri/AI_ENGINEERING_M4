"""Entry point oficial que recibe dos imágenes y emite el JSON validado.

La salida estándar contiene solo ContractChangeOutput; los errores se escriben en stderr.
"""

# Importa argparse, JSON, stderr y rutas para implementar la interfaz pedida.
import argparse
import json
import sys
from pathlib import Path

# Importa dotenv para cargar credenciales sin hardcodearlas.
from dotenv import load_dotenv

# Importa configuración, errores y pipeline completo.
from .config import Settings
from .errors import LegalMoveError
from .pipeline import analyze_contracts


# Fuerza UTF-8 para que el JSON conserve acentos al ejecutarse o redirigirse en Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# Localiza el .env dentro de la carpeta raíz del proyecto oficial.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Declara exactamente los dos paths posicionales exigidos por la rúbrica.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compara un contrato original y su adenda mediante LegalMove."
    )
    parser.add_argument("original_path", help="Ruta PNG, JPG o JPEG del contrato original.")
    parser.add_argument("amendment_path", help="Ruta PNG, JPG o JPEG de la adenda.")
    return parser


# Ejecuta la aplicación y devuelve un código compatible con shells y CI.
def main(argv: list[str] | None = None) -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    argumentos = build_parser().parse_args(argv)

    try:
        configuracion = Settings.from_env()
        resultado = analyze_contracts(
            argumentos.original_path,
            argumentos.amendment_path,
            settings=configuracion,
        )
        print(json.dumps(resultado.output.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0
    except LegalMoveError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        # Evita exponer detalles sensibles y conserva un mensaje útil para la demo.
        print(f"Error inesperado: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


# Permite ejecutar python -m src.main desde la raíz del proyecto.
if __name__ == "__main__":
    raise SystemExit(main())
