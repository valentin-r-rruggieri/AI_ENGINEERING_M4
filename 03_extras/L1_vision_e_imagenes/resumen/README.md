# L1 — Casos prácticos de visión

Cada caso une visión, Pydantic y LangChain. Ejecutalos de menor a mayor con el
`requirements.txt` de la raíz y configurá `OPENAI_API_KEY` o `GEMINI_API_KEY`
según el proveedor que elijas.

- `00`, `01`, `02` y `04`: cuatro casos visuales con LangChain y Pydantic.
- `03` y `05`: dos flujos LangGraph, uno de análisis y otro de routing.
- `06`: agente LangChain que compara un formulario limpio, borroso, roto y manchado.
- `07`: el mismo caso como flujo LangGraph: preparar imagen, analizar y decidir.
- `08`: golden case: extrae un formulario limpio y mide cada campo contra el ground truth.
- `09`: schema Pydantic complejo con descriptions, normalización y reglas cruzadas.
- `10`: genera un formulario bancario ficticio para ampliar los datos sintéticos de práctica.
- `11`: un agente clasifica y lee tres imágenes diferentes: factura, página de libro y adenda.
- `12`: visión local con LM Studio, LangChain y Pydantic; no usa API key de OpenAI ni envía la imagen a la nube.
- `GUIA_DOCENTE_L1.md`: secuencia de 3 horas, demos, actividades, evaluación y
  resolución de problemas frecuentes.

Los archivos `06` y `07` usan las cuatro imágenes de
`02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/`. Requieren
`OPENAI_API_KEY` configurada en el `.env` de la raíz porque realizan análisis
visual real con GPT-4o.

Los archivos `08` y `09` requieren `OPENAI_API_KEY` para GPT-4o Vision. El archivo
`10` requiere la misma clave y usa generación de imágenes; guarda el resultado en
`02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/sinteticos/`.
El archivo `11` usa los recursos de `data/documentos_multitipo/` y requiere `OPENAI_API_KEY`.

El archivo `12` requiere cargar un modelo con visión en LM Studio e iniciar
`Developer > Start Server`. Configurá `LMSTUDIO_MODEL` con el identificador del
modelo que aparece cargado en LM Studio. Después se ejecuta sin API key de OpenAI.
