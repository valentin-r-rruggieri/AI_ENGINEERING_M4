# Tema: ASR local y evaluación

## Objetivo

Esta carpeta muestra que un modelo ASR puede ejecutarse en la máquina local. Se compara audio a texto y la calidad se mide con JiWER.

~~~mermaid
flowchart LR
    A["WAV local"] --> B["Whisper tiny en CPU"]
    B --> C["Transcripción local"]
    C --> D["JiWER"]
    E["Referencia humana"] --> D
    D --> F["WER y revisión"]
~~~

## Archivos de este tema

<table>
<tr><th>Archivo</th><th>Entrada</th><th>Salida</th></tr>
<tr><td>00 asr local punto py</td><td>Audio WAV.</td><td>Texto de Whisper tiny local.</td></tr>
<tr><td>01 wer jiwer punto py</td><td>Referencia e hipótesis.</td><td>WER y regla de revisión.</td></tr>
</table>

## Código ASR

~~~python
transcriptor = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",
    device=-1,
)
resultado = transcriptor(str(audio))
~~~

device igual a menos uno fuerza CPU. Es útil para que el ejercicio sea reproducible, aunque más lento que una GPU.

## Código WER

~~~python
error = wer(referencia, transcripcion)
umbral = 0.15
print("Revisión humana:", error > umbral)
~~~

## Comparación local y remoto

<table>
<tr><th>Aspecto</th><th>Local</th><th>Remoto</th></tr>
<tr><td>Privacidad</td><td>Audio permanece en la máquina.</td><td>Audio viaja al proveedor.</td></tr>
<tr><td>Configuración</td><td>Descarga de modelo y CPU o GPU.</td><td>Clave y conexión.</td></tr>
<tr><td>Latencia</td><td>Depende del equipo.</td><td>Depende de red y servicio.</td></tr>
<tr><td>Costo por uso</td><td>Infraestructura propia.</td><td>Uso de API.</td></tr>
</table>

## Práctica

Ejecutá audio limpio y luego audio ruidoso. Compará las palabras erróneas, el WER y la decisión de revisión.

