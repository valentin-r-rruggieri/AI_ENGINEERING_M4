# AEM4L1 | Visión e Imágenes

## Objetivo

Entender por qué no alcanza con pedirle al modelo "extraé los datos" y cómo Pydantic, el manejo de confianza y los golden cases hacen que el pipeline sea robusto y production-ready.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_formulario_limpio_pydantic.py` | Texto libre sin estructura | Pydantic valida tipos y campos |
| `e02_formulario_cafe_revision_humana.py` | Imagen dañada → el modelo inventa | Confidence + campos opcionales + revisión humana |
| `e03_golden_cases_visuales.py` | Probamos "a ojo" si funciona | Golden cases con métricas reproducibles |

---

## Cómo ejecutar

```bash
python AEM4L1_vision_imagenes/e01_formulario_limpio_pydantic.py
python AEM4L1_vision_imagenes/e02_formulario_cafe_revision_humana.py
python AEM4L1_vision_imagenes/e03_golden_cases_visuales.py
```

---

## Conceptos clave

- **Modelo multimodal:** recibe imagen + texto y devuelve texto.
- **Texto libre vs JSON estructurado:** el backend necesita campos, no párrafos.
- **Pydantic v2:** valida tipos, rangos y campos requeridos en el momento de instanciación.
- **Confidence:** el modelo puede no estar seguro — hay que capturar esa incertidumbre.
- **Golden cases:** ejemplos con output esperado que permiten medir calidad de forma reproducible.
