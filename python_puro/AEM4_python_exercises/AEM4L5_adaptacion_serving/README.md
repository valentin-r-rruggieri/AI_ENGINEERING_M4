# AEM4L5 | Adaptación Avanzada y Serving

Ejercicios Python puro para convertir la teoría de L5 en práctica ejecutable con OpenAI real.

## Objetivo

Entender que adaptar, desplegar y optimizar IA en producción no es una sola decisión. Un sistema sostenible combina LoRA/PEFT, arquitectura de serving, profiling, async y métricas.

## Ejercicios

| Archivo | Problema | Qué se practica |
|---|---|---|
| `e01_serverless_vs_server.py` | Elegir infraestructura sin medir cold start | Medición cold/warm y decisión serverless vs servidor persistente |
| `e02_cprofile_optimizacion.py` | Optimizar a ojo un pipeline lento | `cProfile`, hotspot CPU-bound, regex compilada y etapa LLM real |
| `e03_async_pipeline.py` | Ejecutar N llamadas LLM en serie | Comparación secuencial vs `abatch` async para I/O-bound |
| `e04_integrador_adaptacion_serving.py` | Tomar decisiones aisladas | Plan integral: LoRA/PEFT, serving, profiling, async y métricas |

## Cómo ejecutar

Desde `python_puro/AEM4_python_exercises/`:

```bash
python AEM4L5_adaptacion_serving/e01_serverless_vs_server.py
python AEM4L5_adaptacion_serving/e02_cprofile_optimizacion.py
python AEM4L5_adaptacion_serving/e03_async_pipeline.py
python AEM4L5_adaptacion_serving/e04_integrador_adaptacion_serving.py
```

Estos ejercicios usan OpenAI real. Antes de ejecutar, configurar:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
```

## Conceptos clave

- **LoRA / PEFT:** un modelo base congelado más adapters livianos por cliente o dominio.
- **Serverless:** bueno para tráfico irregular y bajo costo ocioso, con riesgo de cold start.
- **Servidor persistente:** bueno para baja latencia estable, con costo fijo.
- **cProfile:** evidencia para optimizar CPU-bound antes de tocar código por intuición.
- **CPU-bound:** cálculo local pesado; se mejora con profiling, optimización, vectorización o procesos.
- **I/O-bound:** espera por red, storage, APIs o DB; se mejora con async, batching y límites de concurrencia.
- **Métricas:** p50/p95/p99, cold start, costo por request, error rate, tiempo de I/O y tiempo de CPU.

## Uso didáctico

1. Mostrar primero los gráficos Mermaid de los notebooks.
2. Ejecutar el script correspondiente.
3. Leer la sección `VALIDACION`.
4. Cerrar con el `DESAFIO PARA EL ALUMNO`.
