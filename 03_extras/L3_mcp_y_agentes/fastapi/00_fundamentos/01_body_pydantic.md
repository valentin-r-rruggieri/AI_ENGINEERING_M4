# Body FastAPI con Pydantic

## Objetivo

Valida JSON de entrada antes de ejecutar lógica.

```mermaid
flowchart LR
    A[Entrada] --> B[Body FastAPI con Pydantic]
    B --> C[Salida]
```

## Explicación

Pydantic hace explícito el contrato HTTP y FastAPI devuelve 422 si no se cumple.

## Práctica

Mandá un JSON con un campo faltante.
