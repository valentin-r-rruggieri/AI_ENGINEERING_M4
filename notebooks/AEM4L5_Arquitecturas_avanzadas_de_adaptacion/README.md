# AEM4L5 | Arquitecturas avanzadas de adaptación

Notebooks **teórico-pedagógicos** para dar la clase sobre adaptación eficiente (LoRA/PEFT),
patrones de despliegue (serverless vs servidor), profiling y concurrencia (`cProfile`, `asyncio`)
en sistemas de IA, con **Python + LangChain**.

Cada notebook combina teoría extensa, glosario, tablas comparativas, diagramas **Mermaid** y
código mínimo **ejecutable sin API key** (el modelo se simula con `RunnableLambda`).

## Recorrido recomendado

| Orden | Notebook | Tema |
|---|---|---|
| 1 | `AEM4L5_N1_LoRA_PEFT_Adaptacion.ipynb` | Adaptación eficiente: full fine-tuning vs LoRA/PEFT y rol de LangChain. |
| 2 | `AEM4L5_N2_Deploy_Serverless_Servidor.ipynb` | Patrones de despliegue: serverless vs servidor persistente. |
| 3 | `AEM4L5_N3_Profiling_Async_LangChain.ipynb` | Rendimiento: `cProfile`, CPU/IO-bound, `asyncio` y async en LangChain. |
| 4 | `AEM4L5_N4_Caso_Integrador.ipynb` | Arquitectura end-to-end que integra N1–N3. |

## Estructura de cada notebook

1. Título · 2. Objetivo · 3. Mapa visual (Mermaid) · 4. Glosario · 5. Teoría paso a paso ·
6. Tabla comparativa · 7. Gráfico Mermaid · 8. Mini ejemplo · 9. Código Python + LangChain ·
10. Ejercicio guiado · 11. Preguntas de interpretación · 12. Errores comunes · 13. Cierre.

## Setup

Cada notebook trae su propia celda de setup. Solo requiere:

```python
!pip install -q langchain-core
```

No necesita API key, GPU ni `langchain-openai` (este último es opcional y queda comentado).
Los ejemplos `asyncio` usan `await main()` (no `asyncio.run()`), pensados para Jupyter/Colab.

## Notas importantes

- **LangChain no entrena LoRA.** LoRA/PEFT se entrena con `transformers`, `peft`, `accelerate`
  o servicios externos. LangChain **consume** modelos ya adaptados y **orquesta** prompts,
  routing, chains y endpoints. Esto se explica en el N1.
- Si Jupyter/Colab no renderiza Mermaid, copiá el bloque a [Mermaid Live](https://mermaid.live).

## Relación con Python puro

Para llevar la teoría a casos ejecutables con OpenAI real, ver los scripts de
`python_puro/AEM4_python_exercises/AEM4L5_adaptacion_serving/` (cold start y serving, profiling
de CPU vs etapa LLM como I/O, secuencial vs async, e integrador de arquitectura).
