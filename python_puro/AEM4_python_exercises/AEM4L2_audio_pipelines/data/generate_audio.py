"""
Genera archivos de audio hablados para AEM4L2.

Este script crea 3 archivos .wav con voz sintetica real usando el TTS local
de macOS (`say`) y los convierte a WAV con `afconvert`.

No genera tonos ni ruido: los audios contienen las frases de los transcripts.

Archivos:
  llamada_soporte.wav       -> reclamo de entrega no recibida
  indicacion_medica.wav     -> indicacion medica dictada
  reunion_equipo.wav        -> resumen de reunion de equipo

Ejecutar desde la raiz del repo:
    python3 python_puro/AEM4_python_exercises/AEM4L2_audio_pipelines/data/generate_audio.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Voz en espanol disponible en macOS. Si no existe, el script busca otra voz
# espanola instalada y, como ultimo recurso, usa la voz default del sistema.
PREFERRED_VOICE = "Mónica"
SAMPLE_RATE = 22050

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


def main() -> None:
    require_command("say")
    require_command("afconvert")
    voice = available_spanish_voice()

    print("Generando audios hablados de ejemplo...")
    print(f"Voz TTS: {voice or 'default del sistema'}")

    for name, transcript in TRANSCRIPTS.items():
        wav_path = OUTPUT_DIR / f"{name}.wav"
        txt_path = TRANSCRIPTS_DIR / f"{name}_reference.txt"

        synthesize_with_macos_say(transcript, wav_path, voice)
        txt_path.write_text(transcript, encoding="utf-8")

        size_kb = wav_path.stat().st_size // 1024
        print(f"  OK {wav_path.name} ({size_kb} KB)")
        print(f"  OK transcripts/{txt_path.name}")

    print(f"\nArchivos guardados en: {OUTPUT_DIR}")
    print(
        "\nNOTA:\n"
        "  Los WAV ahora contienen voz sintetica hablada, no tonos ni ruido.\n"
        "  Los .txt son referencias humanas para calcular WER.\n"
        "  Si queres usar llamadas reales, reemplaza los WAV y actualiza su transcript de referencia.\n"
    )


if __name__ == "__main__":
    main()
