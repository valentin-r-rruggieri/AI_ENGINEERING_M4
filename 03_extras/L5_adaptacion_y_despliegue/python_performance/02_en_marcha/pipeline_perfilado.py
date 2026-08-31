# Este archivo forma parte del recorrido práctico de rendimiento en Python.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Pipeline asíncrono medido y perfilado.

GUÍA DOCENTE
CUÁNDO USAR: para diagnosticar un flujo que combina CPU y esperas de red.
DIFERENCIA: perf_counter mide todo; cProfile detalla el trabajo de CPU.
EN CLASE: no confundir espera I/O con un cuello de botella de cálculo.
"""

# Importa asyncio, cProfile, io, pstats y time.
import asyncio
import cProfile
import io
import pstats
import time

# Simula una llamada externa con una espera breve.
async def llamar_agente(nombre: str, texto: str) -> str:
    await asyncio.sleep(0.1)
    return f"{nombre}: {texto.lower()}"

# Solapa los dos agentes y normaliza el resultado final.
async def ejecutar_pipeline() -> list[str]:
    resultados = await asyncio.gather(
        llamar_agente("contextualizador", "VIGENCIA"),
        llamar_agente("extractor", "CAMBIO DE PLAZO"),
    )
    return [resultado.strip() for resultado in resultados]

# Perfila y mide el flujo completo.
perfil = cProfile.Profile()
inicio = time.perf_counter()
perfil.enable()
salida_pipeline = asyncio.run(ejecutar_pipeline())
perfil.disable()
latencia_ms = (time.perf_counter() - inicio) * 1000

# Resume las funciones con mayor tiempo acumulado.
salida_perfil = io.StringIO()
pstats.Stats(perfil, stream=salida_perfil).sort_stats("cumulative").print_stats(6)
print(salida_pipeline)
print("Latencia ms:", round(latencia_ms, 2))
print(salida_perfil.getvalue())

# Resumen final: este pipeline combina concurrencia y diagnóstico.
# Ejecuta los agentes en secuencia y compara latencia y perfil.
