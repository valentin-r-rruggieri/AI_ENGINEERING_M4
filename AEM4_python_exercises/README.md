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
python AEM4L1_vision_imagenes/e01_formulario_limpio_pydantic.py
```

Todos los ejercicios usan **mocks por defecto** — funcionan sin API keys.

Para activar APIs reales, copiá `.env.example` a `.env` y completá las keys, luego cambiá `USE_REAL_API = True` dentro del archivo correspondiente.

---

## Módulos y objetivos

| Módulo | Objetivo |
|---|---|
| **AEM4L1** | Pasar de imagen → texto libre → JSON validado con Pydantic |
| **AEM4L2** | Transcribir → medir calidad (WER) → pipeline confiable |
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
