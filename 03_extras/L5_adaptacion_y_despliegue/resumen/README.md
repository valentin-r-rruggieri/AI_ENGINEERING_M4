# L5 — Casos prácticos de adaptación y despliegue

Abrí la guía Markdown antes de ejecutar el caso. Los ejercicios avanzan desde una
decisión LoRA hasta una recomendación observable y auditable de serving.

| Orden | Caso | Concepto |
|---:|---|---|
| 1 | [00 — Decisión LoRA](00_decision_lora.md) | Parámetros y adaptación económica. |
| 2 | [01 — Concurrencia](01_concurrencia_serving.md) | I/O concurrente y latencia. |
| 3 | [02 — Agente observable](02_agente_observable.md) | Langfuse y destino de serving. |
| 4 | [03 — Flujo LangGraph](03_flujo_langgraph.md) | Medir antes de recomendar. |
| 5 | [04 — Asesor](04_asesor_despliegue.md) | Plataforma y réplicas tipadas. |
| 6 | [05 — Routing](05_routing_langgraph.md) | Decisión determinista por carga. |
| 7 | [06 — Perfiles LangChain](06_agente_perfiles_serving_langchain.md) | Comparar escenarios. |
| 8 | [07 — Perfiles LangGraph](07_agente_perfiles_serving_langgraph.md) | Carga por réplica y handoff. |

[Teoría transversal de L5](TEORIA_L5_ADAPTACION_Y_DESPLIEGUE.md) conecta LoRA,
evaluación, concurrencia, Langfuse, Docker y Kubernetes.

Los casos relacionan LoRA, rendimiento, Langfuse y decisiones de serving. El
tercero usa LangChain y envía una traza real a Langfuse usando las credenciales
configuradas en `.env`.

- `00`, `01`, `02` y `04`: cuatro casos de adaptación y serving con LangChain.
- `03` y `05`: flujos LangGraph de recomendación y routing de despliegue.
- `06`: agente LangChain que compara prototipo, API de equipo y servicio público.
- `07`: el mismo tema como LangGraph: medir carga por réplica y recomendar.
