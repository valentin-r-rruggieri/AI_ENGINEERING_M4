# Este archivo forma parte del recorrido práctico de PyTorch.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tensor pequeño y operaciones por filas.

GUÍA DOCENTE
CUÁNDO USAR: para representar lotes, tokens o características numéricas.
DIFERENCIA: un tensor incorpora forma, tipo y operaciones vectorizadas.
EN CLASE: leer shape antes de calcular cualquier operación.
"""

# Importa PyTorch para crear y operar tensores.
import torch

# Representa tres tokens mediante dos características cada uno.
tokens = torch.tensor([
    [1.0, 0.0],
    [0.5, 0.5],
    [0.0, 1.0],
])

# Calcula una suma por token y otra global.
suma_por_token = tokens.sum(dim=1)
suma_total = tokens.sum()

# Muestra forma y resultados para hacer visibles las dimensiones.
print("Shape:", tuple(tokens.shape))
print("Suma por token:", suma_por_token)
print("Suma total:", suma_total.item())

# Resumen final: este ejercicio presenta forma, dimensión y reducción.
# Cambia dim=1 por dim=0 y explica qué representa cada resultado.
