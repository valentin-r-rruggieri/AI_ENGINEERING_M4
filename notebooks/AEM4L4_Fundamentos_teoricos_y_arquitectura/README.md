# AEM4L4 | Fundamentos teoricos y arquitectura

Contiene 12 notebooks progresivos para dar una clase teorica desde lo mas basico. La idea no es resolver ejercicios largos de programacion, sino construir criterio: definiciones claras, ejemplos cotidianos, graficos Mermaid, tablas, una celda Python minima y tres actividades por tema.

Cada notebook incluye una imagen guia local en `assets/visuals/` para abrir el tema visualmente antes de ejecutar codigo. Los laboratorios tambien tienen imagenes para BPE, WordPiece, self-attention, Q/K/V, latencia, LoRA y ADR.

| Orden | Notebook | Tema central | Uso docente |
|---|---|---|---|
| 1 | `E01_mapa_del_ai_engineer.ipynb` | Arquitectura antes que magia | Presentar la cadena completa: texto, tokens, modelo, adaptacion, latencia y evaluacion. |
| 2 | `E02_texto_tokens_y_contexto_desde_cero.ipynb` | Texto, tokens y contexto | Bajar al nivel mas basico antes de hablar de Transformer. |
| 3 | `E03_de_rnn_a_transformer_sin_misterio.ipynb` | RNN/LSTM vs Transformer | Explicar secuencialidad, paralelizacion y dependencias largas. |
| 4 | `E04_self_attention_con_banco_y_contexto.ipynb` | Self-attention | Mostrar como el contexto desambigua palabras como `banco`. |
| 5 | `E05_query_key_value_como_buscador.ipynb` | Query, Key y Value | Explicar Q/K/V con analogia de buscador, sin arrancar por formulas. |
| 6 | `E06_anatomia_del_bloque_transformer.ipynb` | Bloque Transformer | Ubicar attention, FFN, residuales y normalizacion en una cadena simple. |
| 7 | `E07_por_que_attention_cuesta_n_cuadrado.ipynb` | Costo N cuadrado | Visualizar por que mas tokens pueden disparar latencia. |
| 8 | `E08_tokenizacion_palabra_caracter_subword.ipynb` | Tokenizacion basica | Comparar palabra, caracter y subword. |
| 9 | `E09_bpe_vs_wordpiece_en_lenguaje_simple.ipynb` | BPE vs WordPiece | Comparar dos estrategias de subword con ejemplos simples. |
| 10 | `E10_vocabulario_memoria_y_latencia.ipynb` | Vocabulario y memoria | Conectar vocabulario, embeddings, fragmentacion y latencia. |
| 11 | `E11_lora_y_peft_adaptar_sin_reentrenar_todo.ipynb` | PEFT y LoRA | Explicar adaptacion eficiente frente a full fine-tuning. |
| 12 | `E12_chatbot_financiero_decisiones_de_arquitectura.ipynb` | Caso integrador | Cerrar con una decision tipo ADR para un chatbot financiero. |

## Laboratorios visuales para probar frases en vivo

Estos notebooks son complementarios. Estan pensados para abrirlos durante la explicacion, editar una lista de frases o restricciones y mostrar resultados visuales sin depender de APIs ni librerias externas.

| Laboratorio | Mostrar despues de | Que permite probar |
|---|---|---|
| `E13_playground_frases_tokens_contexto.ipynb` | `E02_texto_tokens_y_contexto_desde_cero.ipynb` | Pegar varias frases y comparar palabras, tokens estimados, fragmentacion y alertas de contexto. |
| `E14_playground_tokenizadores_bpe_wordpiece.ipynb` | `E08_tokenizacion_palabra_caracter_subword.ipynb` y `E09_bpe_vs_wordpiece_en_lenguaje_simple.ipynb` | Comparar palabra completa, BPE didactico y WordPiece didactico con terminos tecnicos. |
| `E15_playground_attention_qkv_visual.ipynb` | `E04_self_attention_con_banco_y_contexto.ipynb` y `E05_query_key_value_como_buscador.ipynb` | Cambiar oraciones y token objetivo para visualizar self-attention y Q/K/V como buscador. |
| `E16_playground_transformer_costo_latencia.ipynb` | `E06_anatomia_del_bloque_transformer.ipynb` y `E07_por_que_attention_cuesta_n_cuadrado.ipynb` | Ver tokens estimados, relaciones `N^2`, latencia aproximada y recomendacion de diseno. |
| `E17_playground_lora_adr_chatbot_financiero.ipynb` | `E11_lora_y_peft_adaptar_sin_reentrenar_todo.ipynb` y `E12_chatbot_financiero_decisiones_de_arquitectura.ipynb` | Cambiar restricciones del caso financiero y generar una decision tipo ADR simple. |

## Estructura interna de cada notebook

1. Definiciones base.
2. Mapa visual del tema en Mermaid.
3. Tres ejemplos guiados.
4. Una celda Python minima para visualizar el concepto.
5. Interpretacion docente de la salida.
6. Tres actividades practicas minimas.
7. Errores comunes y correccion docente.
8. Cierre y puente al siguiente tema.

## Progresion docente

1. Primero se construye vocabulario basico: texto, tokens, contexto y arquitectura.
2. Luego se explica por contraste: RNN/LSTM versus Transformer.
3. Despues se abre el Transformer: self-attention, Q/K/V y bloque interno.
4. Mas adelante se conecta tokenizacion con costo, memoria y latencia.
5. Finalmente se introduce adaptacion eficiente con PEFT/LoRA y se integra todo en un chatbot financiero.
