# Hugging Face: Trainer, PEFT y LoRA

Recorrido de adaptación para CPU con un dataset local pequeño. Los scripts descargan
`prajjwal1/bert-tiny` la primera vez y luego pueden reutilizar la caché.

```powershell
pip install -r 03_extras/L5_adaptacion_y_despliegue/huggingface_lora/requirements.txt
python 03_extras/L5_adaptacion_y_despliegue/huggingface_lora/00_entrenamiento/00_trainer_cpu.py
```

El entrenamiento usa `prajjwal1/bert-tiny`, pocas filas y una época. Su objetivo es enseñar
el flujo de Trainer y LoRA, no producir un clasificador de calidad productiva.
