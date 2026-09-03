# L2 · Caso 08 — Auditor de errores críticos
## Teoría ampliada del archivo

### WER global frente a riesgo semántico

El ejemplo tiene una sola sustitución. Matemáticamente:

```text
WER = 1 error / 9 palabras aproximadamente = 0.111
```

Pero el cambio de frecuencia modifica el significado del mensaje. Por eso se agregan términos críticos.

<table>
<tr><th>Señal</th><th>Respuesta</th></tr>
<tr><td>WER bajo y término crítico intacto</td><td>Puede continuar según política.</td></tr>
<tr><td>WER bajo y término crítico afectado</td><td>Revisión humana.</td></tr>
<tr><td>WER alto</td><td>Revisar o pedir nuevo audio.</td></tr>
</table>

### Diseño reutilizable

El patrón sirve para salud, finanzas, legal y soporte. Solo cambia la lista de términos sensibles y la política de escalamiento.

Leé la teoría general: [Teoría completa L2](TEORIA_L2_AUDIO_PIPELINES.md).


## Qué aprendés

Este caso enseña que **WER no alcanza por sí solo**. Una transcripción puede tener pocos errores totales y aun así cambiar un dato peligroso.

El ejemplo compara:

- Referencia: “tomar un comprimido cada **ocho** horas”.
- Transcripción: “tomar un comprimido cada **dos** horas”.

Solo hay una sustitución, pero modifica la frecuencia. Por ese motivo, el pipeline debe detenerse y pedir revisión.

## Idea clave

> La métrica mide cantidad de errores; el dominio determina su gravedad.

## Flujo del ejemplo

```mermaid
flowchart LR
    A["Texto de referencia"] --> C["WER"]
    B["Transcripción ASR"] --> C
    B --> D["Buscar términos críticos"]
    C --> E["Agente LangChain"]
    D --> E
    E --> F["Auditoría Pydantic"]
    F --> G["Continuar o revisar"]
```

## Conceptos

<table>
<tr><th>Concepto</th><th>Explicación</th><th>Uso en el archivo</th></tr>
<tr><td>Referencia</td><td>Texto humano considerado correcto.</td><td>Permite evaluar ASR.</td></tr>
<tr><td>Hipótesis</td><td>Texto devuelto por la transcripción automática.</td><td>Se compara con la referencia.</td></tr>
<tr><td>WER</td><td>Errores de palabra sobre palabras de referencia.</td><td>Entrega una señal numérica.</td></tr>
<tr><td>Término crítico</td><td>Palabra o frase cuyo cambio altera una decisión.</td><td>Frecuencias, montos, fechas o negaciones.</td></tr>
<tr><td>Pydantic</td><td>Contrato de salida de la auditoría.</td><td>Evita una respuesta libre ambigua.</td></tr>
</table>

## Qué hace el agente

El agente recibe la referencia, la transcripción, el WER y los términos críticos ausentes. Devuelve:

```text
wer
terminos_criticos_afectados
nivel_riesgo
accion
motivo
```

No diagnostica ni modifica una indicación. Solo decide si el texto transcripto es confiable para seguir.

## Cómo ejecutar

```powershell
.\.venv\Scripts\python.exe .\03_extras\L2_audio_y_pipelines\resumen\08_auditor_errores_criticos_langchain.py
```

Requiere OPENAI API KEY en el archivo .env.

## Experimento guiado

1. Ejecutá el archivo sin cambios.
2. Cambiá “dos horas” por “ocho horas”.
3. Ejecutalo otra vez.
4. Compará WER, términos afectados y acción.
5. Cambiá “comprimido” por “cápsula”. Debatí si el nivel de riesgo debería ser igual.

## Preguntas para discutir

- ¿Puede WER ser bajo y el riesgo ser alto?
- ¿Qué términos serían críticos en una transferencia bancaria?
- ¿Qué es peor: omitir un dato crítico o inventarlo?
- ¿Quién debería revisar el caso escalado?

## Extensión

Convertí los términos críticos en una lista por dominio:

- Salud: dosis, frecuencia, duración.
- Finanzas: monto, cuenta, moneda.
- Legal: fecha, cláusula, vigencia.
- Soporte: número de ticket, producto, prioridad.
## Código y lectura ampliada

~~~python
terminos_criticos = ["ocho horas", "cinco días", "comprimido"]
afectados = [t for t in terminos_criticos if t not in transcripcion.lower()]
error = wer(referencia.lower(), transcripcion.lower())
~~~

La lista es una política del dominio. WER bajo con una frecuencia alterada no permite automatizar.

### Segundo gráfico: lógica del archivo

~~~mermaid
flowchart LR
    A["Transcripción"] --> B["WER y términos críticos"] --> C["Doble gate"] --> D["Decisión"]
~~~

### Tabla de lectura rápida

| Escenario | WER | Término crítico | Acción |
|---|---:|---|---|
| Claro | Bajo | Intacto | Continuar. |
| Dosis alterada | Bajo | Afectado | Revisar. |
| Degradado | Alto | Incierto | Pedir audio. |

### Fórmula o regla relevante

~~~text
WER = (S + D + I) / N
La decisión final debe combinar métrica, contexto y política de riesgo.
~~~

