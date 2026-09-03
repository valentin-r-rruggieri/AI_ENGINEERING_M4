# Este archivo forma parte del resumen integrador de audio y pipelines.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Benchmark de robustez: comparar Whisper ante audio normal, ruido y degradación.

GUÍA DOCENTE
CUÁNDO USAR: antes de desplegar ASR con condiciones de audio distintas.
DIFERENCIA: un caso aislado es una demo; varios casos comparables son una evaluación.
EN CLASE: anticipar qué variante tendrá mayor WER antes de ejecutar.
"""

# Carga una sola vez las credenciales compartidas del archivo .env de la raíz.
from dotenv import load_dotenv

load_dotenv()

# Importa Path, WER, OpenAI y Pydantic para medir tres archivos de forma uniforme.
from pathlib import Path

from jiwer import wer
from openai import OpenAI
from pydantic import BaseModel, Field


# Define el resultado de un archivo y el reporte conjunto del benchmark.
class CasoBenchmark(BaseModel):
    archivo: str
    wer: float = Field(ge=0)
    palabras_referencia: int = Field(ge=1)


class BenchmarkAudio(BaseModel):
    casos: list[CasoBenchmark] = Field(min_length=3)
    wer_promedio: float = Field(ge=0)
    peor_archivo: str


# Localiza el texto esperado y tres variantes de una misma llamada de soporte.
raiz = Path(__file__).resolve().parents[3]
carpeta_datos = raiz / "02_python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data"
referencia = (carpeta_datos / "transcripts/llamada_soporte_reference.txt").read_text(encoding="utf-8")
archivos = ["llamada_soporte.wav", "llamada_soporte_ruido.wav", "llamada_soporte_mal_estado.wav"]

# Ejecuta Whisper sobre cada variante y calcula WER contra la misma referencia humana.
cliente_audio = OpenAI()
casos_medidos: list[CasoBenchmark] = []

for nombre_archivo in archivos:
    with (carpeta_datos / nombre_archivo).open("rb") as archivo_audio:
        respuesta_asr = cliente_audio.audio.transcriptions.create(
            model="whisper-1",
            file=archivo_audio,
            language="es",
        )
    error_wer = round(wer(referencia.lower(), str(respuesta_asr.text).lower()), 3)
    casos_medidos.append(
        CasoBenchmark(
            archivo=nombre_archivo,
            wer=error_wer,
            palabras_referencia=len(referencia.split()),
        )
    )

# Resume la evaluación sin esconder el peor caso para la discusión docente.
reporte = BenchmarkAudio(
    casos=casos_medidos,
    wer_promedio=round(sum(caso.wer for caso in casos_medidos) / len(casos_medidos), 3),
    peor_archivo=max(casos_medidos, key=lambda caso: caso.wer).archivo,
)
print(reporte.model_dump())

# Resumen final: la calidad del ASR se mide contra variantes, no con un solo audio.
# Agregá llamada_soporte_rapido.wav y verificá cómo cambia el peor caso.

