# AEM4L2 | Audio Pipelines

## Objetivo

Entender que transcribir no alcanza: hay que medir la calidad de la transcripción (WER), detectar errores críticos y decidir si el resumen es confiable antes de entregarlo al usuario.

Los audios de `data/*.wav` son voces TTS habladas generadas localmente para la práctica. No son llamadas humanas reales, pero sí contienen voz transcribible por Whisper. Los archivos `data/transcripts/*.txt` son la referencia humana/esperada para calcular WER.

Además de los audios base, `data/` incluye variantes degradadas para comparar cómo cambia la transcripción cuando el audio está en mal estado. Todas las variantes usan el mismo transcript de referencia del audio base.

| Sufijo | Problema que simula | Ejemplo |
|---|---|---|
| `_ruido.wav` | Ruido blanco de fondo | `llamada_soporte_ruido.wav` |
| `_rapido.wav` | Habla acelerada | `llamada_soporte_rapido.wav` |
| `_entrecortado.wav` | Microcortes/silencios breves | `llamada_soporte_entrecortado.wav` |
| `_pausas.wav` | Pausas largas entre segmentos | `llamada_soporte_pausas.wav` |
| `_mal_estado.wav` | Ruido + volumen bajo + cortes | `llamada_soporte_mal_estado.wav` |

Para probarlos en cualquier ejercicio, cambiá el `AUDIO_PATH` por una variante y dejá el mismo archivo de referencia en `data/transcripts/`. El detalle completo está en `data/audio_variants_manifest.json`.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_audio_transcripcion_basica.py` | Todavía no sabemos qué devuelve un ASR | Whisper real convierte WAV en texto crudo |
| `e02_audio_resumen_libre.py` | La transcripción sola no ayuda al agente | LLM genera un resumen libre, todavía sin contrato |
| `e03_audio_resumen_json_minimo.py` | El resumen libre no es backend-friendly | `with_structured_output` devuelve summary, urgency y action_items |
| `e04_transcripcion_a_resumen.py` | Texto transcripto sin estructura completa | Pydantic fuerza intent, urgency y action_items |
| `e05_wer_error_critico.py` | El WER bajo no detecta errores peligrosos | WER + detección de errores críticos por dominio |
| `e06_audio_pipeline_confiable.py` | Siempre se genera el resumen | Gate de calidad: WER > umbral → revisión humana |

---

## Cómo ejecutar

```bash
python AEM4L2_audio_pipelines/e01_audio_transcripcion_basica.py
python AEM4L2_audio_pipelines/e02_audio_resumen_libre.py
python AEM4L2_audio_pipelines/e03_audio_resumen_json_minimo.py
python AEM4L2_audio_pipelines/e04_transcripcion_a_resumen.py
python AEM4L2_audio_pipelines/e05_wer_error_critico.py
python AEM4L2_audio_pipelines/e06_audio_pipeline_confiable.py
```

---

## Notebooks sugeridos para mostrar por tema

| Tema de clase | Notebook |
|---|---|
| Referencia humana vs transcripción ASR | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E01_resuelto_referencia_vs_asr.ipynb` |
| WER paso a paso | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E02_resuelto_wer_manual.ipynb` |
| Implementar WER como función reutilizable | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E03_resuelto_funcion_simple_wer.ipynb` |
| Transcripción a resumen y action items | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E04_resuelto_transcripcion_a_resumen_action_items.ipynb` |
| Práctica de dominio financiero | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E05_para_resolver_reclamo_bancario.ipynb` |
| Práctica de WER médico | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E06_para_resolver_wer_llamada_medica.ipynb` |
| Starter visual para detectar errores | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E07_inicial_detectar_errores_transcripcion.ipynb` |
| Pipeline evaluado completo | `../../../notebooks/AEM4L2_Introduccion_a_audio_pipelines/notebooks/E08_avanzado_audio_pipeline_evaluado.ipynb` |

---

## Conceptos clave

- **ASR (Automatic Speech Recognition):** convierte audio en texto (Whisper, DeepSpeech).
- **WER (Word Error Rate):** `(S + D + I) / N` — mide cuántas palabras están mal.
- **S/D/I:** Sustituciones / Deleciones / Inserciones.
- **Error crítico:** un error con bajo impacto en WER pero alto impacto en el dominio (ej: "ocho" → "dos" en dosis médica).
- **Reliability gate:** si WER supera un umbral, no generar resumen automático.
