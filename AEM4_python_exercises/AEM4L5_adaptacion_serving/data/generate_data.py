"""Genera documentos para ejercicios de serving, profiling y async."""

from pathlib import Path

DATA_DIR = Path(__file__).parent
DOCS_DIR = DATA_DIR / "documentos"


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    docs = [
        "Ticket 101: cliente informa demora en entrega de notebook empresarial. Solicita prioridad alta.",
        "Ticket 102: usuario pide resumen de contrato de alquiler con foco en plazo y rescicion.",
        "Ticket 103: equipo comercial reporta error intermitente al generar propuestas en PDF.",
        "Ticket 104: area legal solicita clasificar clausulas de confidencialidad en 30 documentos.",
        "Ticket 105: soporte detecta picos de latencia durante procesamiento nocturno de contratos.",
        "Ticket 106: cliente solicita extraccion de action items desde minutas de reuniones semanales.",
    ]
    for i, text in enumerate(docs, start=1):
        (DOCS_DIR / f"doc_{i:02d}.txt").write_text(text, encoding="utf-8")

    base = (
        "El pipeline procesa documentos legales, limpia texto, busca patrones con expresiones regulares, "
        "resume contenido y valida campos. Algunas expresiones aparecen muchas veces: contrato, clausula, "
        "monto, plazo, territorio, rescicion, confidencialidad, auditoria. "
    )
    (DATA_DIR / "texto_largo.txt").write_text(base * 220, encoding="utf-8")

    print(f"Dataset L5 generado en: {DATA_DIR}")


if __name__ == "__main__":
    main()
