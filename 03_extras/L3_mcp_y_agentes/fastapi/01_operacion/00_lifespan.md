# Lifespan FastAPI

## Objetivo

Muestra inicialización y cierre controlados del servicio.

```mermaid
flowchart LR
    A[Entrada] --> B[Lifespan FastAPI]
    B --> C[Salida]
```

## Explicación

Lifespan abre recursos al arrancar y los libera al detener la API.

## Práctica

Identificá qué cliente o conexión viviría allí.
