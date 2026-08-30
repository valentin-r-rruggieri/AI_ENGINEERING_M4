# Este archivo forma parte del recorrido práctico de LangChain.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Modelo y prompt mínimo con ChatOpenAI.

GUÍA DOCENTE
CUÁNDO USAR: para encapsular una llamada de chat dentro de LangChain.
DIFERENCIA: el modelo recibe mensajes con roles, no solo un string aislado.
EN CLASE: separar configuración del modelo e instrucción del usuario.
"""

# Importa os para validar credenciales y ChatOpenAI para la llamada.
import os
from langchain_openai import ChatOpenAI

# Define una pregunta pequeña.
pregunta = "Explica qué es una tool de agente en una sola oración."

if os.getenv("OPENAI_API_KEY"):
    # Configura el modelo con temperatura baja y envía el mensaje.
    modelo = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    respuesta = modelo.invoke(pregunta)
    print(respuesta.content)
else:
    print("Falta OPENAI_API_KEY. Pregunta preparada:", pregunta)

# Resumen final: este ejercicio ejecuta un chat model mediante LangChain.
# Cambia temperature a 0.8 y compara dos ejecuciones.
