# Este archivo forma parte del resumen integrador de visión e imágenes.
# Ejecutalo para crear un formulario sintético que amplíe los datos didácticos.

"""Generación de un formulario bancario sintético con la API de imágenes.

GUÍA DOCENTE
CUÁNDO USAR: para crear ejemplos ficticios antes de probar un pipeline de visión.
DIFERENCIA: la imagen sirve como dato sintético de práctica, no como evidencia bancaria real.
EN CLASE: revisar manualmente la imagen generada antes de usarla como caso de evaluación.
"""

# Carga una sola vez las claves globales del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Base64 y Path para convertir y guardar los bytes de la imagen generada.
import base64
from pathlib import Path
from typing import Any, cast

# Importa el cliente oficial porque la generación usa el endpoint de imágenes de OpenAI.
from openai import OpenAI


# Ubica una carpeta separada para que los datos sintéticos no se mezclen con el golden case.
raiz = Path(__file__).resolve().parents[3]
carpeta_sinteticos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/sinteticos"
carpeta_sinteticos.mkdir(parents=True, exist_ok=True)
ruta_salida = carpeta_sinteticos / "formulario_bancario_sintetico.png"

# Define un formulario ficticio, útil para variar diseño y campos de práctica.
prompt = """
Crear una imagen vertical de un formulario bancario ficticio y profesional en español.
Encabezado: BANCO DEMO EDUCATIVO. Título: SOLICITUD DE CRÉDITO PERSONAL.
Incluir campos claramente delimitados: Nombre completo, DNI, Monto solicitado ARS,
Fecha de nacimiento, Teléfono de contacto y Firma del solicitante. Usar solo datos
de ejemplo obviamente ficticios, como Ana Ejemplo, 00.000.000 y $ 12.345,00. Diseño
limpio, fondo blanco, cabecera azul, texto legible, estilo formulario escaneado.
No usar logos reales, marcas reales, personas reales, firmas reales ni información personal real.
"""

# Solicita una imagen de baja calidad para que el ejercicio sea económico y rápido en clase.
cliente = OpenAI()
respuesta = cliente.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1024",
    quality="low",
    n=1,
)

# Decodifica la imagen Base64 que devuelve la API y la guarda como recurso local reutilizable.
imagenes = cast(list[Any], respuesta.data)
imagen_base64 = cast(str, imagenes[0].b64_json)
ruta_salida.write_bytes(base64.b64decode(imagen_base64))

# Muestra dónde quedó el recurso que luego puede usarse en los ejercicios de visión.
print({"imagen_sintetica": str(ruta_salida), "uso": "práctica visual; revisar antes de evaluar"})

# Resumen final: la generación amplía los ejemplos, pero no reemplaza un golden case validado.
# Modificá el prompt para crear una versión con campos más grandes o con otro diseño visual.
