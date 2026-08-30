# Guía de preparación para tu defensa oral — PIM4 LegalMove

> Una guía para que **te animes a exponer** y llegues tranquilo/a a la defensa.
> No es un examen trampa: es tu momento para **mostrar lo que construiste**. El corrector
> quiere entender tu proyecto y que te vaya bien. Vos ya hiciste lo difícil (el código);
> esto es contarlo.

---

## 1. Primero, la cabeza: cómo pararte frente a la defensa

- **No tenés que ser perfecto/a.** Tenés que ser **claro/a** y **honesto/a**. Se valora más
  que entiendas tu proyecto a que recites de memoria.
- **Nadie conoce tu proyecto mejor que vos.** Lo construiste paso a paso. Confiá en eso.
- **Si algo no sabés, decilo con criterio.** "No lo implementé, pero lo pensaría así..." suma
  mucho más que inventar. Muestra madurez técnica.
- **Los nervios son normales.** Hasta los seniors los tienen. Se calman **ensayando en voz alta**
  (no solo leyendo). Ensayá 2 o 3 veces y vas a sentir la diferencia.

> 💡 **Regla de oro:** no presentes tu proyecto como *"un script que llama a GPT"*.
> Presentalo como *"un pipeline de IA multimodal, multi-agente, validado y observable, que
> automatiza una tarea legal real"*. Esa frase sola ya resume casi toda la rúbrica.

---

## 2. Qué te van a evaluar (para que apuntes a eso)

La defensa evalúa que puedas **demostrar y explicar**, no solo que el código corra:

| Te van a mirar | Y esperan que muestres... |
|---|---|
| Que entendés el problema | Por qué el sistema tiene valor real (no solo qué hace). |
| Parsing multimodal | Que usás visión para leer imágenes y extraer texto fiel. |
| Los 2 agentes | Que hay **separación real** entre contextualizar y extraer. |
| Validación Pydantic | Que el JSON final está **validado**, no es texto libre. |
| Trazabilidad (Langfuse) | Que podés **auditar** cada paso: inputs, outputs, tokens, latencia. |
| Tu comunicación | Que explicás decisiones, corrés la demo y respondés preguntas. |

**El objetivo:** que quede claro que tu solución es *funcional, explicable, validada, trazable
y pensada para un escenario real*.

---

## 3. Cómo estructurar tu exposición (esqueleto simple)

No hace falta un guion palabra por palabra. Memorizá este **orden** y hablá con tus palabras:

1. **Quién sos y qué construiste** (30 seg).
2. **El problema** (1-2 min): la empresa pierde horas comparando contratos a mano → tu sistema lo automatiza.
3. **La arquitectura, en simple** (2-3 min): imágenes → visión → agente 1 (contexto) → agente 2 (cambios) → validación → trazas. *Explicá el mapa antes de correr código.*
4. **Demo, 2 casos** (10-12 min): uno **simple** (1 cambio) y uno **complejo** (varios cambios).
5. **Langfuse** (5 min): mostrá la traza, los spans, tokens y latencia. *Interpretá, no solo muestres.*
6. **Decisiones técnicas** (3 min): por qué visión, por qué 2 agentes, por qué Pydantic.
7. **Cierre** (1 min): "es una solución trazable, validada y lista para evolucionar".

> ⏱️ La defensa suele durar ~30 min. No te apures. Es mejor explicar bien 4 cosas que correr por 10.

---

## 4. Preparación previa (hacé esto ANTES de conectarte)

**Ensayo:**
- [ ] Corré tu proyecto **una vez completo** justo antes. Que no sea la primera vez del día.
- [ ] Practicá la explicación **en voz alta**, cronometrada.
- [ ] Preparate una **respuesta corta** para cada "¿por qué...?" (ver sección 6).

**Pantalla lista (todo abierto de antemano):**
- [ ] El editor con tu proyecto.
- [ ] Una terminal en la carpeta correcta.
- [ ] El README a la vista.
- [ ] Los documentos de prueba (2 pares).
- [ ] El dashboard de Langfuse **con una traza ya generada**.

**Red de seguridad (plan B):**
- [ ] Guardá una **salida anterior** (captura o texto) por si falla la API en vivo.
- [ ] Tené una **traza previa** abierta en Langfuse por si no carga una nueva.

> 🛟 Tener el plan B te da calma. Saber que "si algo falla, tengo respaldo" baja los nervios a la mitad.

---

## 5. Cómo explicar cada pieza en 1-2 frases (tu "elevator pitch")

Si podés decir esto con naturalidad, tenés la defensa ganada:

- **Visión (GPT-4o):** *"Los documentos entran como imágenes escaneadas. Uso un modelo de
  visión, no OCR, porque necesito preservar la estructura: cláusulas, montos, fechas."*
- **Agente 1 (Contextualización):** *"Su única tarea es entender la estructura de ambos
  documentos y armar un mapa. No extrae cambios todavía."*
- **Agente 2 (Extracción):** *"Usa ese mapa para detectar los cambios reales: adiciones,
  eliminaciones y modificaciones. Por eso es más preciso."*
- **Por qué 2 agentes:** *"Divido para conquistar. Un solo prompt que hace todo alucina más;
  separar responsabilidades da precisión y me deja auditar cada etapa."*
- **Pydantic:** *"El output de un LLM no es confiable hasta validarlo. Pydantic garantiza los
  campos y tipos: es un contrato de datos para que otro sistema lo consuma."*
- **Langfuse:** *"Me deja auditar todo: qué entró, qué salió, cuánto tardó y cuántos tokens
  costó cada paso. Si algo falla, sé exactamente dónde."*

---

## 6. Cómo encarar las preguntas del corrector

**Técnica simple:**
1. **Escuchá toda la pregunta** (no interrumpas para "adelantarte").
2. **Reformulá** si te da tiempo a pensar: *"Si entiendo bien, me preguntás por qué...".*
3. **Respondé con el porqué**, no solo el qué.
4. **Si no sabés:** *"Eso no lo implementé, pero lo encararía así..."*. Honestidad + criterio.

**Preguntas típicas (tené la idea, no el libreto):**

| Pregunta | Idea de respuesta |
|---|---|
| ¿Por qué visión y no OCR? | OCR da caracteres sueltos; visión entiende estructura legal. |
| ¿Por qué 2 agentes? | Separar contextualizar de extraer → menos alucinaciones, más auditable. |
| ¿Por qué Pydantic? | Para garantizar estructura y tipos → apto para producción. |
| ¿Cómo manejás errores? | Valido inputs, uso `.env`, y si el output es inválido Pydantic lo frena. |
| ¿Cómo auditás una ejecución? | Abro la traza en Langfuse y reviso los spans en orden. |
| ¿Cómo lo llevarías a producción? | Como servicio con cola, storage, reintentos y monitoreo de costos. |
| ¿Qué limitaciones tiene? | Depende de la calidad del escaneo; asiste, no reemplaza revisión legal. |

---

## 7. Errores comunes (evitalos)

- ❌ Empezar corriendo código sin explicar el problema.
- ❌ Mostrar Langfuse al final sin explicar qué significan los spans.
- ❌ Decir "usé 2 agentes" sin justificar **por qué**.
- ❌ Mostrar el JSON sin mencionar que está **validado**.
- ❌ No tener un caso de respaldo por si falla la demo.
- ❌ Justificar todo con "porque lo pedía la consigna".
- ❌ Hablar muy rápido por los nervios (respirá, hacé pausas).
- ❌ No mencionar limitaciones (mostrar autocrítica **suma**).

---

## 8. Plan B: qué decir si algo falla en vivo

Que algo falle **no te baja la nota si sabés reaccionar**:

- **Falla la API/demo:** *"Depende de una llamada externa. Tengo una salida previa y la traza
  en Langfuse para mostrar el resultado esperado."*
- **No carga Langfuse:** *"El pipeline corre igual; les muestro la instrumentación en código y
  una traza que registré antes."*
- **Falla la validación:** *"Justamente, esto muestra por qué valido: el sistema no acepta un
  output mal formado como si fuera correcto."* (¡convertís el error en un punto a favor!)

---

## 9. Frases que te hacen sonar sólido/a

Usá algunas de estas, con naturalidad:

- "Separé responsabilidades para mejorar la trazabilidad y el mantenimiento."
- "El output del LLM no se considera confiable hasta pasar por validación."
- "El primer agente no extrae cambios; solo construye contexto."
- "La salida está pensada como un contrato de datos para otro sistema."
- "La arquitectura me permite detectar en qué etapa se produjo un error."
- "El sistema asiste y estructura el análisis; no reemplaza la revisión legal humana."

---

## 10. Checklist final (imprimí esto)

- [ ] Entiendo el **problema** y puedo explicarlo en 1 minuto.
- [ ] Puedo explicar la **arquitectura** antes de mostrar código.
- [ ] Tengo **2 casos** de demo listos (simple y complejo).
- [ ] Sé **interpretar** una traza de Langfuse (no solo mostrarla).
- [ ] Tengo respuesta para cada **"¿por qué...?"**.
- [ ] Tengo **plan B** (salida y traza de respaldo).
- [ ] Ensayé **en voz alta** al menos una vez.
- [ ] Sé decir **una limitación** y **una mejora** de mi proyecto.

---

## 11. Mensaje final (leelo antes de entrar)

No estás rindiendo un examen para que te "descubran" algo que no sabés. Estás **mostrando un
proyecto que construiste con tus manos**. El corrector no es tu enemigo: quiere ver que
entendés lo que hiciste.

Respirá. Andá de lo simple a lo complejo. Si algo falla, reaccioná con calma y usá tu plan B.
Y recordá: **si podés explicar por qué tomaste cada decisión, ya estás aprobando la parte más
importante.**

Ahora sí: **animate y a exponer. Lo tenés.** 💪
