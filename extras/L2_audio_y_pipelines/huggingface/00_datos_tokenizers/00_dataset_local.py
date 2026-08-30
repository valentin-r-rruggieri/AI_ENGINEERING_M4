# Este archivo forma parte del recorrido práctico de Hugging Face.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Carga de un CSV local con Datasets.

GUÍA DOCENTE
CUÁNDO USAR: para obtener una tabla preparada para map, split y Trainer.
DIFERENCIA: Dataset conserva schema y operaciones reproducibles.
EN CLASE: inspeccionar features, cantidad de filas y primer ejemplo.
"""

# Importa Path para localizar el CSV y load_dataset para leerlo.
from pathlib import Path
from datasets import load_dataset

# Construye la ruta al dataset pequeño incluido en esta tecnología.
ruta_csv = Path(__file__).resolve().parents[1] / "data/intenciones.csv"

# Carga el archivo como un split llamado train.
dataset = load_dataset("csv", data_files=str(ruta_csv), split="train")

# Muestra estructura y un caso para verificar la entrada.
print("Filas:", len(dataset))
print("Columnas:", dataset.column_names)
print("Primer caso:", dataset[0])

# Resumen final: este ejercicio convierte un CSV en Dataset.
# Agrega una fila al CSV y confirma que cambia la cantidad informada.
