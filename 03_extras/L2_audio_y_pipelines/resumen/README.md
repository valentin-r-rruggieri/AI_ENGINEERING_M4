# L2 — Casos prácticos de audio

Los casos unen Whisper, WER, tokenización y LangChain. Reutilizan los audios de
la lecture y los casos con modelo requieren `OPENAI_API_KEY` en `.env`.

- `00`, `01`, `02` y `04`: cuatro casos de audio interpretados con LangChain.
- `03` y `05`: flujos LangGraph para decisión y routing de calidad.
- `06`: agente LangChain que compara una llamada, una indicación con ruido y una reunión rápida.
- `07`: el mismo recorrido con LangGraph: transcribir con Whisper y clasificar.
- `08`: auditor LangChain que une WER con términos críticos de una indicación.
- `09`: pipeline real de reunión: Whisper transcribe y LangChain produce una minuta Pydantic.
- `10`: benchmark real de Whisper con audio normal, con ruido y degradado.
- `11`: LangGraph auditable: transcripción, WER y decisión de destino.

Cada ejercicio `00` a `11` tiene un Markdown con el mismo prefijo numérico.
Las guías incluyen teoría específica del archivo, gráficos Mermaid, tablas,
fórmulas, experimentos, preguntas de debate y extensiones. Abrí primero el `.md`
y después ejecutá el `.py` asociado.

## Recorrido recomendado para la clase

| Orden | Caso práctico | Concepto principal |
|---:|---|---|
| 1 | [00 — Medición WER](00_medicion_wer.md) | Diferenciar métrica objetiva de explicación LLM. |
| 2 | [01 — Indicación estructurada](01_indicacion_estructurada.md) | LangChain + Pydantic como contrato. |
| 3 | [02 — Pipeline seguro](02_pipeline_audio_seguro.md) | WER, tokens, umbral y revisión humana. |
| 4 | [03 — Flujo LangGraph](03_flujo_langgraph.md) | Estado, nodo y handoff mínimo. |
| 5 | [04 — Clasificar audio](04_clasificar_audio.md) | Prioridad operacional sin diagnóstico. |
| 6 | [05 — Routing](05_routing_langgraph.md) | Regla determinista basada en WER. |
| 7 | [06 — Tres audios con LangChain](06_agente_varios_audios_langchain.md) | ASR real y agente tipado. |
| 8 | [07 — Tres audios con LangGraph](07_agente_varios_audios_langgraph.md) | ASR y clasificación en nodos separados. |
| 9 | [08 — Auditor crítico](08_auditor_errores_criticos_langchain.md) | WER bajo no implica riesgo bajo. |
| 10 | [09 — Minuta de reunión](09_pipeline_minuta_reunion.md) | Audio real a salida estructurada. |
| 11 | [10 — Benchmark Whisper](10_benchmark_variantes_whisper.md) | Comparar robustez con golden cases. |
| 12 | [11 — Flujo de calidad](11_flujo_calidad_langgraph.md) | ASR → WER → decisión auditable. |

`TEORIA_L2_AUDIO_PIPELINES.md` reúne toda la teoría transversal de la lecture:
ASR, preprocesamiento, tokenización, BPE, WordPiece, WER, errores críticos,
Pydantic, golden cases, Transformers y difusión.

Los archivos `06` y `07` reutilizan tres WAV de la carpeta didáctica de L2 y
realizan transcripción real. Requieren `OPENAI_API_KEY` en el `.env` de la raíz.

Los archivos `09`, `10` y `11` también hacen llamadas reales a Whisper. El archivo
`08` trabaja sobre una transcripción incluida para aislar la evaluación de errores críticos.
