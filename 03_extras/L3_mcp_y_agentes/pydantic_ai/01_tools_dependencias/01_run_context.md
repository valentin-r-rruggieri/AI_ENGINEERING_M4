# Run context

## Objetivo

Entrega dependencias explícitas durante la ejecución.

```mermaid
flowchart LR
    A[Entrada] --> B[Run context]
    B --> C[Salida]
```

## Explicación

El contexto evita esconder clientes y configuración como variables globales.

## Práctica

Identificá qué dependencia debe viajar en contexto.
