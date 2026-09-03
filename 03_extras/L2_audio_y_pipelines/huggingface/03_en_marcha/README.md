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

<table>
<tr><th>Archivo</th><th>Pipeline</th><th>Concepto integrador</th></tr>
<tr><td>pipeline audio local punto py</td><td>Audio a texto a WER.</td><td>Privacidad, latencia local y evaluación.</td></tr>
</table>

## Código central

~~~python
resultado = transcriptor(str(audio))
transcripcion = resultado["text"].strip().lower()
print("WER:", round(wer(referencia, transcripcion), 3))
~~~

La normalización lower permite que diferencias de mayúsculas no dominen la métrica. No elimina diferencias de palabras.

## Tabla de decisión

<table>
<tr><th>Resultado</th><th>Lectura</th><th>Siguiente paso</th></tr>
<tr><td>WER bajo</td><td>Texto cercano a referencia.</td><td>Revisar términos críticos y continuar.</td></tr>
<tr><td>WER medio</td><td>Hay dudas.</td><td>Mostrar evidencia y pedir revisión.</td></tr>
<tr><td>WER alto</td><td>ASR no es confiable.</td><td>Mejorar audio o usar otro modelo.</td></tr>
</table>

## Práctica

Cambiá de whisper tiny a whisper base. Registrá tiempo, memoria, WER y calidad cualitativa. Esa tabla es la base de una decisión de arquitectura.

