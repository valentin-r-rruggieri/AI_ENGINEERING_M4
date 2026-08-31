# AEM4 — AI Engineering Module 4

Módulo 4 del programa **AI Engineering** enfocado en pipelines multimodales (visión, audio), protocolo MCP, fundamentos de transformers, arquitecturas de adaptación y un proyecto integrador.

---

## Instalar todos los extras

Desde la raíz del repositorio, activá el entorno virtual y ejecutá una sola vez:

```powershell
pip install -r requirements.txt
```

Esto instala las dependencias de todos los recorridos de `03_extras/`. El proyecto
integrador mantiene su instalación independiente en `04_proyecto_integrador/PIM4_legalmove/`.

## Configurar claves una sola vez

Copiá el archivo global de ejemplo y completá solamente las variables de los
servicios que vayas a utilizar:

```powershell
Copy-Item .env.example .env
```

`OPENAI_API_KEY` habilita los ejercicios de OpenAI, Whisper, LangChain y DSPy.
`GEMINI_API_KEY` se necesita solo para los ejemplos Gemini. Las claves de Langfuse
habilitan las trazas de L5 y LegalMove. El archivo `.env` está ignorado por Git.

---

## Estructura del repositorio

```
AI_ENGINEERING_M4/
├── .vscode/                                             # Configuración de VS Code
├── 01_notebooks/
│   ├── AEM4L1_IA_que_ve_y_crea_vision_e_imagenes/          # Notebooks de visión
│   ├── AEM4L2_Introduccion_a_audio_pipelines/               # Notebooks de audio
│   ├── AEM4L3_Introduccion_a_los_MCP/                       # Notebooks de MCP
│   ├── AEM4L4_Fundamentos_teoricos_y_arquitectura/          # Notebooks de transformers
│   └── AEM4L5_Arquitecturas_avanzadas_de_adaptacion/        # Notebooks de adaptación/serving
├── 02_python_puro/
│   └── AEM4_python_exercises/
│       ├── AEM4L1_vision_imagenes/                          # Scripts Python de visión
│       ├── AEM4L2_audio_pipelines/                          # Scripts Python de audio
│       ├── AEM4L3_mcp/                                      # Scripts Python de MCP
│       ├── AEM4L4_fundamentos_arquitectura/                 # Scripts Python de fundamentos
│       └── AEM4L5_adaptacion_serving/                       # Scripts Python de serving
├── 03_extras/                                                  # Recorridos cortos por lecture
│   ├── L1_vision_e_imagenes/                               # Pydantic, visión, OCR y DSPy
│   ├── L2_audio_y_pipelines/                               # Whisper, audio y tokenización
│   ├── L3_mcp_y_agentes/                                   # MCP, FastAPI y agentes
│   ├── L4_transformers/                                    # PyTorch y Transformers
│   ├── L5_adaptacion_y_despliegue/                         # LoRA, serving y despliegue
│   ├── PI_legalmove/                                       # Acceso directo al proyecto oficial
│   └── PI_comparativas_opcionales/                         # Comparativas no evaluables
├── 04_proyecto_integrador/
│   ├── PIM4_legalmove/                                     # Entrega oficial evaluable
│   └── material_didactico/                                 # Notebooks y ejercicios guiados
├── 05_docs/
│   ├── rubrica/                                           # Criterios y evidencias de evaluación
│   ├── guias_docentes/                                    # Material para preparar las clases
│   └── recursos/                                          # Enlaces y recursos transversales
└── README.md
```

Las carpetas de `01_notebooks/` y `04_proyecto_integrador/material_didactico/notebooks/` contienen secuencias `.ipynb` compatibles con Google Colab. L1 tiene 10 notebooks, L2 tiene 8, L3 tiene 20, L4 tiene 17 y L5 tiene 8. El proyecto integrador agrega otros 8 notebooks.

| Ejercicio | Tipo | Descripción |
|-----------|------|-------------|
| E01 | Resuelto | Concepto base guiado |
| E02 | Resuelto | Siguiente bloque conceptual |
| E03 | Resuelto | Implementación de función/herramienta |
| E04 | Resuelto | Ejemplo integrador |
| E05 | Para resolver | Práctica de estudiante (moderado) |
| E06 | Para resolver | Práctica de estudiante (avanzado) |
| E07 | Inicial | Warm-up mínimo |
| E08 | Avanzado | Ejercicio cumbre del módulo |

**Total: 71 notebooks** listos para Google Colab: 63 de clases AEM4L1-L5 y 8 del proyecto integrador.

---

## Extras prácticos por lecture

`03_extras/` ofrece ejercicios `.py` pequeños para explicar cada componente de las clases sin
ocultar la implementación detrás de helpers. Todos siguen el mismo formato: introducción,
guía docente, comentarios por bloque, resultado visible y una modificación sugerida.

- L1: OpenAI, Gemini, OCR, Pydantic y DSPy.
- L2: OpenAI Whisper, Hugging Face, tokenización, ASR y WER.
- L3: MCP v2, FastAPI, LangChain, LangGraph y PydanticAI.
- L4: PyTorch, atención y Hugging Face Transformers.
- L5: PEFT, LoRA, Langfuse, profiling, serving, Docker y Kubernetes.
- PI: LegalMove con LangChain, LangGraph, PydanticAI y Langfuse.

Cada tecnología instala únicamente su propio `requirements.txt`. Los ejemplos que consumen
servicios externos comprueban sus credenciales antes de realizar llamadas.

---

## Contenido por lección

### AEM4L1 — IA que Ve y Crea (Visión e Imágenes)

Pipeline de extracción estructurada desde imágenes usando modelos multimodales (GPT-4o Vision).

| Notebook | Descripción |
|----------|-------------|
| E01 | Extraer texto plano de ticket de supermercado |
| E02 | Convertir texto extraído a JSON estructurado |
| E03 | Validar JSON con Pydantic `BaseModel` |
| E04 | Manejar campos opcionales y detección booleana |
| E05 | Ejercicio: extraer datos de credencial universitaria |
| E06 | Ejercicio: extraer datos de factura simple |
| E07 | Pipeline mínimo imagen → campos básicos |
| E08 | Evaluación con golden cases (schema, accuracy, completeness) |

**Pipeline:** Texto plano → JSON → Pydantic → Campos opcionales → Evaluación

---

### AEM4L2 — Introducción a Audio Pipelines

Reconocimiento automático del habla (ASR), medición de calidad con WER y post-procesamiento.

| Notebook | Descripción |
|----------|-------------|
| E01 | Comparar referencia vs hipótesis ASR, identificar errores |
| E02 | Calcular WER manualmente (S, D, I) |
| E03 | Función `simple_wer()` con Levenshtein |
| E04 | Post-procesar transcripción → resumen + action items |
| E05 | Ejercicio: clasificar intención en llamada bancaria |
| E06 | Ejercicio: evaluar WER en llamada médica |
| E07 | Detectar errores de transcripción (sustitución, deleción, inserción) |
| E08 | Pipeline completo: WER + resumen + reliability gate |

**Pipeline:** ASR → WER → Post-procesamiento → Quality gate

---

### AEM4L3 — Introducción a los MCP (Model Context Protocol)

Protocolo estándar para conectar LLMs con herramientas, recursos y prompts externos.

| Notebook | Descripción |
|----------|-------------|
| E01 | Clasificar capacidades como Tool / Resource / Prompt |
| E02 | Diseñar contrato de tool con `input_schema`, `output_schema`, `required_scope` |
| E03 | Versionado de esquemas: cambios aditivos vs breaking (SemVer) |
| E04 | Elegir transporte: STDIO (local) vs HTTP Streaming (remoto) |
| E05 | Ejercicio: diseñar servidor MCP para RRHH |
| E06 | Ejercicio: estrategia de migración de tool bancaria |
| E07 | Clasificar items como Tool, Resource o Prompt |
| E08 | Arquitectura MCP completa para universidad |

**Conceptos clave:** 3 primitivas MCP, contratos de tool, scopes (`dominio:objeto:accion`), SemVer, principio de mínimo privilegio, auditoría

---

### AEM4L4 — Fundamentos Teóricos y Arquitectura

Internals de transformers: self-attention, Q/K/V, bloques Transformer, costo cuadrático O(N²), tokenización (BPE vs WordPiece), vocabulario, PEFT, LoRA y decisiones de latencia.

| Notebook | Descripción |
|----------|-------------|
| E01 | Fundamentos para AI Engineering: arquitectura, tokenización, costo y latencia |
| E02 | RNN/LSTM vs Transformer |
| E03 | Self-attention conceptual con mapa de atención |
| E04 | Query, Key y Value con ejemplo trabajado |
| E05 | Bloque Transformer: attention, FFN, LayerNorm y residuales |
| E06 | Costo cuadrático de attention |
| E07 | Tokenización por palabra, carácter y subword |
| E08 | BPE vs WordPiece |
| E09 | Vocabulario, memoria y latencia |
| E10 | PEFT vs full fine-tuning |
| E11 | LoRA conceptual y storage por cliente |
| E12 | ADR para chatbot financiero |

**Conceptos clave:** RNN vs Transformer, self-attention, Q/K/V, bloque Transformer, O(N²), BPE, WordPiece, vocabulario, PEFT, LoRA, ADR

---

### AEM4L5 — Arquitecturas Avanzadas de Adaptación

Decisiones de arquitectura en producción: LoRA vs Full Fine-tuning, Serverless vs Persistente, profiling con cProfile, async I/O.

| Notebook | Descripción |
|----------|-------------|
| E01 | Comparar almacenamiento, costo y flexibilidad: Full FT vs LoRA |
| E02 | Elegir entre Serverless y Servidor Persistente |
| E03 | Profiling con cProfile (`ncalls`, `cumtime`, `tottime`) |
| E04 | Paralelizar I/O-bound con `asyncio.gather()` |
| E05 | Ejercicio: elegir LoRA/FT y despliegue para 4 perfiles |
| E06 | Ejercicio: profilear y optimizar pipeline lento |
| E07 | Clasificar tareas como CPU-bound o I/O-bound |
| E08 | Plan de producción completo (adaptación, serving, profiling, async, métricas) |

**Conceptos clave:** LoRA (50 MB vs 14 GB), cold start, cProfile, asyncio, CPU-bound vs I/O-bound

---

### PIM4 — Proyecto Integrador LegalMove

Pipeline completo de análisis de documentos legales: compara contratos con sus modificaciones usando visión, agentes de contextualización y extracción, validación Pydantic y observabilidad.

| Notebook | Descripción |
|----------|-------------|
| E01 | Detectar cambios mínimos entre contrato y modificación |
| E02 | `ContextualizationAgent`: mapear secciones del contrato |
| E03 | `ExtractionAgent`: extraer cambios usando el mapa contextual |
| E04 | Validación Pydantic: campos obligatorios, tipos, longitud mínima |
| E05 | Ejercicio: aplicar pipeline a contrato de alquiler |
| E06 | Ejercicio: manejar modificación con 3 cambios simultáneos |
| E07 | Depuración: construir JSON manual y validar con Pydantic |
| E08 | Pipeline completo: parsing + agentes + validación + `log_span()` |

**Pipeline:** Imagen/Texto → ContextualizationAgent → ExtractionAgent → ContractChangeOutput (Pydantic) → Trace (log_span)

**Modelo de datos:**
- `sections_changed: List[str]` — secciones modificadas
- `topics_touched: List[str]` — temas (pago, duración, territorio...)
- `summary_of_the_change: str` — descripción del cambio

---

## Convención de nomenclatura

- `AEM4L{X}_{nombre}` — Lección X del módulo 4
- `PIM4_{nombre}` — Proyecto integrador del módulo 4
- `01_notebooks/` — notebooks didácticos por clase
- `02_python_puro/AEM4_python_exercises/` — ejercicios `.py` ejecutables por clase
- `03_extras/` — ejemplos lineales y comentados organizados por lecture y tecnología
- `04_proyecto_integrador/` — notebooks y scripts del PIM separados del material regular
- `guiones_clases_practicas/` — guiones docentes privados, ignorados por Git
- `E{NN}_{tipo}_{descripcion}.ipynb` — Notebooks con número secuencial

---

## Requisitos

- Google Colab (recomendado) o Jupyter Notebook
- Python 3.10+
- Las notebooks son material didáctico autocontenido.
- Los scripts de `02_python_puro/` y `04_proyecto_integrador/PIM4_legalmove/` usan API real de OpenAI cuando llaman modelos.
- Cada tecnología de `03_extras/` tiene dependencias e instrucciones de ejecución.
- Para los scripts con LLM o Whisper, configurar `OPENAI_API_KEY` en `02_python_puro/AEM4_python_exercises/.env`.

---

## Cómo usar

1. Abre cualquier notebook `.ipynb` en [Google Colab](https://colab.research.google.com/)
2. Sigue la progresión E01 → E08 dentro de cada lección
3. Los ejercicios E05-E06 son para resolver; E07 es warm-up; E08 es el desafío avanzado
4. Para las prácticas, abre `03_extras/README.md`, elige la lecture y ejecuta los `.py` en orden numérico
