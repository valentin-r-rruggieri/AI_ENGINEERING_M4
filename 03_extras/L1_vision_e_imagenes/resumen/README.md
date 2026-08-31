# L1 — Casos prácticos de visión

Cada caso une visión, Pydantic y LangChain. Ejecutalos de menor a mayor con el
`requirements.txt` de la raíz y configurá `OPENAI_API_KEY` o `GEMINI_API_KEY`
según el proveedor que elijas.

- `00`, `01`, `02` y `04`: cuatro casos visuales con LangChain y Pydantic.
- `03` y `05`: dos flujos LangGraph, uno de análisis y otro de routing.
- `06`: agente LangChain que compara un formulario limpio, borroso, roto y manchado.
- `07`: el mismo caso como flujo LangGraph: preparar imagen, analizar y decidir.

Los archivos `06` y `07` usan las cuatro imágenes de
`02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/`. Requieren
`OPENAI_API_KEY` configurada en el `.env` de la raíz porque realizan análisis
visual real con GPT-4o.
