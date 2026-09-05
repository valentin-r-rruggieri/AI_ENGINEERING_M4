# 06 — Agente que compara perfiles de serving

## Idea central

Este caso compara tres perfiles de carga —prototipo, API de equipo y servicio público— para enseñar que el despliegue depende de tráfico, latencia, réplicas y observabilidad.

```mermaid
flowchart LR
    A[Perfil de carga] --> B[Agente LangChain]
    B --> C[DecisionDespliegue]
    C --> D[Local / Docker / Kubernetes]
```

## Recorrido del código

`perfiles` contiene inputs de dificultad creciente. El schema `DecisionDespliegue` estandariza la comparación: perfil, destino, réplicas, observabilidad y motivo. `Field(ge=1)` impide una propuesta de cero réplicas.

El prompt ofrece una política docente explícita: poco tráfico → local; tráfico moderado → Docker; alto tráfico y baja latencia → Kubernetes. El agente justifica, pero la política debería estar versionada como regla o herramienta en un sistema real.

| Perfil | Señal | Resultado esperado para debate |
|---|---|---|
| Prototipo local | 2 rpm, tolerante | Desarrollo local. |
| API de equipo | 40 rpm | Contenedor reproducible. |
| Servicio público | 300 rpm, 500 ms | Escalado y observabilidad. |

## Práctica

Cambiá la API de equipo a 200 rpm. Pedí justificar si debe cambiar destino, réplicas o ambos. Después preguntá qué métricas faltan: CPU, memoria, tamaño de modelo, errores y costo.
