# Hugging Face: Trainer, PEFT y LoRA

Recorrido de adaptación para CPU con un dataset local pequeño. Los scripts descargan
`prajjwal1/bert-tiny` la primera vez y luego pueden reutilizar la caché.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\03_extras\L5_adaptacion_y_despliegue\huggingface_lora\02_en_marcha\02_entrenar_y_recargar_lora_cpu.py
```

El entrenamiento usa `prajjwal1/bert-tiny`, pocas filas y una época. Su objetivo es enseñar
el flujo de Trainer y LoRA, no producir un clasificador de calidad productiva.

El ejercicio final completo es `02_en_marcha/02_entrenar_y_recargar_lora_cpu.py`.
Lee el CSV local sin PyArrow ni Trainer, entrena LoRA en CPU con un bucle PyTorch,
guarda solo el adapter, lo recarga
sobre una copia nueva del modelo base y realiza una inferencia de verificación.

En este equipo, PyArrow está bloqueado por una política de Windows. Por eso el
integrador final lee el CSV con `csv` y usa un bucle PyTorch: no requiere PyArrow
y el entrenamiento LoRA sigue siendo real.
# Hugging Face LoRA — De entrenamiento a adapter reutilizable

| Orden | Guía |
|---:|---|
| 1 | [Trainer en CPU](00_entrenamiento/00_trainer_cpu.md) |
| 2 | [LoRA / PEFT](00_entrenamiento/01_lora_peft.md) |
| 3 | [Accuracy](01_evaluacion/00_accuracy.md) |
| 4 | [Guardar adapter](01_evaluacion/01_guardar_adapter.md) |
| 5 | [Entrenar y recargar](02_en_marcha/02_entrenar_y_recargar_lora_cpu.md) |
| 6 | [Clasificador](02_en_marcha/clasificador_lora.md) |
