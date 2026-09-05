# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servidor MCP ejecutado mediante STDIO.

GUÍA DOCENTE
CUÁNDO USAR: cuando un host local inicia el servidor como subproceso.
DIFERENCIA: STDIO no abre un puerto; usa entrada y salida estándar.
EN CLASE: no imprimir mensajes extra porque contaminarían JSON-RPC.
"""

# Importa FastMCP para declarar el servidor local.
from fastmcp import FastMCP

# Crea un servidor con una tool determinista.
mcp = FastMCP("Conversor STDIO")

# Expone una conversión simple con tipos que generan el schema.
@mcp.tool()
def convertir_a_mayusculas(texto: str) -> str:
    """Convierte un texto a mayúsculas."""
    return texto.upper()

# Inicia el transporte STDIO cuando se ejecuta el archivo.
mcp.run()

# Resumen final: este servidor queda listo para un host MCP local.
# Agrega un argumento opcional y revisa cómo cambia el schema en Inspector.
