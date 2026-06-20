# AEM4L4 | Fundamentos Teoricos y Arquitectura

## Objetivo

Dar una clase teorico-practica completa sobre Transformers, self-attention, tokenizacion, costo cuadratico, vocabulario, PEFT y LoRA. Los scripts imprimen output visible para poder explicar en consola y combinan calculos deterministas con OpenAI real cuando corresponde.

---

## Ejercicios

| Archivo | Problema | Solucion |
|---|---|---|
| `e01_self_attention_conceptual.py` | Una frase ambigua necesita relaciones entre tokens | Mapa NxN, Q/K/V y structured output con OpenAI |
| `e02_tokenization_subwords.py` | Word-level pierde terminos tecnicos y char-level alarga contexto | Comparacion word/char/BPE/WordPiece + costo `N^2` |
| `e03_lora_vs_full_finetuning.py` | Full fine-tuning duplica modelos por cliente | Calculo de storage LoRA vs FT + ADR con OpenAI |
| `e04_vocabulario_latencia_budget.py` | Un contexto largo puede romper el SLA | Budget de tokens, pares de attention y estrategias de latencia |
| `e05_integrador_chatbot_financiero.py` | Hay que combinar arquitectura, tokenizacion, LoRA y SLA | Decision estructurada para chatbot financiero con OpenAI |

---

## Como ejecutar

Desde `python_puro/AEM4_python_exercises/`:

```bash
python3 AEM4L4_fundamentos_arquitectura/e01_self_attention_conceptual.py
python3 AEM4L4_fundamentos_arquitectura/e02_tokenization_subwords.py
python3 AEM4L4_fundamentos_arquitectura/e03_lora_vs_full_finetuning.py
python3 AEM4L4_fundamentos_arquitectura/e04_vocabulario_latencia_budget.py
python3 AEM4L4_fundamentos_arquitectura/e05_integrador_chatbot_financiero.py
```

Los ejercicios `e01`, `e03` y `e05` usan OpenAI real y requieren `OPENAI_API_KEY`. Los ejercicios `e02` y `e04` son deterministas y pueden ejecutarse sin credenciales.

---

## Conceptos clave

- **Self-attention:** cada token puede mirar a todos los demas directamente.
- **Q/K/V:** Query busca, Key ofrece y Value aporta informacion.
- **Bloque Transformer:** attention + FFN + normalizacion + residuales.
- **O(N^2):** duplicar tokens cuadruplica pares aproximados de attention.
- **Tokenizacion subword:** BPE y WordPiece balancean cobertura y eficiencia.
- **Vocabulario:** afecta memoria de embeddings, fragmentacion y latencia.
- **PEFT:** adapta entrenando pocos parametros.
- **LoRA:** agrega adapters de bajo rango sin reentrenar toda la base.
