# AEM4L5 | Arquitecturas avanzadas de adaptación

Secuencia de notebooks para dar una clase teórico-práctica sobre adaptación eficiente, serving, profiling y concurrencia en sistemas de IA.

La idea de uso es: explicar el gráfico y la teoría mínima, ejecutar una celda pequeña, discutir la decisión de arquitectura y cerrar con un ejercicio aplicado.

## Recorrido recomendado

| Orden | Notebook | Rol en clase |
|---|---|---|
| 1 | `E01_resuelto_full_finetuning_vs_lora.ipynb` | Comparar full fine-tuning contra LoRA/PEFT con storage y criterio de decisión. |
| 2 | `E02_resuelto_elegir_despliegue.ipynb` | Elegir serverless, servidor persistente o híbrido según tráfico, latencia y costo. |
| 3 | `E03_resuelto_cprofile_basico.ipynb` | Leer `cProfile`, interpretar `ncalls`, `tottime`, `cumtime` y detectar hotspots. |
| 4 | `E04_resuelto_asyncio_io.ipynb` | Comparar ejecución secuencial contra async para tareas I/O-bound. |
| 5 | `E07_inicial_cpu_bound_io_bound.ipynb` | Clasificar cuellos de botella antes de elegir herramienta. |
| 6 | `E05_para_resolver_arquitectura_resumenes.ipynb` | Diseñar una arquitectura de resúmenes con adaptación y serving. |
| 7 | `E06_para_resolver_optimizar_pipeline_lento.ipynb` | Perfilar y optimizar un pipeline lento con evidencia. |
| 8 | `E08_avanzado_production_architecture_plan.ipynb` | Integrar LoRA, serverless, cProfile, async y métricas en un plan de producción. |

## Conceptos cubiertos

- **LoRA / PEFT:** adaptar entrenando adapters livianos sobre un modelo base congelado.
- **Full fine-tuning:** entrenar todos o casi todos los parámetros cuando la adaptación debe ser profunda.
- **Pipeline observable:** preparar datos, configurar adapter, entrenar, evaluar, versionar y servir.
- **Serverless:** pagar por uso y escalar a cero, aceptando posible cold start.
- **Servidor persistente:** mantener modelo cargado para baja latencia estable.
- **cProfile:** medir llamadas, tiempo propio y tiempo acumulado antes de optimizar.
- **CPU-bound vs I/O-bound:** separar cálculo local de espera por red, storage, APIs o DB.
- **asyncio:** solapar esperas I/O-bound con `async`, `await` y `gather`.

## Relación con Python puro

Después de explicar estos notebooks, usar los scripts de `python_puro/AEM4_python_exercises/AEM4L5_adaptacion_serving/` para llevar la teoría a casos ejecutables con OpenAI real:

- Medición de cold start y decisión de serving.
- Profiling de CPU-bound y etapa LLM como I/O.
- Comparación secuencial vs async con llamadas reales.
- Ejercicio integrador de arquitectura de producción.
