# Hugging Face: tokenización y audio

```powershell
pip install -r 03_extras/L2_audio_y_pipelines/huggingface/requirements.txt
python 03_extras/L2_audio_y_pipelines/huggingface/00_datos_tokenizers/00_dataset_local.py
```

Continuá con audio y difusión, y terminá en `03_en_marcha`. Algunos ejemplos descargan
modelos pequeños desde Hugging Face Hub la primera vez.

## Material por tema

| Tema | Guía | Archivos cubiertos |
|---|---|---|
| Datasets y tokenizers | [00 datos y tokenizers](00_datos_tokenizers/README.md) | Dataset local, BPE y WordPiece |
| ASR local | [01 audio](01_audio/README.md) | Whisper tiny y JiWER |
| Difusión | [02 difusión](02_diffusion/README.md) | Arquitecturas y scheduler |
| Integrador local | [03 en marcha](03_en_marcha/README.md) | Pipeline local de audio |

Cada guía incluye teoría, gráficos Mermaid, tablas, código y experimentos.
# Hugging Face para audio

Ejercicios locales para entender datos, tokenizadores, ASR, evaluación y difusión.

| Bloque | Guías por archivo |
|---|---|
| Datos y tokenizadores | [Dataset local](00_datos_tokenizers/00_dataset_local.md) · [BPE y WordPiece](00_datos_tokenizers/01_bpe_wordpiece.md) |
| Audio | [ASR local](01_audio/00_asr_local.md) · [WER con JiWER](01_audio/01_wer_jiwer.md) |
| Difusión | [Transformer vs difusión](02_diffusion/00_transformer_vs_diffusion.md) · [Scheduler](02_diffusion/01_scheduler.md) |
| Integrador | [Pipeline local](03_en_marcha/pipeline_audio_local.md) |
