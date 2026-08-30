# Este archivo forma parte del recorrido práctico de PyTorch.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Bloque Transformer mínimo con atención y red feed-forward.

GUÍA DOCENTE
CUÁNDO USAR: para observar cómo se combinan los componentes de la arquitectura.
DIFERENCIA: el bloque agrega residual y normalización a la atención.
EN CLASE: seguir shape e identidad residual en cada etapa.
"""

# Importa PyTorch y fija una semilla para obtener la misma demostración.
import torch
torch.manual_seed(9)

# Prepara un lote con una secuencia de tres tokens y dimensión cuatro.
entrada = torch.randn(1, 3, 4)

# Crea los componentes mínimos de un bloque encoder.
atencion = torch.nn.MultiheadAttention(embed_dim=4, num_heads=1, batch_first=True)
normalizacion_1 = torch.nn.LayerNorm(4)
feed_forward = torch.nn.Sequential(
    torch.nn.Linear(4, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 4),
)
normalizacion_2 = torch.nn.LayerNorm(4)

# Aplica atención, residual, feed-forward y una segunda residual.
salida_atencion, pesos = atencion(entrada, entrada, entrada)
estado = normalizacion_1(entrada + salida_atencion)
salida = normalizacion_2(estado + feed_forward(estado))

# Muestra que el bloque conserva la forma de entrada.
print("Entrada:", tuple(entrada.shape))
print("Pesos de atención:", tuple(pesos.shape))
print("Salida:", tuple(salida.shape))

# Resumen final: este ejercicio integra atención, residual, FFN y normalización.
# Cambia num_heads a 2 y explica por qué embed_dim debe ser divisible.
