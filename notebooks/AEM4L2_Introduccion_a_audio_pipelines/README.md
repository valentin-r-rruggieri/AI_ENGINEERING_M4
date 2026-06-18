# AEM4L2 - Introduccion a audio pipelines

Notebooks didacticos para acompanar la clase practica de audio pipelines.

Estos notebooks no reemplazan los scripts Python de `python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/`. Funcionan como apoyo visual y modular para explicar conceptos antes de ejecutar los ejercicios con OpenAI real.

## Orden sugerido para clase

| Bloque | Notebook | Para que sirve |
|---|---|---|
| Inicio | `notebooks/E01_resuelto_referencia_vs_asr.ipynb` | Comparar referencia humana vs hypothesis ASR |
| Inicio / WER | `notebooks/E07_inicial_detectar_errores_transcripcion.ipynb` | Clasificar match, substitution, deletion e insertion |
| WER manual | `notebooks/E02_resuelto_wer_manual.ipynb` | Calcular `S`, `D`, `I`, `N` y WER a mano |
| WER como codigo | `notebooks/E03_resuelto_funcion_simple_wer.ipynb` | Convertir la formula en una funcion simple |
| Resumen | `notebooks/E04_resuelto_transcripcion_a_resumen_action_items.ipynb` | Pasar de transcript a summary, intent, urgency y action_items |
| Practica dominio | `notebooks/E05_para_resolver_reclamo_bancario.ipynb` | Resolver un caso bancario estructurado |
| Practica riesgo | `notebooks/E06_para_resolver_wer_llamada_medica.ipynb` | Calcular WER y discutir riesgo medico |
| Cierre | `notebooks/E08_avanzado_audio_pipeline_evaluado.ipynb` | Ver un mini pipeline con gate de confiabilidad |

## Relacion con scripts Python

| Script Python | Notebooks que ayudan |
|---|---|
| `e01_audio_transcripcion_basica.py` | E01, E07 |
| `e02_audio_resumen_libre.py` | E04 |
| `e03_audio_resumen_json_minimo.py` | E04, E05 |
| `e04_transcripcion_a_resumen.py` | E04, E05 |
| `e05_wer_error_critico.py` | E02, E03, E06, E07 |
| `e06_audio_pipeline_confiable.py` | E08 |

## Intencion pedagogica

La clase avanza por capas:

```text
audio -> ASR -> resumen libre -> JSON minimo -> WER -> error critico -> gate
```

Los notebooks explican cada capa con ejemplos pequenos y ejecutables sin consumir API. Los scripts `.py` muestran el pipeline real con Whisper/OpenAI/LangChain.
