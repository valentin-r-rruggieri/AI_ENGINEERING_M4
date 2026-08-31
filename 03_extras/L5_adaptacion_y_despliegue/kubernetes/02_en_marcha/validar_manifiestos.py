# Este archivo forma parte del recorrido práctico de Kubernetes.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Validación local de Deployment y Service relacionados.

GUÍA DOCENTE
CUÁNDO USAR: antes de aplicar manifiestos a un clúster.
DIFERENCIA: esta validación didáctica no reemplaza kubectl dry-run.
EN CLASE: comprobar labels, selectors, ports y health checks.
"""

# Importa Path y PyYAML para cargar ambos manifiestos.
from pathlib import Path
import yaml

# Lee los YAML ubicados junto al script.
carpeta = Path(__file__).resolve().parent
deployment = yaml.safe_load((carpeta / "deployment.yaml").read_text(encoding="utf-8"))
service = yaml.safe_load((carpeta / "service.yaml").read_text(encoding="utf-8"))

# Obtiene etiquetas y puertos que deben coincidir.
labels_pod = deployment["spec"]["template"]["metadata"]["labels"]
selector_service = service["spec"]["selector"]
puerto_contenedor = deployment["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"]
target_port = service["spec"]["ports"][0]["targetPort"]

# Evalúa invariantes mínimas antes del despliegue.
validaciones = {
    "selector_coincide": selector_service.items() <= labels_pod.items(),
    "puerto_coincide": target_port == puerto_contenedor,
    "replicas_positivas": deployment["spec"]["replicas"] > 0,
}
print(validaciones)
print("Manifiestos coherentes:", all(validaciones.values()))

# Resumen final: este ejercicio comprueba la relación entre recursos Kubernetes.
# Cambia targetPort y observa qué validación detecta el error.
