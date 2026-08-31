# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Detección visual de una imagen con poco contraste.

GUÍA DOCENTE
CUÁNDO USAR: para derivar imágenes difíciles antes de ejecutar OCR.
DIFERENCIA: esta regla inspecciona píxeles, no la exactitud del texto reconocido.
EN CLASE: explicar por qué una única métrica visual es insuficiente.
"""

# Importa Path y OpenCV para medir la dispersión de intensidades.
from pathlib import Path
import cv2

# Carga una imagen degradada de los recursos de L1.
raiz = Path(__file__).resolve().parents[4]
ruta = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_borroso.png"
imagen = cv2.imread(str(ruta), cv2.IMREAD_GRAYSCALE)

# Usa la desviación estándar como aproximación pequeña al contraste.
contraste = float(imagen.std())
umbral = 35.0
requiere_revision = contraste < umbral

# Muestra la medición y la decisión.
print({"contraste": round(contraste, 2), "umbral": umbral, "requiere_revision": requiere_revision})

# Resumen final: este ejercicio detecta imágenes potencialmente difíciles.
# Cambia el umbral y compara la decisión sobre la imagen limpia.
