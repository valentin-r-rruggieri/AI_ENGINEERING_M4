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

| Archivo | Qué muestra | Por qué importa |
|---|---|---|
| [00_calcular_wer.py](00_calcular_wer.py) | Matriz de inserciones, deleciones y sustituciones. | Hace visible la matemática que una librería automatiza. |

La guía de código y teoría está en [00_calcular_wer.md](00_calcular_wer.md).

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

| Resultado | Lectura | Acción siguiente |
|---|---|---|
| WER igual a 0 | Coincidencia exacta. | Revisar si la referencia es suficiente. |
| WER bajo | Pocos errores globales. | Buscar términos críticos. |
| WER alto | Calidad baja. | Revisar audio, modelo o pedir repetición. |

## Práctica

Eliminá una palabra de la hipótesis y después cambiá una palabra. Compará deleción y sustitución. ¿Tienen el mismo impacto de negocio?

## Límite de la métrica

WER cuenta palabras, no riesgo. “Ocho” por “dos” puede producir un WER bajo y un impacto alto.
