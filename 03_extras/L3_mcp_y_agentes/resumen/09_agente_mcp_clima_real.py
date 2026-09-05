# Este archivo forma parte del resumen integrador de L3.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente LangChain que reutiliza el MCP real de clima creado en FastMCP.

GUÍA DOCENTE
CUÁNDO USAR: cuando el agente necesita basar una recomendación en una API externa.
DIFERENCIA: LangChain interpreta datos; FastMCP encapsula la conexión con Open-Meteo.
EN CLASE: recorrer primero el servidor de clima y luego ejecutar este integrador.
"""

# Importa asyncio para abrir una sesión MCP asíncrona.
import asyncio
# Importa os para leer modelo y credenciales desde .env.
import os
# Importa Path y sys para reutilizar el servidor creado en otra subcarpeta.
from pathlib import Path
import sys

# Carga las variables globales una vez antes de abrir conexiones externas.
from dotenv import load_dotenv
# Importa el cliente FastMCP y el transporte que publica el servidor por STDIO.
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
# Importa el modelo LangChain que explicará los datos recuperados por MCP.
from langchain_openai import ChatOpenAI
# Importa Pydantic para definir el contrato final de la recomendación.
from pydantic import BaseModel, Field

# Carga OPENAI_API_KEY y OPENAI_AGENT_MODEL desde el .env de la raíz.
load_dotenv()


# Define el resultado que verá quien consume la recomendación del agente.
class RecomendacionClima(BaseModel):
    ciudad: str = Field(description="Ciudad consultada mediante el MCP de clima.")
    temperatura_c: float = Field(description="Temperatura real devuelta por Open-Meteo.")
    recomendacion: str = Field(description="Sugerencia breve y prudente para actividad exterior.")
    justificacion: str = Field(description="Explicación basada en el dato MCP, sin inventar pronósticos.")


# Reutiliza exactamente el servidor MCP creado en fastmcp/01_apis_y_proveedores.
ruta_servidor = Path(__file__).resolve().parents[1] / "fastmcp" / "01_apis_y_proveedores" / "00_api_publica_openmeteo.py"
# Ubica la CLI del entorno activo para iniciar el servidor MCP real por STDIO.
ruta_fastmcp = Path(sys.executable).with_name("fastmcp.exe")
transporte = StdioTransport(
    command=str(ruta_fastmcp),
    args=["run", f"{ruta_servidor}:mcp", "--transport", "stdio", "--no-banner"],
    cwd=str(ruta_servidor.parent),
)


# Consulta la tool remota antes de pedir que el LLM formule una recomendación.
async def consultar_clima_real() -> dict[str, str | float]:
    async with Client(transporte) as cliente:
        respuesta = await cliente.call_tool("consultar_clima", {"ciudad": "Buenos Aires"})
        return dict(respuesta.data)


# Recupera evidencia de Open-Meteo a través del MCP, sin importar su código interno.
clima = asyncio.run(consultar_clima_real())
clave_openai = os.getenv("OPENAI_API_KEY", "")

# Explica la configuración faltante sin crear una recomendación falsa.
if not clave_openai or clave_openai == "your-openai-key-here":
    print("Clima MCP recibido:", clima)
    print("Configurá OPENAI_API_KEY en .env para completar la recomendación LangChain real.")
else:
    # Construye el agente tipado: el modelo interpreta pero no reemplaza a la API externa.
    modelo = ChatOpenAI(model=os.getenv("OPENAI_AGENT_MODEL", "gpt-4o-mini"), temperature=0)
    agente = modelo.with_structured_output(RecomendacionClima)

    # Entrega al LLM únicamente la evidencia MCP disponible y limita su alcance.
    instruccion = f"""
    Sos un asistente prudente de planificación. Generá la salida solicitada.
    Usá solamente estos datos recuperados mediante un MCP real: {clima}.
    No inventes lluvia, viento, alertas ni pronóstico futuro. Recomendá de forma breve.
    """
    recomendacion = agente.invoke(instruccion)

    # Revalida el objeto estructurado antes de imprimir el resultado final.
    recomendacion_validada = RecomendacionClima.model_validate(recomendacion)
    print(recomendacion_validada.model_dump_json(indent=2))

# Resumen final: MCP obtuvo el dato vivo y LangChain produjo una recomendación Pydantic.
# Cambiá Buenos Aires por otra ciudad y explicá qué parte del flujo se reutiliza.
