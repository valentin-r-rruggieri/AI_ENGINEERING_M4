# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Binarización de texto con OpenCV.

GUÍA DOCENTE
CUÁNDO USAR: para separar texto oscuro de un fondo claro.
DIFERENCIA: un umbral fijo es simple; Otsu estima el corte desde la imagen.
EN CLASE: observar el histograma conceptual antes de aplicar Otsu.
"""

# Importa Path para las rutas y OpenCV para procesar píxeles.
from pathlib import Path
import cv2

# Carga directamente la imagen en escala de grises.
raiz = Path(__file__).resolve().parents[4]
entrada = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
salida = Path(__file__).resolve().parent / "formulario_binario.png"
imagen_gris = cv2.imread(str(entrada), cv2.IMREAD_GRAYSCALE)

# Calcula un umbral automático y guarda el resultado binario.
umbral, imagen_binaria = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite(str(salida), imagen_binaria)

# Informa el valor elegido automáticamente.
print({"umbral_otsu": umbral, "salida": str(salida)})

# Resumen final: este ejercicio separa texto y fondo con Otsu.
# Sustituye Otsu por un umbral fijo de 160 y compara la salida.
