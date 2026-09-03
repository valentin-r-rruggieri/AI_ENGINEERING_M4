# Tema: Transformers y difusión en audio

## Objetivo

Esta carpeta separa dos familias de modelos que se confunden con frecuencia. Transformer es muy útil para comprender secuencias; difusión genera o restaura señales paso a paso.

~~~mermaid
flowchart LR
    A["Audio o texto"] --> B["Transformer"]
    B --> C["Transcribir, clasificar, resumir"]
    D["Ruido"] --> E["Modelo de difusión"]
    E --> F["Generar o restaurar audio"]
~~~

## Archivos de este tema

| Archivo | Concepto | Resultado |
|---|---|---|
| [00_transformer_vs_diffusion.py](00_transformer_vs_diffusion.py) | Elección de arquitectura. | Tarea asociada a familia de modelo. |
| [01_scheduler.py](01_scheduler.py) | Paso de ruido en difusión. | Señal limpia y señal ruidosa simuladas. |

Guías: [Transformer y difusión](00_transformer_vs_diffusion.md) y [scheduler](01_scheduler.md).

## Regla de selección

| Tarea | Familia inicial | Por qué |
|---|---|---|
| Transcribir llamada | Transformer. | Comprende secuencia de voz a texto. |
| Clasificar intención | Transformer. | Interpreta contexto textual. |
| Generar sonido | Difusión. | Refina una señal desde ruido. |
| Restaurar audio | Difusión. | Puede modelar detalle acústico. |

## Código del scheduler

~~~python
audio_limpio = torch.linspace(-1, 1, steps=16).reshape(1, 1, 16)
ruido = torch.randn_like(audio_limpio)
audio_ruidoso = scheduler.add_noise(audio_limpio, ruido, instante)
~~~

El scheduler define cuánto ruido se mezcla en cada instante. La red aprende a predecir o eliminar ese ruido; el scheduler no es la red generativa.

## Práctica

Probá instante 10, 50 y 90. Compará media y forma del tensor. Explicá por qué más pasos suelen dar mayor calidad y también mayor latencia.
