# AEM4L2 | Audio Pipelines

## Objetivo

Entender que transcribir no alcanza: hay que medir la calidad de la transcripción (WER), detectar errores críticos y decidir si el resumen es confiable antes de entregarlo al usuario.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_transcripcion_a_resumen.py` | Texto transcripto sin estructura | Pydantic fuerza intent, urgency y action_items |
| `e02_wer_error_critico.py` | El WER bajo no detecta errores peligrosos | WER + detección de errores críticos por dominio |
| `e03_audio_pipeline_confiable.py` | Siempre se genera el resumen | Gate de calidad: WER > umbral → revisión humana |

---

## Cómo ejecutar

```bash
python AEM4L2_audio_pipelines/e01_transcripcion_a_resumen.py
python AEM4L2_audio_pipelines/e02_wer_error_critico.py
python AEM4L2_audio_pipelines/e03_audio_pipeline_confiable.py
```

---

## Conceptos clave

- **ASR (Automatic Speech Recognition):** convierte audio en texto (Whisper, DeepSpeech).
- **WER (Word Error Rate):** `(S + D + I) / N` — mide cuántas palabras están mal.
- **S/D/I:** Sustituciones / Deleciones / Insercciones.
- **Error crítico:** un error con bajo impacto en WER pero alto impacto en el dominio (ej: "ocho" → "dos" en dosis médica).
- **Reliability gate:** si WER supera un umbral, no generar resumen automático.
