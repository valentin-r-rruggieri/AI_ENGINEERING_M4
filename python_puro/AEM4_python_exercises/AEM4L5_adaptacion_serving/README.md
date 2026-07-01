# AEM4L5 | Adaptación Avanzada y Serving

Material de **consola con `rich`** para llevar la teoría de L5 a la práctica: demos
visuales (colores, tablas, spinners) pensadas para **mostrar en vivo en clase**.

Los scripts están en la carpeta [`demos_rich/`](demos_rich/) y son **simulados, sin API
key ni GPU** (el modelo se simula con `RunnableLambda` de `langchain-core`).

## Demos

| Archivo | Tema | Qué muestra |
|---|---|---|
| `demos_rich/demo_1_lora_peft.py` | LoRA / PEFT | Tabla comparativa, % de parámetros entrenables y ahorro de storage. |
| `demos_rich/demo_2_serverless_vs_server.py` | Despliegue | Cold start vs latencia estable + función de decisión por caso. |
| `demos_rich/demo_3_cprofile.py` | Profiling | Hotspots con `cProfile` y comparación lento vs optimizado (speedup). |
| `demos_rich/demo_4_async_vs_secuencial.py` | Concurrencia | Barra de progreso: secuencial vs async (I/O-bound). |
| `demos_rich/demo_5_finetuning_lora_huggingface.py` | Fine-tuning LoRA | Código real de `transformers` + `peft` paso a paso (explicado, NO entrena). |

## Cómo ejecutar

Con el intérprete del proyecto (`.venv`, que ya tiene `rich`):

```powershell
# desde la raíz del workspace
.\.venv\Scripts\python.exe python_puro\AEM4_python_exercises\AEM4L5_adaptacion_serving\demos_rich\demo_2_serverless_vs_server.py
```

O activá el `.venv` una vez (`.\.venv\Scripts\Activate.ps1`) y después:

```powershell
python python_puro\AEM4_python_exercises\AEM4L5_adaptacion_serving\demos_rich\demo_2_serverless_vs_server.py
```

Ver [`demos_rich/README.md`](demos_rich/README.md) para el detalle de cada demo.

## Conceptos clave

- **LoRA / PEFT:** un modelo base congelado más adapters livianos por cliente o dominio.
- **Serverless:** bueno para tráfico irregular y bajo costo ocioso, con riesgo de cold start.
- **Servidor persistente:** bueno para baja latencia estable, con costo fijo.
- **cProfile:** evidencia para optimizar CPU-bound antes de tocar código por intuición.
- **CPU-bound:** cálculo local pesado; se mejora con profiling, optimización o procesos.
- **I/O-bound:** espera por red, storage, APIs o DB; se mejora con async, batching y límites de concurrencia.
- **Métricas:** p50/p95/p99, cold start, costo por request, error rate, tiempo de I/O y de CPU.

## Uso didáctico

1. Mostrar primero los gráficos Mermaid de los notebooks (`notebooks/AEM4L5_...`).
2. Ejecutar el demo correspondiente de `demos_rich/`.
3. Discutir la tabla / el resultado que imprime en consola.
4. Cerrar con la conclusión de cada demo.

> Nota: la carpeta `data/` contenía datos de los ejercicios previos (ya eliminados). Los
> demos de `demos_rich/` no la usan; podés borrarla si no la necesitás.
