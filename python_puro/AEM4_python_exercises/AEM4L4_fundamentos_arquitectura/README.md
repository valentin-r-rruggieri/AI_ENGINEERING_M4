# AEM4L4 | Fundamentos Teóricos y Arquitectura

## Objetivo

Entender cómo las decisiones internas del modelo impactan en latencia, costo, manejo de vocabulario técnico y adaptación a dominios específicos — sin matemáticas densas, con analogías y código didáctico.

---

## Ejercicios

| Archivo | Problema | Solución |
|---|---|---|
| `e01_self_attention_conceptual.py` | Lectura lineal no conecta partes lejanas del texto | Self-attention: mapa de relaciones entre todos los tokens |
| `e02_tokenization_subwords.py` | Vocabulario por palabras completas no maneja términos técnicos | Tokenización subword (BPE/WordPiece) reconstruye palabras raras |
| `e03_lora_vs_full_finetuning.py` | Fine-tuning completo duplica el modelo por cada cliente | LoRA: un modelo base + adapters livianos por cliente |

---

## Cómo ejecutar

```bash
python AEM4L4_fundamentos_arquitectura/e01_self_attention_conceptual.py
python AEM4L4_fundamentos_arquitectura/e02_tokenization_subwords.py
python AEM4L4_fundamentos_arquitectura/e03_lora_vs_full_finetuning.py
```

---

## Conceptos clave

- **Self-attention:** cada token puede "mirar" a todos los demás directamente (vs. RNN secuencial).
- **Q/K/V:** Query (qué busco) × Key (qué ofrece cada token) → Value (información a agregar).
- **O(N²):** la attention es cuadrática — doblar el contexto cuadruplica el costo.
- **Tokenización subword:** BPE y WordPiece dividen palabras en fragmentos, balanceando vocabulario y coverage.
- **LoRA:** entrena matrices de rango bajo (∼1% de parámetros) en lugar del modelo completo.
- **Catastrophic forgetting:** full fine-tuning puede hacer que el modelo "olvide" conocimiento general.
