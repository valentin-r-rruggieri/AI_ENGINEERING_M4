# Este archivo forma parte del recorrido práctico de MCP.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Creación del servidor MCP más pequeño.

GUÍA DOCENTE
CUÁNDO USAR: como contenedor de capacidades reutilizables por distintos hosts.
DIFERENCIA: crear el servidor no publica todavía ninguna tool ni abre un transporte.
EN CLASE: distinguir host, client y server antes de agregar funciones.
"""

# Importa FastMCP, la interfaz actual y simple para crear servidores MCP.
from fastmcp import FastMCP

# Crea un servidor con un nombre reconocible para clientes e Inspector.
mcp = FastMCP("AEM4 Demo")

# Muestra el objeto preparado sin iniciar un proceso bloqueante.
print("Servidor creado:", type(mcp).__name__)
print("Nombre pedagógico: AEM4 Demo")

# Resumen final: este ejercicio crea la frontera del servidor MCP.
# Cambia el nombre y observa cómo debería identificarlo un host.
