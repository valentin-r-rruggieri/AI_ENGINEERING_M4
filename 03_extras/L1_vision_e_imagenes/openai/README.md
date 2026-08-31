# OpenAI con LangChain: visión y generación de imágenes

Recorrido breve con `ChatOpenAI` de LangChain para texto, visión y salidas
estructuradas con Pydantic. Los ejemplos reutilizan recursos de L1.

La única operación específica es la creación final de la imagen: el endpoint de
generación no es un chat y se llama con el cliente oficial después de construir
el prompt mediante LangChain. Así se distingue con claridad la orquestación del
LLM de una API especializada.

```powershell
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="tu-clave"
```

Ejecutá primero `00_fundamentos`, continuá con visión e imágenes y terminá en
`03_en_marcha`. Las llamadas con costo solo se realizan cuando existe `OPENAI_API_KEY`.
