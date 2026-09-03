# Tema: transcripción remota con OpenAI

## Objetivo

Esta carpeta enseña el primer tramo del pipeline: un archivo WAV se convierte en texto con un modelo ASR remoto. Luego LangChain conserva y presenta el texto sin agregar información.

~~~mermaid
flowchart LR
    A["WAV"] --> B["API de transcripción"]
    B --> C["Texto ASR"]
    C --> D["LangChain"]
    D --> E["Texto normalizado"]
~~~

## Archivo de este tema

<table>
<tr><th>Archivo</th><th>Entrada</th><th>Salida</th><th>Concepto</th></tr>
<tr><td>00 transcribir whisper punto py</td><td>indicacion médica WAV</td><td>Texto reconocido</td><td>ASR remoto y postproceso mínimo.</td></tr>
</table>

## Lectura del código

~~~python
with audio.open("rb") as archivo_audio:
    transcripcion = cliente.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=archivo_audio,
    )
~~~

El archivo se abre en modo binario porque la API recibe bytes de audio, no una ruta local. El resultado contiene texto que todavía debe tratarse como hipótesis.

## Teoría

ASR significa Automatic Speech Recognition. Su objetivo es responder “qué se dijo”, no resumir ni decidir acciones. LangChain aparece después de ASR para aplicar una tarea de texto; no reemplaza el paso acústico.

<table>
<tr><th>Responsabilidad</th><th>Herramienta</th></tr>
<tr><td>Voz a texto</td><td>Modelo de transcripción.</td></tr>
<tr><td>Texto a resumen o clasificación</td><td>LangChain y modelo de lenguaje.</td></tr>
<tr><td>Calidad de transcripción</td><td>WER y golden cases.</td></tr>
</table>

## Práctica

Cambiá el audio por la variante con ruido. Antes de ejecutar, anotá qué palabras creés que pueden fallar. Luego compará el texto producido con la referencia humana.

## Preguntas

- ¿Por qué un modelo de chat no es el componente principal de ASR?
- ¿Qué evidencia debe guardarse después de transcribir?
- ¿Qué ocurriría si el audio tuviera dos voces superpuestas?

