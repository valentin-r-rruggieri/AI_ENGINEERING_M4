# L2 · Caso 04 — Clasificar prioridad de audio
## Teoría ampliada del archivo

### Clasificar no es diagnosticar

El archivo asigna prioridad operativa a una transcripción. No indica tratamiento ni reemplaza a una persona experta. La salida sirve para ordenar trabajo.

<table>
<tr><th>Prioridad</th><th>Ejemplo de acción</th></tr>
<tr><td>Baja</td><td>Registrar y responder por canal habitual.</td></tr>
<tr><td>Media</td><td>Derivar a una cola prioritaria.</td></tr>
<tr><td>Alta</td><td>Escalar para revisión humana inmediata.</td></tr>
</table>

### Diseño del prompt

El prompt debe delimitar el rol: clasificar evidencia disponible, no agregar información, no dar diagnóstico. El schema obliga a explicar el motivo de la prioridad.

### Evaluación

Para evaluar este agente se necesita un conjunto de transcripciones con prioridad esperada y una regla explícita para desacuerdos.

Leé la teoría general: [Teoría completa L2](TEORIA_L2_AUDIO_PIPELINES.md).


## Propósito

Una misma transcripción puede requerir acciones distintas. Este caso enseña a separar clasificación operativa de diagnóstico o respuesta médica.

```mermaid
flowchart LR
    A["Transcripción"] --> B["LangChain"]
    B --> C["Prioridad Pydantic"]
    C --> D["Acción operativa"]
```

<table>
<tr><th>Campo</th><th>Pregunta que responde</th></tr>
<tr><td>prioridad</td><td>¿Cuán rápido debe atenderse?</td></tr>
<tr><td>motivo</td><td>¿Qué evidencia justifica la prioridad?</td></tr>
<tr><td>respuesta operativa</td><td>¿Cuál es el siguiente paso?</td></tr>
</table>

## Límite pedagógico

Clasificar prioridad no reemplaza a un profesional ni genera diagnóstico. El agente organiza una derivación.

## Experimento

Probá una transcripción de soporte, otra de reunión y otra con una alerta. Compará el motivo y la respuesta operativa.
## Código y lectura ampliada

~~~python
class PrioridadAudio(BaseModel):
    prioridad: str
    motivo: str
    respuesta_operativa: str

resultado = extractor.invoke("Clasificá sin diagnosticar: " + transcripcion)
~~~

La prioridad organiza trabajo; no genera diagnóstico ni reemplaza una persona experta. El motivo permite revisar la clasificación.

### Segundo gráfico: lógica del archivo

~~~mermaid
flowchart LR
    A["Transcripción"] --> B["Agente"] --> C["Prioridad"] --> D["Acción operativa"]
~~~

### Tabla de lectura rápida

| Prioridad | Ejemplo de ruta |
|---|---|
| Baja | Registrar y atender. |
| Media | Cola prioritaria. |
| Alta | Escalamiento humano. |

### Fórmula o regla relevante

~~~text
WER = (S + D + I) / N
La decisión final debe combinar métrica, contexto y política de riesgo.
~~~

