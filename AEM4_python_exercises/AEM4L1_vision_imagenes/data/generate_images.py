"""
Script de generación de imágenes de ejemplo para AEM4L1.

Crea 3 formularios bancarios como PNG usando Pillow:
  - formulario_bancario_limpio.png   → imagen clara y completa
  - formulario_bancario_cafe.png     → manchas de café sobre DNI y fecha
  - formulario_bancario_borroso.png  → imagen borrosa (blur de escáner)

Ejecutar con:
    python AEM4L1_vision_imagenes/data/generate_images.py

Requiere: pip install Pillow
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Obtiene una fuente escalable. Intenta varias rutas de sistema."""
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_bank_form(draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    """Dibuja el formulario bancario en el canvas dado."""
    W = 800

    # Header
    draw.rectangle([(0, 0), (W, 90)], fill=(0, 51, 153))
    draw.text((40, 15), "BANCO NACIONAL DE CRÉDITO", fill="white", font=fonts["title"])
    draw.text((40, 55), "SOLICITUD DE CRÉDITO PERSONAL", fill=(180, 210, 255), font=fonts["subtitle"])

    # Section divider
    draw.rectangle([(0, 90), (W, 94)], fill=(220, 165, 32))

    # Form fields
    draw.text((40, 110), "DATOS DEL SOLICITANTE", fill=(0, 51, 153), font=fonts["section"])

    fields = [
        ("Apellido y Nombre completo:", "Juan Pérez", 155),
        ("Número de Documento (DNI):", "40.111.222", 225),
        ("Monto Solicitado (ARS):", "$ 50.000,00", 295),
        ("Fecha de Nacimiento:", "12/05/1994", 365),
        ("Teléfono de contacto:", "011-4567-8901", 435),
    ]

    for label, value, y in fields:
        draw.text((40, y), label, fill=(80, 80, 80), font=fonts["label"])
        draw.rectangle([(40, y + 24), (W - 40, y + 56)], outline=(200, 200, 200), fill=(248, 248, 248), width=1)
        draw.text((52, y + 30), value, fill=(20, 20, 20), font=fonts["value"])

    # Signature section
    draw.text((40, 510), "Firma del Solicitante:", fill=(80, 80, 80), font=fonts["label"])
    draw.rectangle([(40, 535), (320, 590)], outline=(160, 160, 160), fill=(250, 250, 250), width=1)
    # Simulated signature strokes
    pts = [(60, 565), (100, 548), (140, 570), (190, 545), (240, 563), (280, 550), (310, 558)]
    draw.line(pts, fill=(20, 20, 80), width=2)

    # Checkbox
    draw.rectangle([(360, 538), (376, 554)], outline=(0, 130, 0), width=2)
    draw.text((358, 537), "✓", fill=(0, 150, 0), font=fonts["label"])
    draw.text((382, 538), "Firma presente", fill=(0, 130, 0), font=fonts["label"])

    # Footer
    draw.rectangle([(0, 605), (W, 620)], fill=(240, 240, 240))
    draw.text((40, 606), "Banco Nacional de Crédito S.A. — Uso exclusivo interno", fill=(150, 150, 150), font=fonts["small"])


def create_clean_form() -> Image.Image:
    """Formulario limpio y legible."""
    img = Image.new("RGB", (800, 620), color="white")
    draw = ImageDraw.Draw(img)
    fonts = {
        "title":    get_font(20),
        "subtitle": get_font(14),
        "section":  get_font(13),
        "label":    get_font(12),
        "value":    get_font(14),
        "small":    get_font(9),
    }
    draw_bank_form(draw, fonts)
    return img


def create_coffee_stained_form(base: Image.Image) -> Image.Image:
    """Formulario con manchas de café sobre DNI y fecha de nacimiento."""
    img = base.copy()
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Mancha principal sobre campo DNI (y=225–280)
    draw.ellipse([(180, 218), (490, 282)], fill=(139, 90, 43, 190))
    # Mancha secundaria con halo más claro
    draw.ellipse([(160, 210), (510, 290)], fill=(160, 110, 60, 80))

    # Mancha sobre campo Fecha de nacimiento (y=365–420)
    draw.ellipse([(130, 358), (420, 422)], fill=(150, 95, 40, 170))
    draw.ellipse([(115, 350), (440, 430)], fill=(170, 120, 65, 70))

    # Gotitas adicionales realistas
    draw.ellipse([(520, 240), (540, 258)], fill=(139, 90, 43, 140))
    draw.ellipse([(95, 375), (110, 388)],  fill=(139, 90, 43, 120))

    img_rgba = img.convert("RGBA")
    combined = Image.alpha_composite(img_rgba, overlay)
    return combined.convert("RGB")


def create_blurry_form(base: Image.Image) -> Image.Image:
    """Formulario borroso — simula escaneo de mala calidad."""
    blurry = base.filter(ImageFilter.GaussianBlur(radius=3.0))
    # Añadir leve ruido de papel
    blurry = blurry.filter(ImageFilter.SMOOTH_MORE)
    return blurry


def main() -> None:
    print("Generando imágenes de formulario bancario...")

    base = create_clean_form()
    path_limpio = OUTPUT_DIR / "formulario_bancario_limpio.png"
    base.save(path_limpio, "PNG", dpi=(150, 150))
    print(f"  OK {path_limpio.name}")

    cafe = create_coffee_stained_form(base)
    path_cafe = OUTPUT_DIR / "formulario_bancario_cafe.png"
    cafe.save(path_cafe, "PNG", dpi=(150, 150))
    print(f"  OK {path_cafe.name}")

    borroso = create_blurry_form(base)
    path_borroso = OUTPUT_DIR / "formulario_bancario_borroso.png"
    borroso.save(path_borroso, "PNG", dpi=(150, 150))
    print(f"  OK {path_borroso.name}")

    print(f"\nImágenes guardadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
