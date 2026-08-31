# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Scheduler de difusión sin descargar un modelo pesado.

GUÍA DOCENTE
CUÁNDO USAR: para explicar cómo se agrega ruido durante el entrenamiento.
DIFERENCIA: el scheduler controla pasos; la red aprende a predecir el ruido.
EN CLASE: observar un solo paso antes de hablar de generación completa.
"""

# Importa PyTorch para crear una señal y Diffusers para el scheduler.
import torch
from diffusers import DDPMScheduler

# Simula un fragmento de audio muy corto con valores entre -1 y 1.
audio_limpio = torch.linspace(-1, 1, steps=16).reshape(1, 1, 16)
ruido = torch.randn_like(audio_limpio)

# Configura cien pasos y selecciona un instante intermedio.
scheduler = DDPMScheduler(num_train_timesteps=100)
instante = torch.tensor([50])
audio_ruidoso = scheduler.add_noise(audio_limpio, ruido, instante)

# Compara estadísticos sin ejecutar un modelo generativo pesado.
print("Media limpia:", round(audio_limpio.mean().item(), 3))
print("Media ruidosa:", round(audio_ruidoso.mean().item(), 3))
print("Shape:", tuple(audio_ruidoso.shape))

# Resumen final: este ejercicio muestra un paso directo de difusión.
# Cambia el instante a 10 y 90 y compara cuánto domina el ruido.
