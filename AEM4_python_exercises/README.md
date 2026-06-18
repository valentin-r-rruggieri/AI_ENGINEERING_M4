# AEM4 Python Exercises

Repositorio educativo con ejercicios progresivos del **Módulo 4 de AI Engineering**.

Cada ejercicio compara una versión básica (que "funciona" pero tiene problemas) con una versión robusta (usando la tecnología correcta).

---

## Estructura del proyecto

```
AEM4_python_exercises/
├── AEM4L1_vision_imagenes/     — Visión + Pydantic + golden cases
├── AEM4L2_audio_pipelines/     — Audio + WER + confiabilidad
├── AEM4L3_mcp/                 — MCP + schemas + scopes
├── AEM4L4_fundamentos_arquitectura/ — Transformer + tokenización + LoRA
├── AEM4L5_adaptacion_serving/  — Serving + profiling + async
└── PIM4_legalmove/             — Proyecto integrador: pipeline completo
```

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
python AEM4L1_vision_imagenes/e01_vision_descripcion_basica.py
```

Todos los ejercicios que llaman modelos usan **OpenAI real mediante LangChain/OpenAI wrappers**. No hay selector de ejecución alternativo.

Antes de ejecutar, copiá `.env.example` a `.env` y completá:

```bash
OPENAI_API_KEY=...
```

Los scripts fallan temprano si falta la API key, para que la clase use siempre el flujo real.

---

## Módulos y objetivos

| Módulo | Objetivo |
|---|---|
| **AEM4L1** | Pasar de imagen → descripción libre → JSON mínimo → Pydantic completo |
| **AEM4L2** | Audio → transcripción → resumen libre → JSON mínimo → WER → gate confiable |
| **AEM4L3** | Wrappers ad hoc → contrato MCP → scopes + versionado |
| **AEM4L4** | Intuir self-attention → tokenización → decisiones LoRA vs FT |
| **AEM4L5** | Elegir arquitectura de serving → profiling → async pipeline |
| **PIM4** | Pipeline frágil → agentes + Pydantic + trazabilidad |

---

## Idea pedagógica central

> Partimos de esto → vemos por qué falla → agregamos esta herramienta → ahora queda bien.

Cada archivo tiene secciones claras:
1. Versión básica / problemática
2. Problema detectado
3. Versión mejorada
4. Comparación ANTES VS DESPUÉS
5. Desafío para el alumno
