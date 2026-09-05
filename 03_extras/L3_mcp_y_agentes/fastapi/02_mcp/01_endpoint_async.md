# Endpoint asíncrono

## Objetivo

Expone una operación HTTP compatible con await.

```mermaid
flowchart LR
    A[Entrada] --> B[Endpoint asíncrono]
    B --> C[Salida]
```

## Explicación

Async sirve para I/O concurrente, no acelera CPU pesada por sí solo.

## Práctica

Compará una llamada remota con una operación CPU.
