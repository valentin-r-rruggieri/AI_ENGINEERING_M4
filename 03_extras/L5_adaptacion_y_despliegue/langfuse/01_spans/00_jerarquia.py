# Este archivo forma parte del recorrido práctico de Langfuse.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Jerarquía de spans en un pipeline.

GUÍA DOCENTE
CUÁNDO USAR: para separar etapas y localizar dónde se consume la latencia.
DIFERENCIA: el span activo se convierte en padre de las observaciones internas.
EN CLASE: dibujar primero la jerarquía esperada y luego verla en Langfuse.
"""

# Carga las variables del archivo .env ubicado en la raíz del proyecto.
from dotenv import load_dotenv

# Busca el .env desde este archivo hacia las carpetas superiores.
load_dotenv()
# Importa os y el cliente Langfuse v4.
import os
from langfuse import get_client

# Define una entrada pequeña y un resultado local.
entrada = {"original": "12 meses", "nuevo": "18 meses"}
salida = {"cambio": "aumento de 6 meses"}

# Crea un span raíz y dos hijos que representan agentes.
langfuse = get_client()
with langfuse.start_as_current_observation(as_type="span", name="legalmove", input=entrada) as raiz:
    with langfuse.start_as_current_observation(as_type="span", name="contextualizador") as contexto:
        contexto.update(output={"tema": "vigencia"})
    with langfuse.start_as_current_observation(as_type="span", name="extractor") as extractor:
        extractor.update(output=salida)
    raiz.update(output=salida)
langfuse.flush()
print("Jerarquía enviada: legalmove -> contextualizador, extractor")
# Resumen final: este ejercicio representa el workflow mediante spans anidados.
# Agrega un span de validación como tercer hijo del pipeline.
