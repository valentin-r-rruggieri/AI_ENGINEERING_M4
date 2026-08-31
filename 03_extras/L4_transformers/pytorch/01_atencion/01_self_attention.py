# Este archivo forma parte del recorrido práctico de PyTorch.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Self-attention escalada paso a paso.

GUÍA DOCENTE
CUÁNDO USAR: para contextualizar cada token con respecto a los demás.
DIFERENCIA: softmax convierte similitudes en pesos que suman uno.
EN CLASE: seguir scores, pesos y suma ponderada por separado.
"""

# Importa math para el escalado y PyTorch para matrices y softmax.
import math
import torch

# Usa tres vectores simples como Q, K y V.
query = torch.tensor([[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]])
key = query.clone()
value = torch.tensor([[10.0, 0.0], [5.0, 5.0], [0.0, 10.0]])

# Calcula similitudes y las escala por la raíz de la dimensión.
scores = query @ key.T / math.sqrt(query.shape[-1])
pesos = torch.softmax(scores, dim=-1)
contexto = pesos @ value

# Muestra el peso y contexto del primer token.
print("Pesos del primer token:", pesos[0])
print("Suma de pesos:", pesos[0].sum().item())
print("Contexto del primer token:", contexto[0])

# Resumen final: este ejercicio completa una atención de una sola cabeza.
# Cambia el primer vector Value y observa cómo afecta al contexto.
