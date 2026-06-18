"""
Genera archivos de audio hablados para AEM4L2.

Este script crea 3 archivos .wav con voz sintetica real usando el TTS local
de macOS (`say`) y los convierte a WAV con `afconvert`.

Tambien crea variantes degradadas de esos mismos audios para comparar como
cambia la transcripcion cuando hay ruido, velocidad alta, cortes o pausas.

Archivos:
  llamada_soporte.wav       -> reclamo de entrega no recibida
  indicacion_medica.wav     -> indicacion medica dictada
  reunion_equipo.wav        -> resumen de reunion de equipo

Variantes por cada audio base:
  *_ruido.wav          -> mismo contenido con ruido blanco de fondo
  *_rapido.wav         -> mismo contenido reproducido mas rapido
  *_entrecortado.wav   -> mismo contenido con microcortes/silencios
  *_pausas.wav         -> mismo contenido con pausas largas insertadas
  *_mal_estado.wav     -> ruido + volumen bajo + cortes, caso dificil

Ejecutar desde la raiz del repo:
    python3 python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/generate_audio.py
"""

from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
import wave
from array import array
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts"
MANIFEST_PATH = OUTPUT_DIR / "audio_variants_manifest.json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Voz en espanol disponible en macOS. Si no existe, el script busca otra voz
# espanola instalada y, como ultimo recurso, usa la voz default del sistema.
PREFERRED_VOICE = "Mónica"
SAMPLE_RATE = 22050
SAMPLE_WIDTH_BYTES = 2
MAX_INT16 = 32767
MIN_INT16 = -32768

# Transcripciones de referencia. Son el ground truth que usamos para medir WER.
TRANSCRIPTS = {
    "llamada_soporte": (
        "Hola, buenos días. Llamo porque el pedido número cuatro cinco dos uno no llegó. "
        "Lo necesitaba para hoy y es muy urgente. Quiero saber si pueden enviarlo urgente "
        "o si tienen que cancelar la compra. Por favor, necesito una solución rápida."
    ),
    "indicacion_medica": (
        "El paciente debe tomar la medicación cada ocho horas durante siete días. "
        "La dosis es de quinientos miligramos. No superar los tres gramos diarios. "
        "En caso de reacción adversa, suspender inmediatamente y consultar al médico."
    ),
    "reunion_equipo": (
        "En la reunión de hoy acordamos que el sprint termina el viernes. "
        "Los tres puntos principales son: primero, revisar los pull requests pendientes. "
        "Segundo, actualizar la documentación de la API. "
        "Tercero, coordinar con el equipo de diseño los nuevos mockups para el dashboard."
    ),
}


def clamp_int16(value: float) -> int:
    # WAV PCM de 16 bits solo permite valores entre -32768 y 32767.
    return max(MIN_INT16, min(MAX_INT16, int(value)))


def require_command(command: str) -> str:
    # Falla temprano con un mensaje claro si falta una herramienta de macOS.
    path = shutil.which(command)
    if path is None:
        raise RuntimeError(f"No encontre `{command}`. En macOS deberia venir instalado.")
    return path


def available_spanish_voice() -> str | None:
    # `say -v ?` lista voces. Buscamos una voz espanola instalada.
    result = subprocess.run(
        ["say", "-v", "?"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    voices = result.stdout.splitlines()
    if any(line.startswith(PREFERRED_VOICE) for line in voices):
        return PREFERRED_VOICE
    for line in voices:
        if "es_ES" in line or "es_MX" in line or "Español" in line:
            return line.split()[0]
    return None


def synthesize_with_macos_say(text: str, wav_path: Path, voice: str | None) -> None:
    # `say` produce AIFF. Luego `afconvert` lo convierte a WAV PCM 16-bit mono.
    aiff_path = wav_path.with_suffix(".aiff")
    say_cmd = ["say"]
    if voice:
        say_cmd.extend(["-v", voice])
    say_cmd.extend(["-o", str(aiff_path), text])
    subprocess.run(say_cmd, check=True)

    subprocess.run(
        [
            "afconvert",
            "-f",
            "WAVE",
            "-d",
            f"LEI16@{SAMPLE_RATE}",
            str(aiff_path),
            str(wav_path),
        ],
        check=True,
    )
    aiff_path.unlink(missing_ok=True)


def read_wav_samples(path: Path) -> tuple[array, int]:
    # Leemos WAV mono PCM 16-bit como array de enteros para poder degradarlo.
    with wave.open(str(path), "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != SAMPLE_WIDTH_BYTES:
            raise RuntimeError(f"{path.name} debe ser WAV mono PCM 16-bit")
        sample_rate = wav.getframerate()
        samples = array("h")
        samples.frombytes(wav.readframes(wav.getnframes()))
    return samples, sample_rate


def write_wav_samples(path: Path, samples: array, sample_rate: int) -> None:
    # Escribimos el resultado conservando mono PCM 16-bit.
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(SAMPLE_WIDTH_BYTES)
        wav.setframerate(sample_rate)
        wav.writeframes(samples.tobytes())


def wav_frame_count(path: Path) -> int:
    # Valida que el WAV tenga audio real y no solo headers vacios.
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes()


def add_background_noise(samples: array, intensity: float = 0.12, seed: int = 7) -> array:
    # Ruido blanco deterministico: suficiente para clase y reproducible entre corridas.
    rng = random.Random(seed)
    noisy = array("h")
    for sample in samples:
        noise = rng.uniform(-MAX_INT16 * intensity, MAX_INT16 * intensity)
        noisy.append(clamp_int16(sample + noise))
    return noisy


def speed_up(samples: array, factor: float = 1.45) -> array:
    # Acelera el audio tomando muestras a saltos. Cambia duracion y pitch,
    # que es util para demostrar que hablar rapido degrada el ASR.
    if factor <= 1:
        return samples
    fast = array("h")
    output_length = int(len(samples) / factor)
    for i in range(output_length):
        source_index = min(len(samples) - 1, int(i * factor))
        fast.append(samples[source_index])
    return fast


def insert_long_pauses(samples: array, sample_rate: int) -> array:
    # Inserta silencios largos cada pocos segundos para simular habla pausada
    # o cortes de llamada donde el audio queda mudo.
    chunk_size = int(sample_rate * 2.4)
    pause_size = int(sample_rate * 0.75)
    silence = array("h", [0]) * pause_size
    output = array("h")
    for start in range(0, len(samples), chunk_size):
        output.extend(samples[start : start + chunk_size])
        if start + chunk_size < len(samples):
            output.extend(silence)
    return output


def add_dropouts(samples: array, sample_rate: int) -> array:
    # Reemplaza pequenos tramos por silencio: simula audio entrecortado,
    # paquetes perdidos o microcortes de una llamada.
    output = array("h", samples)
    interval = int(sample_rate * 0.9)
    dropout = int(sample_rate * 0.16)
    for start in range(interval, len(output), interval):
        for i in range(start, min(start + dropout, len(output))):
            output[i] = 0
    return output


def make_bad_condition(samples: array, sample_rate: int, seed: int) -> array:
    # Caso combinado: baja volumen, agrega ruido y mete cortes cortos. Es el
    # audio "peor estado" para mostrar que el pipeline deberia pedir revision.
    lowered = array("h", [clamp_int16(sample * 0.55) for sample in samples])
    noisy = add_background_noise(lowered, intensity=0.18, seed=seed)
    return add_dropouts(noisy, sample_rate)


def create_audio_variants(base_name: str, wav_path: Path) -> list[dict[str, str]]:
    samples, sample_rate = read_wav_samples(wav_path)
    variants: list[tuple[str, str, array]] = [
        (
            "ruido",
            "Mismo contenido con ruido blanco de fondo.",
            add_background_noise(samples, intensity=0.12, seed=len(base_name)),
        ),
        (
            "rapido",
            "Mismo contenido acelerado para simular habla muy rapida.",
            speed_up(samples, factor=1.45),
        ),
        (
            "entrecortado",
            "Mismo contenido con microcortes y silencios cortos.",
            add_dropouts(samples, sample_rate),
        ),
        (
            "pausas",
            "Mismo contenido con pausas largas insertadas.",
            insert_long_pauses(samples, sample_rate),
        ),
        (
            "mal_estado",
            "Ruido, volumen bajo y cortes combinados.",
            make_bad_condition(samples, sample_rate, seed=len(base_name) * 3),
        ),
    ]

    manifest_entries: list[dict[str, str]] = []
    for suffix, description, variant_samples in variants:
        variant_name = f"{base_name}_{suffix}.wav"
        variant_path = OUTPUT_DIR / variant_name
        write_wav_samples(variant_path, variant_samples, sample_rate)
        manifest_entries.append(
            {
                "file": variant_name,
                "base_audio": wav_path.name,
                "reference_transcript": f"transcripts/{base_name}_reference.txt",
                "problem": suffix,
                "description": description,
            }
        )
    return manifest_entries


def main() -> None:
    require_command("say")
    require_command("afconvert")
    voice = available_spanish_voice()

    print("Generando audios hablados de ejemplo...")
    print(f"Voz TTS: {voice or 'default del sistema'}")

    manifest: list[dict[str, str]] = []

    for name, transcript in TRANSCRIPTS.items():
        wav_path = OUTPUT_DIR / f"{name}.wav"
        txt_path = TRANSCRIPTS_DIR / f"{name}_reference.txt"

        if wav_path.exists() and wav_frame_count(wav_path) > 0:
            print(f"  REUSE {wav_path.name} (audio base ya existe)")
        else:
            synthesize_with_macos_say(transcript, wav_path, voice)
            if wav_frame_count(wav_path) == 0:
                raise RuntimeError(
                    f"`say` genero {wav_path.name} sin audio. "
                    "Conserva/restaura el WAV base antes de crear variantes."
                )
        txt_path.write_text(transcript, encoding="utf-8")

        size_kb = wav_path.stat().st_size // 1024
        print(f"  OK {wav_path.name} ({size_kb} KB)")
        print(f"  OK transcripts/{txt_path.name}")

        variant_entries = create_audio_variants(name, wav_path)
        manifest.extend(variant_entries)
        for entry in variant_entries:
            variant_path = OUTPUT_DIR / entry["file"]
            size_kb = math.ceil(variant_path.stat().st_size / 1024)
            print(f"  OK {entry['file']} ({size_kb} KB) - {entry['problem']}")

    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "nota": (
                    "Todas las variantes usan el mismo transcript de referencia "
                    "del audio base. Cambia solo AUDIO_PATH para comparar ASR/WER."
                ),
                "variants": manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  OK {MANIFEST_PATH.name}")

    print(f"\nArchivos guardados en: {OUTPUT_DIR}")
    print(
        "\nNOTA:\n"
        "  Los WAV base contienen voz sintetica hablada.\n"
        "  Las variantes degradadas permiten probar ruido, velocidad, pausas y cortes.\n"
        "  Los .txt son referencias humanas para calcular WER.\n"
        "  Si queres usar llamadas reales, reemplaza los WAV y actualiza su transcript de referencia.\n"
    )


if __name__ == "__main__":
    main()
