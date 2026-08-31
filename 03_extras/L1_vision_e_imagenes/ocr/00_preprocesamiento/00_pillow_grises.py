# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Conversión de una imagen a escala de grises.

GUÍA DOCENTE
CUÁNDO USAR: antes del OCR cuando el color no aporta información textual.
DIFERENCIA: escala de grises reduce canales; todavía no separa texto y fondo.
EN CLASE: comparar modo RGB y modo L de Pillow.
"""

# Importa Path para localizar la imagen y Pillow para transformarla.
from pathlib import Path
from PIL import Image

# Abre el formulario incluido en L1.
raiz = Path(__file__).resolve().parents[4]
entrada = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"
salida = Path(__file__).resolve().parent / "formulario_grises.png"
imagen = Image.open(entrada)

# Convierte los tres canales de color en un canal de intensidad.
imagen_gris = imagen.convert("L")
imagen_gris.save(salida)

# Muestra el cambio realizado.
print({"modo_original": imagen.mode, "modo_nuevo": imagen_gris.mode, "salida": str(salida)})

# Resumen final: este ejercicio reduce la imagen a intensidades de gris.
# Repite el proceso con formulario_bancario_borroso.png y compara visualmente.
