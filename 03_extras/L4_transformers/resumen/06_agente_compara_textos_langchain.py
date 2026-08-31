# Este archivo forma parte del resumen integrador de Transformers.
# Ejecutalo para comparar cómo cambian tokens y atención al cambiar el texto.

"""Agente LangChain que explica dos entradas antes de entrar a un Transformer.

GUÍA DOCENTE
CUÁNDO USAR: para enseñar que cada texto produce una cantidad distinta de tokens.
DIFERENCIA: la tokenización prepara los datos; el agente explica sus métricas.
EN CLASE: comparar la forma de atención de una frase corta y una más extensa.
"""

# Carga una sola vez las claves globales definidas en el archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa LangChain y Pydantic para convertir métricas técnicas en una explicación clara.
from langchain.agents import create_agent
from pydantic import BaseModel


# Define la respuesta que el agente debe producir para cada texto tokenizado.
class ExplicacionEntrada(BaseModel):
    texto: str = ""
    tokens: list[str] = []
    forma_atencion: str = ""
    explicacion: str


# Declara dos entradas contrastantes sin necesitar descargar un modelo pesado.
textos = [
    "el contrato vence mañana",
    "el contrato de servicios vence mañana y requiere una adenda firmada",
]

# Crea un agente que explica métricas calculadas localmente, no inventa el cálculo.
agente = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    response_format=ExplicacionEntrada,
    system_prompt=(
        "Sos tutor de Transformers. Conservá exactamente los tokens y la forma de atención "
        "recibidos. Explicá en lenguaje claro que una matriz de atención compara cada token "
        "con los demás tokens de esa misma entrada."
    ),
)

# Calcula la tokenización didáctica y la forma cuadrada de self-attention por texto.
for texto in textos:
    tokens = texto.split()
    forma_atencion = f"({len(tokens)}, {len(tokens)})"
    pedido = f"Texto: {texto}. Tokens: {tokens}. Forma de self-attention: {forma_atencion}."
    respuesta = agente.invoke({"messages": [{"role": "user", "content": pedido}]})["structured_response"]
    explicacion = ExplicacionEntrada.model_validate({
        **respuesta.model_dump(),
        "texto": texto,
        "tokens": tokens,
        "forma_atencion": forma_atencion,
    })
    print(explicacion.model_dump())

# Resumen final: más tokens cambian la matriz de atención y el costo del cálculo.
# Agregá una palabra a la primera frase y observá cómo cambia la forma cuadrada.
