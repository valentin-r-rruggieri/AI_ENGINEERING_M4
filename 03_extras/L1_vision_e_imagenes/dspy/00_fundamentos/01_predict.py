# Este archivo forma parte del recorrido práctico de DSPy.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Ejecución de un predictor DSPy.

GUÍA DOCENTE
CUÁNDO USAR: para convertir una signature en una llamada concreta al modelo.
DIFERENCIA: Predict realiza una inferencia directa; ChainOfThought pide razonamiento adicional.
EN CLASE: configurar el LM una sola vez y luego ejecutar el módulo.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar credenciales y DSPy para configurar el modelo.
import os
import dspy

# Prepara un fragmento contractual muy breve.
texto = "El contrato tendrá una vigencia de dieciocho meses desde su firma."

# Configura el modelo que utilizarán los módulos DSPy.
modelo = dspy.LM("openai/gpt-4.1-mini")
dspy.configure(lm=modelo)

# Declara y ejecuta una tarea pequeña de resumen.
resumir = dspy.Predict("texto -> resumen")
resultado = resumir(texto=texto)
print(resultado.resumen)
# Resumen final: este ejercicio ejecuta una signature mediante Predict.
# Cambia Predict por ChainOfThought y compara la estructura devuelta.
