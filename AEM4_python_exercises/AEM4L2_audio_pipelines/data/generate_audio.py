"""
Script de generación de archivos de audio de ejemplo para AEM4L2.

Crea 3 archivos .wav con tonos variados (simulan voces) + transcripciones de referencia.

  llamada_soporte.wav       → reclamo de entrega no recibida
  indicacion_medica.wav     → prescripción médica dictada
  reunion_equipo.wav        → resumen de reunión de equipo

Ejecutar con:
    python AEM4L2_audio_pipelines/data/generate_audio.py

Requiere: numpy, scipy (o solo wave de stdlib como fallback)
"""

import wave
import struct
import math
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 22050   # Hz — calidad suficiente para ASR

# Transcripciones de referencia (ground truth)
TRANSCRIPTS = {
    "llamada_soporte": (
        "Hola buenos días llamo porque el pedido número cuatro cinco dos uno no llegó "
        "lo necesitaba para hoy y es muy urgente quiero saber si pueden enviarlo urgente "
        "o si tienen que cancelar la compra por favor necesito una solución rápida"
    ),
    "indicacion_medica": (
        "El paciente debe tomar la medicación cada ocho horas durante siete días "
        "la dosis es de quinientos miligramos no superar los tres gramos diarios "
        "en caso de reacción adversa suspender inmediatamente y consultar al médico"
    ),
    "reunion_equipo": (
        "En la reunión de hoy acordamos que el sprint termina el viernes "
        "los tres puntos principales son primero revisar los pull requests pendientes "
        "segundo actualizar la documentación de la API "
        "tercero coordinar con el equipo de diseño los nuevos mockups para el dashboard"
    ),
}


def create_speech_like_wav(filename: Path, transcript: str, duration_s: float = 5.0) -> None:
    """
    Crea un archivo WAV con tonos variados que simulan patrones de habla.
    NO es voz real — es un placeholder válido para demostrar el pipeline.
    El transcript de referencia contiene el texto real.
    """
    n_samples = int(SAMPLE_RATE * duration_s)

    # Generar tonos variados que imitan la cadencia del habla
    words = transcript.split()
    samples = []

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Frecuencia base de voz (~150–300 Hz para habla masculina/femenina)
        word_idx = int(t / duration_s * len(words))
        # Variar la frecuencia por palabra para simular prosodia
        base_freq = 180 + (hash(words[min(word_idx, len(words) - 1)]) % 100)
        # Añadir armónicos para que suene más natural
        value = (
            0.5  * math.sin(2 * math.pi * base_freq * t) +
            0.25 * math.sin(2 * math.pi * base_freq * 2 * t) +
            0.15 * math.sin(2 * math.pi * base_freq * 3 * t)
        )
        # Envolvente de amplitud (ataque y decay suave)
        envelope = min(t / 0.1, 1.0) * min((duration_s - t) / 0.1, 1.0)
        value *= envelope * 0.6
        samples.append(int(32767 * value))

    with wave.open(str(filename), 'w') as f:
        f.setnchannels(1)     # mono
        f.setsampwidth(2)     # 16-bit PCM
        f.setframerate(SAMPLE_RATE)
        packed = struct.pack(f"<{len(samples)}h", *samples)
        f.writeframes(packed)


def main() -> None:
    print("Generando archivos de audio de ejemplo...")

    for name, transcript in TRANSCRIPTS.items():
        # Crear WAV
        wav_path = OUTPUT_DIR / f"{name}.wav"
        duration = max(4.0, len(transcript.split()) * 0.4)  # ~0.4s por palabra
        create_speech_like_wav(wav_path, transcript, duration_s=duration)
        print(f"  OK {wav_path.name}  ({duration:.1f}s, {len(transcript.split())} palabras)")

        # Guardar transcript de referencia
        txt_path = TRANSCRIPTS_DIR / f"{name}_reference.txt"
        txt_path.write_text(transcript, encoding="utf-8")
        print(f"  OK transcripts/{txt_path.name}")

    print(f"\nArchivos guardados en: {OUTPUT_DIR}")
    print("""
NOTA:
  Los archivos .wav contienen tonos sintéticos (no voz real).
  El pipeline ASR usa los archivos de referencia .txt como ground truth.
  Para audio real: reemplazá los .wav con grabaciones propias
  y actualizá los archivos de referencia con la transcripción correcta.
""")


if __name__ == "__main__":
    main()
