# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Idioma y segmentación de página en Tesseract.

GUÍA DOCENTE
CUÁNDO USAR: cuando idioma o layout afectan el reconocimiento.
DIFERENCIA: lang selecciona vocabulario; psm describe la organización de la página.
EN CLASE: probar una configuración por vez para poder comparar.
"""

# Importa las herramientas para abrir la imagen y ejecutar OCR.
from pathlib import Path
from PIL import Image
import pytesseract

# Selecciona una página con varios bloques de texto.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
configuracion = "--psm 6"

try:
    # Ejecuta OCR en español con un modo de bloque uniforme.
    texto = pytesseract.image_to_string(Image.open(ruta), lang="spa", config=configuracion)
    print(texto[:500])
except pytesseract.TesseractNotFoundError:
    print("Instalá Tesseract OCR antes de ejecutar el ejercicio.")
except pytesseract.TesseractError:
    print("Instalá el paquete de idioma español de Tesseract o cambia lang por eng.")

# Resumen final: este ejercicio controla idioma y segmentación del OCR.
# Cambia psm 6 por psm 11 y compara el orden del texto reconocido.
