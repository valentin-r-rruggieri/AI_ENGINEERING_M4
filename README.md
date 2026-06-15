# AEM4 — AI Engineering Module 4

Módulo 4 del programa **AI Engineering** enfocado en pipelines multimodales (visión, audio), protocolo MCP, fundamentos de transformers, arquitecturas de adaptación y un proyecto integrador.

---

## Estructura del repositorio

```
AI_ENGINEERING_M4/
├── AEM4L1_IA_que_ve_y_crea_vision_e_imagenes/    # Visión + extracción estructurada
├── AEM4L2_Introduccion_a_audio_pipelines/         # ASR + WER + transcripción
├── AEM4L3_Introduccion_a_los_MCP/                 # Model Context Protocol
├── AEM4L4_Fundamentos_teoricos_y_arquitectura/    # Transformers, atención, tokenización
├── AEM4L5_Arquitecturas_avanzadas_de_adaptacion/  # LoRA, despliegue, profiling, asyncio
├── PIM4_Proyecto_Integrador_LegalMove/            # Proyecto integrador (contratos legales)
├── GUION_AEM4L1_Vision_Imagenes.md
├── GUION_AEM4L2_Audio_Pipelines.md
├── GUION_AEM4L3_MCP.md
├── GUION_AEM4L4_Fundamentos_Teoricos.md
├── GUION_AEM4L5_Arquitecturas_Avanzadas.md
├── GUION_PIM4_LegalMove.md
└── README.md
```

Cada carpeta contiene **8 notebooks** `.ipynb` compatibles con Google Colab:

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

**Total: 48 notebooks** listos para Google Colab.

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

Internals de transformers: self-attention, Q/K/V, costo cuadrático O(N²), tokenización (BPE vs WordPiece).

| Notebook | Descripción |
|----------|-------------|
| E01 | Mapas de atención conceptual (qué palabras atienden a cuáles) |
| E02 | Analogía Q/K/V con búsqueda en e-commerce |
| E03 | Escalado O(N²): tokens vs operaciones vs memoria GPU |
| E04 | Comparar BPE vs WordPiece con ejemplos |
| E05 | Ejercicio: relaciones de atención en texto clínico |
| E06 | Ejercicio: estimar costo de tokens en contrato legal |
| E07 | Contar tokens y calcular relaciones N² |
| E08 | ADR (Architecture Decision Record) para chatbot financiero |

**Conceptos clave:** RNN vs Transformer, self-attention, Q/K/V, O(N²), BPE, WordPiece, ADR

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
- `GUION_AEM4L{X}_{nombre}.md` — Guión/docencia de cada lección
- `E{NN}_{tipo}_{descripcion}.ipynb` — Notebooks con número secuencial

---

## Requisitos

- Google Colab (recomendado) o Jupyter Notebook
- Python 3.10+
- Las notebooks usan funciones mock — no requieren API keys para ejecución en clase

---

## Cómo usar

1. Abre cualquier notebook `.ipynb` en [Google Colab](https://colab.research.google.com/)
2. Sigue la progresión E01 → E08 dentro de cada lección
3. Los ejercicios E05-E06 son para resolver; E07 es warm-up; E08 es el desafío avanzado
