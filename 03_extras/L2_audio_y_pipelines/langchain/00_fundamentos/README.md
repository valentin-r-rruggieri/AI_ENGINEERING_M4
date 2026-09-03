# Tema: LangChain después de ASR

## Objetivo

LangChain no transcribe audio. Recibe la transcripción obtenida por ASR y la convierte en una salida útil: resumen, clasificación, extracción o respuesta estructurada.

~~~mermaid
flowchart LR
    A["WAV"] --> B["ASR"]
    B --> C["Transcripción"]
    C --> D["Prompt LangChain"]
    D --> E["Modelo de lenguaje"]
    E --> F["Resumen o JSON"]
~~~

## Archivo de este tema

| Archivo | Entrada | Salida | Aprendizaje |
|---|---|---|---|
| [00_resumir_transcripcion.py](00_resumir_transcripcion.py) | Texto ASR simulado. | Una oración resumen. | Separar ASR de postproceso. |

La guía de código y teoría está en [00_resumir_transcripcion.md](00_resumir_transcripcion.md).

## Código central

~~~python
prompt = ChatPromptTemplate.from_template(
    "Resumí en una oración: {transcripcion}"
)
cadena = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0)
respuesta = cadena.invoke({"transcripcion": transcripcion})
~~~

El operador vertical crea una cadena: el prompt produce el mensaje y el modelo produce una respuesta. temperature igual a cero reduce variación, útil para ejercicios de extracción y resumen.

## Tabla de responsabilidades

| Componente | No debe hacer | Sí debe hacer |
|---|---|---|
| ASR | Inventar intención. | Producir texto fiel. |
| Prompt | Ocultar reglas. | Delimitar tarea y límites. |
| LLM | Corregir mágicamente audio. | Interpretar texto disponible. |
| Pydantic | Validar verdad factual. | Validar forma de salida. |

## Práctica

Cambiá la transcripción por una frase ambigua. Luego agregá al prompt: “no inventes datos”. Compará el resumen y discutí qué error proviene de ASR y cuál del LLM.
