# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Accuracy de un clasificador mediante predicciones pequeñas.

GUÍA DOCENTE
CUÁNDO USAR: para medir cuántas etiquetas fueron acertadas.
DIFERENCIA: accuracy no muestra qué clase concentra los errores.
EN CLASE: calcular los aciertos manualmente antes de ejecutar.
"""

# Importa NumPy para comparar arreglos de etiquetas.
import numpy as np

# Simula etiquetas reales y predicciones de cuatro casos.
etiquetas = np.array([1, 1, 0, 0])
predicciones = np.array([1, 0, 0, 0])

# Compara posición por posición y calcula el promedio de aciertos.
aciertos = predicciones == etiquetas
accuracy = float(aciertos.mean())

# Muestra los casos y la métrica resultante.
print("Aciertos:", aciertos.tolist())
print("Accuracy:", accuracy)

# Resumen final: este ejercicio mide la proporción de casos correctos.
# Cambia la última predicción y observa el salto producido por un dataset pequeño.
