# AEM4 Python Exercises

Repositorio educativo con ejercicios progresivos del **Módulo 4 de AI Engineering**.

Cada ejercicio compara una versión básica (que "funciona" pero tiene problemas) con una versión robusta (usando la tecnología correcta).

---

## Estructura del proyecto

```
python_puro/AEM4_python_exercises/
├── AEM4L1_vision_imagenes/     — Visión + Pydantic + golden cases
├── AEM4L2_audio_pipelines/     — Audio + WER + confiabilidad
├── AEM4L3_mcp/                 — MCP real + GitHub + schemas + scopes
├── AEM4L4_fundamentos_arquitectura/ — Transformer + tokenización + LoRA
└── AEM4L5_adaptacion_serving/  — Serving + profiling + async
```

El proyecto integrador vive separado en `proyecto_integrador/python/PIM4_legalmove/` para que no se mezcle con los ejercicios de clase.

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## Ejecutar un ejercicio

```bash
python python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/e01_vision_descripcion_basica.py
```

Todos los ejercicios que llaman modelos usan **OpenAI real mediante LangChain/OpenAI wrappers**. No hay selector de ejecución alternativo.

Antes de ejecutar, copiá `.env.example` a `.env` y completá:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
GITHUB_TOKEN=...   # solo para AEM4L3 GitHub MCP
```

Los scripts fallan temprano si falta la API key, para que la clase use siempre el flujo real.

---

## Módulos y objetivos

| Módulo | Objetivo |
|---|---|
| **AEM4L1** | Pasar de imagen → descripción libre → JSON mínimo → Pydantic completo |
| **AEM4L2** | Audio → transcripción → resumen libre → JSON mínimo → WER → gate confiable |
| **AEM4L3** | Notebooks conceptuales de MCP → MCP server real con GitHub → OpenAI host por STDIO |
| **AEM4L4** | Self-attention → Q/K/V → tokenización → latencia → PEFT/LoRA → ADR financiero |
| **AEM4L5** | Elegir arquitectura de serving → profiling → async pipeline |

---

## Idea pedagógica central

> Partimos de esto → vemos por qué falla → agregamos esta herramienta → ahora queda bien.

Cada archivo tiene secciones claras:
1. Versión básica / problemática
2. Problema detectado
3. Versión mejorada
4. Comparación ANTES VS DESPUÉS
5. Desafío para el alumno
