# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Conversión de una imagen local a Base64.

GUÍA DOCENTE
CUÁNDO USAR: cuando una API necesita recibir una imagen local como data URL.
DIFERENCIA: Base64 transporta bytes; no analiza ni modifica la imagen.
EN CLASE: mostrar la relación entre bytes, MIME type y data URL.
"""

# Importa base64 para convertir bytes binarios en texto transportable.
import base64

# Importa Path para construir una ruta portable dentro del repositorio.
from pathlib import Path

# Localiza el formulario que ya forma parte de los recursos de M4.
raiz = Path(__file__).resolve().parents[4]
imagen = raiz / "python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/formulario_bancario_limpio.png"

# Lee la imagen y transforma sus bytes a Base64.
contenido_base64 = base64.b64encode(imagen.read_bytes()).decode("utf-8")
data_url = f"data:image/png;base64,{contenido_base64}"

# Muestra solo una vista previa para no llenar la terminal.
print("Archivo:", imagen.name)
print("Inicio de la data URL:", data_url[:70] + "...")
print("Caracteres codificados:", len(contenido_base64))

# Resumen final: este ejercicio prepara una imagen local para una API multimodal.
# Cambia la imagen limpia por formulario_bancario_borroso.png y compara el tamaño.
