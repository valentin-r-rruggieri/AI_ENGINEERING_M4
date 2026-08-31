# Este archivo forma parte del recorrido práctico de OCR.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Similitud simple entre OCR y texto de referencia.

GUÍA DOCENTE
CUÁNDO USAR: para evaluar OCR con casos cuyo texto esperado es conocido.
DIFERENCIA: la similitud global no explica por sí sola cada tipo de error.
EN CLASE: discutir qué normalizaciones son válidas para el negocio.
"""

# Importa SequenceMatcher para comparar dos secuencias de caracteres.
from difflib import SequenceMatcher

# Define un texto esperado y una salida OCR con errores realistas.
referencia = "Titular Ana Perez Documento 30111222"
salida_ocr = "Titular Ana Peres Documento 301I1222"

# Normaliza mayúsculas y espacios antes de comparar.
referencia_normalizada = " ".join(referencia.lower().split())
ocr_normalizado = " ".join(salida_ocr.lower().split())
similitud = SequenceMatcher(None, referencia_normalizada, ocr_normalizado).ratio()

# Muestra una métrica entre cero y uno.
print({"similitud": round(similitud, 3), "requiere_revision": similitud < 0.95})

# Resumen final: este ejercicio convierte una comparación textual en una señal de calidad.
# Cambia un dígito adicional y observa cuánto afecta la similitud global.
