# Este archivo resume L4 mediante un caso práctico de tokens y embeddings.
# Lee cada bloque y modifica una variable por vez.

"""Caso 1: convertir una frase en tokens y vectores.

GUÍA DOCENTE
CUÁNDO USAR: antes de pasar texto a un Transformer.
DIFERENCIA: tokens son identificadores; embeddings son representaciones numéricas.
EN CLASE: seguir las dimensiones de cada transformación.
"""

# Carga el .env para mantener el patrón uniforme de los resúmenes.
from dotenv import load_dotenv
load_dotenv()

# Importa LangChain e intenta importar PyTorch para crear embeddings reales en CPU.
from langchain_openai import ChatOpenAI
try:
    import torch
except ImportError:
    torch = None

# Define una frase pequeña para observar cada etapa sin ruido.
texto = "el contrato vence mañana"
tokens = texto.split()
ids = list(range(1, len(tokens) + 1))

if torch:
    # Crea una capa de embedding pequeña y consulta su forma de salida.
    embedding = torch.nn.Embedding(num_embeddings=20, embedding_dim=4)
    vectores = embedding(torch.tensor([ids]))
    forma_vectores = tuple(vectores.shape)
else:
    # Conserva la forma esperada para explicar el concepto sin la dependencia.
    forma_vectores = (1, len(ids), 4)

# Pide a LangChain una explicación de la dimensión obtenida.
explicacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
    f"Explica en una oración qué representa la forma de embeddings {forma_vectores}."
).content

# Muestra texto, tokens, ids y la dimensión que recibirá la atención.
print({"tokens": tokens, "ids": ids, "forma_embeddings": forma_vectores, "explicacion": explicacion})

# Resumen final: cada token obtiene un vector de dimensión cuatro.
# Agrega una palabra y observá qué dimensión de la forma cambia.
