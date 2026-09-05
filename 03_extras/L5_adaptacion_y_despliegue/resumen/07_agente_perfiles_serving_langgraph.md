# 07 — Grafo: capacidad por réplica antes de recomendar

## Idea central

El integrador final calcula una métrica objetiva antes de preguntar al agente. De esta forma la recomendación recibe evidencia explícita: solicitudes por minuto divididas por réplicas actuales.

```mermaid
flowchart LR
    A[Perfil] --> B[medir_carga]
    B --> C[carga por réplica]
    C --> D[recomendar_despliegue]
    D --> E[DecisionDespliegue]
```

## Recorrido del código

`EstadoServing` llega con perfil, tráfico, latencia objetivo y réplicas. `medir_carga` calcula:

\[
carga\ por\ réplica = \frac{peticiones\ por\ minuto}{réplicas\ actuales}
\]

Después `recomendar_despliegue` recibe esa métrica en el prompt y construye `DecisionDespliegue`. Pydantic valida la forma final y Python vuelve a fijar el perfil desde el estado.

| Nodo | Input | Output | Beneficio |
|---|---|---|---|
| `medir_carga` | Tráfico + réplicas | Carga por réplica | Cálculo reproducible. |
| `recomendar_despliegue` | Perfil + métrica | Recomendación | Explicación contextual. |

## Límite

Carga por réplica no equivale a capacidad real. Una request puede durar 10 ms o 10 segundos; el modelo puede necesitar CPU, GPU o I/O. La métrica es una base para conversación, no un autoscaler completo.

## Práctica

Duplicá las réplicas del servicio público. Verificá que la carga calculada disminuye y discutí el costo de mantener esas réplicas.
