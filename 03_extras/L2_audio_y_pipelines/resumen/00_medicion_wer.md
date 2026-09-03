# L2 · Caso 00 — Medición WER
## Teoría ampliada del archivo

### La matemática que ejecuta el script

El archivo usa jiwer para calcular la distancia de edición entre referencia e hipótesis. La fórmula es:

```text
WER = (S + D + I) / N
```

Si la referencia tiene diez palabras y aparecen una sustitución y una omisión, el WER es 0.20. La métrica no dice cuál palabra importa más: solo cuenta diferencias.

### Lectura del código

<table>
<tr><th>Bloque</th><th>Responsabilidad</th></tr>
<tr><td>referencia</td><td>Ground truth humano.</td></tr>
<tr><td>transcripcion</td><td>Hipótesis producida por ASR.</td></tr>
<tr><td>wer</td><td>Compara ambas secuencias.</td></tr>
<tr><td>ChatOpenAI</td><td>Traduce la métrica a una explicación docente.</td></tr>
</table>

### Limitaciones

Antes de comparar, conviene normalizar mayúsculas, puntuación y espacios. Si no, una coma puede crear una diferencia que no representa un error de reconocimiento. También hay que revisar términos críticos aunque el WER sea bajo.

Leé la teoría general: [Teoría completa L2](TEORIA_L2_AUDIO_PIPELINES.md).


## Propósito

WER mide cuánto difiere una transcripción automática de una referencia humana. Es el primer paso para evaluar ASR con evidencia.

```mermaid
flowchart LR
    A["Referencia humana"] --> C["WER"]
    B["Transcripción ASR"] --> C
    C --> D["Interpretar calidad"]
```

<table>
<tr><th>Sigla</th><th>Significado</th></tr>
<tr><td>S</td><td>Sustituciones: una palabra cambia por otra.</td></tr>
<tr><td>D</td><td>Deleciones: una palabra se pierde.</td></tr>
<tr><td>I</td><td>Inserciones: aparece una palabra extra.</td></tr>
<tr><td>N</td><td>Total de palabras de referencia.</td></tr>
</table>

Fórmula: WER = (S + D + I) / N.

## En el código

El script calcula WER con jiwer y luego usa LangChain para convertir ese número en una explicación comprensible.

## Experimento

Cambiá “comprimido” por “cápsula”. Después eliminá “ocho”. Compará cuál error produce mayor WER.

## Preguntas

- ¿WER indica qué palabra falló?
- ¿Un WER igual a cero garantiza que el audio original sea bueno?
- ¿Por qué necesitamos una referencia humana?
## Código y lectura ampliada

~~~python
from jiwer import wer

referencia = "tomar un comprimido cada ocho horas"
hipotesis = "tomar un comprimido cada dos horas"
error = wer(referencia, hipotesis)
print(error)
~~~

El script entrega una distancia global. Normalizá mayúsculas y puntuación antes de comparar para no medir diferencias superficiales.

### Segundo gráfico: lógica del archivo

~~~mermaid
flowchart LR
    A["Referencia"] --> B["Alinear palabras"] --> C["S, D e I"] --> D["WER"]
~~~

### Tabla de lectura rápida

| WER | Lectura | Acción |
|---:|---|---|
| 0 | Coincidencia. | Conservar evidencia. |
| Bajo | Pocos errores. | Buscar términos críticos. |
| Alto | Baja calidad. | Revisar audio y ASR. |

### Fórmula o regla relevante

~~~text
WER = (S + D + I) / N
La decisión final debe combinar métrica, contexto y política de riesgo.
~~~
## Explicación profunda del caso

Este primer caso separa intencionalmente dos preguntas que en clase suelen mezclarse: **qué tan distinta es una transcripción** y **cómo se explica esa diferencia a una persona**. JiWER responde lo primero; LangChain solo redacta la segunda parte.

```mermaid
flowchart LR
    A[Referencia humana] --> C[jiwer.wer]
    B[Hipótesis ASR] --> C
    C --> D[Error numérico]
    D --> E[LangChain explica]
    E --> F[Salida visible]
```

### 1. Configuración compartida

```python
from dotenv import load_dotenv
load_dotenv()
```

El script carga `.env` antes de crear `ChatOpenAI`. En este caso JiWER funciona sin claves; LangChain sí necesita una credencial. Esto permite mostrar que no todas las piezas del pipeline dependen de un proveedor externo.

### 2. Referencia e hipótesis

```python
referencia = "tomar un comprimido cada ocho horas"
transcripcion = "tomar un comprimido cada ocho horas"
```

Ambas cadenas son iguales para que la salida inicial sea WER `0.0`. La referencia representa lo que una persona verificó; `transcripcion` representa lo que habría devuelto ASR. Cambiar solo una palabra permite aislar el efecto de una sustitución.

### 3. La métrica ocurre antes del LLM

```python
error_wer = wer(referencia, transcripcion)
```

La fórmula es `WER = (S + D + I) / N`: sustituciones, eliminaciones e inserciones divididas por palabras de referencia. El LLM no participa aquí, por lo que el número es repetible para el mismo par de textos.

| Bloque | Input | Output | Riesgo si se omite |
|---|---|---|---|
| Referencia | Texto humano | Patrón medible | No hay evaluación objetiva. |
| `wer` | Referencia + hipótesis | Distancia normalizada | Se confunde fluidez con calidad. |
| LangChain | Valor ya calculado | Explicación en lenguaje natural | Puede explicar mal, pero no altera WER. |

### 4. LangChain interpreta, no recalcula

La instrucción incluye `WER={error_wer}`. `ChatOpenAI(...).invoke(...)` devuelve un mensaje y `.content` extrae su texto. El resultado es útil para una interfaz o informe, pero el dato fuente sigue siendo `error_wer`.

### Discusión docente

Un WER de 0 no prueba que una orden sea segura: la referencia podría estar mal o el audio podría pertenecer a otro paciente. Un WER bajo tampoco pesa los daños: “ocho” por “dos” es una sola sustitución y puede ser crítica. El próximo caso agrega estructura para que otro sistema no reciba un párrafo ambiguo.

| Cambio experimental | WER esperado | Pregunta |
|---|---:|---|
| Cambiar `comprimido` por `cápsula` | Mayor que 0 | ¿Es un error de palabra o de significado? |
| Quitar `ocho` | Mayor que 0 | ¿Qué tipo de operación cuenta? |
| Agregar una palabra | Mayor que 0 | ¿Por qué WER puede crecer aun si se conserva la frase? |
