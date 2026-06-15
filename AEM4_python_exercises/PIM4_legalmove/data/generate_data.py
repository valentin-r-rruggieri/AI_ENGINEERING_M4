"""
Genera imagenes PNG y golden datasets para PIM4 LegalMove.

Archivos:
  - contrato_original.png
  - adenda_simple.png      (1 cambio: duracion 12 -> 18 meses)
  - adenda_compleja.png    (3 cambios: precio, duracion, territorio)
  - expected/cambio_simple.json
  - expected/cambio_complejo.json
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).parent
EXPECTED_DIR = OUTPUT_DIR / "expected"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
EXPECTED_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size: int) -> ImageFont.FreeTypeFont:
    paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font, max_chars: int = 92) -> int:
    line = ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if len(test) > max_chars:
            draw.text((x, y), line, fill=(35, 35, 35), font=font)
            y += 22
            line = word
        else:
            line = test
    if line:
        draw.text((x, y), line, fill=(35, 35, 35), font=font)
        y += 22
    return y


def draw_doc(title: str, subtitle: str, clauses: list[tuple[str, str, str]], color=(255, 255, 255), height=720) -> Image.Image:
    width = 850
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)
    fonts = {
        "title": get_font(18),
        "sub": get_font(12),
        "head": get_font(13),
        "body": get_font(11),
    }

    draw.rectangle([(0, 0), (width, 86)], fill=(238, 241, 245))
    draw.text((42, 18), title, fill=(15, 35, 80), font=fonts["title"])
    draw.text((42, 52), subtitle, fill=(80, 80, 80), font=fonts["sub"])
    draw.line([(42, 92), (width - 42, 92)], fill=(20, 20, 20), width=2)

    y = 118
    for number, heading, text in clauses:
        draw.text((42, y), f"Clausula {number} - {heading}", fill=(0, 55, 145), font=fonts["head"])
        y += 27
        y = wrap(draw, text, 58, y, fonts["body"])
        y += 18

    y = max(y + 12, height - 118)
    draw.text((42, y), "Firma y sello de las partes:", fill=(80, 80, 80), font=fonts["sub"])
    draw.rectangle([(42, y + 24), (350, y + 76)], outline=(145, 145, 145), width=1)
    draw.rectangle([(455, y + 24), (765, y + 76)], outline=(145, 145, 145), width=1)
    draw.text((42, y + 82), "CLIENTE", fill=(120, 120, 120), font=fonts["sub"])
    draw.text((455, y + 82), "PROVEEDOR", fill=(120, 120, 120), font=fonts["sub"])
    return img


def create_contrato_original() -> Image.Image:
    return draw_doc(
        "CONTRATO COMERCIAL DE SERVICIOS",
        "Version original - Enero 2024",
        [
            ("1", "Monto mensual de pago", "El cliente abonara al proveedor la suma de pesos un mil ($1.000) mensuales, pagaderos dentro de los primeros cinco dias habiles de cada mes."),
            ("2", "Duracion del contrato", "El presente contrato tendra una vigencia de doce (12) meses, contados a partir de la fecha de firma del presente instrumento."),
            ("3", "Territorio de operacion", "El proveedor prestara los servicios objeto de este contrato exclusivamente en el territorio de la Republica Argentina."),
            ("4", "Confidencialidad", "Las partes se comprometen a mantener confidencialidad sobre toda informacion intercambiada durante la relacion contractual."),
        ],
    )


def create_adenda_simple() -> Image.Image:
    return draw_doc(
        "ADENDA NRO 1",
        "Modificacion simple - Marzo 2024",
        [
            ("2 modificada", "Nueva duracion del contrato", "Por acuerdo de partes, la vigencia del contrato se extiende a dieciocho (18) meses, quedando sin efecto el plazo de doce meses estipulado en la clausula 2 original."),
        ],
        color=(255, 255, 247),
        height=560,
    )


def create_adenda_compleja() -> Image.Image:
    return draw_doc(
        "ADENDA NRO 2",
        "Modificacion compleja - Julio 2024",
        [
            ("1 modificada", "Nuevo monto mensual de pago", "Por acuerdo de partes, el monto mensual se incrementa a pesos un mil quinientos ($1.500), quedando sin efecto el monto de la clausula 1 original."),
            ("2 modificada", "Nueva duracion del contrato", "La vigencia del contrato se extiende a veinticuatro (24) meses, quedando sin efecto el plazo original de doce meses."),
            ("3 modificada", "Expansion del territorio de operacion", "El proveedor amplia la prestacion de servicios a los territorios de Argentina, Uruguay y Paraguay."),
        ],
        color=(255, 255, 247),
        height=700,
    )


def save_expected(name: str, payload: dict) -> None:
    path = EXPECTED_DIR / f"{name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK expected/{path.name}")


def main() -> None:
    print("Generando imagenes y golden datasets de PIM4...")
    create_contrato_original().save(OUTPUT_DIR / "contrato_original.png", "PNG", dpi=(150, 150))
    print("  OK contrato_original.png")
    create_adenda_simple().save(OUTPUT_DIR / "adenda_simple.png", "PNG", dpi=(150, 150))
    print("  OK adenda_simple.png")
    create_adenda_compleja().save(OUTPUT_DIR / "adenda_compleja.png", "PNG", dpi=(150, 150))
    print("  OK adenda_compleja.png")

    save_expected("cambio_simple", {
        "sections_changed": ["duration"],
        "topics_touched": ["duracion contractual"],
        "summary_of_the_change": "La duracion del contrato se extiende de 12 a 18 meses.",
    })
    save_expected("cambio_complejo", {
        "sections_changed": ["payment_terms", "duration", "service_territory"],
        "topics_touched": ["monto mensual", "duracion contractual", "territorio de operacion"],
        "summary_of_the_change": "El monto mensual sube de $1.000 a $1.500. La duracion se extiende de 12 a 24 meses. El territorio se amplia de Argentina a Argentina, Uruguay y Paraguay.",
    })
    print(f"Dataset PIM4 generado en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
