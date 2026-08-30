"""Genera las cuatro imágenes de prueba usadas por el proyecto LegalMove.

Es material de apoyo fuera de la entrega oficial: los PNG ya generados son los
archivos que se usan al ejecutar el proyecto.
"""

# Importa rutas, ajuste de texto y Pillow para crear documentos legibles.
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


# Ubica la carpeta oficial sin depender de desde dónde se ejecute el script.
raiz = Path(__file__).resolve().parents[1] / "PIM4_legalmove" / "data" / "test_contracts"


# Busca una fuente común de Windows y usa la fuente predeterminada como respaldo.
def cargar_fuente(tamano: int):
    for ruta in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]:
        if Path(ruta).exists():
            return ImageFont.truetype(ruta, tamano)
    return ImageFont.load_default()


# Dibuja un documento simple, grande y fácil de leer por GPT-4o Vision.
def crear_documento(ruta: Path, titulo: str, lineas: list[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    imagen = Image.new("RGB", (1600, 2100), "white")
    dibujo = ImageDraw.Draw(imagen)
    fuente_titulo = cargar_fuente(42)
    fuente_texto = cargar_fuente(28)
    x, y = 120, 110
    dibujo.text((x, y), titulo, fill="black", font=fuente_titulo)
    y += 100
    for linea in lineas:
        for fragmento in wrap(linea, width=82, break_long_words=False):
            dibujo.text((x, y), fragmento, fill="black", font=fuente_texto)
            y += 44
        y += 22
    imagen.save(ruta)


# Crea el caso simple: dos modificaciones claras y sin ambigüedades.
crear_documento(
    raiz / "caso_simple" / "contrato_original.png",
    "CONTRATO DE SERVICIOS",
    [
        "Entre LegalMove S.A. y Cliente Demo S.R.L. se celebra el presente contrato.",
        "CLÁUSULA 1 - OBJETO. LegalMove prestará el servicio de revisión documental.",
        "CLÁUSULA 2 - MONTO MENSUAL. El cliente abonará USD 1.000 por mes.",
        "CLÁUSULA 3 - VENCIMIENTO. El contrato vencerá el 31 de diciembre de 2024.",
    ],
)
crear_documento(
    raiz / "caso_simple" / "adenda.png",
    "ADENDA NÚMERO 1 AL CONTRATO DE SERVICIOS",
    [
        "Las partes acuerdan modificar únicamente las cláusulas indicadas a continuación.",
        "CLÁUSULA 2 - MONTO MENSUAL. Se reemplaza USD 1.000 por USD 1.500 por mes.",
        "CLÁUSULA 3 - VENCIMIENTO. Se reemplaza el 31 de diciembre de 2024 por el 30 de junio de 2025.",
        "Las demás cláusulas del contrato original mantienen plena vigencia.",
    ],
)

# Crea el caso complejo: una adición, una modificación y una eliminación.
crear_documento(
    raiz / "caso_complejo" / "contrato_original.png",
    "ACUERDO DE CONFIDENCIALIDAD",
    [
        "Entre LegalMove S.A. y Cliente Demo S.R.L. se celebra este acuerdo de confidencialidad.",
        "CLÁUSULA 1 - INFORMACIÓN CONFIDENCIAL. Incluye datos técnicos, comerciales y legales.",
        "CLÁUSULA 3 - ALCANCE TERRITORIAL. Las obligaciones rigen exclusivamente en Argentina.",
        "CLÁUSULA 4 - RESTRICCIÓN DE USO. La información solo podrá usarse para evaluar una alianza comercial.",
        "CLÁUSULA 5 - VIGENCIA. La confidencialidad tendrá una duración de tres años.",
    ],
)
crear_documento(
    raiz / "caso_complejo" / "adenda.png",
    "ADENDA AL ACUERDO DE CONFIDENCIALIDAD",
    [
        "Las partes acuerdan los siguientes cambios al acuerdo original.",
        "CLÁUSULA 3 - ALCANCE TERRITORIAL. Se reemplaza Argentina por Argentina, Chile y Uruguay.",
        "CLÁUSULA 4 - RESTRICCIÓN DE USO. Se elimina la restricción que limita el uso a evaluar una alianza comercial.",
        "CLÁUSULA 6 - SEGURIDAD DE LA INFORMACIÓN. Se agrega la obligación de notificar incidentes de seguridad dentro de 48 horas.",
        "Las cláusulas no modificadas mantienen plena vigencia.",
    ],
)
