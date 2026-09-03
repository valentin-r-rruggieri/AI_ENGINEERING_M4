# Tema: pipeline local completo

## Objetivo

Este tema cierra el recorrido local: Whisper tiny procesa un WAV en CPU y JiWER mide su calidad sin enviar audio a una API externa.

~~~mermaid
flowchart LR
    A["Audio local"] --> B["Whisper tiny"]
    B --> C["Transcripción"]
    C --> D["WER"]
    E["Referencia"] --> D
    D --> F["Decisión de calidad"]
~~~

## Archivo de este tema

| Archivo | Pipeline | Concepto integrador |
|---|---|---|
| [pipeline_audio_local.py](pipeline_audio_local.py) | Audio a texto a WER. | Privacidad, latencia local y evaluación. |

La guía de código y teoría está en [pipeline_audio_local.md](pipeline_audio_local.md).

## Código central

~~~python
resultado = transcriptor(str(audio))
transcripcion = resultado["text"].strip().lower()
print("WER:", round(wer(referencia, transcripcion), 3))
~~~

La normalización lower permite que diferencias de mayúsculas no dominen la métrica. No elimina diferencias de palabras.

## Tabla de decisión

| Resultado | Lectura | Siguiente paso |
|---|---|---|
| WER bajo | Texto cercano a referencia. | Revisar términos críticos y continuar. |
| WER medio | Hay dudas. | Mostrar evidencia y pedir revisión. |
| WER alto | ASR no es confiable. | Mejorar audio o usar otro modelo. |

## Práctica

Cambiá de whisper tiny a whisper base. Registrá tiempo, memoria, WER y calidad cualitativa. Esa tabla es la base de una decisión de arquitectura.
