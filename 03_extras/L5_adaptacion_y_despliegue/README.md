# L5: Adaptación y despliegue

## Orden sugerido

1. `huggingface_lora`: Trainer, PEFT, LoRA, evaluación y guardado del adapter.
2. `python_performance`: medición, profiling, concurrencia y timeouts.
3. `langfuse`: traces, spans, métricas e integraciones.
4. `arquitecturas_serving`: servidor, serverless, cold start, costos y concurrencia.
5. `docker`: servicio FastAPI dentro de un contenedor.
6. `kubernetes`: Deployment, Service, probes, recursos y réplicas.
7. `langchain`: cadena que los servicios exponen y despliegan.

Terminá con los ejemplos `en_marcha` y continuá en `../PI_legalmove` para abrir el
flujo LegalMove oficial con Langfuse.

Antes del proyecto, recorré `resumen/`: reúne tres casos prácticos de LoRA,
concurrencia, observabilidad y elección de despliegue.

## Propuesta de clase práctica

La clase funciona mejor como una historia única: **adaptar un modelo, medirlo,
observarlo y desplegarlo**. Cada script tiene ahora un Markdown hermano con
teoría, diagrama, explicación y práctica.

```mermaid
flowchart LR
    A[LoRA en CPU] --> B[Medir latencia]
    B --> C[Observar con Langfuse]
    C --> D[Empaquetar con Docker]
    D --> E[Escalar con Kubernetes]
```

| Momento | Mostrar en vivo | Pregunta para el grupo |
|---|---|---|
| 1 | `huggingface_lora/02_en_marcha/02_entrenar_y_recargar_lora_cpu.py` | ¿Por qué guardar solo el adapter y no todo el modelo? |
| 2 | `python_performance/01_asyncio/00_gather.py` | ¿Cuándo la concurrencia reduce latencia y cuándo no? |
| 3 | `langfuse/03_en_marcha/pipeline_observable.py` | ¿Cómo sabemos dónde falló o se demoró el flujo? |
| 4 | `docker/02_en_marcha/servicio_contenedor.py` | ¿Qué necesita una API para ser operable? |
| 5 | `kubernetes/02_en_marcha/validar_manifiestos.py` | ¿Qué debe coincidir antes de escalar réplicas? |
| 6 | `resumen/06_agente_perfiles_serving_langchain.py` | ¿Cuándo recomendar Docker y cuándo Kubernetes? |

No conviene mostrar todos los archivos en una clase. Usá los fundamentos para
explicar y los integradores para ejecutar, modificar una variable y pedir una
decisión razonada a las y los alumnos.
