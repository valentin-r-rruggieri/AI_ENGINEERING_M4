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

| Archivo | Entrada | Salida |
|---|---|---|
| [00_asr_local.py](00_asr_local.py) | Audio WAV. | Texto de Whisper tiny local. |
| [01_wer_jiwer.py](01_wer_jiwer.py) | Referencia e hipótesis. | WER y regla de revisión. |

Guías: [ASR local](00_asr_local.md) y [WER con JiWER](01_wer_jiwer.md).

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

| Aspecto | Local | Remoto |
|---|---|---|
| Privacidad | Audio permanece en la máquina. | Audio viaja al proveedor. |
| Configuración | Descarga de modelo y CPU o GPU. | Clave y conexión. |
| Latencia | Depende del equipo. | Depende de red y servicio. |
| Costo por uso | Infraestructura propia. | Uso de API. |

## Práctica

Ejecutá audio limpio y luego audio ruidoso. Compará las palabras erróneas, el WER y la decisión de revisión.
