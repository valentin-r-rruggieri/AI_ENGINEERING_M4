# Caso 09 — Agente LangChain que reutiliza un MCP de API externa

## Objetivo

Este resumen conecta las piezas creadas en subcarpetas anteriores. No define
otro servidor ni copia la lógica de Open-Meteo: inicia y consume el servidor
`fastmcp/01_apis_y_proveedores/00_api_publica_openmeteo.py` mediante MCP real.

```mermaid
flowchart LR
    A[Open-Meteo] --> B[Servidor FastMCP de clima]
    B -->|tool MCP| C[Cliente MCP del resumen]
    C --> D[Agente LangChain]
    D --> E[RecomendacionClima Pydantic]
```

| Parte reutilizada | Responsabilidad |
|---|---|
| Servidor FastMCP | Traduce Open-Meteo a `consultar_clima(ciudad)`. |
| Cliente de este resumen | Consume la tool por STDIO real. |
| Agente LangChain | Formula una recomendación prudente. |
| Pydantic | Impone ciudad, temperatura, recomendación y justificación. |

## Ejecución

```powershell
.\.venv\Scripts\python.exe .\03_extras\L3_mcp_y_agentes\resumen\09_agente_mcp_clima_real.py
```

El primer tramo siempre consulta Open-Meteo por MCP. Para el segundo tramo se
necesita `OPENAI_API_KEY`: sin ella, el script muestra el dato real recibido y
explica la configuración faltante, sin inventar una recomendación.

## Relación con publicación web

Para clase se usa STDIO. Si el servidor de clima está publicado en la web,
reemplazá el transporte local por `Client("https://tu-dominio/mcp/")`. El flujo
del agente y el modelo Pydantic no cambian porque el contrato MCP es el mismo.

## Práctica

Creá un segundo agente que use el MCP de `01_api_propia_clientes.py` cuando tu
backend de prueba esté configurado. El patrón será idéntico: MCP primero,
agente después y salida Pydantic al final.
