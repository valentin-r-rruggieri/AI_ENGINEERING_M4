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
# OpenAI Whisper

Ejemplos progresivos de ASR, evaluación y posprocesamiento. Cada script tiene una guía de teoría y lectura de código junto a él.

| Tema | Script | Guía |
|---|---|---|
| Transcripción | [00_transcribir_whisper.py](00_transcripcion/00_transcribir_whisper.py) | [Explicación](00_transcripcion/00_transcribir_whisper.md) |
| Métrica WER | [00_calcular_wer.py](01_evaluacion/00_calcular_wer.py) | [Explicación](01_evaluacion/00_calcular_wer.md) |
| Pipeline completo | [pipeline_audio.py](02_en_marcha/pipeline_audio.py) | [Explicación](02_en_marcha/pipeline_audio.md) |
