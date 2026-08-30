# Este archivo forma parte del recorrido práctico de PyTorch.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Tabla de embeddings para convertir IDs en vectores.

GUÍA DOCENTE
CUÁNDO USAR: al transformar tokens discretos en representaciones entrenables.
DIFERENCIA: el ID identifica; el embedding contiene características numéricas.
EN CLASE: relacionar vocabulario, dimensión y shape de salida.
"""

# Importa PyTorch y fija una semilla para repetir los valores.
import torch
torch.manual_seed(7)

# Crea un vocabulario de seis tokens con vectores de dimensión cuatro.
tabla_embeddings = torch.nn.Embedding(num_embeddings=6, embedding_dim=4)
ids = torch.tensor([1, 4, 1])

# Busca un vector por cada ID de entrada.
vectores = tabla_embeddings(ids)

# Muestra que IDs iguales producen inicialmente vectores iguales.
print("IDs:", ids.tolist())
print("Shape:", tuple(vectores.shape))
print("Primer y tercer vector iguales:", torch.equal(vectores[0], vectores[2]))

# Resumen final: este ejercicio transforma IDs en vectores densos.
# Cambia embedding_dim a 2 y observa la nueva forma del tensor.
