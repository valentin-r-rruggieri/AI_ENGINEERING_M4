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

<table>
<tr><th>Archivo</th><th>Entrada</th><th>Salida</th><th>Aprendizaje</th></tr>
<tr><td>00 resumir transcripción punto py</td><td>Texto ASR simulado.</td><td>Una oración resumen.</td><td>Separar ASR de postproceso.</td></tr>
</table>

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

<table>
<tr><th>Componente</th><th>No debe hacer</th><th>Sí debe hacer</th></tr>
<tr><td>ASR</td><td>Inventar intención.</td><td>Producir texto fiel.</td></tr>
<tr><td>Prompt</td><td>Ocultar reglas.</td><td>Delimitar tarea y límites.</td></tr>
<tr><td>LLM</td><td>Corregir mágicamente audio.</td><td>Interpretar texto disponible.</td></tr>
<tr><td>Pydantic</td><td>Validar verdad factual.</td><td>Validar forma de salida.</td></tr>
</table>

## Práctica

Cambiá la transcripción por una frase ambigua. Luego agregá al prompt: “no inventes datos”. Compará el resumen y discutí qué error proviene de ASR y cuál del LLM.

