# Este archivo forma parte del recorrido práctico de PyTorch.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Proyecciones Query, Key y Value.

GUÍA DOCENTE
CUÁNDO USAR: como primer paso de self-attention.
DIFERENCIA: Q pregunta, K permite comparar y V aporta contenido.
EN CLASE: verificar que las tres matrices parten de los mismos embeddings.
"""

# Importa PyTorch y fija una semilla reproducible.
import torch
torch.manual_seed(4)

# Simula tres tokens con embeddings de dimensión cuatro.
embeddings = torch.randn(3, 4)

# Crea tres proyecciones lineales independientes.
proyeccion_q = torch.nn.Linear(4, 4, bias=False)
proyeccion_k = torch.nn.Linear(4, 4, bias=False)
proyeccion_v = torch.nn.Linear(4, 4, bias=False)
query = proyeccion_q(embeddings)
key = proyeccion_k(embeddings)
value = proyeccion_v(embeddings)

# Muestra que cada proyección conserva la forma pero cambia los valores.
print("Q shape:", tuple(query.shape))
print("K shape:", tuple(key.shape))
print("V shape:", tuple(value.shape))
print("Q y K son iguales:", torch.equal(query, key))

# Resumen final: este ejercicio produce Q, K y V desde los embeddings.
# Usa una dimensión de salida 2 y anticipa las nuevas formas.
