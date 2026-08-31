# L2 — Casos prácticos de audio

Los casos unen Whisper, WER, tokenización y LangChain. Reutilizan los audios de
la lecture y los casos con modelo requieren `OPENAI_API_KEY` en `.env`.

- `00`, `01`, `02` y `04`: cuatro casos de audio interpretados con LangChain.
- `03` y `05`: flujos LangGraph para decisión y routing de calidad.
- `06`: agente LangChain que compara una llamada, una indicación con ruido y una reunión rápida.
- `07`: el mismo recorrido con LangGraph: transcribir con Whisper y clasificar.

Los archivos `06` y `07` reutilizan tres WAV de la carpeta didáctica de L2 y
realizan transcripción real. Requieren `OPENAI_API_KEY` en el `.env` de la raíz.
