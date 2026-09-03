# Tema: pipeline remoto completo

## Objetivo

Este tema une ASR, LangChain y evaluación. Es el primer pipeline completo: audio real, texto, resumen y WER.

~~~mermaid
flowchart LR
    A["Audio WAV"] --> B["Transcripción remota"]
    B --> C["Texto ASR"]
    C --> D["LangChain resume"]
    C --> E["WER"]
    D --> F["Salida para usuario"]
    E --> G["Señal de calidad"]
~~~

## Archivo de este tema

| Archivo | Etapas | Resultado |
|---|---|---|
| [pipeline_audio.py](pipeline_audio.py) | Audio a texto, texto a resumen, texto contra referencia. | Transcripción, resumen y WER. |

La guía de código y teoría está en [pipeline_audio.md](pipeline_audio.md).

## Lectura del flujo

~~~python
transcripcion = respuesta.text.lower()
resumen = cadena.invoke({"texto": transcripcion}).content
calidad = wer(referencia, transcripcion)
~~~

El orden importa. Primero se obtiene evidencia ASR, después se genera el resumen. El WER se calcula sobre el texto transcripto, no sobre el resumen.

## Tabla de fallas

| Falla observada | Causa probable | Qué no hacer |
|---|---|---|
| Resumen incorrecto | ASR entendió mal el audio. | Cambiar el prompt sin revisar el texto. |
| WER alto | Ruido, cortes o referencia distinta. | Automatizar sin revisión. |
| Texto correcto y resumen pobre | Prompt o modelo LLM. | Culpar a Whisper automáticamente. |

## Extensión

Agregá un gate:

~~~text
si WER > 0.15, no mostrar resumen automático
si WER <= 0.15, mostrar resumen y conservar transcripción
~~~

El umbral debe justificarse con golden cases del dominio.
