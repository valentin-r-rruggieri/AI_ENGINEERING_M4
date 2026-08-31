# L1: IA que ve y crea

## Orden sugerido

1. `pydantic`: contratos y validación de las salidas.
2. `openai`: ChatOpenAI, visión, Base64 y salida estructurada con Pydantic.
3. `google_gemini`: ChatGoogleGenerativeAI, visión y extracción JSON con Pydantic.
4. `ocr`: preprocesamiento, Tesseract y control de calidad.
5. `dspy`: signatures y salidas estructuradas.

Todos los proveedores LLM se invocan desde LangChain. Terminá con los ejercicios
`en_marcha` de OpenAI, Gemini y OCR; el resultado esperado es un pipeline visual
que devuelve información validada.

Después recorré `resumen/`: contiene tres casos prácticos que combinan visión,
Pydantic, LangChain, Gemini, OpenAI, OCR y revisión humana.
