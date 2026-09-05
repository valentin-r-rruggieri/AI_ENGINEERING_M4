# Replicas y capacidad

## Objetivo

Relacionar RPS por Pod, margen operativo y escala horizontal.

```mermaid
flowchart LR
    A[Ejercicio Python] --> B[Concepto tecnico]
    B --> C[Resultado visible]
    C --> D[Decision tecnica]
```

## Como leer el codigo

Abri primero kubernetes\01_operacion\01_replicaspy. Los comentarios del archivo separan preparacion, calculo o llamada principal y salida. Ejecutalo antes de modificarlo: relaciona cada variable con una decision de adaptacion o despliegue.

## Que explicar en clase

1. Que problema operativo resuelve el ejercicio.
2. Que supuesto simplifica el ejemplo y que dato real deberia medirse.
3. Como cambiaria la decision al modificar una sola variable.

## Practica

Eleva el trafico a 8 RPS y calcula las replicas.

En produccion, valida la conclusion con metricas reales, pruebas de carga y observabilidad.

