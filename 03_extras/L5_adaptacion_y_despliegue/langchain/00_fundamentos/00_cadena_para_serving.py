# Este archivo forma parte del recorrido práctico de LangChain para serving.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Construye una cadena LangChain mínima que puede exponerse como servicio.

GUÍA DOCENTE
CUÁNDO USAR: antes de montar una capacidad LLM en FastAPI o un contenedor.
DIFERENCIA: una cadena separa prompt y modelo; el servidor solo expone la cadena.
EN CLASE: mostrar la cadena antes de explicar concurrencia, Docker y Kubernetes.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os para comprobar la clave de OpenAI.
import os

# Importa el prompt y el wrapper LangChain que se servirá después.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Define una entrada pequeña como la que llegaría desde un endpoint.
consulta = "¿Qué riesgo existe si un contrato no fija fecha de vencimiento?"

# Encadena prompt y modelo sin crear todavía un servidor web.
prompt = ChatPromptTemplate.from_template("Respondé en dos oraciones: {consulta}")
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta = cadena.invoke({"consulta": consulta})
print(respuesta.content)
# Resumen final: esta cadena es el objeto que FastAPI puede exponer y Docker contenerizar.
# Cambiá la consulta y observá que el contrato de entrada se mantiene.
