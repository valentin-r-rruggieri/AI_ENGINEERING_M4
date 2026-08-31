# Este archivo resume L4 mediante un caso práctico de self-attention.
# Lee cada bloque y modifica una variable por vez.

"""Caso 2: observar qué tokens se relacionan dentro de una cláusula.

GUÍA DOCENTE
CUÁNDO USAR: para explicar Query, Key, Value y pesos de atención.
DIFERENCIA: atención pondera relaciones; no es una búsqueda literal de palabras.
EN CLASE: leer filas y columnas de la matriz de atención.
"""

# Carga el .env para mantener el patrón uniforme de los resúmenes.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain e intenta importar PyTorch para calcular una atención pequeña.
from langchain_openai import ChatOpenAI
try:
    import torch
except ImportError:
    torch = None

# Representa tres tokens de una cláusula mediante vectores de dimensión cuatro.
tokens = ["contrato", "vence", "mañana"]

if torch:
    # Fija la semilla y calcula atención de un único head en CPU.
    torch.manual_seed(7)
    entrada = torch.randn(1, 3, 4)
    capa = torch.nn.MultiheadAttention(embed_dim=4, num_heads=1, batch_first=True)
    _, pesos = capa(entrada, entrada, entrada)
    forma_pesos = tuple(pesos.shape)
else:
    # Mantiene visible la forma de una matriz de atención sin PyTorch.
    forma_pesos = (1, len(tokens), len(tokens))

# Pide a LangChain una explicación legible de la matriz de atención.
explicacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    f"Explica en una oración qué significa una matriz de atención con forma {forma_pesos}."
).content

# Muestra qué tamaño tienen las relaciones token a token.
print({"tokens": tokens, "forma_atencion": forma_pesos, "explicacion": explicacion})

# Resumen final: cada token puede ponderar a los demás tokens de la secuencia.
# Explicá por qué una secuencia de cuatro tokens produciría una matriz 4 x 4.
