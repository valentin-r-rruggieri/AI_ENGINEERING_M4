# 02 — Entrenar y recargar LoRA en CPU

## Objetivo

Este integrador recorre el ciclo completo: crear adapter, entrenar brevemente, guardarlo y recargarlo para inferencia.

```mermaid
flowchart LR
    A[Dataset] --> B[LoRA + Trainer]
    B --> C[Adapter guardado]
    C --> D[Modelo base + adapter]
    D --> E[Predicción recargada]
```

## Qué comprobar

| Etapa | Evidencia |
|---|---|
| Entrenamiento | Pérdida o métrica por pasos. |
| Guardado | Archivos de adapter presentes. |
| Recarga | Inferencia sin reentrenar. |
| Evaluación | Resultado comparable al original. |

## Límite

Un entrenamiento corto de CPU es demostrativo. No permite afirmar robustez sin partición de evaluación y ejemplos variados.
