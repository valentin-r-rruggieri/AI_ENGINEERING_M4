# AEM4L2 - Introduccion a audio pipelines

Notebooks didacticos para acompanar la clase practica de audio pipelines.

Estos notebooks no reemplazan los scripts Python de `python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/`. Funcionan como apoyo visual y modular para explicar conceptos antes de ejecutar los ejercicios con OpenAI real.

## Orden sugerido para clase

| Bloque | Notebook | Para que sirve |
|---|---|---|
| Base 1 | `notebooks/E01_resuelto_referencia_vs_asr.ipynb` | Entender las 4 etapas: audio, ASR, LLM/post-proceso y gate |
| Base 2 | `notebooks/E02_resuelto_wer_manual.ipynb` | Comparar audio/transcript correcto vs incorrecto y ver propagacion de errores |
| Base 3 | `notebooks/E03_resuelto_funcion_simple_wer.ipynb` | Aprender tokenizacion: palabra, caracter, subword, BPE y WordPiece |
| Base 4 | `notebooks/E04_resuelto_transcripcion_a_resumen_action_items.ipynb` | Clasificar errores ASR cotidianos: substitution, deletion, insertion, puntuacion |
| WER | `notebooks/E05_para_resolver_reclamo_bancario.ipynb` | Calcular WER desde cero con tabla, formula y barras visuales |
| Estructura | `notebooks/E06_para_resolver_wer_llamada_medica.ipynb` | Pasar de transcript a resumen libre, JSON minimo y estructura validable |
| Modelos | `notebooks/E07_inicial_detectar_errores_transcripcion.ipynb` | Diferenciar Transformers y diffusion models en audio |
| Cierre | `notebooks/E08_avanzado_audio_pipeline_evaluado.ipynb` | Integrar golden cases, WER, error critico y reliability gate |

## Relacion con scripts Python

| Script Python | Notebooks que ayudan |
|---|---|
| `e01_audio_transcripcion_basica.py` | E01, E02 |
| `e02_audio_resumen_libre.py` | E06 |
| `e03_audio_resumen_json_minimo.py` | E06 |
| `e04_transcripcion_a_resumen.py` | E06 |
| `e05_wer_error_critico.py` | E03, E04, E05 |
| `e06_audio_pipeline_confiable.py` | E08 |

## Intencion pedagogica

La clase avanza por capas, de menor a mayor complejidad:

```text
4 etapas -> referencia vs hypothesis -> tokenizacion -> errores ASR
-> WER -> estructura -> modelos -> reliability gate
```

Los notebooks explican cada capa con teoria, tablas, ejemplos cotidianos y mini codigo ejecutable sin consumir API. Los scripts `.py` muestran el pipeline real con Whisper/OpenAI/LangChain.
