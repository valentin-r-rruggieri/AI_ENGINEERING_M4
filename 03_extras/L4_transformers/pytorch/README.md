# PyTorch: tensores y self-attention

Recorrido local para observar las operaciones que sostienen un Transformer: tensores,
embeddings, Query/Key/Value y atención escalada.

```powershell
pip install -r 03_extras/L4_transformers/pytorch/requirements.txt
python 03_extras/L4_transformers/pytorch/00_fundamentos/00_tensores.py
```

Todos los ejemplos usan tensores pequeños y CPU.
# PyTorch — De tensores a bloque Transformer

| Orden | Guía | Concepto |
|---:|---|---|
| 1 | [Tensores](00_fundamentos/00_tensores.md) | Shape y reducciones. |
| 2 | [Embeddings](00_fundamentos/01_embeddings.md) | IDs a vectores. |
| 3 | [Q, K y V](01_atencion/00_query_key_value.md) | Proyecciones aprendibles. |
| 4 | [Self-attention](01_atencion/01_self_attention.md) | Scores, softmax y contexto. |
| 5 | [Bloque Transformer](02_en_marcha/bloque_transformer.md) | Atención, residual, normalización y FFN. |
