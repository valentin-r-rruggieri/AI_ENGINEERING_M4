# PydanticAI dentro de un span

## Objetivo

Combinar salida tipada del agente con evidencia de ejecucion.

```mermaid
flowchart LR
    A[Ejercicio Python] --> B[Concepto tecnico]
    B --> C[Resultado visible]
    C --> D[Decision tecnica]
```

## Como leer el codigo

Abri primero langfuse\02_integraciones\01_pydantic_ai_spanpy. Los comentarios del archivo separan preparacion, calculo o llamada principal y salida. Ejecutalo antes de modificarlo: relaciona cada variable con una decision de adaptacion o despliegue.

## Que explicar en clase

1. Que problema operativo resuelve el ejercicio.
2. Que supuesto simplifica el ejemplo y que dato real deberia medirse.
3. Como cambiaria la decision al modificar una sola variable.

## Practica

Agrega un campo al output y revisa la traza.

En produccion, valida la conclusion con metricas reales, pruebas de carga y observabilidad.

