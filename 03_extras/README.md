# Extras prácticos de AEM4

Los ejercicios están organizados por lecture. Dentro de cada clase aparecen únicamente
las tecnologías y los temas que se explican en ese momento.

## Capa común: LangChain

LangChain es la capa principal de integración con modelos: OpenAI se usa mediante
`ChatOpenAI`, Gemini mediante `ChatGoogleGenerativeAI` y Pydantic recibe las salidas
estructuradas de esas cadenas. Los recorridos de MCP, LangGraph, PydanticAI y Langfuse
se conectan a esa misma capa para enseñar cómo se arma un sistema completo.

OCR, PyTorch, tokenización, Whisper, Docker y Kubernetes conservan ejemplos técnicos
propios porque no son chats. Cuando intervienen en un flujo con LLM, el ejemplo los
combina con LangChain para la interpretación, resumen o salida tipada.

## Recorridos

- `L1_vision_e_imagenes`: Pydantic, OpenAI, Gemini, OCR y DSPy.
- `L2_audio_y_pipelines`: OpenAI Whisper y Hugging Face para audio y tokenización.
- `L3_mcp_y_agentes`: MCP, FastAPI, LangChain, LangGraph y PydanticAI.
- `L4_transformers`: PyTorch y Hugging Face Transformers.
- `L5_adaptacion_y_despliegue`: LoRA, rendimiento, observabilidad y despliegue.
- `PI_legalmove`: acceso directo a la entrega oficial del proyecto integrador.
- `PI_comparativas_opcionales`: material no evaluable de comparación.

## Cómo usar cada clase

1. Abrí primero el `README.md` de la lecture.
2. Desde la raíz del proyecto activá `.venv` e instalá una sola vez `requirements.txt`.
3. Ejecutá las carpetas numeradas de menor a mayor.
4. Modificá una sola variable por vez y observá el resultado.
5. Cerrá con la carpeta `en_marcha` o con el ejercicio indicado en el proyecto.

Los ejemplos son lineales, comentados y ejecutables sin `main()`. Los casos que usan
un proveedor remoto cargan las claves desde `.env` y ejecutan directamente su flujo real.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
