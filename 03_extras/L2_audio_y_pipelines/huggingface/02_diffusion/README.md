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

<table>
<tr><th>Archivo</th><th>Concepto</th><th>Resultado</th></tr>
<tr><td>00 transformer vs diffusion punto py</td><td>Elección de arquitectura.</td><td>Tarea asociada a familia de modelo.</td></tr>
<tr><td>01 scheduler punto py</td><td>Paso de ruido en difusión.</td><td>Audio limpio y audio ruidoso simulados.</td></tr>
</table>

## Regla de selección

<table>
<tr><th>Tarea</th><th>Familia inicial</th><th>Por qué</th></tr>
<tr><td>Transcribir llamada</td><td>Transformer.</td><td>Comprende secuencia de voz a texto.</td></tr>
<tr><td>Clasificar intención</td><td>Transformer.</td><td>Interpreta contexto textual.</td></tr>
<tr><td>Generar sonido</td><td>Difusión.</td><td>Refina una señal desde ruido.</td></tr>
<tr><td>Restaurar audio</td><td>Difusión.</td><td>Puede modelar detalle acústico.</td></tr>
</table>

## Código del scheduler

~~~python
audio_limpio = torch.linspace(-1, 1, steps=16).reshape(1, 1, 16)
ruido = torch.randn_like(audio_limpio)
audio_ruidoso = scheduler.add_noise(audio_limpio, ruido, instante)
~~~

El scheduler define cuánto ruido se mezcla en cada instante. La red aprende a predecir o eliminar ese ruido; el scheduler no es la red generativa.

## Práctica

Probá instante 10, 50 y 90. Compará media y forma del tensor. Explicá por qué más pasos suelen dar mayor calidad y también mayor latencia.

