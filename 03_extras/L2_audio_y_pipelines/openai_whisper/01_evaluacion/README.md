# Tema: evaluación de transcripciones con WER

## Objetivo

Este tema explica cómo se mide la diferencia entre una referencia humana y una transcripción automática. El archivo implementa la distancia de edición de manera visible.

~~~mermaid
flowchart TD
    A["Referencia humana"] --> C["Matriz de distancia"]
    B["Hipótesis ASR"] --> C
    C --> D["Errores mínimos"]
    D --> E["WER"]
~~~

## Archivo de este tema

<table>
<tr><th>Archivo</th><th>Qué muestra</th><th>Por qué importa</th></tr>
<tr><td>00 calcular wer punto py</td><td>La matriz de inserciones, deleciones y sustituciones.</td><td>Hace visible la matemática que una librería automatiza.</td></tr>
</table>

## Fórmula

~~~text
WER = (S + D + I) / N

S = sustituciones
D = deleciones
I = inserciones
N = palabras en la referencia
~~~

## Lectura del código

~~~python
costo = 0 if referencia[fila - 1] == hipotesis[columna - 1] else 1

distancias[fila][columna] = min(
    distancias[fila - 1][columna] + 1,
    distancias[fila][columna - 1] + 1,
    distancias[fila - 1][columna - 1] + costo,
)
~~~

Las tres opciones representan borrar, insertar o sustituir una palabra. La última celda de la matriz es la cantidad mínima de cambios.

## Tabla de interpretación

<table>
<tr><th>Resultado</th><th>Lectura</th><th>Acción siguiente</th></tr>
<tr><td>WER igual a 0</td><td>Coincidencia exacta.</td><td>Revisar si la referencia es suficiente.</td></tr>
<tr><td>WER bajo</td><td>Pocos errores globales.</td><td>Buscar términos críticos.</td></tr>
<tr><td>WER alto</td><td>Calidad baja.</td><td>Revisar audio, modelo o pedir repetición.</td></tr>
</table>

## Práctica

Eliminá una palabra de la hipótesis y después cambiá una palabra. Compará deleción y sustitución. ¿Tienen el mismo impacto de negocio?

## Límite de la métrica

WER cuenta palabras, no riesgo. “Ocho” por “dos” puede producir un WER bajo y un impacto alto.

