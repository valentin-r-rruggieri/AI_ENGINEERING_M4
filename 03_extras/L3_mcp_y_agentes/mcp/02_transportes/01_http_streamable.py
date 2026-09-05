# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Servidor MCP como aplicación Streamable HTTP.

GUÍA DOCENTE
CUÁNDO USAR: cuando varios clientes accederán al servidor por red.
DIFERENCIA: Streamable HTTP abre un endpoint; STDIO usa un subproceso local.
EN CLASE: ejecutar uvicorn y conectar al endpoint /mcp.
"""

# Importa FastMCP para construir el servidor HTTP.
from fastmcp import FastMCP

# Declara una tool de solo lectura.
mcp = FastMCP("Contratos HTTP")

# Expone una consulta pequeña para probar el transporte.
@mcp.tool()
def estado_contrato(identificador: str) -> dict[str, str]:
    """Consulta el estado de un contrato de demostración."""
    return {"identificador": identificador, "estado": "vigente"}

# Convierte el servidor en una aplicación ASGI con endpoint /mcp.
app = mcp.http_app(path="/mcp", transport="streamable-http")

# Muestra la instrucción solo al ejecutar el archivo directamente con Python.
print("Ejecutá: uvicorn 01_http_streamable:app --reload")

# Resumen final: este ejercicio expone MCP sobre Streamable HTTP.
# Conecta un cliente a http://127.0.0.1:8000/mcp y lista las tools.
