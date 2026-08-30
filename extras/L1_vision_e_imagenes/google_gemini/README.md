# Google Gemini: texto y visión

Ejemplos mínimos del SDK `google-genai` para texto, imágenes y JSON estructurado.
Reutilizan el formulario de L1 para poder comparar la misma entrada con OpenAI.

```powershell
pip install -r extras/L1_vision_e_imagenes/google_gemini/requirements.txt
$env:GEMINI_API_KEY="tu-clave"
python extras/L1_vision_e_imagenes/google_gemini/00_fundamentos/00_cliente.py
```

El recorrido termina con un extractor visual validado por Pydantic.
