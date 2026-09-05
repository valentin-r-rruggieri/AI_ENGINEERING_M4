# Costo mensual de serving

## Objetivo

Comparar costo fijo por hora con costo variable por solicitudes.

```mermaid
flowchart LR
    A[Ejercicio Python] --> B[Concepto tecnico]
    B --> C[Resultado visible]
    C --> D[Decision tecnica]
```

## Como leer el codigo

Abri primero arquitecturas_serving\01_costos_carga\00_costo_mensualpy. Los comentarios del archivo separan preparacion, calculo o llamada principal y salida. Ejecutalo antes de modificarlo: relaciona cada variable con una decision de adaptacion o despliegue.

## Que explicar en clase

1. Que problema operativo resuelve el ejercicio.
2. Que supuesto simplifica el ejemplo y que dato real deberia medirse.
3. Como cambiaria la decision al modificar una sola variable.

## Practica

Multiplica las solicitudes por cien y revisa la recomendacion.

En produccion, valida la conclusion con metricas reales, pruebas de carga y observabilidad.

