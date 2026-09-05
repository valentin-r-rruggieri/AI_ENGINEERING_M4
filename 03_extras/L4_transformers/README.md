# L4: Fundamentos de Transformers

## Orden sugerido

1. `pytorch/00_fundamentos`: tensores y embeddings.
2. `pytorch/01_atencion`: Query, Key, Value y self-attention.
3. `pytorch/02_en_marcha`: bloque Transformer pequeño.
4. `huggingface/00_transformers`: pipeline e inspección de parámetros.
5. `huggingface/01_en_marcha`: tokenización e inferencia completas.
6. `langchain`: explicación de una inferencia para una persona usuaria.

El recorrido esperado es `texto -> tokens -> embeddings -> atención -> salida`.

Después recorré `resumen/`: contiene tres casos prácticos para ver tokens,
embeddings, atención y una explicación tipada de la inferencia.
# L4 — Transformers

## Ruta desde lo mínimo a lo integrador

1. [PyTorch](pytorch/README.md): tensores → embeddings → Q/K/V → self-attention → bloque Transformer.
2. [Hugging Face](huggingface/README.md): pipeline → parámetros → tokenización e inferencia explícita.
3. [LangChain](langchain/README.md): explicar resultados ya calculados.
4. [Resumen](resumen/README.md): ocho casos integradores con LangChain y LangGraph.
