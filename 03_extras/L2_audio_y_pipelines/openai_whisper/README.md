# OpenAI Whisper: transcripción y evaluación

```powershell
pip install -r 03_extras/L2_audio_y_pipelines/openai_whisper/requirements.txt
$env:OPENAI_API_KEY="tu-clave"
python 03_extras/L2_audio_y_pipelines/openai_whisper/00_transcripcion/00_transcribir_whisper.py
```

Continuá con WER y terminá en `02_en_marcha`. Si falta la clave, los ejercicios muestran
el recurso preparado sin realizar una llamada con costo.

## Material por tema

| Tema | Guía | Archivos cubiertos |
|---|---|---|
| Transcripción | [00 transcripción](00_transcripcion/README.md) | 00 transcribir whisper punto py |
| Evaluación | [01 evaluación](01_evaluacion/README.md) | 00 calcular wer punto py |
| Integrador | [02 en marcha](02_en_marcha/README.md) | pipeline audio punto py |

Cada guía incluye teoría, fórmula, gráfico Mermaid, tabla, código explicado y práctica.
