# Este archivo forma parte del recorrido práctico de OpenAI.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Cálculo pequeño de Word Error Rate.

GUÍA DOCENTE
CUÁNDO USAR: para medir una transcripción contra un texto de referencia.
DIFERENCIA: WER cuenta sustituciones, inserciones y eliminaciones de palabras.
EN CLASE: resolver primero el ejemplo a mano y luego ejecutar el algoritmo.
"""

# Define una referencia y una hipótesis con un error visible.
referencia = "tomar una tableta cada ocho horas".split()
hipotesis = "tomar una tableta cada seis horas".split()

# Crea la matriz utilizada por la distancia de edición.
filas = len(referencia) + 1
columnas = len(hipotesis) + 1
distancias = [[0] * columnas for _ in range(filas)]

# Inicializa los costos de eliminar o insertar todas las palabras.
for fila in range(filas):
    distancias[fila][0] = fila
for columna in range(columnas):
    distancias[0][columna] = columna

# Calcula el menor costo para transformar una frase en la otra.
for fila in range(1, filas):
    for columna in range(1, columnas):
        costo = 0 if referencia[fila - 1] == hipotesis[columna - 1] else 1
        distancias[fila][columna] = min(
            distancias[fila - 1][columna] + 1,
            distancias[fila][columna - 1] + 1,
            distancias[fila - 1][columna - 1] + costo,
        )

# Divide los errores por la cantidad de palabras de referencia.
errores = distancias[-1][-1]
wer = errores / len(referencia)
print({"errores": errores, "palabras": len(referencia), "wer": round(wer, 3)})

# Resumen final: este ejercicio calcula WER con distancia de edición.
# Elimina una palabra de la hipótesis y observa cómo cambia el resultado.
