# AEM4L5 | Adaptación Avanzada y Serving

## Objetivo

Entender que el despliegue, el profiling y la concurrencia no son detalles técnicos — son decisiones de arquitectura que impactan directamente en el costo, la latencia y la experiencia del usuario.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_serverless_vs_server.py` | Siempre elegimos servidor 24/7 sin evaluar el patrón de tráfico | Función de recomendación basada en criterios objetivos |
| `e02_cprofile_optimizacion.py` | Optimizamos "a ojo" sin saber dónde está el cuello de botella | cProfile muestra exactamente qué función consume el tiempo |
| `e03_async_pipeline.py` | 5 llamadas secuenciales tardan 5 segundos | asyncio.gather() procesa las 5 en paralelo en ~1 segundo |

---

## Cómo ejecutar

```bash
python AEM4L5_adaptacion_serving/e01_serverless_vs_server.py
python AEM4L5_adaptacion_serving/e02_cprofile_optimizacion.py
python AEM4L5_adaptacion_serving/e03_async_pipeline.py
```

---

## Conceptos clave

- **Serverless:** el proveedor asigna y libera recursos por request (pagar por uso, no por uptime).
- **Cold start:** tiempo que tarda en activarse una función serverless desde cero (~2–30s).
- **cProfile:** profiler de Python que mide `ncalls`, `tottime` y `cumtime` por función.
- **CPU-bound:** el cuello de botella es el procesador (cálculos pesados).
- **I/O-bound:** el cuello de botella es esperar respuestas externas (red, disco, API).
- **asyncio.gather():** ejecuta múltiples coroutines I/O-bound en paralelo sin threads.
