# L2: Audio y pipelines

## Orden sugerido

1. `openai_whisper`: transcripción remota y evaluación WER.
2. `huggingface/00_datos_tokenizers`: datasets, BPE y WordPiece.
3. `huggingface/01_audio`: transcripción local y WER.
4. `huggingface/02_diffusion`: diferencia entre Transformers y difusión.
5. `langchain`: postproceso de transcripciones con prompts y cadenas.
6. Ejecutá los dos pipelines `en_marcha` para comparar API y ejecución local.

El resultado esperado es el recorrido `audio -> transcripción -> evaluación` y una
primera comprensión de cómo el texto se convierte en tokens.

Después recorré `resumen/`: contiene tres casos prácticos de WER, salida tipada y
decisión de revisión sobre una transcripción.
