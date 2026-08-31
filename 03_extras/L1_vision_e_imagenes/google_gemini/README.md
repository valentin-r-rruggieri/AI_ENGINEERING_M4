# Google Gemini con LangChain: texto y visión

Ejemplos mínimos con `ChatGoogleGenerativeAI` de LangChain para texto, imágenes
y JSON estructurado. Reutilizan el formulario de L1 para comparar la misma
entrada con OpenAI sin cambiar la interfaz de orquestación.

```powershell
python -m pip install -r requirements.txt
$env:GEMINI_API_KEY="tu-clave"
python 03_extras/L1_vision_e_imagenes/google_gemini/00_fundamentos/00_cliente.py
```

El recorrido termina con un extractor visual validado por Pydantic.
