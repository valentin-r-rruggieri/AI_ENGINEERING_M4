# L4 — Casos prácticos de Transformers

Abrí primero la guía Markdown y después ejecutá el `.py`. Los casos separan el
cálculo técnico de la explicación generativa: PyTorch o Python calculan métricas;
LangChain las comunica; Pydantic conserva una salida estable.

## Recorrido recomendado para clase

| Orden | Caso práctico | Concepto principal |
|---:|---|---|
| 1 | [00 — Tokens y embeddings](00_tokens_y_embeddings.md) | Texto → IDs → vectores. |
| 2 | [01 — Self-attention](01_atencion_contrato.md) | Query, Key, Value y matriz `T × T`. |
| 3 | [02 — Explicador](02_explicador_transformer.md) | LLM como traductor de métricas. |
| 4 | [03 — Flujo LangGraph](03_flujo_langgraph.md) | Tokenizar antes de explicar. |
| 5 | [04 — Tutor de atención](04_tutor_atencion.md) | Explicación Pydantic de una matriz. |
| 6 | [05 — Routing](05_routing_langgraph.md) | Longitud de secuencia y costo. |
| 7 | [06 — Comparar textos](06_agente_compara_textos_langchain.md) | `T²` en dos entradas. |
| 8 | [07 — Grafo integrador](07_agente_compara_textos_langgraph.md) | Handoffs auditables. |

[Teoría transversal de L4](TEORIA_L4_TRANSFORMERS.md) reúne tokenización,
embeddings, atención, complejidad y rol de cada framework.

Estos casos conectan tokenización, embeddings, atención y explicación con
LangChain. Si no están instalados PyTorch o Transformers, los ejemplos muestran
la misma forma de datos con una demo local y señalan el `requirements.txt` raíz.

- `00`, `01`, `02` y `04`: cuatro casos que explican métricas con LangChain.
- `03` y `05`: flujos LangGraph de tokenización y routing de atención.
- `06`: agente LangChain que compara tokens y atención de dos textos.
- `07`: el mismo recorrido como LangGraph: tokenizar, calcular atención y explicar.
