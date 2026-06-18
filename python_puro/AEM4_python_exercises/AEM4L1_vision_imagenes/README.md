# AEM4L1 | Visión e Imágenes

## Objetivo

Entender el flujo completo de visión paso a paso: primero una llamada multimodal básica, luego una extracción mínima estructurada, y recién después Pydantic completo, manejo de confianza y golden cases.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_vision_descripcion_basica.py` | Primer contacto con imagen + LLM | Descripción libre con `ChatOpenAI` multimodal |
| `e02_vision_json_minimo.py` | El texto libre no es backend-friendly | JSON mínimo con `with_structured_output` |
| `e03_formulario_limpio_pydantic.py` | Extracción completa sin contrato fuerte | Pydantic valida tipos y campos |
| `e04_formulario_cafe_revision_humana.py` | Imagen dañada → el modelo puede inventar | Confidence + campos opcionales + revisión humana |
| `e05_golden_cases_visuales.py` | Probamos "a ojo" si funciona | Golden cases con métricas reproducibles |

---

## Cómo ejecutar

```bash
python AEM4L1_vision_imagenes/e01_vision_descripcion_basica.py
python AEM4L1_vision_imagenes/e02_vision_json_minimo.py
python AEM4L1_vision_imagenes/e03_formulario_limpio_pydantic.py
python AEM4L1_vision_imagenes/e04_formulario_cafe_revision_humana.py
python AEM4L1_vision_imagenes/e05_golden_cases_visuales.py
```

---

## Conceptos clave

- **Modelo multimodal:** recibe imagen + texto y devuelve texto.
- **Texto libre vs JSON estructurado:** el backend necesita campos, no párrafos.
- **Structured output:** LangChain puede pedirle al modelo una salida compatible con un schema.
- **Pydantic v2:** valida tipos, rangos y campos requeridos en el momento de instanciación.
- **Confidence:** el modelo puede no estar seguro — hay que capturar esa incertidumbre.
- **Golden cases:** ejemplos con output esperado que permiten medir calidad de forma reproducible.
