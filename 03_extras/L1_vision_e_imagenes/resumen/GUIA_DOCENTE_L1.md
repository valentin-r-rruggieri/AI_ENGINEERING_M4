# Guía docente — L1: IA que ve y crea

Esta clase muestra un flujo completo: una imagen entra al sistema, un modelo multimodal la interpreta, Pydantic valida el resultado y una métrica decide si se acepta o se revisa con una persona.

Está pensada para **3 horas**, pero cada bloque puede acortarse. Los ejemplos usan documentos ficticios y leen las credenciales desde el archivo .env de la raíz.

## Resultado de aprendizaje

Al final de la clase, cada estudiante debe poder construir y explicar:

    imagen → Base64 + mensaje multimodal → modelo de visión con LangChain
    → salida estructurada Pydantic → validación y métricas
    → aceptar o enviar a revisión humana

También debe distinguir cuándo conviene OCR y cuándo visión multimodal, y entender por qué se usan golden cases y datos sintéticos.

## Antes de entrar al aula

Desde la raíz AI_ENGINEERING_M4 verificar:

1. Existe .env con OPENAI_API_KEY. La demo alternativa requiere GEMINI_API_KEY.
2. El entorno virtual está instalado.
3. En PowerShell usar este intérprete; no usar py si Windows no tiene el launcher.

    .\.venv\Scripts\python.exe --version
    .\.venv\Scripts\python.exe .\03_extras\L1_vision_e_imagenes\resumen\08_golden_case_formulario.py

Los ejercicios con GPT-4o o Gemini realizan llamadas reales. Ejecutar cada demo una vez y reutilizar la salida al explicarla.

## Mapa de recursos

| Tema | Archivo | Qué muestra |
| --- | --- | --- |
| Imagen a datos | 00_formulario_openai.py | Visión con GPT-4o, LangChain y Pydantic. |
| Otro proveedor | 01_formulario_gemini.py | La misma idea con Gemini. |
| OCR frente a visión | 02_revision_visual.py | Texto, estructura y contexto no son lo mismo. |
| Estado explícito | 03_flujo_langgraph.py | Flujo visual en LangGraph. |
| Agente visual | 04_agente_respuesta_visual.py | Agente LangChain que responde sobre una imagen. |
| Routing | 05_routing_langgraph.py | Decisión de ruta según documento. |
| Calidad documental | 06_agente_documentos_danados_langchain.py | Formulario limpio, borroso, roto y manchado. |
| Calidad con grafo | 07_agente_documentos_danados_langgraph.py | El mismo caso como nodos y estado. |
| Golden case | 08_golden_case_formulario.py | Medición contra la respuesta esperada. |
| Schema robusto | 09_validacion_pydantic_detallada.py | Descriptions, normalización y reglas entre campos. |
| Datos sintéticos | 10_generar_formulario_sintetico.py | Formulario ficticio generado para practicar. |
| Tres documentos | 11_agente_tres_tipos_documentales.py | Factura, libro y adenda con un solo agente. |

Las imágenes están en 02_python_puro/AEM4_python_exercises/AEM4L1_vision_imagenes/data/.

## Guion de clase

### 0:00–0:15 — Apertura: qué es “ver”

Empezar preguntando: **“¿Qué debería devolver una IA al recibir una foto de un formulario?”** Anotar campos posibles: nombre, DNI, monto, fecha, firma y confianza.

Decir:

> Un modelo de visión no recibe solo caracteres. Puede relacionar texto, posición, casilleros, tablas, firmas y calidad visual. Pero una primera respuesta nunca debe convertirse sola en una decisión de negocio.

Presentar el flujo: imagen → modelo de visión → contrato Pydantic → validación → revisión humana.

### 0:15–0:40 — Primera demo: imagen a JSON

Ejecutar 00_formulario_openai.py. Mostrar el archivo de arriba hacia abajo:

1. load_dotenv() carga la clave una vez desde la raíz.
2. La imagen se prepara en Base64.
3. HumanMessage combina la consigna y la imagen.
4. ChatOpenAI es el wrapper de LangChain.
5. Pydantic convierte la respuesta en datos verificables.

Si existe la clave, ejecutar 01_formulario_gemini.py. La intención no es competir proveedores: LangChain permite cambiar el modelo conservando el mismo contrato de salida.

Preguntar:

- ¿Qué parte conoce la imagen y cuál la regla de negocio?
- ¿Por qué una salida libre es menos segura que un schema?
- ¿Qué hacemos si una firma no se distingue?

### 0:40–1:05 — OCR versus visión

Abrir 02_revision_visual.py. OCR es muy bueno para recuperar caracteres en documentos limpios y previsibles. La visión multimodal es útil cuando importa el contexto: tablas, casilleros, firmas, sellos, tachaduras, café sobre el papel o una pregunta de negocio.

No presentar visión como reemplazo total de OCR. En un producto real pueden trabajar juntos: OCR recupera texto económico y visión revisa layout o casos difíciles.

Mostrar una imagen limpia y una manchada. Antes de ejecutar, pedir que predigan qué campos serán inciertos.

### 1:05–1:30 — Pydantic: el contrato de datos

Ejecutar 09_validacion_pydantic_detallada.py. Detenerse en:

- Tipos: monto numérico, fecha válida y firma booleana.
- Field(description=...): las descriptions guían al modelo sobre qué identificar.
- Normalización: un DNI puede venir con puntos, pero se guarda consistente.
- Reglas cruzadas: una aceptación debe ser compatible con la calidad del documento.
- model_validate(): frontera final antes de utilizar datos en el negocio.

Decir:

> Pydantic no hace que el modelo vea mejor. Impide que una respuesta ambigua o mal formada llegue silenciosamente a una decisión real.

Actividad corta: agregar un campo email opcional y decidir si su ausencia bloquea el formulario o solo requiere revisión.

### 1:30–1:45 — Pausa y repaso

Pedir que dibujen el flujo sin mirar el código. Corregir la confusión más habitual: LangChain orquesta mensajes y modelos; Pydantic valida la salida; ninguno reemplaza al modelo de visión.

### 1:45–2:10 — Calidad y revisión humana

Ejecutar 06_agente_documentos_danados_langchain.py. Trabajar los cuatro escenarios: limpio, borroso, roto y manchado.

La meta no es que el agente sea infalible. La meta es que declare incertidumbre y escale el caso cuando corresponde.

Luego abrir 07_agente_documentos_danados_langgraph.py:

- LangChain alcanza para una consulta o agente simple.
- LangGraph conviene cuando se quieren ver estado, routing, reintentos y pasos explícitos.

Si falta tiempo, ejecutar solo LangChain y leer LangGraph como diagrama de flujo.

### 2:10–2:30 — Golden cases: demostrar calidad

Ejecutar 08_golden_case_formulario.py. Antes de mostrar el resultado, explicar el ground truth: ya se sabe qué valor correcto tiene cada campo del formulario limpio. El script compara la extracción con ese valor y mide precisión por campo.

Ideas clave:

- Una respuesta linda no demuestra calidad.
- Un golden case posee una entrada conocida y una salida esperada explícita.
- Deben existir casos estándar, variantes y casos de borde.
- Medir por campo deja detectar errores de fechas, montos o identificadores.

Preguntar: si el resultado fuera 5/6, ¿se despliega? Responder: depende del campo fallado y su riesgo; no solo del promedio.

### 2:30–2:45 — Un agente ante documentos distintos

Ejecutar 11_agente_tres_tipos_documentales.py. Lee y clasifica una factura, una página de libro y una adenda contractual.

| Documento | Datos que importan |
| --- | --- |
| Factura | Emisor, número, fecha y total. |
| Libro | Título, capítulo, página y contenido. |
| Adenda | Contrato, monto y vigencia modificados. |

Explicar que no hay tres aplicaciones: existe un schema común con tipo, título, identificador, datos clave, resumen y confianza.

### 2:45–3:00 — Datos sintéticos y cierre

Mostrar 10_generar_formulario_sintetico.py. El objetivo es ampliar la práctica sin usar documentos personales reales.

Aclarar:

- Los datos sintéticos deben identificarse como ficticios.
- No sustituyen toda la diversidad de documentos reales.
- Nunca se imprimen claves ni documentos sensibles en logs productivos.

Cerrar con el recorrido: **ver → estructurar → validar → medir → decidir → mejorar**.

## Tres actividades prácticas

### 1. Contrato robusto

Desde 09_validacion_pydantic_detallada.py, agregar un campo con una regla de validación. Entregar entrada válida, inválida y una explicación de la description para la IA.

### 2. Calidad documental

Desde 06_agente_documentos_danados_langchain.py, cambiar el umbral de aceptación y justificar qué caso se acepta, cuál se escala y a qué persona o área.

### 3. Nuevo tipo documental

Desde 11_agente_tres_tipos_documentales.py, proponer recibo, certificado, orden de compra o DNI ficticio. Definir datos clave, adaptar el schema y escribir el expected output.

## Entrega mínima

1. Una imagen ficticia o autorizada.
2. Un modelo Pydantic con tipos, descriptions y una regla.
3. Un script LangChain que imprima la salida validada.
4. Un golden case con resultado esperado y métrica por campo.
5. Una regla de revisión humana para datos inciertos.

## Corrección rápida

| Criterio | Evidencia |
| --- | --- |
| Visión multimodal | La imagen se envía y se extrae información pertinente. |
| Pydantic | Hay tipos, descriptions y validación real. |
| Calidad | Indica qué hacer con imagen ilegible o dato ausente. |
| Evaluación | Incluye expected output y una métrica. |
| Explicación | Distingue OCR, visión, LangChain, LangGraph y Pydantic. |
| Seguridad | No usa datos sensibles sin autorización ni expone claves. |

## Problemas frecuentes

| Problema | Resolución |
| --- | --- |
| py no se reconoce | Usar .\.venv\Scripts\python.exe archivo.py. |
| Error de API key | Revisar el .env de la raíz y OPENAI_API_KEY. Abrir otra terminal antes de reintentar. |
| Gemini pide key | Agregar GEMINI_API_KEY o usar la demo de OpenAI. |
| No encuentra imagen | Ejecutar desde la raíz y no mover data/. |
| Resultado dudoso | Marcar revisión humana y guardar el caso para evaluar; no corregirlo a mano. |
| La salida cambia | Usar temperatura baja, schema y golden cases para medir. |

## Mensaje de cierre

Un proyecto de visión no termina cuando el modelo reconoce una imagen. Recién empieza cuando esa respuesta se puede validar, medir, explicar y tratar con seguridad ante la incertidumbre.

