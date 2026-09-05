# Capas y cache de Docker

## Objetivo

Entender por que requirements se instala antes de copiar el codigo.

```mermaid
flowchart LR
    A[Ejercicio Python] --> B[Concepto tecnico]
    B --> C[Resultado visible]
    C --> D[Decision tecnica]
```

## Como leer el codigo

Abri primero docker\01_operacion\01_capas_imagenpy. Los comentarios del archivo separan preparacion, calculo o llamada principal y salida. Ejecutalo antes de modificarlo: relaciona cada variable con una decision de adaptacion o despliegue.

## Que explicar en clase

1. Que problema operativo resuelve el ejercicio.
2. Que supuesto simplifica el ejemplo y que dato real deberia medirse.
3. Como cambiaria la decision al modificar una sola variable.

## Practica

Mueve COPY del codigo antes de pip install y analiza la cache.

En produccion, valida la conclusion con metricas reales, pruebas de carga y observabilidad.

