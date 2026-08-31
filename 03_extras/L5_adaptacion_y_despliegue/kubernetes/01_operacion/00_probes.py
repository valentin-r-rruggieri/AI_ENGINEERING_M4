# Este archivo forma parte del recorrido práctico de Kubernetes.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Readiness y liveness probes.

GUÍA DOCENTE
CUÁNDO USAR: para separar disponibilidad para tráfico de salud del proceso.
DIFERENCIA: readiness retira tráfico; liveness puede reiniciar el contenedor.
EN CLASE: evitar una liveness demasiado agresiva durante la carga del modelo.
"""

# Importa Path y PyYAML para leer las probes.
from pathlib import Path
import yaml

# Obtiene la configuración del primer contenedor.
ruta = Path(__file__).resolve().parents[1] / "02_en_marcha/deployment.yaml"
deployment = yaml.safe_load(ruta.read_text(encoding="utf-8"))
contenedor = deployment["spec"]["template"]["spec"]["containers"][0]

# Extrae path, puerto y demora inicial de cada probe.
for nombre in ["readinessProbe", "livenessProbe"]:
    probe = contenedor[nombre]
    print(nombre, {
        "path": probe["httpGet"]["path"],
        "port": probe["httpGet"]["port"],
        "initialDelaySeconds": probe["initialDelaySeconds"],
    })

# Resumen final: este ejercicio compara readiness y liveness.
# Aumenta la demora de liveness para un modelo con carga lenta.
