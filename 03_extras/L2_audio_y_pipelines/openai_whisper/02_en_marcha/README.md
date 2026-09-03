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

<table>
<tr><th>Archivo</th><th>Etapas</th><th>Resultado</th></tr>
<tr><td>pipeline audio punto py</td><td>Audio a texto, texto a resumen, texto contra referencia.</td><td>Transcripción, resumen y WER.</td></tr>
</table>

## Lectura del flujo

~~~python
transcripcion = respuesta.text.lower()
resumen = cadena.invoke({"texto": transcripcion}).content
calidad = wer(referencia, transcripcion)
~~~

El orden importa. Primero se obtiene evidencia ASR, después se genera el resumen. El WER se calcula sobre el texto transcripto, no sobre el resumen.

## Tabla de fallas

<table>
<tr><th>Falla observada</th><th>Causa probable</th><th>Qué no hacer</th></tr>
<tr><td>Resumen incorrecto</td><td>ASR entendió mal el audio.</td><td>Cambiar el prompt sin revisar el texto.</td></tr>
<tr><td>WER alto</td><td>Ruido, cortes o referencia distinta.</td><td>Automatizar sin revisión.</td></tr>
<tr><td>Texto correcto y resumen pobre</td><td>Prompt o modelo LLM.</td><td>Culpar a Whisper automáticamente.</td></tr>
</table>

## Extensión

Agregá un gate:

~~~text
si WER > 0.15, no mostrar resumen automático
si WER <= 0.15, mostrar resumen y conservar transcripción
~~~

El umbral debe justificarse con golden cases del dominio.

