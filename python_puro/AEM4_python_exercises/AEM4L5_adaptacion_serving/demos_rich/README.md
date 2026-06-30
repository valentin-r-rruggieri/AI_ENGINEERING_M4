# Demos de consola con `rich` — AEM4L5

Scripts **para mostrar en vivo en clase**, en la terminal, con colores, tablas,
paneles y spinners (`rich`). Son **simulados, sin API key ni GPU**: están pensados
para proyectar y explicar cada concepto mientras corren.

Complementan los notebooks teóricos de
`notebooks/AEM4L5_Arquitecturas_avanzadas_de_adaptacion/` (los notebooks son para
leer/estudiar; estos scripts son para la demo visual en consola).

## Scripts

| Script | Tema | Qué muestra |
|---|---|---|
| `demo_1_lora_peft.py` | LoRA / PEFT | Tabla comparativa, % de parámetros entrenables y ahorro de storage por cliente. |
| `demo_2_serverless_vs_server.py` | Despliegue | Cold start vs latencia estable (simulado) + función de decisión por caso. |
| `demo_3_cprofile.py` | Profiling | Hotspots con `cProfile` y comparación lento vs optimizado (speedup). |
| `demo_4_async_vs_secuencial.py` | Concurrencia | Barra de progreso y cronómetro: secuencial (~2.5 s) vs async (~0.5 s). |

## Cómo correrlos

```bash
# (Opcional) instalar rich si no lo tenés:
pip install rich

# Desde esta carpeta:
python demo_1_lora_peft.py
python demo_2_serverless_vs_server.py
python demo_3_cprofile.py
python demo_4_async_vs_secuencial.py
```

> Cada script fuerza la salida a UTF-8, así los emojis y tildes se ven bien en
> cualquier terminal de Windows (cmd, PowerShell o la terminal de VS Code).

## Notas pedagógicas

- **demo_3** mide los tiempos **sin** el profiler para reportar el speedup real, y
  usa `cProfile` solo para la tabla de hotspots. Mensaje clave: *optimizar después
  de medir, y volver a medir*.
- **demo_4** usa `asyncio.run()` porque son scripts (no notebooks). En Jupyter/Colab
  se usaría `await main()`. El async solo acelera porque el cuello de botella es
  **espera (I/O)**, no cálculo (CPU).
- Los tiempos de **demo_2** están acelerados (factor `ACELERAR`) para no demorar la
  clase; las proporciones (cold start vs warm) se mantienen.
