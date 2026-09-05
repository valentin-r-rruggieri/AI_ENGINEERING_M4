# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, publicá el servidor y modificá una variable por vez.

"""MCP que protege la conexión con una API propia de clientes.

GUÍA DOCENTE
CUÁNDO USAR: cuando un agente debe acceder a un backend de la organización.
DIFERENCIA: la clave queda en .env y nunca se entrega al modelo ni al cliente MCP.
EN CLASE: reemplazar la URL de ejemplo por un backend de prueba controlado.
"""

# Importa os para leer la URL y token privados desde el entorno.
import os
# Importa dotenv para cargar .env antes de atender una tool.
from dotenv import load_dotenv
# Importa FastMCP para publicar una única capacidad de negocio.
from fastmcp import FastMCP
# Importa httpx para conectar el servidor MCP con la API interna.
import httpx

# Carga una vez las variables privadas del proyecto.
load_dotenv()
# Crea el servidor que representa la frontera segura de la API interna.
mcp = FastMCP("Clientes internos")


# Publica una consulta que deja token y URL dentro del servidor, fuera del agente.
@mcp.tool
async def buscar_cliente(cliente_id: str) -> dict[str, object]:
    """Consulta un cliente por ID en la API interna configurada."""
    base_url = os.getenv("API_PROPIA_BASE_URL", "").rstrip("/")
    token = os.getenv("API_PROPIA_TOKEN", "")
    if not base_url or not token or "tu-organizacion" in base_url:
        return {"estado": "configuración pendiente", "detalle": "Completá API_PROPIA_BASE_URL y API_PROPIA_TOKEN."}

    async with httpx.AsyncClient(timeout=15) as cliente:
        respuesta = await cliente.get(
            f"{base_url}/clientes/{cliente_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    # Entrega una respuesta controlada sin revelar el token ni cabeceras internas.
    if respuesta.status_code == 404:
        return {"cliente_id": cliente_id, "estado": "no encontrado"}
    respuesta.raise_for_status()
    return {"cliente_id": cliente_id, "estado": "encontrado", "datos": respuesta.json()}

# Resumen final: este MCP mantiene secretos y detalles HTTP del lado del servidor.
# Cambiá la ruta /clientes/{id} según el contrato real de tu backend.
