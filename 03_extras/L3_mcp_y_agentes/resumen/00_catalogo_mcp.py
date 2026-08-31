# Este archivo resume L3 mediante un catálogo MCP mínimo.
# Lee cada bloque y modifica una variable por vez.

"""Caso 1: publicar tool, resource y prompt en un servidor MCP.

GUÍA DOCENTE
CUÁNDO USAR: cuando varias aplicaciones deben reutilizar la misma capacidad.
DIFERENCIA: una tool ejecuta acciones; un resource entrega contexto.
EN CLASE: identificar servidor, cliente, host y contrato de la tool.
"""

# Carga el .env para mantener el patrón común de los casos integradores.
from dotenv import load_dotenv
load_dotenv()

# Importa MCPServer y LangChain para explicar la capacidad publicada.
try:
    from mcp.server import MCPServer
except ImportError:
    MCPServer = None
from langchain_openai import ChatOpenAI

# Define una respuesta local que también consumirá el agente del caso siguiente.
catalogo = {"C-100": "vigente", "C-200": "en revisión"}

if MCPServer:
    # Crea el servidor y publica sus tres primitivas pedagógicas.
    servidor = MCPServer("CatalogoContratos")

    @servidor.tool()
    def consultar_contrato(codigo: str) -> str:
        """Devuelve el estado de un contrato."""
        return catalogo.get(codigo, "contrato inexistente")

    @servidor.resource("contratos://politica")
    def politica() -> str:
        return "Las bajas requieren revisión humana."

    @servidor.prompt()
    def revisar_contrato(codigo: str) -> str:
        return f"Revisá el contrato {codigo} usando la política disponible."

    explicacion = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke(
        "Explica brevemente la diferencia entre una tool, un resource y un prompt MCP."
    ).content
    print("MCP preparado: tool, resource y prompt para CatalogoContratos")
    print(explicacion)
else:
    # Explica la dependencia faltante sin detener el recorrido práctico.
    print("Falta mcp. Catálogo local preparado:", catalogo)

# Resumen final: MCP convierte capacidades locales en contratos reutilizables.
# Cambia el estado de C-200 y observa qué respondería la tool.
