# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servidor MCP consumido como toolset.

GUÍA DOCENTE
CUÁNDO USAR: cuando las tools se publican fuera del proceso del agente.
DIFERENCIA: MCPToolset descubre capacidades sin redefinir sus funciones.
EN CLASE: iniciar el servidor HTTP antes de ejecutar el agente.
"""

# Importa os y Agent; MCPToolset se carga como dependencia opcional.
import os
from pydantic_ai import Agent

try:
    # Importa el adaptador cuando fue instalado con pydantic-ai[mcp].
    from pydantic_ai.mcp import MCPToolset
    mcp_disponible = True
except ImportError:
    mcp_disponible = False

if os.getenv("OPENAI_API_KEY") and mcp_disponible:
    # Apunta al servidor y conecta sus capacidades al agente.
    tools_mcp = MCPToolset("http://127.0.0.1:8000/mcp")
    agente = Agent(
        "openai:gpt-4.1-mini",
        toolsets=[tools_mcp],
        instructions="Usa las tools MCP para responder cálculos contractuales.",
    )
    try:
        resultado = agente.run_sync("Compara un plazo original de 12 con uno nuevo de 18 meses.")
        print(resultado.output)
    except Exception as error:
        print("Iniciá primero el servidor MCP. Detalle:", type(error).__name__)
elif not mcp_disponible:
    print('Instalá la integración: pip install "pydantic-ai[mcp]"')
else:
    print("Falta OPENAI_API_KEY. MCP configurado en http://127.0.0.1:8000/mcp")

# Resumen final: este ejercicio conecta un agente con tools remotas.
# Cambia la URL y observa qué error de conexión se informa.
