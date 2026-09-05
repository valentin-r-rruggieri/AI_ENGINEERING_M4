# Aplicacion antes de Docker

## Objetivo

Comprobar una API FastAPI local antes de empaquetarla.

```mermaid
flowchart LR
    A[Ejercicio Python] --> B[Concepto tecnico]
    B --> C[Resultado visible]
    C --> D[Decision tecnica]
```

## Como leer el codigo

Abri primero docker\00_fundamentos\00_app_minimapy. Los comentarios del archivo separan preparacion, calculo o llamada principal y salida. Ejecutalo antes de modificarlo: relaciona cada variable con una decision de adaptacion o despliegue.

## Que explicar en clase

1. Que problema operativo resuelve el ejercicio.
2. Que supuesto simplifica el ejemplo y que dato real deberia medirse.
3. Como cambiaria la decision al modificar una sola variable.

## Practica

Levanta Uvicorn y cambia el mensaje de la ruta.

En produccion, valida la conclusion con metricas reales, pruebas de carga y observabilidad.

