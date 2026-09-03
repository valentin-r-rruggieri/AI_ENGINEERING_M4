# L2 · Caso 01 — Indicación estructurada
## Teoría ampliada del archivo

### De lenguaje libre a contrato

El modelo puede responder un párrafo, pero un sistema posterior necesita campos predecibles. Con structured output, LangChain solicita una instancia compatible con ReporteAudio y Pydantic comprueba los tipos.

<table>
<tr><th>Pregunta</th><th>Respuesta del schema</th></tr>
<tr><td>¿Qué se dijo?</td><td>transcripción.</td></tr>
<tr><td>¿Qué significa en pocas palabras?</td><td>resumen.</td></tr>
<tr><td>¿Hay suficiente evidencia?</td><td>confianza y requiere revisión.</td></tr>
</table>

### Regla de seguridad

Un resumen nunca debe reemplazar el texto original. La transcripción queda como evidencia para que una persona pueda revisar la decisión.

### Lectura del código

1. Se carga la configuración.
2. Se declara ReporteAudio.
3. Se entrega una transcripción al extractor.
4. El resultado vuelve con tipos validados.
5. Se imprime model dump.

Leé la teoría general: [Teoría completa L2](TEORIA_L2_AUDIO_PIPELINES.md).


## Propósito

Una transcripción es texto. Un pipeline necesita un objeto claro para que otro sistema pueda usarlo sin adivinar campos.

```mermaid
flowchart LR
    A["Texto transcripto"] --> B["LangChain"]
    B --> C["ReporteAudio Pydantic"]
    C --> D["Resumen, confianza y revisión"]
```

<table>
<tr><th>Campo</th><th>Uso</th></tr>
<tr><td>transcripción</td><td>Conserva la evidencia original.</td></tr>
<tr><td>resumen</td><td>Explica la idea principal.</td></tr>
<tr><td>confianza</td><td>Declara grado de certeza.</td></tr>
<tr><td>requiere revisión</td><td>Evita automatizar sin evidencia.</td></tr>
</table>

## En el código

with structured output pide al modelo una respuesta compatible con ReporteAudio. Pydantic comprueba sus tipos.

## Experimento

Cambiá la frecuencia de la indicación y comprobá qué debe conservarse literal en la transcripción.

## Preguntas

- ¿Por qué resumen y transcripción no son lo mismo?
- ¿Qué dato no debería inventar nunca el agente?
## Código y lectura ampliada

~~~python
class ReporteAudio(BaseModel):
    transcripcion: str
    resumen: str
    requiere_revision: bool
    confianza: float = Field(ge=0, le=1)

reporte = extractor.with_structured_output(ReporteAudio).invoke(texto_audio)
~~~

El schema se define antes de invocar al modelo. Pydantic valida tipos y límites, pero no prueba que la transcripción sea verdadera.

### Segundo gráfico: lógica del archivo

~~~mermaid
flowchart LR
    A["Texto transcripto"] --> B["Prompt"] --> C["Schema Pydantic"] --> D["Backend"]
~~~

### Tabla de lectura rápida

| Campo | Control | Propósito |
|---|---|---|
| transcripcion | str | Conserva evidencia. |
| confianza | 0 a 1 | Expresa duda. |
| requiere_revision | bool | Activa control humano. |

### Fórmula o regla relevante

~~~text
WER = (S + D + I) / N
La decisión final debe combinar métrica, contexto y política de riesgo.
~~~
## Explicación profunda del caso

Este caso no transcribe audio. Parte de texto ya obtenido y enseña a convertirlo en un **contrato de datos**. La idea es que una pantalla, una API o una persona reciban campos reconocibles en lugar de un párrafo de respuesta libre.

```mermaid
flowchart LR
    A[Texto ASR] --> B[Prompt LangChain]
    B --> C[LLM con structured output]
    C --> D[Pydantic ReporteAudio]
    D --> E[Diccionario validado]
```

### 1. El modelo Pydantic expresa el contrato

```python
class ReporteAudio(BaseModel):
    transcripcion: str
    resumen: str
    requiere_revision: bool
    confianza: float = Field(ge=0, le=1)
```

Cada campo responde una pregunta distinta. `transcripcion` conserva la fuente textual; `resumen` la vuelve legible; `requiere_revision` obliga a tomar una postura operativa; `confianza` solo admite valores de 0 a 1. `Field` no hace que el LLM sea más veraz: controla la forma que puede atravesar el pipeline.

| Campo | Tipo | Regla | Uso posterior |
|---|---|---|---|
| `transcripcion` | `str` | Texto obligatorio | Trazabilidad contra el audio. |
| `resumen` | `str` | Texto obligatorio | Lectura rápida de una persona. |
| `requiere_revision` | `bool` | Sí / no explícito | Routing humano. |
| `confianza` | `float` | Entre 0 y 1 | Señal complementaria, no evidencia única. |

### 2. Fijar una entrada pequeña

`texto_audio` funciona como salida de Whisper simulada. Se mantiene breve para que el alumno se concentre en el pasaje texto → esquema. En producción no se debe reemplazar la transcripción fuente por un resumen: ambos cumplen roles distintos.

### 3. Pedir structured output en LangChain

```python
extractor = ChatOpenAI(...).with_structured_output(ReporteAudio)
reporte = extractor.invoke("Organiza esta indicación ..." + texto_audio)
```

`with_structured_output(ReporteAudio)` entrega el esquema al modelo y valida la respuesta recibida. La instrucción “conserva el texto” y “sin agregar datos médicos” limita el alcance: el LLM organiza, no receta ni corrige la fuente acústica.

### 4. Hacer visible un objeto consumible

`reporte.model_dump()` transforma el objeto Pydantic en un diccionario que puede serializarse como JSON. La salida es estable aunque el orden narrativo de un LLM normalmente no lo sería.

## Errores que este caso permite explicar

| Situación | Qué sucede | Control apropiado |
|---|---|---|
| Falta `resumen` | Pydantic rechaza la forma | Revisar prompt o respuesta. |
| `confianza=1.4` | Viola `le=1` | No aceptar salida silenciosamente. |
| El LLM inventa una dosis | Puede tener forma válida | Comparar con `transcripcion` y evidencia. |
| ASR confundió una frecuencia | El esquema no lo descubre solo | WER + términos críticos antes de este paso. |

La lección es complementaria: Pydantic protege estructura; WER protege fidelidad frente a referencia; la revisión humana protege decisiones sensibles.
