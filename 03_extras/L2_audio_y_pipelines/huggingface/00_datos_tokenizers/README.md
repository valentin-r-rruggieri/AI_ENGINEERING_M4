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

<table>
<tr><th>Archivo</th><th>Concepto</th><th>Salida visible</th></tr>
<tr><td>00 dataset local punto py</td><td>Dataset desde CSV.</td><td>Filas, columnas y primer caso.</td></tr>
<tr><td>01 bpe wordpiece punto py</td><td>Subwords.</td><td>Dos segmentaciones del mismo texto.</td></tr>
</table>

## Dataset

~~~python
dataset = load_dataset("csv", data_files=str(ruta_csv), split="train")
print(dataset.column_names)
print(dataset[0])
~~~

Un Dataset preserva schema y permite operaciones reproducibles como map, filter, split y Trainer. Un CSV solo guarda filas; Dataset agrega una interfaz de machine learning.

## BPE y WordPiece

<table>
<tr><th>Esquema</th><th>Idea</th><th>Ventaja</th></tr>
<tr><td>BPE</td><td>Fusiona pares frecuentes.</td><td>Construye subpalabras frecuentes.</td></tr>
<tr><td>WordPiece</td><td>Selecciona unidades estadísticamente útiles.</td><td>Representa continuaciones con ##.</td></tr>
</table>

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

