# Este archivo forma parte del recorrido práctico de FastMCP.
# Lee la explicación, publicá el servidor y modificá una capacidad por vez.

"""MCP real que conecta una tool con la API pública Open-Meteo.

GUÍA DOCENTE
CUÁNDO USAR: cuando un agente necesita datos vivos de un proveedor externo.
DIFERENCIA: FastMCP define el contrato; httpx realiza la llamada HTTP al proveedor.
EN CLASE: publicar el servidor y pedir el clima de una ciudad distinta.
"""

# Importa FastMCP para publicar capacidades accesibles por clientes MCP.
from fastmcp import FastMCP
# Importa httpx para llamar una API HTTP externa desde la tool.
import httpx

# Crea el servidor que encapsula al proveedor meteorológico.
mcp = FastMCP("Clima Open-Meteo")


# Publica una tool asíncrona que primero busca coordenadas y luego consulta el pronóstico.
@mcp.tool
async def consultar_clima(ciudad: str) -> dict[str, str | float]:
    """Devuelve temperatura actual y descripción para una ciudad."""
    async with httpx.AsyncClient(timeout=15) as cliente:
        ubicacion = await cliente.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": ciudad, "count": 1, "language": "es"},
        )
        resultados = ubicacion.json().get("results", [])
        if not resultados:
            return {"ciudad": ciudad, "estado": "ciudad no encontrada"}

        lugar = resultados[0]
        pronostico = await cliente.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lugar["latitude"],
                "longitude": lugar["longitude"],
                "current": "temperature_2m,weather_code",
            },
        )
        actual = pronostico.json()["current"]

    # Devuelve un diccionario pequeño para que el agente tenga evidencia clara.
    return {
        "ciudad": str(lugar["name"]),
        "temperatura_c": float(actual["temperature_2m"]),
        "codigo_tiempo": str(actual["weather_code"]),
    }

# Resumen final: el servidor transforma una API pública en una tool MCP tipada.
# Publicalo con: fastmcp run 00_api_publica_openmeteo.py:mcp --transport streamable-http
