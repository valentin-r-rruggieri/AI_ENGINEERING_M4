# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline local de preprocesamiento, OCR y control de calidad.

GUÍA DOCENTE
CUÁNDO USAR: para automatizar documentos impresos conservando revisión humana.
DIFERENCIA: el pipeline combina señales visuales y textuales.
EN CLASE: seguir cada transformación y discutir dónde puede fallar.
"""

# Importa herramientas de rutas, OpenCV, Pillow y Tesseract.
from pathlib import Path
import cv2
from PIL import Image
import pytesseract

# Selecciona el formulario y prepara una imagen binaria en memoria.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
imagen_gris = cv2.imread(str(ruta), cv2.IMREAD_GRAYSCALE)
contraste = float(imagen_gris.std())
_, imagen_binaria = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

try:
    # Convierte el arreglo de OpenCV a Pillow y ejecuta OCR.
    texto = pytesseract.image_to_string(Image.fromarray(imagen_binaria), config="--psm 6")
    caracteres_utiles = len(texto.strip())
    requiere_revision = contraste < 35 or caracteres_utiles < 30
    print(texto[:500])
    print({"contraste": round(contraste, 2), "caracteres": caracteres_utiles, "revision": requiere_revision})
except pytesseract.TesseractNotFoundError:
    print("Instalá Tesseract OCR y agregalo al PATH de Windows.")

# Resumen final: este pipeline prepara, transcribe y controla una imagen.
# Cambia a la imagen borrosa y observa qué regla activa la revisión.
