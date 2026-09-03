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

| Archivo | Entrada | Salida | Concepto |
|---|---|---|---|
| [00_transcribir_whisper.py](00_transcribir_whisper.py) | Indicación médica WAV | Texto reconocido | ASR remoto y postproceso mínimo. |

La explicación detallada de cada bloque está en [00_transcribir_whisper.md](00_transcribir_whisper.md).

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

| Responsabilidad | Herramienta |
|---|---|
| Voz a texto | Modelo de transcripción. |
| Texto a resumen o clasificación | LangChain y modelo de lenguaje. |
| Calidad de transcripción | WER y golden cases. |

## Práctica

Cambiá el audio por la variante con ruido. Antes de ejecutar, anotá qué palabras creés que pueden fallar. Luego compará el texto producido con la referencia humana.

## Preguntas

- ¿Por qué un modelo de chat no es el componente principal de ASR?
- ¿Qué evidencia debe guardarse después de transcribir?
- ¿Qué ocurriría si el audio tuviera dos voces superpuestas?
