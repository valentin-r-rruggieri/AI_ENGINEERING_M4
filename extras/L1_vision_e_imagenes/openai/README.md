# OpenAI: visión y generación de imágenes

Recorrido breve por el cliente de OpenAI, Responses API, análisis visual, salidas
estructuradas y generación de imágenes. Los ejemplos reutilizan recursos de L1.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r extras/L1_vision_e_imagenes/openai/requirements.txt
$env:OPENAI_API_KEY="tu-clave"
```

Ejecutá primero `00_fundamentos`, continuá con visión e imágenes y terminá en
`03_en_marcha`. Las llamadas con costo solo se realizan cuando existe `OPENAI_API_KEY`.
