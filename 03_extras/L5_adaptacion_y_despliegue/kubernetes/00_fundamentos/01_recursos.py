# Este archivo forma parte del recorrido práctico de Kubernetes.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Requests y limits del contenedor.

GUÍA DOCENTE
CUÁNDO USAR: para reservar capacidad y limitar el consumo de cada Pod.
DIFERENCIA: request guía scheduling; limit establece el máximo permitido.
EN CLASE: discutir qué ocurre si el modelo necesita más memoria que el límite.
"""

# Importa Path y PyYAML para acceder a recursos del contenedor.
from pathlib import Path
import yaml

# Lee el manifiesto compartido con el integrador.
ruta = Path(__file__).resolve().parents[1] / "02_en_marcha/deployment.yaml"
deployment = yaml.safe_load(ruta.read_text(encoding="utf-8"))
contenedor = deployment["spec"]["template"]["spec"]["containers"][0]
recursos = contenedor["resources"]

# Muestra reserva y límite de CPU/memoria.
print("Requests:", recursos["requests"])
print("Limits:", recursos["limits"])

# Comprueba una regla pedagógica de memoria.
print("Memoria declarada:", "memory" in recursos["requests"] and "memory" in recursos["limits"])

# Resumen final: este ejercicio diferencia reserva y límite.
# Reduce el limit de memoria y analiza el riesgo de OOMKilled.
