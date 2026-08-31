# Este archivo forma parte del recorrido práctico de PydanticAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Comparación entre una tool local y una MCP.

GUÍA DOCENTE
CUÁNDO USAR: para decidir dónde debe vivir una capacidad.
DIFERENCIA: local simplifica prototipos; MCP mejora reutilización entre hosts.
EN CLASE: comparar proceso, transporte, secretos y ownership.
"""

# Describe dos implementaciones de la misma capacidad.
comparacion = [
    {
        "criterio": "proceso",
        "tool_local": "mismo proceso del agente",
        "tool_mcp": "servidor independiente",
    },
    {
        "criterio": "reutilizacion",
        "tool_local": "solo esta aplicación",
        "tool_mcp": "cualquier cliente compatible",
    },
    {
        "criterio": "fallos",
        "tool_local": "excepción local",
        "tool_mcp": "red, auth o servidor",
    },
]

# Imprime una comparación legible sin necesitar credenciales.
for fila in comparacion:
    print(fila)

# Deriva una decisión para LegalMove.
decision = "MCP" if True else "local"
print("Capacidad compartida entre frameworks:", decision)

# Resumen final: este ejercicio hace explícito el trade-off de ubicación.
# Cambia el caso a una tool privada de un solo script y revisa la decisión.
