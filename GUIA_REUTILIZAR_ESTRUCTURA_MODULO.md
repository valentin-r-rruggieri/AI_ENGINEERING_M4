# Guia para reutilizar la estructura del modulo

Este documento resume que se hizo en este proyecto, cual era el objetivo pedagogico
y como se puede replicar la misma forma de trabajo en otras lectures, otros modulos
o proyectos integradores.

La idea no fue solamente crear archivos sueltos. El objetivo fue construir un
sistema de materiales de clase que sea ordenado, ejecutable, facil de explicar y
facil de mantener.

---

## Objetivo principal

El objetivo del proyecto fue transformar el Modulo 4 de AI Engineering en un
conjunto de materiales didacticos completos, con tres niveles bien separados:

1. Notebooks para explicar y estudiar los conceptos en clase.
2. Ejercicios de Python puro para practicar con scripts ejecutables.
3. Un proyecto integrador para unir los temas del modulo en un caso mas cercano
   a produccion.

Esta separacion permite usar el mismo contenido de distintas formas:

- En clase, con notebooks guiados y explicaciones paso a paso.
- En practica, con archivos `.py` que el alumno puede correr, modificar y depurar.
- En evaluacion o cierre, con un proyecto integrador que combina varias piezas del
  modulo.

---

## Que se hizo

Se organizo el repositorio con una estructura clara por tipo de material:

```text
AI_ENGINEERING_M4/
+-- README.md
+-- notebooks/
+-- python_puro/
|   +-- AEM4_python_exercises/
+-- proyecto_integrador/
```

Cada carpeta cumple un rol distinto.

### 1. Notebooks por lecture

La carpeta `notebooks/` contiene una carpeta por lecture:

```text
notebooks/
+-- AEM4L1_IA_que_ve_y_crea_vision_e_imagenes/
+-- AEM4L2_Introduccion_a_audio_pipelines/
+-- AEM4L3_Introduccion_a_los_MCP/
+-- AEM4L4_Fundamentos_teoricos_y_arquitectura/
+-- AEM4L5_Arquitecturas_avanzadas_de_adaptacion/
```

La funcion de los notebooks es explicar. Por eso deben ser autocontenidos,
progresivos y pensados para que un alumno pueda seguir el razonamiento sin
necesitar mirar primero el codigo final.

Cada notebook deberia incluir:

1. Titulo y objetivo.
2. Contexto conceptual.
3. Glosario o conceptos clave.
4. Ejemplo minimo.
5. Explicacion paso a paso.
6. Codigo ejecutable.
7. Preguntas o mini desafio.
8. Errores comunes.
9. Cierre con criterio de uso real.

En lectures teoricas, como fundamentos de transformers o arquitectura, se priorizo
que el notebook explique el concepto antes de mostrar codigo. En lectures mas
practicas, se priorizo que el codigo sea simple, ejecutable y facil de modificar.

### 2. Ejercicios de Python puro

La carpeta `python_puro/AEM4_python_exercises/` contiene scripts `.py` separados
por lecture:

```text
python_puro/AEM4_python_exercises/
+-- requirements.txt
+-- common.py
+-- AEM4L1_vision_imagenes/
+-- AEM4L2_audio_pipelines/
+-- AEM4L3_mcp/
+-- AEM4L4_fundamentos_arquitectura/
+-- AEM4L5_adaptacion_serving/
```

La funcion de estos archivos es practicar. A diferencia de los notebooks, los
scripts tienen que poder correrse desde terminal y mostrar un flujo concreto.

La estructura pedagogica recomendada para cada `.py` es:

1. Presentar una version basica que funciona pero tiene limitaciones.
2. Mostrar cual es el problema.
3. Implementar una version mas robusta.
4. Comparar antes y despues.
5. Dejar un desafio para que el alumno complete o mejore.

Ejemplo de progresion:

```text
Esto funciona
-> pero falla en este caso
-> entonces agregamos validacion / profiling / async / schema / trazabilidad
-> ahora el resultado es mas confiable
```

Esta logica evita que el alumno reciba la solucion como una caja negra. Primero ve
el problema, despues entiende por que se necesita la herramienta.

### 3. Datos locales y generadores

Se incorporaron carpetas `data/` y scripts `generate_data.py` para crear datasets,
imagenes, audios o JSON esperados desde el propio repositorio.

Esto es importante porque los ejercicios no deben depender de archivos externos
dificiles de recuperar.

Patron recomendado:

```text
AEMXLn_nombre/
+-- e01_*.py
+-- e02_*.py
+-- data/
|   +-- generate_data.py
|   +-- archivo_de_prueba.ext
|   +-- expected/
|       +-- caso_esperado.json
+-- README.md
```

Cuando un ejercicio evalua calidad, conviene agregar golden cases:

- Inputs conocidos.
- Salida esperada.
- Comparacion automatica o semi-automatica.
- Mensaje claro cuando algo no coincide.

### 4. Demos visuales para terminal

En AEM4L5 se agrego una carpeta de demos con `rich`:

```text
python_puro/AEM4_python_exercises/AEM4L5_adaptacion_serving/demos_rich/
```

Estos scripts no reemplazan los ejercicios principales. Sirven para mostrar en vivo
conceptos como LoRA, serverless, profiling o async con una salida mas visual en la
terminal.

Regla para este tipo de demos:

- Deben ser simulados si el objetivo es explicar el concepto.
- No deben requerir API key ni GPU si son para mostrar en clase.
- Deben correr rapido.
- Deben tener README propio.
- Todas las dependencias necesarias deben estar declaradas en `requirements.txt`.

### 5. Proyecto integrador

El proyecto integrador vive separado:

```text
proyecto_integrador/
+-- README.md
+-- requirements.txt
+-- src/
+-- data/
```

La funcion del proyecto integrador es mostrar como se conectan los temas del modulo
en un flujo mas profesional.

En este modulo, el proyecto integrador se organizo como un pipeline con:

- Parsing multimodal.
- Agentes o componentes separados.
- Validacion con Pydantic.
- Trazabilidad.
- Datos de prueba.
- Golden cases.
- README orientado a ejecucion y defensa.

Para otros modulos, el proyecto integrador deberia seguir la misma logica:

1. Caso de negocio o problema concreto.
2. Entrada clara.
3. Pipeline modular.
4. Salida estructurada.
5. Validacion.
6. Observabilidad o logs.
7. Datos de prueba reproducibles.
8. Guia de ejecucion.

---

## Como replicarlo en otra lecture

Para crear una nueva lecture con esta misma metodologia, usar este checklist.

### Paso 1: definir el objetivo de aprendizaje

Antes de crear archivos, definir:

- Que concepto se quiere ensenar.
- Que problema real representa.
- Que herramienta o tecnica se introduce.
- Que deberia poder explicar el alumno al final.

Ejemplo:

```text
Lecture: Evaluacion de agentes
Objetivo: que el alumno entienda por que no alcanza con mirar una respuesta bonita.
Herramienta: golden cases, rubricas y evaluacion automatica.
Resultado esperado: un script que compara outputs contra criterios definidos.
```

### Paso 2: crear la carpeta del notebook

```text
notebooks/AEMXLn_nombre_de_la_lecture/
+-- README.md
+-- E01_resuelto_*.ipynb
+-- E02_resuelto_*.ipynb
+-- E03_resuelto_*.ipynb
+-- E04_resuelto_*.ipynb
+-- E05_para_resolver_*.ipynb
+-- E06_para_resolver_*.ipynb
+-- E07_inicial_*.ipynb
+-- E08_avanzado_*.ipynb
```

La progresion sugerida es:

| Orden | Tipo | Uso |
|---|---|---|
| E01 | Resuelto | Concepto base |
| E02 | Resuelto | Segundo bloque conceptual |
| E03 | Resuelto | Implementacion guiada |
| E04 | Resuelto | Mini integrador |
| E05 | Para resolver | Practica moderada |
| E06 | Para resolver | Practica desafiante |
| E07 | Inicial | Warm-up simple |
| E08 | Avanzado | Cierre de la lecture |

### Paso 3: crear la carpeta de Python puro

```text
python_puro/AEMX_python_exercises/AEMXLn_nombre/
+-- README.md
+-- e01_*.py
+-- e02_*.py
+-- e03_*.py
+-- e04_integrador_*.py
+-- data/
    +-- generate_data.py
```

Cada script deberia poder ejecutarse de forma directa:

```powershell
.\.venv\Scripts\python.exe python_puro\AEMX_python_exercises\AEMXLn_nombre\e01_nombre.py
```

### Paso 4: documentar comandos exactos

El README de cada lecture debe incluir:

- Que aprende el alumno.
- Que archivos correr.
- En que orden correrlos.
- Que variables de entorno hacen falta.
- Si requiere API real o si es simulado.
- Como regenerar datos.
- Como validar que todo funciona.

### Paso 5: agregar validacion minima

Antes de dar por cerrada una lecture, validar:

```powershell
.\.venv\Scripts\python.exe -m compileall python_puro\AEMX_python_exercises
```

Y ejecutar al menos:

- Un script simple.
- Un script integrador.
- El generador de datos, si existe.
- Un caso con golden expected, si existe.

---

## Criterios de calidad

Para que el material sirva en otro modulo, deberia cumplir estos criterios:

- La estructura se entiende mirando carpetas y nombres.
- Cada lecture tiene README propio.
- Los notebooks explican antes de mostrar codigo complejo.
- Los `.py` se pueden correr desde terminal.
- Los datos se pueden regenerar.
- Las dependencias estan declaradas.
- No hay claves ni secretos hardcodeados.
- Si hay API real, se aclara explicitamente.
- Si hay modo simulado, se aclara explicitamente.
- Los errores esperados aparecen explicados para el alumno.
- El proyecto integrador esta separado de los ejercicios de clase.

---

## Plantilla rapida para otro modulo

```text
AI_ENGINEERING_MX/
+-- README.md
+-- notebooks/
|   +-- AEMXL1_nombre/
|   +-- AEMXL2_nombre/
|   +-- AEMXL3_nombre/
|   +-- AEMXL4_nombre/
|   +-- AEMXL5_nombre/
+-- python_puro/
|   +-- AEMX_python_exercises/
|       +-- README.md
|       +-- requirements.txt
|       +-- common.py
|       +-- AEMXL1_nombre/
|       +-- AEMXL2_nombre/
|       +-- AEMXL3_nombre/
|       +-- AEMXL4_nombre/
|       +-- AEMXL5_nombre/
+-- proyecto_integrador/
    +-- README.md
    +-- requirements.txt
    +-- src/
    +-- data/
```

---

## Instruccion para usar este documento con otro equipo o modulo

Cuando se quiera crear otro modulo, este documento se puede entregar como criterio
base. La consigna seria:

```text
Replicar la estructura pedagogica de AI_ENGINEERING_M4.

Para cada lecture:
- Crear notebooks autocontenidos y progresivos.
- Crear ejercicios Python puro ejecutables.
- Incluir README propio.
- Generar datos locales cuando haga falta.
- Separar demos visuales de ejercicios principales.
- Validar con compileall y ejecucion minima.

Para el proyecto integrador:
- Separarlo en una carpeta propia.
- Usar estructura src/.
- Incluir datos de prueba reproducibles.
- Documentar setup, uso, arquitectura y criterios de evaluacion.
```

El resultado esperado no es solo que "funcione". El resultado esperado es que sea
facil de ensenar, facil de ejecutar, facil de revisar y facil de adaptar a nuevas
lectures.
