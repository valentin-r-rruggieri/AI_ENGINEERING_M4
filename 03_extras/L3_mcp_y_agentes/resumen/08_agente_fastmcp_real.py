# Este archivo forma parte del resumen integrador de L3.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Agente LangChain que consume un MCP FastMCP real y devuelve Pydantic.

GUÍA DOCENTE
CUÁNDO USAR: cuando un agente debe fundamentar su respuesta en una capacidad MCP publicada.
DIFERENCIA: el agente no conoce el catálogo de Python; lo consulta mediante un cliente MCP.
EN CLASE: probar primero STDIO y luego configurar la URL HTTP del mismo servidor publicado.
"""

# Importa asyncio para abrir la sesión MCP asíncrona desde este script lineal.
import asyncio
# Importa os para leer la URL opcional del servidor y la clave del modelo.
import os
# Importa Path para construir la ruta portable al servidor FastMCP local.
from pathlib import Path
# Importa sys para localizar la CLI FastMCP instalada en el entorno virtual.
import sys

# Carga el archivo .env global una única vez para los ejemplos de extras.
from dotenv import load_dotenv
# Importa el cliente que habla el protocolo MCP real por STDIO o HTTP.
from fastmcp import Client
# Importa el transporte STDIO que publica el servidor real como subproceso.
from fastmcp.client.transports import StdioTransport
# Importa el wrapper LangChain del modelo OpenAI.
from langchain_openai import ChatOpenAI
# Importa Pydantic para validar el contrato final del agente.
from pydantic import BaseModel, Field

# Carga credenciales y configuraciones antes de crear conexiones externas.
load_dotenv()


# Define la respuesta estable que recibirá la persona usuaria.
class InformeContrato(BaseModel):
    codigo: str = Field(description="Código consultado mediante la tool MCP.")
    estado: str = Field(description="Estado devuelto por el servidor MCP.")
    accion_recomendada: str = Field(description="Acción basada solo en la política MCP.")
    explicacion: str = Field(description="Justificación breve que relaciona estado y política.")


# Ubica el servidor real incluido en la carpeta FastMCP de esta misma lecture.
ruta_servidor = Path(__file__).resolve().parents[1] / "fastmcp" / "00_fundamentos" / "00_servidor_contratos.py"
# Permite cambiar de STDIO local a un servidor FastMCP ya publicado por HTTP.
origen_mcp = os.getenv("FASTMCP_CONTRATOS_URL") or ruta_servidor
# Define el proceso de publicación para el modo local. El modo HTTP usa la URL directamente.
ruta_fastmcp = Path(sys.executable).with_name("fastmcp.exe")
transporte_stdio = StdioTransport(
    command=str(ruta_fastmcp),
    args=["run", f"{ruta_servidor}:mcp", "--transport", "stdio", "--no-banner"],
    cwd=str(ruta_servidor.parent),
)


# Consulta capacidades reales del servidor antes de solicitar una conclusión al LLM.
async def consultar_mcp() -> dict[str, str]:
    # Si existe URL usa HTTP; si no, publica el mismo objeto real mediante STDIO.
    transporte = origen_mcp if isinstance(origen_mcp, str) else transporte_stdio
    async with Client(transporte) as cliente:
        respuesta_contrato = await cliente.call_tool(
            "consultar_estado_contrato", {"codigo": "C-200"}
        )
        respuesta_politica = await cliente.read_resource("legalmove://politica-operativa")
        respuesta_prompt = await cliente.get_prompt("revisar_contrato", {"codigo": "C-200"})
        return {
            "contrato": str(respuesta_contrato.data),
            "politica": str(respuesta_politica),
            "prompt": str(respuesta_prompt),
        }


# Recupera primero evidencia real por MCP: no hay catálogo local en el agente.
evidencia_mcp = asyncio.run(consultar_mcp())
clave_openai = os.getenv("OPENAI_API_KEY", "")

# Evita un traceback confuso cuando falta la única credencial necesaria para el LLM.
if not clave_openai or clave_openai == "your-openai-key-here":
    print("Configurá OPENAI_API_KEY en .env para ejecutar el agente LangChain real.")
else:
    # Crea el modelo LangChain y fuerza la respuesta al esquema Pydantic declarado.
    modelo = ChatOpenAI(model=os.getenv("OPENAI_AGENT_MODEL", "gpt-4o-mini"), temperature=0)
    agente = modelo.with_structured_output(InformeContrato)

    # Pide una decisión trazable usando exclusivamente las respuestas MCP recibidas.
    instruccion = f"""
    Sos un agente de LegalMove. Respondé solo con el esquema solicitado.
    No inventes datos ni acciones. Usá exclusivamente esta evidencia MCP real:
    contrato: {evidencia_mcp['contrato']}
    política: {evidencia_mcp['politica']}
    prompt del servidor: {evidencia_mcp['prompt']}
    """
    informe = agente.invoke(instruccion)

    # Revalida explícitamente el resultado antes de entregarlo a la persona usuaria.
    informe_validado = InformeContrato.model_validate(informe)
    print(informe_validado.model_dump_json(indent=2))

# Resumen final: FastMCP aportó la evidencia y LangChain produjo una decisión Pydantic.
# Definí FASTMCP_CONTRATOS_URL con un endpoint publicado para cambiar STDIO por HTTP.
