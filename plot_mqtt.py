#!/usr/bin/env python3

import os
import re
import matplotlib.pyplot as plt

LOG_FILE = "mqtt_capture.log"
PLOTS_DIR = "plots"
OUTPUT_FILE = os.path.join(PLOTS_DIR, "GM102B.png")

# Crear carpeta plots si no existe
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

valores = []

# Leer archivo log
with open(LOG_FILE, "r") as f:
    for linea in f:
        if "Payload" in linea:
            resultado = re.search(r'"GM102B":([0-9.]+)', linea)
            if resultado:
                valor = float(resultado.group(1))
                valores.append(valor)

# Generar gráfica si hay datos
if len(valores) > 0:

    # Crear gráfica
    plt.figure()
    plt.plot(valores, marker='o')
    plt.title("Valores del sensor GM102B")
    plt.xlabel("Muestras")
    plt.ylabel("Valor")
    plt.grid(True)

    # Guardar gráfica PNG
    plt.savefig(OUTPUT_FILE)

    print("\nGrafica PNG creada en:", OUTPUT_FILE)

    # MOSTRAR gráfica en ventana (ESTO ES LO IMPORTANTE)
    plt.show()

    # Cerrar figura
    plt.close()

    # Grafica ASCII
    print("\nGrafica ASCII:\n")

    max_val = max(valores)
    min_val = min(valores)
    ancho = 50

    for i in range(len(valores)):

        valor = valores[i]

        if max_val != min_val:
            barras = int((valor - min_val) * ancho / (max_val - min_val))
        else:
            barras = 1

        print(f"Muestra {i:03d} ({valor:6.2f}) | {'*'*barras}")

else:
    print("No hay datos para graficar")
