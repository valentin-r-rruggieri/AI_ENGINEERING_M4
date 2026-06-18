# AEM4L1_IA_que_ve_y_crea_vision_e_imagenes

## 📚 Estructura de Notebooks (10 ejercicios)

### 🏃 Recorrido Pedagógico Fundamental (Nuevo - E01-E02)
**Estos ejercicios explican Pydantic DESDE CERO**

- **E01** — `E01_resuelto_pydantic_modelo_basico.ipynb`
  - Qué es Pydantic y por qué lo necesitas
  - BaseModel, tipos simples, validación automática
  - 📦 Dependencias: `pydantic`

- **E02** — `E02_resuelto_pydantic_validacion_tipos.ipynb`
  - Validadores personalizados
  - Tipos especiales (EmailStr, constr)
  - Listas y modelos anidados
  - 📦 Dependencias: `pydantic`, `email-validator`

### 🔄 Aplicación Práctica (E03-E05)
**Pipeline real: Imagen → Texto → JSON → Validación**

- **E03** — `E03_resuelto_ticket_a_texto.ipynb`
  - Simular extracción de texto desde imagen (Vision API mock)
  - 📦 Dependencias: Ninguna (built-in)

- **E04** — `E04_resuelto_ticket_a_json.ipynb`
  - Transformar texto a JSON estructurado
  - 📦 Dependencias: Ninguna (built-in)

- **E05** — `E05_resuelto_json_con_pydantic.ipynb`
  - Validar JSON con Pydantic (barrera de seguridad del LLM)
  - 📦 Dependencias: `pydantic`

### 🎯 Casos Reales Resueltos (E06+)

- **E06** — `E06_resuelto_formulario_medico_campos_faltantes.ipynb`
  - Formulario médico con campos opcionales
  - 📦 Dependencias: `pydantic`

- **E07** — `E07_para_resolver_credencial_universitaria.ipynb`
  - Extracción de documento de identidad (para resolver)
  - 📦 Dependencias: `pydantic`

- **E08** — `E08_para_resolver_factura_simple.ipynb`
  - Factura de supermercado (para resolver)
  - 📦 Dependencias: `pydantic`

- **E09** — `E09_inicial_imagen_a_campos_basicos.ipynb`
  - Inicial: Extraer campos básicos (resuelto)
  - 📦 Dependencias: `pydantic`

- **E10** — `E10_avanzado_golden_cases_visuales.ipynb`
  - Avanzado: Golden cases con múltiples tipos de documentos (resuelto)
  - 📦 Dependencias: `pydantic`

## 📦 Dependencias Resumen

| Notebook | Dependencia | Instalación Automática |
|----------|-------------|------------------------|
| E01 | `pydantic` | ✅ SÍ (en el notebook) |
| E02 | `pydantic`, `email-validator` | ✅ SÍ (en el notebook) |
| E03 | ✅ Built-in | ✅ SÍ (no necesita) |
| E04 | ✅ Built-in | ✅ SÍ (no necesita) |
| E05 | `pydantic` | ✅ SÍ (en el notebook) |
| E06 | `pydantic` | ✅ SÍ (en el notebook) |
| E07 | `pydantic` | ✅ SÍ (en el notebook) |
| E08 | `pydantic` | ✅ SÍ (en el notebook) |
| E09 | `pydantic` | ✅ SÍ (en el notebook) |
| E10 | `pydantic` | ✅ SÍ (en el notebook) |

## 🚀 Uso en Google Colab

Cada notebook RESUELTO incluye una celda de instalación al inicio:
```python
!pip install pydantic email-validator
```

Ejecuta esa celda primero antes de ejecutar el resto.
