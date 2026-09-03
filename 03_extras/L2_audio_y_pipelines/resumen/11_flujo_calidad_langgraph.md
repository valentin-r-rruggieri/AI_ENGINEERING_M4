# L2 · Caso 11 — LangGraph auditable para una llamada
## Teoría ampliada del archivo

### Un pipeline auditable

El grafo guarda evidencia en cada etapa y separa responsabilidades.

```text
audio -> transcripción -> WER -> decisión -> destino operativo
```

<table>
<tr><th>Nodo</th><th>Entrada</th><th>Salida</th></tr>
<tr><td>Transcribir</td><td>Archivo WAV.</td><td>Texto ASR.</td></tr>
<tr><td>Medir</td><td>Texto y referencia.</td><td>WER.</td></tr>
<tr><td>Decidir</td><td>WER y texto.</td><td>Destino y motivo.</td></tr>
</table>

### Escalabilidad

Después se pueden agregar nodos de detección de términos críticos, logging, reintentos y observabilidad. La regla es conservar cada etapa simple y comprobable.

### Política de decisión

WER mayor a 0.15 es una regla didáctica. En producción debe surgir de golden cases, costos de revisión y riesgos del dominio.

Leé la teoría general: [Teoría completa L2](TEORIA_L2_AUDIO_PIPELINES.md).


## Qué aprendés

Este caso muestra una arquitectura visible. En lugar de ejecutar todo en un bloque, el pipeline conserva estado entre pasos:

1. Transcribe la llamada.
2. Calcula WER.
3. Decide qué destino operativo corresponde.

La ventaja no es “hacer más código”. La ventaja es poder inspeccionar dónde apareció un error.

## Arquitectura

```mermaid
flowchart LR
    A["Llamada con ruido"] --> B["Nodo transcribir"]
    B --> C["Estado: transcripción"]
    C --> D["Nodo medir calidad"]
    D --> E["Estado: WER"]
    E --> F["Nodo decidir destino"]
    F --> G["Reporte Pydantic"]
```

## Estado del grafo

<table>
<tr><th>Campo</th><th>Quién lo agrega</th><th>Por qué importa</th></tr>
<tr><td>archivo</td><td>Entrada</td><td>Indica qué WAV se analiza.</td></tr>
<tr><td>referencia</td><td>Entrada</td><td>Permite calcular WER.</td></tr>
<tr><td>transcripción</td><td>Nodo ASR</td><td>Es evidencia antes de interpretar.</td></tr>
<tr><td>WER</td><td>Nodo de calidad</td><td>Es señal objetiva de error.</td></tr>
<tr><td>decisión</td><td>Nodo LangChain</td><td>Explica el siguiente paso.</td></tr>
</table>

## Qué decide el último nodo

El agente recibe la transcripción y el WER. Su tarea es elegir un destino:

- Procesar soporte.
- Pedir revisión humana.
- Pedir un nuevo audio.

La regla del ejemplo propone escalar cuando WER es mayor a 0.15. Ese número es una hipótesis didáctica, no una regla universal. En producción el umbral depende del riesgo, los costos y la evidencia obtenida con golden cases.

## Cómo ejecutar

```powershell
.\.venv\Scripts\python.exe .\03_extras\L2_audio_y_pipelines\resumen\11_flujo_calidad_langgraph.py
```

## Experimento guiado

1. Ejecutá el flujo con la llamada ruidosa.
2. Cambiá el archivo por la llamada limpia.
3. Compará WER, motivo y destino.
4. Subí el umbral a 0.25.
5. Discutí qué tipo de error pasa a automatizarse por esa decisión.

## LangChain y LangGraph

<table>
<tr><th>Herramienta</th><th>Mejor para</th><th>En este caso</th></tr>
<tr><td>LangChain</td><td>Una llamada a un modelo y salida estructurada.</td><td>Redacta la decisión final.</td></tr>
<tr><td>LangGraph</td><td>Varios pasos con estado visible.</td><td>Conecta ASR, WER y decisión.</td></tr>
</table>

## Preguntas para discutir

- ¿Por qué la transcripción debe quedar en el estado?
- ¿Qué nodo se puede reintentar sin repetir todo?
- ¿Dónde agregarías una detección de términos críticos?
- ¿Qué información guardarías en un log de auditoría?

## Extensión

Agregar un nodo antes de decidir destino:

```mermaid
flowchart LR
    A["Transcribir"] --> B["Medir WER"]
    B --> C["Detectar términos críticos"]
    C --> D["Decidir destino"]
```

Así el pipeline combina métrica general, riesgo semántico y decisión operativa.
## Código y lectura ampliada

~~~python
grafo.add_node("transcribir_llamada", transcribir_llamada)
grafo.add_node("medir_calidad", medir_calidad)
grafo.add_node("decidir_destino", decidir_destino)
grafo.add_edge(START, "transcribir_llamada")
grafo.add_edge("transcribir_llamada", "medir_calidad")
grafo.add_edge("medir_calidad", "decidir_destino")
~~~

Cada nodo tiene una responsabilidad: evidenciar, medir o decidir. Esto permite reintentar y auditar sin ocultar pasos.

### Segundo gráfico: lógica del archivo

~~~mermaid
flowchart LR
    A["WAV"] --> B["Transcripción"] --> C["WER"] --> D["Destino"]
~~~

### Tabla de lectura rápida

| Nodo | Entrada | Salida |
|---|---|---|
| Transcribir | WAV | Texto ASR. |
| Medir | Texto y referencia | WER. |
| Decidir | WER y texto | Destino y motivo. |

### Fórmula o regla relevante

~~~text
WER = (S + D + I) / N
La decisión final debe combinar métrica, contexto y política de riesgo.
~~~
## Explicación profunda del caso

Este es el integrador más completo de L2: transforma una llamada ruidosa en texto, mide WER y toma una decisión estructurada. Cada etapa aparece como nodo para que se pueda auditar qué dato originó la decisión final.

```mermaid
flowchart LR
    A[Estado inicial: archivo + referencia] --> B[transcribir_llamada]
    B --> C[Estado: + transcripción]
    C --> D[medir_calidad]
    D --> E[Estado: + WER]
    E --> F[decidir_destino]
    F --> G[DecisionLlamada]
```

### 1. Distinguir estado de negocio y resultado final

```python
class EstadoLlamada(TypedDict):
    archivo: str
    referencia: str
    transcripcion: NotRequired[str]
    wer: NotRequired[float]
    decision: NotRequired[dict[str, object]]
```

El estado es la bitácora del pipeline. Arranca con el audio y la referencia; cada nodo agrega evidencia. `DecisionLlamada` es diferente: contiene solamente lo que una operación de soporte necesita consumir (`wer`, `destino`, `motivo`).

### 2. Nodo uno: convertir bytes en texto

```python
def transcribir_llamada(state):
    with (... / state["archivo"]).open("rb") as archivo_audio:
        respuesta_asr = cliente_audio.audio.transcriptions.create(...)
    return {"transcripcion": str(respuesta_asr.text)}
```

El nodo utiliza solo `archivo`, conserva la referencia sin tocar y agrega una transcripción. Si falla ASR, el flujo no debería inventar una decisión: se debe registrar el error y detenerse o derivar a revisión.

### 3. Nodo dos: medir objetivamente

```python
error_wer = round(wer(state["referencia"].lower(), state["transcripcion"].lower()), 3)
return {"wer": error_wer}
```

El cálculo ocurre antes del LLM. Minúsculas reducen diferencias de estilo; no corrigen contenido. El nodo devuelve únicamente `wer`, permitiendo comparar qué decisión surgiría con el mismo texto y otro umbral.

### 4. Nodo tres: convertir evidencia en destino

El prompt recibe WER **y** transcripción. Además impone una política: si WER es mayor que `0.15`, elegir revisión o nuevo audio; si no, procesar soporte. `with_structured_output(DecisionLlamada)` exige una respuesta con tres campos, y `model_validate` confirma el contrato antes de actualizar estado.

| Nodo | Input de estado | Output de actualización | Razón de existir separado |
|---|---|---|---|
| `transcribir_llamada` | `archivo` | `transcripcion` | ASR no decide negocio. |
| `medir_calidad` | Referencia + transcripción | `wer` | La métrica es reproducible y no generativa. |
| `decidir_destino` | WER + transcripción | `decision` | La explicación contextual llega después de medir. |

### 5. Aristas = orden auditable

```python
START → transcribir_llamada → medir_calidad → decidir_destino → END
```

Las aristas prohiben que el LLM decida antes de conocer WER. Esa propiedad importa más que la cantidad de nodos: el flujo expresa una política de seguridad que se puede leer, probar y modificar.

```mermaid
sequenceDiagram
    participant U as Usuario
    participant G as Grafo
    participant A as ASR
    participant M as JiWER
    participant L as LangChain
    U->>G: archivo ruidoso + referencia
    G->>A: transcribir
    A-->>G: texto
    G->>M: referencia + texto
    M-->>G: WER
    G->>L: texto + WER + regla
    L-->>G: destino estructurado
    G-->>U: decisión validada
```

## Prueba didáctica recomendada

Ejecutá con `llamada_soporte.wav` y luego con `llamada_soporte_ruido.wav`. Compará los tres niveles de evidencia: transcripción, WER y motivo. Si la decisión cambia, verificá que cambió por la métrica o por el contenido, no porque el agente “pareció más seguro”.

## Límite profesional

WER no detecta por sí solo términos de negocio críticos. Una versión de producción debe combinar este grafo con el auditor del caso 08, manejo de errores de red, trazabilidad de modelo y revisión humana para casos sensibles.
