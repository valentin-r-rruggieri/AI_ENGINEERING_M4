# Tema: datasets y tokenización

## Objetivo

Esta carpeta muestra cómo se preparan datos de texto y cómo distintos tokenizers dividen una misma frase. Es la base para entender por qué nombres, jerga y palabras nuevas afectan ASR y LLMs.

~~~mermaid
flowchart LR
    A["CSV local"] --> B["Dataset"]
    B --> C["Texto"]
    C --> D["BPE"]
    C --> E["WordPiece"]
    D --> F["Tokens"]
    E --> F
~~~

## Archivos de este tema

| Archivo | Concepto | Salida visible |
|---|---|---|
| [00_dataset_local.py](00_dataset_local.py) | Dataset desde CSV. | Filas, columnas y primer caso. |
| [01_bpe_wordpiece.py](01_bpe_wordpiece.py) | Subwords. | Dos segmentaciones del mismo texto. |

Guías: [dataset local](00_dataset_local.md) y [BPE / WordPiece](01_bpe_wordpiece.md).

## Dataset

~~~python
dataset = load_dataset("csv", data_files=str(ruta_csv), split="train")
print(dataset.column_names)
print(dataset[0])
~~~

Un Dataset preserva schema y permite operaciones reproducibles como map, filter, split y Trainer. Un CSV solo guarda filas; Dataset agrega una interfaz de machine learning.

## BPE y WordPiece

| Esquema | Idea | Ventaja |
|---|---|---|
| BPE | Fusiona pares frecuentes. | Construye subpalabras frecuentes. |
| WordPiece | Selecciona unidades estadísticamente útiles. | Representa continuaciones con `##`. |

~~~python
tokens_bpe = tokenizer_bpe.tokenize("hiperpersonalización contractual")
tokens_wordpiece = tokenizer_wordpiece.tokenize("hiperpersonalización contractual")
~~~

## Gráfico de granularidad

~~~mermaid
flowchart TD
    A["Palabra completa"] --> B["Pocos tokens, poco flexible"]
    C["Caracteres"] --> D["Muchos tokens, máxima cobertura"]
    E["Subwords"] --> F["Equilibrio para palabras nuevas"]
~~~

## Práctica

Usá un apellido raro y después una palabra de dominio. Contá tokens en BPE y WordPiece. Explicá cuál podría manejar mejor una palabra no vista.
