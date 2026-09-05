# 03 — Flujo LangGraph: tool antes que agente

## Qué problema resuelve

Este caso vuelve explícita una política esencial: primero se consulta la capacidad que aporta el hecho; después el LLM redacta la respuesta. LangGraph representa ese orden como nodos y aristas.

```mermaid
flowchart LR
    A[START + código] --> B[consultar_tool]
    B --> C[estado_contrato]
    C --> D[responder_agente]
    D --> E[RespuestaAgente]
    E --> F[END]
```

## Recorrido paso a paso

### 1. Estado que evoluciona

```python
class EstadoMCP(TypedDict):
    codigo: str
    estado_contrato: NotRequired[str]
    respuesta: NotRequired[dict[str, object]]
```

`codigo` está presente al inicio. El primer nodo agrega `estado_contrato`; el segundo agrega `respuesta`. `NotRequired` documenta que esas claves no existen antes de su nodo correspondiente.

### 2. Nodo de capacidad verificable

```python
def consultar_tool(state: EstadoMCP) -> dict:
    catalogo = {"C-100": "vigente", "C-200": "en revisión"}
    return {"estado_contrato": catalogo.get(state["codigo"], "inexistente")}
```

El nodo recibe todo por `state` y devuelve solamente la actualización que produce. No llama al LLM. En un sistema real este bloque sería el cliente de una tool MCP remota, pero la interfaz de entrada/salida se mantiene igual.

### 3. Nodo de presentación estructurada

`responder_agente` recibe código y estado desde el grafo. `with_structured_output(RespuestaAgente)` pide dos campos y `model_validate` confirma que existen antes de convertirlos en diccionario.

### 4. Aristas que obligan al orden

```python
START → consultar_tool → responder_agente → END
```

El LLM no puede ejecutarse antes de que exista `estado_contrato`. Esa es la ventaja de declarar el flujo: la dependencia entre evidencia y respuesta se puede leer y verificar.

| Nodo | Lee | Agrega | Riesgo que evita |
|---|---|---|---|
| `consultar_tool` | Código | Estado | Inventar un estado. |
| `responder_agente` | Código + estado | Respuesta | Responder sin fuente. |

## Práctica

Cambiá `C-200` por un código inexistente. Después mové mentalmente la arista del agente antes de la tool y explicá por qué esa arquitectura sería menos confiable.
