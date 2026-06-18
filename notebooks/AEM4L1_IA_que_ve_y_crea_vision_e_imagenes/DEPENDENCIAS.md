# 📦 Dependencias del Curso AEM4L1

## Resumen Rápido

Para usar todos los notebooks, instala:

```bash
pip install pydantic email-validator
```

## Detalles por Notebook

### ✅ E01 — Pydantic: Modelo Básico
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E02 — Pydantic: Validación y Tipos Avanzados
- **Dependencias:** `pydantic` + `email-validator`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic email-validator`
- **Nota:** `email-validator` es necesaria para usar `EmailStr`

### ✅ E03 — Ticket: Imagen → Texto
- **Dependencias:** Ninguna (usa solo `json` y `print`)
- **Celda de instalación:** NO ❌
- **Ejecutable:** Sí, sin instalar nada

### ✅ E04 — Ticket: Texto → JSON
- **Dependencias:** Ninguna (usa solo `json`)
- **Celda de instalación:** NO ❌
- **Ejecutable:** Sí, sin instalar nada

### ✅ E05 — JSON del LLM → Pydantic
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E06 — Formulario Médico
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E07 — Credencial Universitaria (para resolver)
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E08 — Factura Simple (para resolver)
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E09 — Imagen → Campos Básicos (inicial)
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

### ✅ E10 — Golden Cases Visuales (avanzado)
- **Dependencias:** `pydantic`
- **Celda de instalación:** SÍ ✅ (incluida en el notebook)
- **Comando:** `pip install pydantic`

## 🚀 En Google Colab

1. Los notebooks **RESUELTOS** (E01, E02, E03, E04, E05, E06) incluyen celdas de instalación
2. Ejecuta la primera celda de código de cualquier notebook para instalar las dependencias
3. Luego ejecuta el resto del notebook normalmente

**Ejemplo:**
```
Celda 1: !pip install pydantic email-validator  ← Ejecuta primero
Celda 2: from pydantic import BaseModel          ← Luego esto
```

## 📋 Para los Notebooks "para resolver"

Si trabajas en E07, E08, E09, E10, debes agregar tú una celda al inicio:

```python
import sys
!{sys.executable} -m pip install -q pydantic
```

## ✨ Best Practices

- ✅ Ejecuta PRIMERO la celda de `pip install`
- ✅ Si ves error `ModuleNotFoundError`, ejecuta `pip install` nuevamente
- ✅ En Colab, usa `-q` para instalar silenciosamente: `pip install -q pydantic`
- ✅ No necesitas instalar `json` o `datetime` — vienen con Python

## 🆘 Troubleshooting

**Error: `ModuleNotFoundError: No module named 'pydantic'`**
- Solución: Ejecuta la celda de `pip install` al inicio

**Error: `ModuleNotFoundError: No module named 'email_validator'`**
- Solución: En E02, ejecuta `pip install email-validator` (incluida en el notebook)

**Error en Colab: `ImportError`**
- Solución: Reinicia el kernel (Ctrl+M) tras instalar paquetes nuevos
