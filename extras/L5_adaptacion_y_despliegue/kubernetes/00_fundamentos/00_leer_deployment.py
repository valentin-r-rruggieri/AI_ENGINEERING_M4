# Este archivo forma parte del recorrido práctico de Kubernetes.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Lectura de un Deployment desde YAML.

GUÍA DOCENTE
CUÁNDO USAR: para inspeccionar declarativamente cómo debe ejecutarse una aplicación.
DIFERENCIA: Deployment administra Pods; Service ofrece una dirección estable.
EN CLASE: localizar apiVersion, kind, metadata y spec.
"""

# Importa Path y PyYAML para leer el manifiesto.
from pathlib import Path
import yaml

# Localiza el Deployment final del recorrido.
ruta = Path(__file__).resolve().parents[1] / "02_en_marcha/deployment.yaml"
deployment = yaml.safe_load(ruta.read_text(encoding="utf-8"))

# Extrae los campos más importantes sin imprimir todo el documento.
resumen = {
    "kind": deployment["kind"],
    "nombre": deployment["metadata"]["name"],
    "replicas": deployment["spec"]["replicas"],
    "imagen": deployment["spec"]["template"]["spec"]["containers"][0]["image"],
}
print(resumen)

# Resumen final: este ejercicio inspecciona el estado deseado de la aplicación.
# Cambia replicas en el YAML y confirma que el resumen se actualiza.
