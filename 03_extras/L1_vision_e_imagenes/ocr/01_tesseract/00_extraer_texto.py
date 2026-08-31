# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Extracción de texto con Tesseract.

GUÍA DOCENTE
CUÁNDO USAR: para documentos impresos con layout relativamente estable.
DIFERENCIA: Tesseract reconoce texto; no razona sobre el significado del documento.
EN CLASE: separar el concepto de OCR del análisis semántico posterior.
"""

# Importa Path y Pillow para abrir el recurso local.
from pathlib import Path
from PIL import Image

# Importa el puente de Python hacia el ejecutable Tesseract.
import pytesseract

# Localiza y abre el formulario de prueba.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

try:
    # Ejecuta OCR usando el modelo de idioma disponible por defecto.
    texto = pytesseract.image_to_string(Image.open(ruta))
    print(texto[:500])
except pytesseract.TesseractNotFoundError:
    print("Instalá Tesseract OCR y agregalo al PATH de Windows.")

# Resumen final: este ejercicio convierte una imagen en texto sin estructura.
# Cambia a la imagen borrosa y observa qué caracteres se degradan primero.
